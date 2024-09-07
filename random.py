import tkinter as tk
from tkinter import ttk
import time
from datetime import datetime
import threading
import winsound
from ttkthemes import ThemedTk
from PIL import Image, ImageTk
import math

class ClockApp(ThemedTk):
    def __init__(self):
        super().__init__(theme="arc")

        self.title("Clock App")
        self.geometry("500x400")
        self.configure(bg="#f0f0f0")

        style = ttk.Style(self)
        style.configure("TNotebook", background="#f0f0f0")
        style.configure("TNotebook.Tab", background="#e0e0e0", padding=[10, 5])
        style.map("TNotebook.Tab", background=[("selected", "#ffffff")])

        self.notebook = ttk.Notebook(self)
        self.notebook.pack(expand=True, fill="both", padx=10, pady=10)

        self.watch_frame = WatchFrame(self.notebook)
        self.alarm_frame = AlarmFrame(self.notebook)
        self.timer_frame = TimerFrame(self.notebook)
        self.stopwatch_frame = StopwatchFrame(self.notebook)

        self.notebook.add(self.watch_frame, text="Watch")
        self.notebook.add(self.alarm_frame, text="Alarm")
        self.notebook.add(self.timer_frame, text="Timer")
        self.notebook.add(self.stopwatch_frame, text="Stopwatch")

class WatchFrame(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.configure(style="TFrame")
        
        self.canvas = tk.Canvas(self, width=300, height=300, bg="#ffffff", highlightthickness=0)
        self.canvas.pack(pady=20)

        self.draw_clock_face()
        self.update_time()

    def draw_clock_face(self):
        self.canvas.create_oval(10, 10, 290, 290, outline="#000000", width=2)

        for i in range(12):
            angle = i * math.pi/6 - math.pi/2
            x1 = 150 + 130 * math.cos(angle)
            y1 = 150 + 130 * math.sin(angle)
            x2 = 150 + 140 * math.cos(angle)
            y2 = 150 + 140 * math.sin(angle)
            self.canvas.create_line(x1, y1, x2, y2, fill="#000000", width=2)

    def update_time(self):
        self.canvas.delete("hands")
        now = datetime.now()

        hour_angle = (now.hour % 12 + now.minute / 60) * math.pi/6 - math.pi/2
        hour_x = 150 + 60 * math.cos(hour_angle)
        hour_y = 150 + 60 * math.sin(hour_angle)
        self.canvas.create_line(150, 150, hour_x, hour_y, fill="#000000", width=4, tags="hands")

        minute_angle = (now.minute + now.second / 60) * math.pi/30 - math.pi/2
        minute_x = 150 + 90 * math.cos(minute_angle)
        minute_y = 150 + 90 * math.sin(minute_angle)
        self.canvas.create_line(150, 150, minute_x, minute_y, fill="#000000", width=3, tags="hands")

        second_angle = now.second * math.pi/30 - math.pi/2
        second_x = 150 + 120 * math.cos(second_angle)
        second_y = 150 + 120 * math.sin(second_angle)
        self.canvas.create_line(150, 150, second_x, second_y, fill="#ff0000", width=2, tags="hands")
        
        self.after(1000, self.update_time)

class AlarmFrame(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.configure(style="TFrame")
        
        self.alarm_time = tk.StringVar()
        self.alarm_time.set("00:00:00")
        
        ttk.Label(self, text="Set Alarm (HH:MM:SS)", font=("Arial", 14)).pack(pady=20)
        self.alarm_entry = ttk.Entry(self, textvariable=self.alarm_time, font=("Arial", 18), width=10, justify="center")
        self.alarm_entry.pack(pady=10)
        
        self.set_button = ttk.Button(self, text="Set Alarm", command=self.set_alarm, style="Accent.TButton")
        self.set_button.pack(pady=10)
        
        self.status_label = ttk.Label(self, text="", font=("Arial", 12))
        self.status_label.pack(pady=10)

    def set_alarm(self):
        alarm_time = self.alarm_time.get()
        self.status_label.config(text=f"Alarm set for {alarm_time}")
        threading.Thread(target=self.run_alarm, args=(alarm_time,), daemon=True).start()

    def run_alarm(self, alarm_time):
        while True:
            current_time = time.strftime("%::%M:%S")
            if current_time == alarm_time:
                self.status_label.config(text="Alarm ringing!")
                winsound.Beep(1000, 1000)
                break
            time.sleep(1)

class TimerFrame(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.configure(style="TFrame")
        
        self.remaining_time = tk.IntVar()
        self.remaining_time.set(0)
        
        ttk.Label(self, text="Set Timer (seconds)", font=("Arial", 14)).pack(pady=20)
        self.timer_entry = ttk.Entry(self, font=("Arial", 18), width=10, justify="center")
        self.timer_entry.pack(pady=10)
        
        self.start_button = ttk.Button(self, text="Start Timer", command=self.start_timer, style="Accent.TButton")
        self.start_button.pack(pady=10)
        
        self.time_label = ttk.Label(self, text="", font=("Arial", 24))
        self.time_label.pack(pady=20)

    def start_timer(self):
        try:
            seconds = int(self.timer_entry.get())
            self.remaining_time.set(seconds)
            self.update_timer()
        except ValueError:
            self.time_label.config(text="Please enter a valid number")

    def update_timer(self):
        if self.remaining_time.get() > 0:
            minutes, seconds = divmod(self.remaining_time.get(), 60)
            time_str = f"{minutes:02d}:{seconds:02d}"
            self.time_label.config(text=time_str)
            self.remaining_time.set(self.remaining_time.get() - 1)
            self.after(1000, self.update_timer)
        else:
            self.time_label.config(text="Timer finished!")
            winsound.Beep(1000, 1000)

class StopwatchFrame(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.configure(style="TFrame")
        
        self.elapsed_time = 0
        self.running = False
        
        self.time_label = ttk.Label(self, text="00:00:00", font=("Arial", 36))
        self.time_label.pack(pady=30)
        
        button_frame = ttk.Frame(self)
        button_frame.pack(pady=20)
        
        self.start_button = ttk.Button(button_frame, text="Start", command=self.start_stop, style="Accent.TButton", width=10)
        self.start_button.pack(side="left", padx=10)
        
        self.reset_button = ttk.Button(button_frame, text="Reset", command=self.reset, width=10)
        self.reset_button.pack(side="left", padx=10)

    def start_stop(self):
        if self.running:
            self.running = False
            self.start_button.config(text="Start")
        else:
            self.running = True
            self.start_button.config(text="Stop")
            self.update()

    def reset(self):
        self.running = False
        self.elapsed_time = 0
        self.time_label.config(text="00:00:00")
        self.start_button.config(text="Start")

    def update(self):
        if self.running:
            self.elapsed_time += 0.1
            minutes, seconds = divmod(int(self.elapsed_time), 60)
            hours, minutes = divmod(minutes, 60)
            centiseconds = int((self.elapsed_time - int(self.elapsed_time)) * 100)
            time_str = f"{hours:02d}:{minutes:02d}:{seconds:02d}.{centiseconds:02d}"
            self.time_label.config(text=time_str)
            self.after(100, self.update)

if __name__ == "__main__":
    app = ClockApp()
    app.mainloop()
