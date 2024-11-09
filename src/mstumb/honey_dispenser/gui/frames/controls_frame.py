import ttkbootstrap as tk


# Frame for title and buttons
from mstumb.honey_dispenser.config import Config, Settings, Setting


class ControlsFrame(tk.Frame):
    def __init__(self, root, **kw):
        super().__init__(master=root, **kw)
        self.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Control Frame inside frame2
        control_frame = tk.LabelFrame(self, text="Controls")
        control_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        # Configure control_frame to allow scale_frame to expand
        control_frame.columnconfigure(0, weight=1)
        control_frame.rowconfigure(0, weight=1)

        # Scale section
        scale_frame = tk.LabelFrame(control_frame, text="Scale")
        scale_frame.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

        # Configure columns in scale_frame to center content
        scale_frame.columnconfigure(0, weight=1)
        scale_frame.columnconfigure(1, weight=1)
        scale_frame.columnconfigure(2, weight=1)
        scale_frame.columnconfigure(3, weight=1)

        # Labels and entry fields
        current_weight_label = tk.Label(scale_frame, text="Current:")
        current_weight_label.grid(row=0, column=0, sticky="E")  # Align to the right (east)

        self.current_weight = tk.DoubleVar(self)
        self.current_weight_value = tk.Entry(scale_frame, width=5, textvariable=self.current_weight)
        self.current_weight_value.grid(row=0, column=1, sticky="W")  # Align to the left

        set_weight_label = tk.Label(scale_frame, text="Set:")
        set_weight_label.grid(row=0, column=2, sticky="E")  # Align to the right

        self.set_weight = tk.IntVar(self, Config.instance().get(Setting.WEIGHT_SET))
        self.set_weight.trace("w", lambda *args: Config.instance().update(Setting.WEIGHT_SET, self.set_weight.get()))

        self.set_weight_value = tk.Entry(scale_frame, width=5, textvariable=self.set_weight)
        self.set_weight_value.grid(row=0, column=3, sticky="W")  # Align to the left

        # Centering buttons
        calibrate_button = tk.Button(scale_frame, text="Calibrate", command=lambda: self.master.dispenser.calibrate(), width=12)
        calibrate_button.grid(row=2, column=0, columnspan=2, pady=5, padx=10, sticky="ew")  # Span both columns, center horizontally

        tare_button = tk.Button(scale_frame, text="Tare", command=lambda: self.master.dispenser.tare_scale(), width=12)
        tare_button.grid(row=2, column=2, columnspan=2,pady=5, padx=10, sticky="ew")  # Span both columns, center horizontally

        # Lid section
        lid_frame = tk.LabelFrame(control_frame, text="Lid")
        lid_frame.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")

        # Configure lid_frame columns to allow content centering
        lid_frame.columnconfigure(0, weight=1)
        lid_frame.columnconfigure(1, weight=1)

        # Labels and spinboxes
        max_steps_label = tk.Label(lid_frame, text="Max")
        max_steps_label.grid(row=0, column=0, sticky="E")  # Align right

        self.max_steps_value = tk.IntVar(self, Config.instance().get(Setting.MAX_STEPS))
        self.max_steps_value.trace("w", lambda *args: Config.instance().update(Setting.MAX_STEPS, self.max_steps_value.get()))
        max_steps_spinbox = tk.Spinbox(lid_frame, from_=0, to=100, width=5, textvariable=self.max_steps_value)
        max_steps_spinbox.grid(row=0, column=1, sticky="W")  # Align left

        current_steps_label = tk.Label(lid_frame, text="Current:")
        current_steps_label.grid(row=1, column=0, sticky="E")  # Align right

        self.current_steps_value = tk.IntVar()
        self.current_steps_display = tk.Entry(lid_frame, width=5, textvariable=self.current_steps_value, state='readonly')
        self.current_steps_display.grid(row=1, column=1, sticky="W")  # Align to the left

        steps_label = tk.Label(lid_frame, text="Steps")
        steps_label.grid(row=2, column=0, sticky="E")  # Align right
        self.stepper_steps = tk.IntVar(self, 4)
        steps_spinbox = tk.Spinbox(lid_frame, from_=1, to=self.max_steps_value.get(), width=5, textvariable=self.stepper_steps)
        steps_spinbox.grid(row=2, column=1, sticky="W")  # Align left

        # Centering buttons
        left_button = tk.Button(lid_frame, text="Left", width=12,
                                 command=lambda: self.master.dispenser.rotate_stepper(self.stepper_steps.get(), direction=1))
        left_button.grid(row=3, column=0, pady=5, padx=10, sticky="ew")  # Span entire cell width

        right_button = tk.Button(lid_frame, text="Right", width=12,
                                  command=lambda: self.master.dispenser.rotate_stepper(self.stepper_steps.get(), direction=-1))
        right_button.grid(row=3, column=1, pady=5, padx=10, sticky="ew")  # Span entire cell width

        # Scale slider, centered and spanning both columns
        self.speed_scale = tk.Scale(lid_frame, from_=0.01, to=0.0001, orient=tk.HORIZONTAL, length=80, value=0.001)
        self.speed_scale.set(self.master.dispenser.speed)
        self.speed_scale.grid(row=4, column=0, columnspan=2, pady=5, padx=15, sticky="ew")  # Center horizontally, span both columns

        # Closing section
        closing_frame = tk.LabelFrame(control_frame, text="Closing")
        closing_frame.grid(row=2, column=0, padx=5, pady=5, sticky="nsew")

        # Configure lid_frame columns to allow content centering
        closing_frame.columnconfigure(0, weight=1)
        closing_frame.columnconfigure(1, weight=1)
        closing_frame.columnconfigure(2, weight=1)  # Added for unit label

        # Labels and spinboxes
        max_steps_label = tk.Label(closing_frame, text="Close before")
        max_steps_label.grid(row=0, column=0, sticky="E")  # Align right

        self.close_before_value = tk.IntVar(self, Config.instance().get(Setting.WEIGHT_BEFORE))
        # Use a lambda directly in the trace method to update the config
        self.close_before_value.trace("w", lambda *args: Config.instance().update(Setting.WEIGHT_BEFORE, self.close_before_value.get()))
        close_before_spinbox = tk.Spinbox(closing_frame, from_=0, to=200, width=5, textvariable=self.close_before_value)
        close_before_spinbox.grid(row=0, column=1, sticky="W")  # Align left

        # Add "g" label next to the spinbox
        unit_label = tk.Label(closing_frame, text="g")
        unit_label.grid(row=0, column=2, sticky="W")