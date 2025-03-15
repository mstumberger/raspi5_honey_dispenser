try:
    import RPi.GPIO as GPIO
except ModuleNotFoundError:
    print("Using noop GPIO")
    from mstumb.honey_dispenser.gpio.noop import GPIO
import time
import threading

class PiezoBuzzer:
    def __init__(self, pin):
        self.pin = pin
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.OUT)
        self.pwm = GPIO.PWM(self.pin, 1000)  # Initialize PWM with 1000 Hz frequency

    def play_sound(self, frequency, duration):
        self.pwm.ChangeFrequency(frequency)
        self.pwm.start(50)  # Start PWM with 50% duty cycle
        time.sleep(duration)
        self.pwm.stop()

    def _play_in_thread(self, sound_method):
        thread = threading.Thread(target=sound_method)
        thread.start()

    def filling_sound(self):
        # Play a success sound (e.g., two short beeps)
        self._play_in_thread(lambda: self.play_sound(1000, 0.1))
        time.sleep(0.1)
        self._play_in_thread(lambda: self.play_sound(1500, 0.1))

    def success_sound(self):
        # Play a start sound (e.g., ascending tone)
        def play_ascending():
            for freq in range(500, 1500, 100):
                self.play_sound(freq, 0.05)
        self._play_in_thread(play_ascending)

    def start_sound(self):
        # Play a filling sound (e.g., intermittent beeps)
        def play_intermittent():
            for _ in range(3):
                self.play_sound(800, 0.1)
                time.sleep(0.1)
        self._play_in_thread(play_intermittent)

    def cleanup(self):
        self.pwm.stop()
        GPIO.cleanup()

# Example usage
if __name__ == "__main__":
    buzzer = PiezoBuzzer(pin=12)  # Use GPIO 18 for the buzzer

    try:
        while True:
            print("Playing start sound...")
            buzzer.start_sound()
            time.sleep(1)

            print("Playing filling sound...")
            buzzer.filling_sound()
            time.sleep(1)

            print("Playing success sound...")
            buzzer.success_sound()
            time.sleep(1)

    finally:
        buzzer.cleanup()