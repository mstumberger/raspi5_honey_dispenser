import os
import time
import lgpio

FAN_PWM_PIN = 18  # PWM control pin (BCM)
FAN_TACH_PIN = 17  # Tachometer pin (BCM)
TEMP_MIN = 40  # Temperature to start fan (°C)
TEMP_MAX = 80  # Temperature for full speed (°C)
PWM_FREQ = 25000  # 25 kHz

class CoolerController:
    def __init__(self, pwm_pin, tach_pin, pwm_freq=PWM_FREQ):
        """Initialize fan controller with PWM and RPM monitoring"""
        self.pwm_pin = pwm_pin
        self.tach_pin = tach_pin
        self.pwm_freq = pwm_freq
        self.pulse_count = 0

        # Initialize lgpio chip
        self.h = lgpio.gpiochip_open(0)
        lgpio.gpio_claim_output(self.h, self.pwm_pin)
        lgpio.tx_pwm(self.h, self.pwm_pin, self.pwm_freq, 0)  # Start at 0% duty cycle

        # Set up tachometer input
        lgpio.gpio_claim_input(self.h, self.tach_pin)
        lgpio.gpio_set_edge(self.h, self.tach_pin, lgpio.RISING_EDGE)
        lgpio.callback(self.h, self.tach_pin, lgpio.RISING_EDGE, self.count_pulse)

    def count_pulse(self, chip, gpio, level, timestamp):
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
        lgpio.tx_pwm(self.h, self.pwm_pin, self.pwm_freq, speed)  # Update PWM duty cycle
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
        lgpio.tx_pwm(self.h, self.pwm_pin, self.pwm_freq, 0)  # Stop fan
        lgpio.gpiochip_close(self.h)
        print("Fan control stopped. GPIO cleaned up.")

# Create an instance of the FanController and run it
if __name__ == "__main__":
    fan_controller = CoolerController(FAN_PWM_PIN, FAN_TACH_PIN)
    fan_controller.run()
