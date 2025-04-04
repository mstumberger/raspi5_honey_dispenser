from tkinter import messagebox

import ttkbootstrap as tk


# Frame for title and buttons
class TopFrame(tk.Frame):
    # Initialize fullscreen state
    fullscreen = False

    def __init__(self, root,  **kw):
        super().__init__(master=root, height=50, **kw)
        self.root = root
        self.pack(fill=tk.X)

        title_label = tk.Label(self, text="Honey Dispenser")
        title_label.pack(side=tk.LEFT, padx=10)

        fullscreen_button = tk.Button(self, text="Fullscreen", command=self.toggle_fullscreen)
        fullscreen_button.pack(side=tk.RIGHT, padx=5)

        exit_button = tk.Button(self, text="Shutdown", command=self.shutdown)
        exit_button.pack(side=tk.RIGHT, padx=5)

    # Function to toggle fullscreen and adjust font size
    def toggle_fullscreen(self):
        self.fullscreen = not self.fullscreen
        self.root.attributes("-fullscreen", self.fullscreen)

    def shutdown(self):
        # Ask for confirmation before shutting down
        response = messagebox.askyesno("Shutdown", "Are you sure you want to shut down the Raspberry Pi?")
        if response:
            import os
            # Execute the shutdown command
            os.system("sudo shutdown now")
