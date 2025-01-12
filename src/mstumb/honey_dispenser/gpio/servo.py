try:
    import RPi.GPIO as GPIO
except ModuleNotFoundError:
    print("Using noop GPIO")
    from mstumb.honey_dispenser.gpio.noop import GPIO

import time

class LidController:

    def __init__(self, servo_pin=18):
        # Pin configuration
        SERVO_PIN = servo_pin  # GPIO pin connected to the servo signal wire

        # Set up GPIO
        GPIO.setmode(GPIO.BCM)  # BCM pin-numbering scheme
        GPIO.setup(SERVO_PIN, GPIO.OUT)

        # Set up PWM
        self.pwm = GPIO.PWM(SERVO_PIN, 50)  # 50 Hz (standard servo frequency)
        self.pwm.start(0)  # Start with PWM off (duty cycle 0)

    def set_angle(self, angle):
        """
        Set the angle of the servo motor.
        :param angle: Desired angle (0-180 degrees)
        """
        if 0 <= angle <= 200:
            duty_cycle = 2 + (angle / 18)  # Convert angle to duty cycle
            self.pwm.ChangeDutyCycle(duty_cycle)
            time.sleep(0.5)  # Allow servo to move to position
            self.pwm.ChangeDutyCycle(0)  # Turn off PWM to avoid jitter
        else:
            print("Angle out of range. Must be between 0 and 180 degrees.")

    def close(self):
        self.pwm.stop()  # Stop PWM


if __name__ == '__main__':
    lid_controller = LidController()
    try:
        print("Controlling MG996R Servo. Press Ctrl+C to exit.")
        while True:
            open_angle = float(input("Enter angle (0-180): "))
            lid_controller.set_angle(open_angle)
    except KeyboardInterrupt:
        print("Exiting program.")
    finally:
        lid_controller.close()
        GPIO.cleanup()  # Clean up GPIO settings