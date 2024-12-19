import tkinter as tk
import tkinter.font as tkFont
from tkinter import ttk, simpledialog, messagebox

class Register:
    def __init__(self, root):
        # setting window settings
        self.root = tk.Toplevel(root)
        self.root.title("Registration Window")
        self.root.geometry('730x480')
        iconpic = tk.PhotoImage(file='iconpic.jpg')
        self.root.iconphoto(False, iconpic)
        self.root.resizable(False, False)

        Label1 = tk.Label(self.root, text="Welcome Student", font=tkFont.Font(family='Castellar', size=40),
                          anchor="center", fg="#cc0000")
        Label1.place(x=90, y=0)

        Label2 = tk.Label(self.root, text="Enter UserID:", font=tkFont.Font(family='Times Roman', size=20),
                          anchor="center", fg="blue")
        Label2.place(x=30, y=70)

        Label3 = tk.Label(self.root, text="Enter Name:", font=tkFont.Font(family='Times Roman', size=20),
                          anchor="center", fg="blue")
        Label3.place(x=30, y=140)

        Label3 = tk.Label(self.root, text="Enter Password:", font=tkFont.Font(family='Times Roman', size=20),
                          anchor="center", fg="blue")
        Label3.place(x=30, y=210)

        Label4 = tk.Label(self.root, text="Enter Class:", font=tkFont.Font(family='Times Roman', size=20),
                          anchor="center", fg="blue")
        Label4.place(x=30, y=280)

        custom_font = ("Helvetica", 14)
        entry_userID = tk.Entry(self.root, font=custom_font, width=60)
        entry_userID.place(x=200, y=78)

        Label5 = tk.Label(self.root, text="No spaces allowed!", font=('Arial', 12, 'italic'), fg="red")
        Label5.place(x=200, y=105)

        entry_Name = tk.Entry(self.root, font=custom_font, width=60)
        entry_Name.place(x=190, y=149)
        entry_Password = tk.Entry(self.root, show="*", font=custom_font, width=60)
        entry_Password.place(x=235, y=218)
        entry_Class = tk.Entry(self.root, font=custom_font, width=60)
        entry_Class.place(x=185, y=289)

        style = ttk.Style()
        style.configure("TButton", padding=10, font=("Helvetica", 14, "bold"))

        def reg_func():
            user_id = entry_userID.get()
            name = entry_Name.get()
            password = entry_Password.get()
            class_name=entry_Class.get()
            if ' ' in user_id:
                messagebox.showerror("Error", "No spaces allowed in UserID")
                return

            file_path = "user_credentials.txt"
            def is_username_registered(userid):
                # Check if the username is already registered in the text file
                try:
                    with open(file_path, "r") as file:
                        lines = file.readlines()
                        registered_userid = [line.split(":")[0].strip() for line in lines]
                    return userid in registered_userid
                except FileNotFoundError:
                    return False


            if name and password:
                # Check if the userid is already registered
                if is_username_registered(user_id):
                    messagebox.showerror("Registration Error", "UserID already registered.")
                else:
                    confirm = messagebox.askyesno("Message",
                                                  "Do you want to register with these details?")
                    if confirm:
                        # Store the username and password in the text file
                        with open(file_path, "a") as file:
                            file.write(f"{user_id}:{name}:{password}:{class_name}\n")
                        messagebox.showinfo("Registration", "Registration successful!")
                        self.root.destroy()
            else:
                messagebox.showerror("Registration Error", "Username and password are required for registration")
        reg_button = ttk.Button(self.root, text="Register", command=reg_func, style="TButton")
        reg_button.place(x=250, y=350)