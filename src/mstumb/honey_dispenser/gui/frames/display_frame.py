from tkinter import ttk
import tkinter as tk
from mstumb.honey_dispenser.gui.gauge import ResizingGauge

class DisplayFrame(tk.Frame):
    def __init__(self, root, **kw):
        super().__init__(master=root, **kw)
        self.pack(fill=tk.BOTH, side=tk.LEFT, expand=True)
        # Configure frame3 grid layout to make it responsive
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=2)  # Less weight for the gauge (smaller analog display)
        self.rowconfigure(1, weight=1)  # More weight for the controls section

        # Gauge Frame inside frame3
        gauge_frame = tk.LabelFrame(self, text="Analog display")
        gauge_frame.grid(row=0, column=0, padx=3, pady=3, sticky="nsew")

        # Gauge placeholder
        self.gauge = ResizingGauge(gauge_frame, height=500, width=900,  # Smaller gauge size
                                   max_value=1000,
                                   min_value=0,
                                   label='Filled honey',
                                   unit='g',
                                   divisions=16, yellow=90, red=90,
                                   red_low=50, yellow_low=85, bg='lavender')
        self.gauge.pack(pady=20, fill=tk.BOTH, expand=True)

        # Frame for additional controls (jars filled, fill jar button, and credits)
        controls_frame = tk.Frame(self)
        controls_frame.grid(row=1, column=0, padx=3, pady=3, sticky="nsew")

        # Configure controls_frame to allow the button to expand
        controls_frame.columnconfigure(0, weight=1)  # Allow the button to expand horizontally
        controls_frame.rowconfigure(0, weight=1)     # Allow the jars filled label to expand
        controls_frame.rowconfigure(1, weight=3)     # More weight for the button (bigger button)
        controls_frame.rowconfigure(2, weight=1)     # Allow the credit label to expand

        # Jars filled display
        self.label_jars = tk.Label(controls_frame, text=f"Jars Filled: {self.master.dispenser.jars_filled}")
        self.label_jars.grid(row=0, column=0, pady=10, sticky="nsew")  # Place at the top

        # Fill jar button - Using tk.Button with explicit size
        fill_jar_button = tk.Button(
            controls_frame,
            text="Fill jar",
            command=lambda: self.master.dispenser.fill_jar(),
            width=30,  # Increase width (in characters)
            height=5,  # Increase height (in lines of text)
            font=("Arial", 20)  # Increase font size
        )
        fill_jar_button.grid(row=1, column=0, pady=20, sticky="nsew")  # Span the entire cell

        # Credit label
        credit_label = tk.Label(controls_frame, text="Created by:")
        credit_label.grid(row=2, column=0, pady=5, sticky="s")  # Place at the bottom

        credit_label_name = tk.Label(controls_frame, text="Marko Štumberger")
        credit_label_name.grid(row=3, column=0, pady=5, sticky="s")  # Place at the bottom