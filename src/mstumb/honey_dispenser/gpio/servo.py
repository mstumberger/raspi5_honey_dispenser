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
        self.set_angle(0)

    def set_angle(self, angle, speed=0.5):
        """
        Set the angle of the servo motor with adjustable speed.
        :param angle: Desired angle (0-180 degrees)
        :param speed: Speed factor (1.0 is default, >1 is slower, <1 is faster)
        """
        angle = abs(angle)
        if 0 <= angle <= 180:
            # Determine current angle
            current_duty = 2 + (self.current_angle / 18) if hasattr(self, 'current_angle') else 0
            target_duty = 2 + (angle / 18)

            # Gradual movement
            step = 0.1 if speed > 1 else 0.2  # Smaller steps for slower speeds
            step = step * (1.0 / speed)  # Adjust step size by speed factor

            if current_duty < target_duty:
                duty_range = range(int(current_duty * 10), int(target_duty * 10), int(step * 10))
            else:
                duty_range = range(int(current_duty * 10), int(target_duty * 10), -int(step * 10))

            for duty in map(lambda x: x / 10, duty_range):
                self.pwm.ChangeDutyCycle(duty)
                time.sleep(0.02)  # Delay for smooth movement

            # Set final duty cycle
            self.pwm.ChangeDutyCycle(target_duty)
            time.sleep(0.5)  # Allow the servo to stabilize at the target position
            self.pwm.ChangeDutyCycle(0)  # Turn off PWM to avoid jitter

            self.current_angle = angle
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