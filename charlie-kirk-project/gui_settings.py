import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import json
from pathlib import Path


class SettingsWindow:
    def __init__(self, config_path="config.json"):
        self.config_path = config_path
        self.config = self.load_config()
        self.window = None

    def load_config(self):
        """Load configuration from JSON file"""
        try:
            with open(self.config_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            # Default configuration
            return {
                "timer": 2.0,
                "iris_threshold": 0.35,
                "spam_loops": 4,
                "sound_enabled": True,
                "sound_path": "./assets/we-are-charlie-kirk-song.mp3",
                "start_minimized": False
            }

    def save_config(self):
        """Save configuration to JSON file"""
        with open(self.config_path, 'w') as f:
            json.dump(self.config, f, indent=4)

    def show(self):
        """Display the settings window"""
        if self.window is not None and self.window.winfo_exists():
            self.window.lift()
            self.window.focus_force()
            return

        self.window = tk.Tk()
        self.window.title("Charlie-Kirkification Settings")
        self.window.geometry("500x450")
        self.window.resizable(False, False)

        # Main container
        main_frame = ttk.Frame(self.window, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Title
        title = ttk.Label(main_frame, text="⚙️ Settings", font=("Arial", 16, "bold"))
        title.grid(row=0, column=0, columnspan=2, pady=(0, 20))

        # Timer setting
        ttk.Label(main_frame, text="Timer Threshold (seconds):", font=("Arial", 10)).grid(row=1, column=0, sticky=tk.W, pady=5)
        self.timer_var = tk.DoubleVar(value=self.config["timer"])
        timer_spinbox = ttk.Spinbox(main_frame, from_=0.5, to=10.0, increment=0.5, textvariable=self.timer_var, width=15)
        timer_spinbox.grid(row=1, column=1, sticky=tk.W, pady=5)
        ttk.Label(main_frame, text="(How long you can look down before spam)", font=("Arial", 8), foreground="gray").grid(row=2, column=0, columnspan=2, sticky=tk.W)

        # Iris threshold
        ttk.Label(main_frame, text="Iris Detection Threshold:", font=("Arial", 10)).grid(row=3, column=0, sticky=tk.W, pady=(15, 5))
        self.threshold_var = tk.DoubleVar(value=self.config["iris_threshold"])
        threshold_scale = ttk.Scale(main_frame, from_=0.2, to=0.5, orient=tk.HORIZONTAL, variable=self.threshold_var, length=200)
        threshold_scale.grid(row=3, column=1, sticky=tk.W, pady=(15, 5))
        self.threshold_label = ttk.Label(main_frame, text=f"{self.config['iris_threshold']:.2f}")
        self.threshold_label.grid(row=3, column=1, sticky=tk.E, pady=(15, 5))
        threshold_scale.configure(command=lambda v: self.threshold_label.configure(text=f"{float(v):.2f}"))
        ttk.Label(main_frame, text="(Lower = more sensitive)", font=("Arial", 8), foreground="gray").grid(row=4, column=0, columnspan=2, sticky=tk.W)

        # Spam loops
        ttk.Label(main_frame, text="Spam Loops:", font=("Arial", 10)).grid(row=5, column=0, sticky=tk.W, pady=(15, 5))
        self.loops_var = tk.IntVar(value=self.config["spam_loops"])
        loops_spinbox = ttk.Spinbox(main_frame, from_=1, to=20, increment=1, textvariable=self.loops_var, width=15)
        loops_spinbox.grid(row=5, column=1, sticky=tk.W, pady=(15, 5))
        ttk.Label(main_frame, text="(More loops = more spam)", font=("Arial", 8), foreground="gray").grid(row=6, column=0, columnspan=2, sticky=tk.W)

        # Sound enabled
        ttk.Label(main_frame, text="Sound Enabled:", font=("Arial", 10)).grid(row=7, column=0, sticky=tk.W, pady=(15, 5))
        self.sound_enabled_var = tk.BooleanVar(value=self.config["sound_enabled"])
        sound_checkbox = ttk.Checkbutton(main_frame, variable=self.sound_enabled_var)
        sound_checkbox.grid(row=7, column=1, sticky=tk.W, pady=(15, 5))

        # Sound path
        ttk.Label(main_frame, text="Sound File:", font=("Arial", 10)).grid(row=8, column=0, sticky=tk.W, pady=(15, 5))
        sound_frame = ttk.Frame(main_frame)
        sound_frame.grid(row=8, column=1, sticky=(tk.W, tk.E), pady=(15, 5))
        self.sound_path_var = tk.StringVar(value=self.config["sound_path"])
        sound_entry = ttk.Entry(sound_frame, textvariable=self.sound_path_var, width=20)
        sound_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        sound_browse_btn = ttk.Button(sound_frame, text="Browse", command=self.browse_sound)
        sound_browse_btn.pack(side=tk.LEFT, padx=(5, 0))

        # Start minimized
        ttk.Label(main_frame, text="Start Minimized to Tray:", font=("Arial", 10)).grid(row=9, column=0, sticky=tk.W, pady=(15, 5))
        self.start_minimized_var = tk.BooleanVar(value=self.config["start_minimized"])
        minimized_checkbox = ttk.Checkbutton(main_frame, variable=self.start_minimized_var)
        minimized_checkbox.grid(row=9, column=1, sticky=tk.W, pady=(15, 5))

        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=10, column=0, columnspan=2, pady=(30, 0))

        save_btn = ttk.Button(button_frame, text="Save", command=self.save_and_close)
        save_btn.pack(side=tk.LEFT, padx=5)

        cancel_btn = ttk.Button(button_frame, text="Cancel", command=self.window.destroy)
        cancel_btn.pack(side=tk.LEFT, padx=5)

        reset_btn = ttk.Button(button_frame, text="Reset to Default", command=self.reset_defaults)
        reset_btn.pack(side=tk.LEFT, padx=5)

        self.window.mainloop()

    def browse_sound(self):
        """Browse for sound file"""
        filename = filedialog.askopenfilename(
            title="Select Sound File",
            filetypes=[("Audio Files", "*.mp3 *.wav *.ogg"), ("All Files", "*.*")]
        )
        if filename:
            self.sound_path_var.set(filename)

    def save_and_close(self):
        """Save configuration and close window"""
        self.config["timer"] = self.timer_var.get()
        self.config["iris_threshold"] = self.threshold_var.get()
        self.config["spam_loops"] = self.loops_var.get()
        self.config["sound_enabled"] = self.sound_enabled_var.get()
        self.config["sound_path"] = self.sound_path_var.get()
        self.config["start_minimized"] = self.start_minimized_var.get()

        self.save_config()
        messagebox.showinfo("Settings", "Settings saved successfully!\nRestart detection for changes to take effect.")
        self.window.destroy()

    def reset_defaults(self):
        """Reset to default values"""
        if messagebox.askyesno("Reset", "Reset all settings to default values?"):
            self.timer_var.set(2.0)
            self.threshold_var.set(0.35)
            self.loops_var.set(4)
            self.sound_enabled_var.set(True)
            self.sound_path_var.set("./assets/we-are-charlie-kirk-song.mp3")
            self.start_minimized_var.set(False)


if __name__ == "__main__":
    # Test the settings window
    settings = SettingsWindow()
    settings.show()
