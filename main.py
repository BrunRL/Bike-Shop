from tkinter import Tk, ttk
import tkinter
import auth
import database
from ui_helpers import create_label, create_entry


def main():

    # Initialize the database
    database.create_table()


    # Creates the main window
    window = Tk()
    window.title("Login System")
    window.geometry("600x600")

    window.tk.call("source", "Azure-ttk-theme-2.1.0/azure.tcl")
    window.tk.call("set_theme", "light")

    # Creates text for company name
    msg = tkinter.Message(window, text='Bricks-and-Mortar', aspect=1000)
    msg.pack()

    # Login section using UI helpers
    create_label(window, "Username")
    username_entry = create_entry(window)

    create_label(window, "Password")
    password_entry = create_entry(window, show="*")

    create_label(window, "Age")
    age_entry = create_entry(window)


    # Login button
    login_button = ttk.Button(window, text="Login", style='TButton', command=lambda: auth.login(window, username_entry, password_entry, age_entry))
    login_button.pack(pady=10)

    # Signup button
    signup_button = ttk.Button(window, text="Sign Up", style='TButton', command=lambda: auth.sign_up(window))
    signup_button.pack(pady=10)

    # Quit button
    quit = ttk.Button(window, text='Quit', style='Accent.TButton', command=window.quit)
    quit.pack()
    quit.place(relx=0.1, rely=0.9, anchor="sw")

    window.mainloop()

if __name__ == "__main__":
    main()

