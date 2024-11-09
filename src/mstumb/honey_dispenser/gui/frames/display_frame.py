import ttkbootstrap as tk


# Frame for the gauge and fill jar button
from mstumb.honey_dispenser.gui.gauge import ResizingGauge


class DisplayFrame(tk.Frame):
    def __init__(self, root, **kw):
        super().__init__(master=root, **kw)
        self.pack(fill=tk.BOTH, side=tk.LEFT, expand=True)
        # Configure frame3 grid layout to make it responsive
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=2)  # Gauge should take up 2/3 of the height
        self.rowconfigure(1, weight=1)  # Remaining space for other components

        # Gauge Frame inside frame3
        gauge_frame = tk.LabelFrame(self, text="Analog display")
        gauge_frame.grid(row=0, rowspan=1, column=0, padx=3, pady=3, sticky="nsew")

        # Gauge placeholder
        self.gauge = ResizingGauge(gauge_frame, height=600, width=900,
                                   max_value=1000,
                                   min_value=0,
                                   label='Filled honey',
                                   unit='g',
                                   divisions=16, yellow=90, red=90,
                                   red_low=50, yellow_low=85, bg='lavender')
        self.gauge.pack(pady=20, fill=tk.BOTH, expand=True)

        # Frame for additional controls (jars filled, fill jar button, and credits)
        controls_frame = tk.Frame(self)
        controls_frame.grid(row=2, rowspan=2, column=0, padx=3, pady=3, sticky="nsew")

        # Jars filled display
        self.label_jars = tk.Label(controls_frame, text=f"Jars Filled: {self.master.dispenser.jars_filled}")
        self.label_jars.pack(pady=10)

        # Fill jar button
        fill_jar_button = tk.Button(controls_frame, text="Fill jar", command=lambda: self.master.dispenser.fill_jar())
        fill_jar_button.pack(pady=20, fill=tk.BOTH, expand=True)

        # Credit label
        credit_label = tk.Label(controls_frame, text="Created by:")
        credit_label.pack()
        credit_label_name = tk.Label(controls_frame, text="Marko Štumberger")
        credit_label_name.pack()
