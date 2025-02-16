import os
import time

try:
    import RPi.GPIO as GPIO
except ModuleNotFoundError:
    print("Using noop GPIO")
    from mstumb.honey_dispenser.gpio.noop import GPIO

FAN_PWM_PIN = 18  # PWM control pin
FAN_TACH_PIN = 17  # Tachometer pin (for RPM measurement)
TEMP_MIN = 40  # Temperature to start fan (°C)
TEMP_MAX = 80  # Temperature for full speed (°C)


class CoolerController:
    def __init__(self, pwm_pin=FAN_PWM_PIN, tach_pin=FAN_TACH_PIN, pwm_freq=25000):
        """Initialize fan controller with PWM and RPM monitoring"""
        self.pwm_pin = pwm_pin
        self.tach_pin = tach_pin
        self.pwm_freq = pwm_freq
        self.pulse_count = 0

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
        """Updates the fan speed based on CPU temperature"""
        temp = self.get_cpu_temp()
        speed = self.calculate_fan_speed(temp)
        self.fan.ChangeDutyCycle(speed)
        rpm = self.get_rpm()
        print(f"Temp: {temp}°C -> Fan Speed: {speed:.1f}% -> RPM: {rpm:.1f}")

    def run(self, interval=5):
        """Main loop to monitor temperature and adjust fan speed"""
        try:
            while True:
                self.update_fan_speed()
                time.sleep(interval)
        except KeyboardInterrupt:
            self.cleanup()

    def cleanup(self):
        """Stops the fan and cleans up GPIO"""
        self.fan.stop()
        GPIO.cleanup()
        print("Fan control stopped. GPIO cleaned up.")


# Create an instance of the FanController and run it
if __name__ == "__main__":
    fan_controller = CoolerController(FAN_PWM_PIN, FAN_TACH_PIN)
    fan_controller.run()
