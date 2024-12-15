# sudo adduser pi gpio # enable using gpio without sudo!!
import time
from datetime import timedelta

from mstumb.honey_dispenser.config import Config, Setting, ScaleSetting, StepperSetting

try:
    import RPi.GPIO as GPIO
except ModuleNotFoundError:
    print("Using noop GPIO")
    from mstumb.honey_dispenser.gpio.noop import GPIO

simulation = False
try:
    from HX711 import SimpleHX711, Rate, Mass, Options, ReadType
except ModuleNotFoundError:
    print("Using noop HX711")
    simulation = True
    from mstumb.honey_dispenser.gpio.noop import SimpleHX711, Rate, Mass, Options, ReadType


class Dispenser:
    def __init__(self, speed=0.001):
        # self.hx: SimpleHX711 = SimpleHX711(20, 21, 21, -400534, Rate.HZ_80)  # Pins for HX711
        if not simulation:
            self.hx = SimpleHX711(
                Config.instance().get(ScaleSetting.DT),
                Config.instance().get(ScaleSetting.SCK),
                Config.instance().get(ScaleSetting.REF_UNIT),
                Config.instance().get(ScaleSetting.ZERO_VALUE),
                Rate.HZ_10)
        else:
            self.hx = SimpleHX711(None, None, None, None, self)
        self.setup_scale()

        self.stepper_pins = [  # GPIO pins for stepper motor
            Config.instance().get(StepperSetting.STEP1),
            Config.instance().get(StepperSetting.STEP2),
            Config.instance().get(StepperSetting.STEP3),
            Config.instance().get(StepperSetting.STEP4)
        ]
        self.setup_stepper()
        self.max_steps = Config.instance().get(Setting.MAX_STEPS)
        self.current_step = 0  # Start with the lid fully open (0 steps)
        self.lid_opened = False

        self.weight = 0

        # Stepper control
        self.target_weight = Config.instance().get(Setting.WEIGHT_SET)
        self.jars_filled = Config.instance().get(Setting.JARS_FILLED)
        self.speed = speed  # Delay between steps for stepper motor speed adjustment

        # Rotary encoder
        self.encoder_pin_A = 17  # GPIO pin for rotary encoder A
        self.encoder_pin_B = 27  # GPIO pin for rotary encoder B
        self.last_encoded = 0
        self.encoder_value = 0
        self.setup_rotary_encoder()

        self.led_pin = 23
        GPIO.setup(self.led_pin, GPIO.OUT)

        self.close_before_target = 0
        self.direction = -1

    def setup_scale(self):
        self.hx.setUnit(Mass.Unit.G)

    def tare_scale(self):
        print("Taring the scale...")
        self.hx.zero(Options(
            timedelta(seconds=1),
            ReadType.Average)
        )
        print("Scale tared.")

    def setup_stepper(self):
        GPIO.setmode(GPIO.BCM)
        for pin in self.stepper_pins:
            GPIO.setup(pin, GPIO.OUT)
            GPIO.output(pin, False)

    def setup_rotary_encoder(self):
        GPIO.setup(self.encoder_pin_A, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.encoder_pin_B, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(self.encoder_pin_A, GPIO.BOTH, callback=self.rotary_callback)
        GPIO.add_event_detect(self.encoder_pin_B, GPIO.BOTH, callback=self.rotary_callback)

    def rotary_callback(self, channel):
        MSB = GPIO.input(self.encoder_pin_A)  # Most significant bit
        LSB = GPIO.input(self.encoder_pin_B)  # Least significant bit

        encoded = (MSB << 1) | LSB
        delta = (encoded - self.last_encoded) % 4

        if delta == 1:  # Clockwise rotation
            self.encoder_value += 1
            self.target_weight += 10  # Adjust weight increment
        elif delta == 3:  # Counterclockwise rotation
            self.encoder_value -= 1
            self.target_weight -= 10  # Adjust weight decrement

        self.target_weight = max(0, self.target_weight)  # Avoid negative weight
        self.last_encoded = encoded

    def set_steps_to(self, step):
        print(f"Set current step to: {step}")
        self.current_step = step

    def rotate_stepper(self, steps, direction=1, speed=None):
        if speed is None:
            speed = self.speed  # Use default speed if not provided
        step_sequence = [
            [1, 0, 0, 1],
            [1, 0, 0, 0],
            [1, 1, 0, 0],
            [0, 1, 0, 0],
            [0, 1, 1, 0],
            [0, 0, 1, 0],
            [0, 0, 1, 1],
            [0, 0, 0, 1],
        ]
        # Adjust for direction
        direction *= self.direction
        if direction < 0:
            step_sequence.reverse()
        print(self.current_step,  direction * steps, self.current_step + direction * steps)
        for i in range(steps):
            for step in step_sequence:
                for pin in range(4):
                    GPIO.output(self.stepper_pins[pin], step[pin])
                time.sleep(speed)

        self.current_step += direction * steps

    def open_lid(self):
        print("Opening lid...")
        GPIO.output(self.led_pin, True)
        # Move the lid in the direction of opening
        self.rotate_stepper(self.max_steps, direction=self.direction)  # Use direction=1 to indicate opening
        self.lid_opened = True

    def position_lid(self, current_weight):
        if current_weight is not None:
            current_weight_log = current_weight
            current_weight += self.close_before_target

            # Define weights for lid positioning
            fully_open_weight = self.target_weight / 3
            fully_closed_weight = self.target_weight

            # Calculate closure level: 0 (open) to 1 (closed) as weight approaches the target
            if current_weight <= fully_open_weight:
                closure_level = 0  # Lid fully open
            elif fully_open_weight < current_weight < fully_closed_weight:
                closure_level = (current_weight - fully_open_weight) / (fully_closed_weight - fully_open_weight)
            else:
                closure_level = 1  # Lid fully closed at or above target weight

            # Calculate target step position based on closure level
            target_steps = int(closure_level * (self.direction * self.max_steps))
            steps_to_move = ((self.direction * self.max_steps) - (self.direction * self.current_step)) - target_steps
            direction = 1 if steps_to_move > 0 else -1  # Closing if positive, opening if negative
            # Move the motor to the target step position if needed
            if steps_to_move != 0:
                self.rotate_stepper(abs(steps_to_move), direction=direction)

            print(f"Current Weight: {current_weight_log}g with closing before {self.close_before_target}g, Lid Step Position: {self.current_step}/{self.max_steps}")

    def close_lid(self):
        print("Closing lid...")
        GPIO.output(self.led_pin, False)
        self.lid_opened = False

    def get_weight(self):
        try:
            return self.hx.weight(
                Options(
                    timedelta(milliseconds=150),
                    ReadType.Average
                )
            ).getValue()
        except RuntimeError:
            return None

    def fill_jar(self):
        self.open_lid()

    def check_weight(self, weight=None):
        if weight is None:
            weight = self.get_weight()
        if self.lid_opened:
            # Call position_lid to adjust lid based on weight
            self.position_lid(weight)
            if weight >= self.target_weight:
                self.close_lid()
                self.jars_filled += 1
                Config.instance().update(Setting.JARS_FILLED, self.jars_filled)
                print(f"Jar filled! Total jars: {self.jars_filled}")
        return weight

    def calibrate(self):
        print("Calibration started.")
        knownWeight = 200
        samples = 50

        print("1. Remove all objects from the scale, you have 10s")
        time.sleep(2)
        print("Working...")
        zeroValue = self.hx.read(Options(int(samples)))

        print("2. Place object on the scale, you have 10s")
        time.sleep(2)
        print("Working...")
        raw = self.hx.read(Options(int(samples)))
        refUnitFloat = (raw - zeroValue) / knownWeight
        refUnit = round(refUnitFloat, 0)

        if refUnit == 0:
            refUnit = 1

        self.hx.setReferenceUnit(str(round(refUnit)))
        self.hx.setOffset(str(round(zeroValue)))

        # save to settings for next time

    def cleanup(self):
        GPIO.cleanup()


