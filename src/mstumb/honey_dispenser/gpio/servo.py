import RPi.GPIO as GPIO
import time

# Pin configuration
SERVO_PIN = 18  # GPIO pin connected to the servo signal wire

# Set up GPIO
GPIO.setmode(GPIO.BCM)  # BCM pin-numbering scheme
GPIO.setup(SERVO_PIN, GPIO.OUT)

# Set up PWM
pwm = GPIO.PWM(SERVO_PIN, 50)  # 50 Hz (standard servo frequency)
pwm.start(0)  # Start with PWM off (duty cycle 0)

def set_angle(angle):
    """
    Set the angle of the servo motor.
    :param angle: Desired angle (0-180 degrees)
    """
    if 0 <= angle <= 200:
        duty_cycle = 2 + (angle / 18)  # Convert angle to duty cycle
        pwm.ChangeDutyCycle(duty_cycle)
        time.sleep(0.5)  # Allow servo to move to position
        pwm.ChangeDutyCycle(0)  # Turn off PWM to avoid jitter
    else:
        print("Angle out of range. Must be between 0 and 180 degrees.")

try:
    print("Controlling MG996R Servo. Press Ctrl+C to exit.")
    while True:
        angle = float(input("Enter angle (0-180): "))
        set_angle(angle)
except KeyboardInterrupt:
    print("Exiting program.")
finally:
    pwm.stop()  # Stop PWM
    GPIO.cleanup()  # Clean up GPIO settings