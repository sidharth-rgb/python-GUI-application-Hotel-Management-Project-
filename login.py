



import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import subprocess
import os

class LoginWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Login - Hotel Management System")
        self.root.geometry("500x500+500+200")
        self.root.resizable(False, False)

        # Variables
        self.username = tk.StringVar()
        self.password = tk.StringVar()
        self.show_password = tk.BooleanVar()

        # ===== Frame =====
        frame = tk.Frame(self.root, bd=4, relief=tk.RIDGE, padx=20, pady=20)
        frame.place(x=70, y=50, width=360, height=350)

        tk.Label(frame, text="Username", font=("Arial", 12)).grid(row=0, column=0, pady=10, sticky="w")
        tk.Entry(frame, textvariable=self.username, font=("Arial", 12), width=25).grid(row=1, column=0, pady=5)

        tk.Label(frame, text="Password", font=("Arial", 12)).grid(row=2, column=0, pady=10, sticky="w")
        self.password_entry = tk.Entry(frame, textvariable=self.password, font=("Arial", 12), width=25, show="*")
        self.password_entry.grid(row=3, column=0, pady=5)

        tk.Checkbutton(frame, text="Show Password", variable=self.show_password, command=self.toggle_password).grid(row=4, column=0, pady=5)

        tk.Button(frame, text="Login", command=self.login_function, font=("Arial", 12, "bold"), bg="black", fg="white", width=25).grid(row=5, column=0, pady=20)

    def toggle_password(self):
        if self.show_password.get():
            self.password_entry.config(show="")
        else:
            self.password_entry.config(show="*")

    def login_function(self):
        user = self.username.get()
        pwd = self.password.get()

        #  you can replace with your own uedr name and password
        if user == "sidharth" and pwd == "sidharth":
            messagebox.showinfo("Login Success", f"Welcome {user}")
            self.root.destroy()
            subprocess.Popen(["python", "hotel.py"])
        else:
            messagebox.showerror("Error", "Invalid Username or Password")


if __name__ == "__main__":
    root = tk.Tk()
    obj = LoginWindow(root)
    root.mainloop()



