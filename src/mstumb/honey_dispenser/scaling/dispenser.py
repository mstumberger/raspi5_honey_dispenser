# sudo adduser pi gpio # enable using gpio without sudo!!
import time
from datetime import timedelta
from tkinter import messagebox

from mstumb.honey_dispenser.config import Config, Setting, ScaleSetting, StepperSetting
from mstumb.honey_dispenser.gpio.buzzer import PiezoBuzzer
from mstumb.honey_dispenser.gpio.cooler import CoolerController
from mstumb.honey_dispenser.gpio.servo import LidController
from mstumb.honey_dispenser.gui.top_level import KnownWeightDialog

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
                Rate.HZ_10
            )
        else:
            self.hx = SimpleHX711(None, None, None, None, None, self)
        self.setup_scale()
        # self.cooling_controller = CoolerController()
        # self.cooling_controller.start()

        # Servo control for lid
        self.lid_controller = LidController(servo_pin=18)  # Replace with your desired GPIO pin
        self.max_steps = 180
        self.target_weight = Config.instance().get(Setting.WEIGHT_SET)
        self.jars_filled = Config.instance().get(Setting.JARS_FILLED)
        self.lid_opened = False
        self.speed = speed  # Delay between steps for stepper motor speed adjustment

        # Rotary encoder
        self.encoder_pin_A = 17  # GPIO pin for rotary encoder A
        self.encoder_pin_B = 27  # GPIO pin for rotary encoder B
        self.last_encoded = 0
        self.encoder_value = 0

        self.led_pin = 23
        GPIO.setup(self.led_pin, GPIO.OUT)

        self.buzzer = PiezoBuzzer(pin=12)  # Use GPIO 18 for the buzzer
        self.close_before_target = 0
        self.direction = 1
        self.speed = 1
        self.current_step = 0

    def setup_scale(self):
        self.hx.setUnit(Mass.Unit.G)

    def tare_scale(self):
        print("Taring the scale...")
        self.hx.zero(Options(
            timedelta(seconds=1),
            ReadType.Average)
        )
        print("Scale tared.")

    def open_lid(self):
        print("Opening lid...")
        GPIO.output(self.led_pin, True)
        self.buzzer.start_sound()
        self.lid_controller.set_angle(self.max_steps)  # Fully open the lid
        self.lid_opened = True



    def position_lid(self, current_weight):
        # Calculate lid position based on weight
        if current_weight is not None:
            current_weight_log = current_weight
            current_weight += self.close_before_target

            # Define weights for lid positioning
            fully_open_weight = 0  # Lid fully open at 0g
            fully_closed_weight = self.target_weight  # Lid fully closed at target weight

            # Calculate closure level: 0 (fully open) to 1 (fully closed)
            if current_weight <= fully_open_weight:
                closure_level = 0  # Fully open
            elif fully_open_weight < current_weight < fully_closed_weight:
                closure_level = (current_weight - fully_open_weight) / (fully_closed_weight - fully_open_weight)
            else:
                closure_level = 1  # Fully closed at or above target weight

            # Map closure level to angle (180° open to 0° closed)
            target_angle = int((1 - closure_level) * self.max_steps)  # Invert closure level for correct servo angle

            print(f"Current Weight: {current_weight_log}g with closing before {self.close_before_target}g, Lid Step Position: {target_angle}")

            self.lid_controller.set_angle(target_angle)

    def close_lid(self):
        print("Closing lid...")
        GPIO.output(self.led_pin, False)
        self.buzzer.success_sound()
        self.lid_controller.set_angle(0)  # Fully close the lid
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
            if int(weight + self.close_before_target) >= self.target_weight:
                self.close_lid()
                self.jars_filled += 1
                Config.instance().update(Setting.JARS_FILLED, self.jars_filled)
                print(f"Jar filled! Total jars: {self.jars_filled}")
            else:
                self.buzzer.filling_sound()
        return weight

    def calibrate(self):
        """Perform the calibration process with user confirmation at each step."""
        if not messagebox.askokcancel("Calibration", "Calibration started. Proceed?"):
            return

        # Step 1: Remove all objects from the scale
        if not messagebox.askokcancel("Step 1", "Remove all objects from the scale. Click OK to continue."):
            return

        # Step 2: Get the known weight from the user
        known_weight = KnownWeightDialog().result
        if known_weight is None:  # User clicked Cancel
            return

        samples = 50

        print("Working...")
        zero_value = self.hx.read(Options(int(samples)))  # Read zero value
        print(f"Zero value measured: {zero_value}")

        # Step 2: Place the known weight on the scale
        if not messagebox.askokcancel("Step 2", f"Place the {known_weight}g weight on the scale. Click OK to continue."):
            return

        print("Working...")
        raw = self.hx.read(Options(int(samples)))  # Read raw value with known weight
        print(f"Raw value with weight measured: {raw}")

        # Calculate reference unit
        ref_unit_float = (raw - zero_value) / known_weight
        ref_unit = round(ref_unit_float, 0)
        if ref_unit == 0:
            ref_unit = 1

        # Set reference unit and offset
        self.hx.setReferenceUnit(str(round(ref_unit)))
        self.hx.setOffset(str(round(zero_value)))

        # Save calibration values to config
        Config.instance().update(ScaleSetting.ZERO_VALUE, zero_value)
        Config.instance().update(ScaleSetting.REF_UNIT, ref_unit)

        messagebox.showinfo("Calibration Complete", f"Calibration complete!\nZERO_VALUE: {zero_value}\nREF_UNIT: {ref_unit}")


    def cleanup(self):
        self.lid_controller.close()
        self.buzzer.cleanup()
        GPIO.cleanup()
