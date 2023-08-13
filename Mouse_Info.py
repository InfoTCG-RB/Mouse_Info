import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import pyautogui
import time
import psutil
import os

def get_complementary_color(color):
    return tuple(255 - x for x in color)

class App:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Mouse Position Tracker")

        self.is_paused = False
        self.last_x, self.last_y = 0, 0
        self.next_update_time = time.time() + 10  # Schedule the next CPU/Memory update

        self.track_cpu_memory = tk.BooleanVar(value=False)
        self.track_cpu_memory.trace("w", self.toggle_cpu_memory_tracking)

        self.track_magnification = tk.BooleanVar(value=True)
        self.track_magnification.trace("w", self.toggle_magnification)

        self.track_hex_color = tk.BooleanVar(value=True)
        self.track_dec_color = tk.BooleanVar(value=False)

        self.mouse_position_label = tk.Label(self.root, text="Mouse Position: X=0, Y=0")
        self.mouse_position_label.grid(row=0, pady=10)

        self.mouse_color_label = tk.Label(self.root, text="Pixel Color: DEC=(0, 0, 0) HEX=#000000")
        self.mouse_color_label.grid(row=1, pady=10)

        self.magnified_label = tk.Label(self.root)
        self.magnified_label.grid(row=2, pady=10)

        self.usage_label = tk.Label(self.root, text="CPU Usage: 0.00%  Memory Usage: 0.00 MB")
        self.progress_bar = ttk.Progressbar(self.root, orient="horizontal", length=200, mode="determinate", maximum=10)

        self.button_frame = tk.Frame(self.root)
        self.button_frame.grid(row=4, pady=5)

        self.pause_button = tk.Button(self.button_frame, text="Pause", command=self.toggle_pause)
        self.pause_button.grid(row=0, column=0, padx=5)

        self.help_button = tk.Button(self.button_frame, text="Help", command=self.show_help)
        self.help_button.grid(row=0, column=1, padx=5)

        self.settings_button = tk.Button(self.button_frame, text="Settings", command=self.show_settings)
        self.settings_button.grid(row=0, column=2, padx=5)

        # Call these functions to set initial visibility
        self.toggle_cpu_memory_tracking()
        self.toggle_magnification()

        # Bind keyboard shortcuts
        self.root.bind("<Control-s>", self.toggle_pause)  # Bind Ctrl-S to pause/resume
        self.root.bind("<F1>", self.show_help)  # Bind F1 to open help

        # Start tracking
        self.update_info()

        self.root.mainloop()

    def update_info(self):
        x, y = pyautogui.position()

        if not self.is_paused and (x != self.last_x or y != self.last_y):
            screenshot = pyautogui.screenshot(region=(x - 2, y - 2, 5, 5))
            center_pixel_color = screenshot.getpixel((2, 2))

            color_text = ""
            if self.track_dec_color.get():
                color_text += f"Pixel Color: DEC={center_pixel_color} "
            if self.track_hex_color.get():
                pixel_color_hex = "#{:02x}{:02x}{:02x}".format(*center_pixel_color)
                color_text += f"HEX={pixel_color_hex}"

            if self.track_dec_color.get() or self.track_hex_color.get():
                self.mouse_color_label.config(text=color_text)
                self.mouse_color_label.grid(row=1, pady=10)  # Ensure the label is visible
            else:
                self.mouse_color_label.grid_forget()  # Hide the label

            if self.track_magnification.get():
                magnified_image = screenshot.resize((200, 200), Image.NEAREST)
                line_color = get_complementary_color(center_pixel_color)
                center = magnified_image.size[0] // 2
                for i in range(center - 8, center + 9):
                    for j in range(center - 2, center + 3):
                        magnified_image.putpixel((i, j), line_color)
                        magnified_image.putpixel((j, i), line_color)

                magnified_image_tk = ImageTk.PhotoImage(magnified_image)
                self.magnified_label.config(image=magnified_image_tk)
                self.magnified_label.image = magnified_image_tk

            self.mouse_position_label.config(text=f"Mouse Position: X={x}, Y={y}")

            self.last_x, self.last_y = x, y

        if self.track_cpu_memory.get() and time.time() >= self.next_update_time:
            process = psutil.Process(os.getpid())
            cpu_usage = process.cpu_percent(interval=1)
            memory_usage = process.memory_info().rss / (1024 ** 2)  # Convert to MB
            self.usage_label.config(text=f"CPU Usage: {cpu_usage:.2f}%  Memory Usage: {memory_usage:.2f} MB")
            self.next_update_time = time.time() + 10  # Schedule next update in 10 seconds

        # Update progress bar
        if self.track_cpu_memory.get():
            progress_value = 10 - (self.next_update_time - time.time())
            self.progress_bar["value"] = progress_value

        self.root.after(50, self.update_info)  # Update every 50ms

    def toggle_pause(self, event=None):
        self.is_paused = not self.is_paused
        self.pause_button.config(text="Resume" if self.is_paused else "Pause")

    def show_help(self, event=None):
        help_window = tk.Toplevel(self.root)
        help_window.title("Help")

        help_text = (
            "Mouse Position Tracker - Help\n\n"
            "This program provides real-time tracking of the mouse cursor's position, pixel color, "
            "and a magnified view of the area around the cursor.\n\n"
            "Features:\n"
            "- Mouse Location: Displays the current X and Y coordinates of the cursor.\n"
            "- Pixel Color: Shows the color of the pixel under the cursor in DEC and HEX formats.\n"
            "- Magnification: Provides a magnified view of the area around the cursor with a bullseye at the center.\n"
            "- CPU/Memory Tracking: Monitors the CPU and memory usage of the program.\n\n"
            "Controls:\n"
            "- Pause/Resume Button: Stops and resumes tracking. Shortcut: Ctrl-S.\n"
            "- Help Button: Opens this help window. Shortcut: F1.\n"
            "- Settings Button: Allows enabling or disabling various features.\n\n"
            "Settings Options:\n"
            "- Enable CPU/Memory Tracking: Toggles tracking of CPU and memory usage.\n"
            "- Enable Magnification: Toggles the magnified view.\n"
            "- Enable Hex Color: Toggles displaying the pixel color in HEX format.\n"
            "- Enable Dec Color: Toggles displaying the pixel color in DEC format."
        )

        help_label = tk.Label(help_window, text=help_text, justify=tk.LEFT)
        help_label.pack(padx=10, pady=10)

    def show_settings(self):
        settings_window = tk.Toplevel(self.root)
        settings_window.title("Settings")

        track_cpu_memory_checkbox = tk.Checkbutton(settings_window, text="Enable CPU/Memory Tracking", variable=self.track_cpu_memory)
        track_cpu_memory_checkbox.pack(pady=10)

        track_magnification_checkbox = tk.Checkbutton(settings_window, text="Enable Magnification", variable=self.track_magnification)
        track_magnification_checkbox.pack(pady=10)

        track_hex_color_checkbox = tk.Checkbutton(settings_window, text="Enable Hex Color", variable=self.track_hex_color)
        track_hex_color_checkbox.pack(pady=10)

        track_dec_color_checkbox = tk.Checkbutton(settings_window, text="Enable Dec Color", variable=self.track_dec_color)
        track_dec_color_checkbox.pack(pady=10)

    def toggle_cpu_memory_tracking(self, *args):
        if self.track_cpu_memory.get():
            self.usage_label.grid(row=3, pady=10)
            self.progress_bar.grid(row=3, pady=5, columnspan=3)
        else:
            self.usage_label.grid_forget()
            self.progress_bar.grid_forget()

    def toggle_magnification(self, *args):
        if self.track_magnification.get():
            self.magnified_label.grid(row=2, pady=10)
        else:
            self.magnified_label.grid_forget()

# Create the application
app = App()
