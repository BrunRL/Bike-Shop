from tkinter import Toplevel, Button, messagebox
import database
from dashboard import open_dashboard
from ui_helpers import create_label, create_entry
from re import search

# Takes user entries for username, password, age to sign up
def sign_up(window):
    signup_window = Toplevel(window)
    signup_window.title("Sign Up")
    signup_window.geometry("300x200")

    # Use ui_helpers to create labels and entries
    create_label(signup_window, "Username")
    username_entry = create_entry(signup_window)

    create_label(signup_window, "Password")
    password_entry = create_entry(signup_window, show="*")

    create_label(signup_window, "Age")
    age_entry = create_entry(signup_window)

    def handle_signup(): # Checks for the validity of each entry in signup, displaying errors if incorrect
        username = username_entry.get()
        password = password_entry.get()
        age = age_entry.get()

        if not is_password_valid(password):
            messagebox.showwarning("Input Error", "Please enter a valid password.")
            return

        if not is_age_valid(age):
            messagebox.showwarning("Input Error",
                                   "Please enter a valid age. You must be older than 18 to use this application.")
            return

        if not username or not password or not age:
            messagebox.showwarning("Input Error", "Please fill in all fields.")
            return

        if database.add_user(username, password, age,False):
            messagebox.showinfo("Success", "Account created successfully!")
            signup_window.destroy()
        else:
            messagebox.showerror("Error", "Username already exists!")

    Button(signup_window, text="Sign Up", command=handle_signup).pack(pady=10)

<<<<<<< Updated upstream
# Defines the parameters for what makes a password valid or invalid
def is_password_valid(password: str) -> bool:
    if not password \
            or len(password) < 8 \
            or not search("[a-z]", password) \
            or not search("[A-Z]", password) \
            or not search("[1-9]", password) \
            or search("\s", password):
        return False
    return True

# If the user is younger than 18, returns false
def is_age_valid(age: int) -> bool:
    if not age \
            or int(age) < 18:
        return False
    return True

# Checks for the validity of each entry in login, displaying errors if incorrect
def login(window, username_entry, password_entry, age_entry):
=======

def login(window, username_entry, password_entry):
>>>>>>> Stashed changes
    username = username_entry.get()
    password = password_entry.get()
    age = age_entry.get()

    if not is_password_valid(password):
        messagebox.showwarning("Input Error", "Please enter a valid password.")
        return

    if not is_age_valid(age):
        messagebox.showwarning("Input Error", "Please enter a valid age. You must be older than 18 to use this application.")
        return

    if not username:
        messagebox.showwarning("Input Error", "Please enter both username and password.")
        return

    if database.verify_user(username, password, age):
        messagebox.showinfo("Success", "Login successful!")
        open_dashboard(window, username)
    else:
        messagebox.showerror("Error", "Invalid credentials")