# -*- coding: utf-8 -*-
import ttkbootstrap as tk
from mstumb.honey_dispenser.gui.frames.top_frame import TopFrame


class Gui(tk.Window):
    def __init__(self, dispenser, config):
        tk.Window.__init__(self, title="Honey Dispenser", themename='darkly')
        self.geometry("600x400")  # Set a default size for the window
        self.dispenser = dispenser
        self.config = config
        self.top_frame = TopFrame(self)

