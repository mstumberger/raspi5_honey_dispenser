import os
import time
import threading
from collections import deque

try:
    import RPi.GPIO as GPIO
except ModuleNotFoundError:
    print("Using noop GPIO")
    from mstumb.honey_dispenser.gpio.noop import GPIO

FAN_PWM_PIN = 19  # PWM control pin
FAN_TACH_PIN = 16  # Tachometer pin (for RPM measurement)
TEMP_MIN = 55  # Temperature to start fan (°C)
TEMP_MAX = 75  # Temperature for full speed (°C)
TEMP_HISTORY_SIZE = 3  # Number of temperature readings to average


class CoolerController(threading.Thread):
    def __init__(self, pwm_pin=FAN_PWM_PIN, tach_pin=FAN_TACH_PIN, pwm_freq=10000, interval=5):
        """Initialize fan controller with PWM and RPM monitoring"""
        super().__init__()  # Initialize the Thread base class
        self.pwm_pin = pwm_pin
        self.tach_pin = tach_pin
        self.pwm_freq = pwm_freq
        self.interval = interval
        self.pulse_count = 0
        self.running = False
        self.temp_history = deque(maxlen=TEMP_HISTORY_SIZE)  # Store last 3 temperature readings

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pwm_pin, GPIO.OUT)
        GPIO.setup(self.tach_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

        # Set up PWM
        self.fan = GPIO.PWM(self.pwm_pin, self.pwm_freq)
        self.fan.start(0)  # Start fan off

        # Set up tachometer interrupt
        GPIO.add_event_detect(self.tach_pin, GPIO.FALLING, callback=self.count_pulse)

    def count_pulse(self, channel):
        """Counts pulses from the fan's tachometer output"""
        self.pulse_count += 1


    def get_cpu_temp(self):
        """Reads the CPU temperature"""
        temp = os.popen("vcgencmd measure_temp").readline()
        return float(temp.replace("temp=", "").replace("'C\n", ""))

    def calculate_fan_speed(self, temp):
        """Maps temperature to PWM duty cycle (0-100%)"""
        if temp < TEMP_MIN:
            return 0
        elif temp > TEMP_MAX:
            return 100
        else:
            return (temp - TEMP_MIN) / (TEMP_MAX - TEMP_MIN) * 100

    def get_rpm(self):
        """Calculates RPM from tachometer pulse count"""
        pulses = self.pulse_count
        self.pulse_count = 0  # Reset counter after reading
        rpm = (pulses / 2) * 60  # Each revolution = 2 pulses
        return rpm

    def update_fan_speed(self):
        """Updates the fan speed based on the average of the last three temperature readings"""
        temp = self.get_cpu_temp()
        self.temp_history.append(temp)  # Store new temperature reading

        if len(self.temp_history) < TEMP_HISTORY_SIZE:
            avg_temp = temp  # Not enough readings yet, use the current temp
        else:
            avg_temp = sum(self.temp_history) / len(self.temp_history)

        speed = self.calculate_fan_speed(avg_temp)
        self.fan.ChangeDutyCycle(speed)
        rpm = self.get_rpm()
        print(f"Temp: {temp}°C (Avg: {avg_temp:.1f}°C) -> Fan Speed: {speed:.1f}% -> RPM: {rpm:.1f}")

    def run(self):
        """Main loop to monitor temperature and adjust fan speed"""
        self.running = True
        try:
            while self.running:
                self.update_fan_speed()
                time.sleep(self.interval)
        except KeyboardInterrupt:
            self.cleanup()

    def stop(self):
        """Stops the fan control loop"""
        self.running = False

    def cleanup(self):
        """Stops the fan and cleans up GPIO"""
        self.fan.ChangeDutyCycle(0)
        self.fan.stop()
        # GPIO.cleanup()
        print("Fan control stopped. GPIO cleaned up.")


# Example usage
if __name__ == "__main__":
    fan_controller = CoolerController(interval=5)
    fan_controller.start()  # Start the thread

    # Main thread can continue doing other work
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        fan_controller.cleanup()  # Clean up GPIO