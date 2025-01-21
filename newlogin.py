# Import modules
from tkinter import *
import os

# Helper function to destroy widgets
def destroy_widgets(parent):
    for widget in parent.winfo_children():
        widget.destroy()

# Register screen
def register():
    destroy_widgets(root)
    root.title("Register")
    root.geometry("300x250")

    global username, password, username_entry, password_entry

    username = StringVar()
    password = StringVar()

    Label(root, text="Please enter details below", bg="blue").pack()
    Label(root, text="").pack()
    
    Label(root, text="Username * ").pack()
    username_entry = Entry(root, textvariable=username)
    username_entry.pack()

    Label(root, text="Password * ").pack()
    password_entry = Entry(root, textvariable=password, show='*')
    password_entry.pack()

    Label(root, text="").pack()
    Button(root, text="Register", width=10, height=1, bg="blue", command=register_user).pack()

# Register user logic
def register_user():
    username_info = username.get()
    password_info = password.get()

    with open(username_info, "w") as file:
        file.write(username_info + "\n")
        file.write(password_info)

    username_entry.delete(0, END)
    password_entry.delete(0, END)

    Label(root, text="Registration Success", fg="green", font=("calibri", 11)).pack()
    Button(root, text="Go to Login", command=main_account_screen).pack()

# Login screen
def login():
    destroy_widgets(root)
    root.title("Login")
    root.geometry("300x250")

    global username_verify, password_verify, username_login_entry, password_login_entry

    username_verify = StringVar()
    password_verify = StringVar()

    Label(root, text="Please enter details below to login").pack()
    Label(root, text="").pack()

    Label(root, text="Username * ").pack()
    username_login_entry = Entry(root, textvariable=username_verify)
    username_login_entry.pack()

    Label(root, text="").pack()
    Label(root, text="Password * ").pack()
    password_login_entry = Entry(root, textvariable=password_verify, show='*')
    password_login_entry.pack()

    Label(root, text="").pack()
    Button(root, text="Login", width=10, height=1, command=login_verify).pack()

# Login verification logic
def login_verify():
    username1 = username_verify.get()
    password1 = password_verify.get()

    username_login_entry.delete(0, END)
    password_login_entry.delete(0, END)

    if os.path.exists(username1):
        with open(username1, "r") as file:
            verify = file.read().splitlines()
            if password1 in verify:
                login_success()
            else:
                popup_message("Invalid Password")
    else:
        popup_message("User Not Found")

# Popup message
def popup_message(message):
    popup = Toplevel(root)
    popup.title("Message")
    popup.geometry("150x100")
    Label(popup, text=message).pack()
    Button(popup, text="OK", command=popup.destroy).pack()

# Login success
def login_success():
    popup_message("Login Success")

# Main account screen
def main_account_screen():
    destroy_widgets(root)
    root.title("Account Login")
    root.geometry("300x250")

    Label(root, text="Select Your Choice", bg="blue", width="300", height="2", font=("Calibri", 13)).pack()
    Label(root, text="").pack()

    Button(root, text="Login", height="2", width="30", command=login).pack()
    Label(root, text="").pack()

    Button(root, text="Register", height="2", width="30", command=register).pack()

# Initialize main window
root = Tk()
main_account_screen()
root.mainloop()
