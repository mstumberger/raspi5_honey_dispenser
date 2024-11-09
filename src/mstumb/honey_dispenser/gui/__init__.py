from tkinter import font

import tkinter as tk

from mstumb.honey_dispenser.gpio.executor import GPIOExecutor


class DispenserGUI:
    def __init__(self, root, gpio_executor: GPIOExecutor):
        self.gpio_executor = gpio_executor
        self.root = root
        self.root.title("Honey Dispenser")

        # Customize Fonts
        self.digital_font = font.Font(family="Helvetica", size=36, weight="bold")
        self.button_font = font.Font(family="Arial", size=14)

        # Frame to hold weight display
        self.frame_weight = tk.Frame(root, bg="white", padx=10, pady=10)
        self.frame_weight.pack(pady=20)

        self.label_current_weight = tk.Label(self.frame_weight, text="Current Weight: 0 g", font=self.digital_font,
                                             bg="white", fg="blue")
        self.label_current_weight.pack()

        # Target weight display
        self.target_weight = tk.IntVar(root, 500)
        self.label_weight = tk.Label(root, text=f"Target Weight: {self.target_weight} g", font=self.digital_font,
                                     bg="white", fg="blue")
        self.label_weight.pack(pady=10)

        # Jars filled display
        self.jars_filled = tk.IntVar(root, 500)
        self.label_jars = tk.Label(root, text=f"Jars Filled: {self.jars_filled}", font=self.digital_font,
                                   bg="white", fg="blue")
        self.label_jars.pack(pady=10)

        # Control Buttons
        self.button_frame = tk.Frame(root, padx=10, pady=10)
        self.button_frame.pack()

        self.button_calibrate = tk.Button(self.button_frame, text="Calibrate", command=self.calibrate,
                                          font=self.button_font, bg="lightgray", width=15)
        self.button_calibrate.grid(row=0, column=0, padx=5, pady=5)

        self.button_fill = tk.Button(self.button_frame, text="Fill Jar", command=self.fill_jar, font=self.button_font,
                                     bg="lightgray", width=15)
        self.button_fill.grid(row=0, column=1, padx=5, pady=5)

        self.button_zero = tk.Button(self.button_frame, text="Zero", command=self.zero, font=self.button_font,
                                     bg="lightgray", width=15)
        self.button_zero.grid(row=1, column=0, padx=5, pady=5)

        self.button_tare = tk.Button(self.button_frame, text="Tare", command=self.tare, font=self.button_font,
                                     bg="lightgray", width=15)
        self.button_tare.grid(row=1, column=1, padx=5, pady=5)

        self.button_exit = tk.Button(root, text="Exit", command=self.quit, font=self.button_font, bg="red", width=10)
        self.button_exit.pack(pady=20)

        self.speed_scale = tk.Scale(root, from_=0.0001, to=0.01, resolution=0.0001, orient=tk.HORIZONTAL,
                                    label="Stepper Speed (s)", font=self.button_font, length=300)

        self.speed = tk.DoubleVar(root, 1)
        self.speed_scale.set(self.speed.get())
        self.speed_scale.pack(pady=10)

        # Update the display periodically
        self.update_display(10)

    def update_display(self, current_weight):
        # Update current weight display
        # current_weight = self.doser.get_weight()
        self.label_current_weight.config(text=f"Current Weight: {current_weight:.2f} g")

        # Update target weight and jars filled
        self.label_weight.config(text=f"Target Weight: {self.target_weight.get()} g")
        self.label_jars.config(text=f"Jars Filled: {self.jars_filled.get()}")

        self.speed = self.speed_scale.get()
        self.root.after(100, self.update_display, current_weight + 10)  # Refresh every 100ms

    def calibrate(self):
        self.gpio_executor.calibrate()

    def fill_jar(self):
        self.gpio_executor.fill_jar()
        self.update_display(100)

    def zero(self):
        print("Zeroing scale...")

    def tare(self):
        print("Taring scale...")
        self.gpio_executor.tare()

    def quit(self):
        self.gpio_executor.cleanup()
        self.root.quit()
