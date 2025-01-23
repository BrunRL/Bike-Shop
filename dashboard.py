from tkinter import Toplevel, Label, Frame, Button, Entry, StringVar, ttk
from product import populate_products_list
from basket import populate_basket
from qr_code import open_qr_code_menu

# Creates the dashboard window and opens in a maximised window
def open_dashboard(window, username):
    window.destroy()
    dashboard = Toplevel()
    dashboard.title("Dashboard")
    dashboard.geometry("400x300")
    dashboard.state('zoomed')

    dashboard.tk.call("source", "Azure-ttk-theme-2.1.0/azure.tcl") # Loads the azure theme
    dashboard.tk.call("set_theme", "light") # Sets azure theme to light mode

    ttk.Label(dashboard, text="Bricks and Mortar", style='TLabel',  font=("Arial", 16)).pack(pady=50)

    search_frame = Frame(dashboard) # Creates a frame for the search bar
    search_frame.pack(side='top', fill='x', pady=5, anchor='nw')

    content_frame = ttk.Frame(dashboard, style='Card.TFrame') # Creates a frame for the products
    content_frame.pack(fill='both', expand=True)

    def load_content(populate_function, *args): # Function that removes everything from the content frame and then re-adds using populate_function
        for widget in content_frame.winfo_children():
            widget.destroy()
        populate_function(content_frame, *args)

    ttk.Button(dashboard, text="View basket", style='Accent.TButton',
           command=lambda: load_content(populate_basket, username)
           ).pack(side='top', pady=5, anchor='s') # Creates a button that shows what is inside the basket using populate_basket

    ttk.Button(dashboard, text="QR Codes", style='TButton',
           command=lambda: open_qr_code_menu()
           ).pack(side='top', pady=5, anchor='s')
    load_content(populate_products_list, username, "") # Creates a button that displays the qr code menu


    search_var = StringVar()

    def on_search(event=None):
        query = search_var.get()
        load_content(populate_products_list, username, query) # Function which takes search bar value and then shows products based on the value


    # Creates a search button and entry which when the search button is pressed or key is released in the entry, on_search is run
    Label(search_frame, text="Search: ").pack(side='left', padx=5)
    search_entry = Entry(search_frame, textvariable=search_var, width=30)
    search_entry.pack(side='left', padx=5)
    Button(search_frame, text="Search", command=on_search).pack(side='left', padx=5)
    search_entry.bind("<KeyRelease>", on_search)

    ttk.Button(search_frame, text="View All Products", style='Accent.TButton',
           command=lambda: load_content(populate_products_list, username, "")
           ).pack(side='left', padx=10) # Creates a button to view all products

    ttk.Button(search_frame, text="Bikes", style='TButton',
           command=lambda: load_content(populate_products_list, username, "", "Bike")
           ).pack(side='left', padx=5) # Creates a button to view all bikes

    ttk.Button(search_frame, text="Helmets", style='TButton',
           command=lambda: load_content(populate_products_list, username, "", "Helmet")
           ).pack(side='left', padx=5) # Creates a button to view all helmets

    ttk.Button(search_frame, text="Lights", style='TButton',
           command=lambda: load_content(populate_products_list, username, "", "Light")
           ).pack(side='left', padx=5) # Creates a button to view all lights




