# -*- coding: utf-8 -*-
import ttkbootstrap as tk

from mstumb.honey_dispenser.config import Config, Setting
from mstumb.honey_dispenser.gui.frames.controls_frame import ControlsFrame
from mstumb.honey_dispenser.gui.frames.display_frame import DisplayFrame
from mstumb.honey_dispenser.gui.frames.top_frame import TopFrame


class Gui(tk.Window):
    def __init__(self, dispenser):
        tk.Window.__init__(self, title="Honey Dispenser", themename='darkly')
        self.geometry("600x400")  # Set a default size for the window
        self.dispenser = dispenser
        self.top_frame = TopFrame(self)
        self.controls_frame = ControlsFrame(self)
        self.display_frame = DisplayFrame(self)

        self.get_reading()

    def get_reading(self):
        measurement = self.dispenser.check_weight()

        if measurement:
            # Update current weight display
            current_weight = abs(round(measurement, Config.instance().get(Setting.ROUNDING)))
            self.display_frame.gauge.set_value(current_weight)
            self.controls_frame.current_weight.set(current_weight)


        # Update current stepper step
        self.controls_frame.current_steps_value.set(self.dispenser.current_step)

        # self.label_weight.config(text=f"Target Weight: {} g")
        self.display_frame.label_jars.config(text=f"Jars Filled: {self.dispenser.jars_filled}")

        self.dispenser.speed = self.controls_frame.speed_scale.get()
        print(self.dispenser.speed)
        self.dispenser.max_steps = self.controls_frame.max_steps_value.get()
        self.dispenser.close_before_target = self.controls_frame.close_before_value.get()

        # Update target weight
        self.dispenser.target_weight = self.controls_frame.set_weight.get()

        # Update fan speed
        self.dispenser.cooling_controller.update_fan_speed()

        self.after(200, self.get_reading)  # Refresh every 100ms
