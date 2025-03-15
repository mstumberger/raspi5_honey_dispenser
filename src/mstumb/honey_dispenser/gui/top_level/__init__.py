import tkinter as tk


class KnownWeightDialog(tk.Toplevel):
    def __init__(self, default_weight=200):
        """
        Initialize the custom dialog for entering the known weight.

        Args:
            default_weight (int): The default value for the known weight.
        """
        super().__init__()
        self.default_weight = default_weight
        self.result = None

        # Configure the dialog
        self.title("Enter Known Weight")
        self.geometry("300x150")

        # Label
        label = tk.Label(self, text="Enter the known weight (in grams):")
        label.pack(pady=10)

        # Entry widget for weight input
        self.weight_var = tk.IntVar(value=self.default_weight)
        weight_entry = tk.Entry(self, textvariable=self.weight_var)
        weight_entry.pack(pady=10)

        # OK and Cancel buttons
        button_frame = tk.Frame(self)
        button_frame.pack(pady=10)

        ok_button = tk.Button(button_frame, text="OK", command=self.on_ok)
        ok_button.pack(side="left", padx=10)

        cancel_button = tk.Button(button_frame, text="Cancel", command=self.on_cancel)
        cancel_button.pack(side="right", padx=10)

        # Make the dialog modal
        self.grab_set()
        self.wait_window(self)

    def on_ok(self):
        """Handle the OK button click."""
        self.result = self.weight_var.get()
        self.destroy()

    def on_cancel(self):
        """Handle the Cancel button click."""
        self.result = None
        self.destroy()