import tkinter as tk
from tkinter import simpledialog, messagebox
from datetime import datetime, timedelta

class TimePickerDialog(simpledialog.Dialog):
    def body(self, master):
        tk.Label(master, text="Select Time:").grid(row=0, column=0)
        self.time_var = tk.StringVar()
        self.time_var.set(datetime.now().strftime("%I:%M %p"))
        self.time_entry = tk.Entry(master, textvariable=self.time_var)
        self.time_entry.grid(row=0, column=1)
        return self.time_entry

    def apply(self):
        selected_time = self.time_var.get()
        self.result = selected_time