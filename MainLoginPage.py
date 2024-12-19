import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from MainScreen import App
from Registration import Register
import os

class LoginPage:
    def __init__(self, root):
        self.root = root
        self.root.title("Login Page")
        iconpic = tk.PhotoImage(file='iconpic.jpg')
        self.root.iconphoto(False, iconpic)
        # Set a custom font and size
        custom_font = ("Helvetica", 20)

        self.label_username = tk.Label(root, text="UserID:", font=custom_font, bg="white")
        self.label_password = tk.Label(root, text="Password:", font=custom_font, bg="white")

        self.entry_username = tk.Entry(root, font=custom_font)
        self.entry_password = tk.Entry(root, show="*", font=custom_font)

        self.label_username.place(x=490, y=50)
        self.label_password.place(x=458, y=150)
        self.entry_username.place(x=590, y=50)
        self.entry_password.place(x=590, y=150)

        # Style for Login Button
        self.login_button_style = ttk.Style()
        self.login_button_style.configure("Login.TButton", padding=10, font=("Helvetica", 12, "bold"))
        self.login_button = ttk.Button(root, text="Login", command=self.login, style="Login.TButton")
        # Style for Register Button
        self.register_button_style = ttk.Style()
        self.register_button_style.configure("Register.TButton", padding=10, font=("Helvetica", 12, "bold"))
        self.register_button = ttk.Button(root, text="Register Yourself", command=self.register,
                                          style="Register.TButton")
        # Style for Delete Button
        self.delete_user_button_style = ttk.Style()
        self.delete_user_button_style.configure("DeleteUser.TButton", padding=10, font=("Helvetica", 12, "bold"))
        self.delete_user_button = ttk.Button(root, text="Delete User", command=self.delete_user,
                                             style="DeleteUser.TButton")

        self.login_button.place(x=450, y=290)
        self.register_button.place(x=580, y=290)
        self.delete_user_button.place(x=741, y=290)

        # Specify the file path for storing user credentials
        self.file_path = "user_credentials.txt"

    def register(self):
        window = Register(self.root)

    def login(self):
        # Implement login logic here
        user_id = self.entry_username.get()
        password = self.entry_password.get()
        username=""

        if self.is_valid_login(user_id, password):
            # Destroy the login page window
            self.root.destroy()

            with open(self.file_path, "r") as file:
                lines = file.readlines()
                credentials = [line.strip().split(":") for line in lines]
            l1=[entry[1] for entry in credentials if entry[0] == user_id]
            l2 = [entry[3] for entry in credentials if entry[0] == user_id]
            l3 = [entry[0] for entry in credentials if entry[0] == user_id]
            # Open a new window with the username
            self.open_new_window(l1[0], l2[0], l3[0])

        else:
            messagebox.showerror("Login Error", "Invalid username or password")

    def open_new_window(self, username, sem, uid):
        new_window = App(self.root, username, sem, uid)


    def is_valid_login(self, user_id, password):
        # Check if the provided username and password match the stored credentials in the text file
        try:
            with open(self.file_path, "r") as file:
                lines = file.readlines()
                credentials = [line.strip().split(":") for line in lines]
            return any(entry[0] == user_id and entry[2] == password for entry in credentials)
        except FileNotFoundError:
            return False

    def delete_user(self):
        # Open a dialog to get user_id and password
        user_id = simpledialog.askstring("Delete User", "Enter your User ID:")
        password = simpledialog.askstring("Delete User", "Enter your Password:", show='*')

        if self.is_valid_login(user_id, password):
            # Confirm user's intention to delete the profile
            confirmation = messagebox.askyesno("Delete User", f"Do you want to delete the profile for {user_id}?")

            if confirmation:
                # Remove user details from user_credentials.txt
                self.remove_user_from_file(user_id)
                messagebox.showinfo("Delete User", "Profile deleted successfully!")
        else:
            messagebox.showerror("Delete User", "Invalid username or password")

    def remove_user_from_file(self, user_id):
        try:
            with open(self.file_path, "r") as file:
                lines = file.readlines()
            with open(self.file_path, "w") as file:
                for line in lines:
                    if not line.startswith(f"{user_id}:"):
                        file.write(line)
            calendar_files = [f"{user_id}_calendar.json"]
            for file_name in calendar_files:
                file_path = os.path.join(os.getcwd(), file_name)
                if os.path.exists(file_path):
                    os.remove(file_path)
            note_files = [f"{user_id}_notes.json"]
            for file_name in note_files:
                file_path = os.path.join(os.getcwd(), file_name)
                if os.path.exists(file_path):
                    os.remove(file_path)
            note_files = [f"{user_id}_reminder.json"]
            for file_name in note_files:
                file_path = os.path.join(os.getcwd(), file_name)
                if os.path.exists(file_path):
                    os.remove(file_path)
        except FileNotFoundError:
            messagebox.showerror("Error", "User credentials file not found.")

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("925x500+300+200")
    root.resizable(False, False)
    img = tk.PhotoImage(file="login.png")
    tk.Label(root, image=img).place(x=30, y=50)
    root.configure(bg="#fff")
    app = LoginPage(root)
    root.mainloop()