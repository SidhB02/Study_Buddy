import json
import tkinter as tk
import tkinter.font as tkFont
from tkinter import ttk, simpledialog, messagebox, LEFT, END
from tkcalendar import Calendar, DateEntry
from plyer import notification
from datetime import datetime, timedelta
import threading
from Time_Picker import TimePickerDialog
import time

class App:
    def __init__(self, root, username, sem, uid):
        # setting window settings
        self.root = tk.Tk()
        blank = " "
        self.root.title("Study Buddy" + 110 * blank + f"Welcome {username}!")
        self.root.geometry('1080x720')
        iconpic = tk.PhotoImage(file='iconpic.jpg')
        self.root.iconphoto(False, iconpic)
        self.root.resizable(False, False)

        Label1 = tk.Label(self.root)
        Label1["anchor"] = "center"
        Label1["cursor"] = "arrow"
        ft = tkFont.Font(family='Brush Script MT', size=40)
        Label1["font"] = ft
        Label1["fg"] = "#cc0000"
        Label1["justify"] = "center"
        Label1["text"] = f"Class:{sem}"
        Label1["relief"] = "flat"
        Label1.pack(pady=10)

        # Button for "Logout" in "User Details" tab
        Button1 = tk.Button(self.root)
        Button1["bg"] = "#2b71d9"
        ft = tkFont.Font(family='Times', size=18)
        Button1["font"] = ft
        Button1["fg"] = "#ffffff"
        Button1["justify"] = "center"
        Button1["text"] = "Logout"
        Button1.place(x=990, y=5, width=73, height=34)
        Button1["command"] = self.Button1_command

        # Create a notebook to hold tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(pady=4, fill=tk.BOTH, expand=True)

        # Create tabs for "User Details," "Notes," and "Reminders"
        self.notes_tab = ttk.Frame(self.notebook)
        self.reminders_tab = ttk.Frame(self.notebook)
        self.calendar_tab = ttk.Frame(self.notebook)

        self.notebook.add(self.notes_tab, text="Notes")
        self.notebook.add(self.reminders_tab, text="Reminders")
        self.notebook.add(self.calendar_tab, text="Calendar")

        # Writing Contents of Notes_Tab
        # Adjusting font size
        style = ttk.Style()
        style.theme_use('default')
        style.configure('TNotebook.Tab', font=('Helvetica', 20))
        style.map("TNotebook.Tab", background=[('selected', 'green3'), ('active', 'green3')])
        style.configure("TButton", font=("Helvetica", 12))

        notes = {}
        try:
            with open(f"{uid}_notes.json", "r") as f:
                notes = json.load(f)
        except FileNotFoundError:
            pass

        self.sub_notebook = ttk.Notebook(self.notes_tab)
        self.sub_notebook.pack(expand=True, fill="both")

        def save_note():
            title = self.title_entry.get()
            content = self.content_entry.get("1.0", END)

            # Add the note to the notes dictionary
            notes[title] = content.strip()

            # Save the notes dictionary to the file
            with open(f"{uid}_notes.json", "w") as f:
                json.dump(notes, f)

            # Add the note to the notebook
            note_content = tk.Text(self.sub_notebook, width=40, height=10, font=("Bookman Old Style", 18))
            note_content.insert(END, content)
            self.sub_notebook.forget(self.sub_notebook.select())
            self.sub_notebook.add(note_content, text=title)

            # Clear entry widgets
            self.title_entry.delete(0, tk.END)
            self.content_entry.delete("1.0", tk.END)

        def add_note():
            note_frame = ttk.Frame(self.sub_notebook)
            self.sub_notebook.add(note_frame, text="New Note")
            # Create entry widgets for the title and content of the note
            title_label = ttk.Label(note_frame, text="Title:", font=("Bookman Old Style", 21))
            title_label.place(x=55, y=20)
            self.title_entry = ttk.Entry(note_frame, width=70, font='BookmanOldStyle 16')
            self.title_entry.place(x=130, y=25)

            content_label = ttk.Label(note_frame, text="Content:", font=("Bookman Old Style", 20))
            content_label.place(x=10, y=80)
            self.content_entry = tk.Text(note_frame, width=110, height=26, font=("Bookman Old Style", 18))
            self.content_entry.place(x=130, y=80)

        def load_notes():
            try:
                with open(f"{uid}_notes.json", "r") as f:
                    notes = json.load(f)

                for title, content in notes.items():
                    # Add the note to the notebook
                    note_content = tk.Text(self.sub_notebook, width=40, height=10, font=("Bookman Old Style", 17))
                    note_content.insert(END, content)
                    self.sub_notebook.add(note_content, text=title)

            except FileNotFoundError:
                # If the file does not exist, do nothing
                pass

        # Call the load_notes function when the app starts
        load_notes()

        def delete_note():
            # Get the current tab index
            current_tab = self.sub_notebook.index(self.sub_notebook.select())
            # Get the title of the note to be deleted
            note_title = self.sub_notebook.tab(current_tab, "text")
            # Show a confirmation dialog
            confirm = messagebox.askyesno("Delete Note",
                                          f"Are you sure you want to delete {note_title}?")

            if confirm:
                # Remove the note from the notebook
                self.sub_notebook.forget(current_tab)

                # Remove the note from the notes dictionary
                notes.pop(note_title)

                # Save the notes dictionary to the file
                with open(f"{uid}_notes.json", "w") as f:
                    json.dump(notes, f)

        new_button = ttk.Button(self.notes_tab, text="New Note", style="TButton", command=add_note)
        new_button.pack(side=LEFT, padx=10, pady=10)

        delete_button = ttk.Button(self.notes_tab, text="Delete Note", style="TButton", command=delete_note)
        delete_button.pack(side=LEFT, padx=10, pady=10)

        save_button = ttk.Button(self.notes_tab, text="Save Note", command=save_note, style="TButton")
        save_button.pack(side=LEFT, padx=10, pady=10)

        # Writing Contents of Reminders_Tab
        def save_reminders():
            with open(f"{uid}_reminder.json", "w") as file:
                data = [(dt.strftime("%Y-%m-%d %H:%M:%S"), text) for dt, text in reminders]
                json.dump(data, file)

        def load_reminders():
            try:
                with open(f"{uid}_reminder.json", "r") as file:
                    data = json.load(file)
                    now = datetime.now()
                    reminders = [(datetime.strptime(dt, "%Y-%m-%d %H:%M:%S"), text) for dt, text in data
                                 if datetime.strptime(dt, "%Y-%m-%d %H:%M:%S") > now]
            except FileNotFoundError:
                pass

        def handle_reminders():
            while True:
                now = datetime.now()
                for reminder in reminders[:]:
                    reminder_datetime, reminder_text = reminder
                    try:
                        if now >= reminder_datetime:
                            show_reminder_notification(reminder_text)
                            reminders.remove(reminder)
                    except Exception as e:
                        print(f"Error handling reminder: {e}")
                time.sleep(1)
        def pick_time():
            dialog = TimePickerDialog(self.root, title="Pick Time")
            selected_time = dialog.result
            if selected_time:
                time_button.config(text=selected_time)

        def set_reminder():
            reminder_text = reminder_entry.get()
            selected_date = date_cal.selection_get()
            time_str = time_button.cget("text")
            if not all((reminder_text, selected_date, time_str)):
                messagebox.showerror("Incomplete Information", "Please fill in all fields.")
                return

            try:
                reminder_time = datetime.strptime(time_str, "%I:%M %p")
            except ValueError:
                messagebox.showerror("Invalid Time Format", "Please enter time in hh:mm AM/PM format.")
                return

            reminder_datetime = datetime(selected_date.year, selected_date.month, selected_date.day,
                                         reminder_time.hour, reminder_time.minute)

            if reminder_datetime <= datetime.now():
                messagebox.showerror("Invalid Date/Time", "Please select a future date and time.")
                return

            reminders.append((reminder_datetime, reminder_text))
            messagebox.showinfo("Reminder Set", f"Reminder set for "
                                                f"{reminder_datetime.strftime('%Y-%m-%d %I:%M %p')}")

        def show_reminder_notification(reminder_text):
            notification.notify(
                title="Reminder",
                message=reminder_text,
                app_name="Notifier",
                app_icon="ico.ico",
                timeout=60  # Adjust the timeout value
            )

        reminders = []
        load_reminders()
        self.reminder_thread = threading.Thread(target=handle_reminders)
        self.reminder_thread.daemon = True  # Daemonize the thread so it exits when the main program exits
        self.reminder_thread.start()

        # Save reminders to a file every minute
        self.reminders_tab.after(60000, save_reminders)

        Rem_Label=tk.Label(self.reminders_tab, text="Enter Reminder:", font=("Times Roman", 18))
        Rem_Label.place(x=40, y=20)
        reminder_entry = tk.Entry(self.reminders_tab, width=80, font=("Comic Sans MS", 15))
        reminder_entry.place(x=220, y=22)

        date_label=tk.Label(self.reminders_tab, text="Select Date:", font=("Times Roman", 18))
        date_label.place(x=85, y=90)
        date_cal = Calendar(self.reminders_tab, selectmode="day", year=datetime.now().year, month=datetime.now().month,
                            day=datetime.now().day)
        date_cal.place(x=220, y=90)

        time_label = tk.Label(self.reminders_tab, text="Select time:", font=("Times Roman", 18))
        time_label.place(x=85, y=300)
        time_button = ttk.Button(self.reminders_tab, text="Pick Time", command=pick_time, style="TButton")
        time_button.place(x=220, y=300)

        rem_but=ttk.Button(self.reminders_tab, text="Set Reminder", style="TButton", command=set_reminder)
        rem_but.place(x=500, y=400)

        # Writing Contents of Calendar_Tab
        def add_event():
            date = cal.get_date()
            event = event_entry.get()

            if date and event:
                date_str = date.strftime('%Y-%m-%d')
                if date_str in calendar:
                    calendar[date_str].append(event)
                else:
                    calendar[date_str] = [event]

                event_entry.delete(0, tk.END)
                save_calendar()
                update_display_for_selected_date()
            else:
                messagebox.showwarning("Error", "Please select a date and enter an event.")

        def select_event_from_text(event):
            text.tag_remove(tk.SEL, 1.0, tk.END)
            index = text.index(tk.CURRENT)
            start_date = get_date_from_text(index)
            text.tag_add(tk.SEL, f"{start_date}.0", f"{start_date}.end")

        def get_date_from_text(position):
            line, _ = position.split('.')
            return line.strip()

        def get_selected_date():
            index = text.index(tk.SEL_FIRST)
            return get_date_from_text(index)

        def update_display_for_selected_date(event=None):
            selected_date = cal.get_date()
            update_display(selected_date)

        def update_display(selected_date=None):
            text.config(state=tk.NORMAL)
            text.delete(1.0, tk.END)

            if selected_date:
                selected_date_str = selected_date.strftime('%Y-%m-%d')
                events = calendar.get(selected_date_str, [])
                if events:
                    text.insert(tk.END, f"{selected_date_str}:\n")
                    for event in events:
                        text.insert(tk.END, f"  - {event}\n")
                    text.insert(tk.END, "\n")
            text.config(state=tk.DISABLED)

        def load_calendar():
            try:
                with open(f"{uid}_calendar.json", "r") as file:
                    return json.load(file)
            except (json.JSONDecodeError, FileNotFoundError):
                return {}

        def save_calendar():
            with open(f"{uid}_calendar.json", "w") as file:
                json.dump(calendar, file, indent=2)

        calendar = load_calendar()
        cal = DateEntry(self.calendar_tab, width=12, background='darkblue', foreground='white', borderwidth=2,
                        font=('Arial', 20))
        cal.place(x=40, y=15)
        cal.bind("<<DateEntrySelected>>", update_display_for_selected_date)
        event_label = tk.Label(self.calendar_tab, text="Event:", font=("Bookman Old Style", 22))
        event_label.place(x=28, y=72)
        event_entry = tk.Entry(self.calendar_tab, width=28, font='BookmanOldStyle 20')
        event_entry.place(x=120, y=80)
        add_button = ttk.Button(self.calendar_tab, text="Add Event", style="TButton", command=add_event)
        add_button.place(x=120, y=200)
        text = tk.Text(self.calendar_tab, height=33, width=63, state=tk.DISABLED)
        text.place(x=550, y=10)
        text.bind("<ButtonRelease-1>", select_event_from_text)
        update_display()


    def Button1_command(self):
        confirm = messagebox.askyesno("Logout",
                                      "Are you sure you want to logout?")
        if confirm:
            self.root.destroy()
