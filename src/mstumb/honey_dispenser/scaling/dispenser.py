# sudo adduser pi gpio # enable using gpio without sudo!!
import time
from datetime import timedelta

from mstumb.honey_dispenser.config import Config, Setting, ScaleSetting, StepperSetting
from mstumb.honey_dispenser.gpio.servo import LidController

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
            self.hx = SimpleHX711(None, None, None, None, self)
        self.setup_scale()

        # Servo control for lid
        self.lid_controller = LidController(servo_pin=18)  # Replace with your desired GPIO pin

        self.target_weight = Config.instance().get(Setting.WEIGHT_SET)
        self.jars_filled = Config.instance().get(Setting.JARS_FILLED)
        self.lid_opened = False
        self.close_before_target = 0

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
        self.lid_controller.set_angle(180)  # Fully open the lid
        self.lid_opened = True

    def close_lid(self):
        print("Closing lid...")
        self.lid_controller.set_angle(0)  # Fully close the lid
        self.lid_opened = False

    def position_lid(self, current_weight):
        # Calculate lid position based on weight
        if current_weight is not None:
            fully_open_weight = self.target_weight / 3
            fully_closed_weight = self.target_weight

            if current_weight <= fully_open_weight:
                closure_level = 0  # Fully open
            elif fully_open_weight < current_weight < fully_closed_weight:
                closure_level = (current_weight - fully_open_weight) / (fully_closed_weight - fully_open_weight)
            else:
                closure_level = 1  # Fully closed at or above target weight

            # Map closure level to angle (0° to 180°)
            target_angle = int(closure_level * 180)
            print(f"Setting lid angle to {target_angle}° for weight: {current_weight}g")
            self.lid_controller.set_angle(target_angle)

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
        self.lid_controller.close()
        GPIO.cleanup()

