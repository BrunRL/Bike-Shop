from tkinter import Button, Frame
import database
from PIL import Image, ImageTk
from database import is_admin
from ui_helpers import *


def populate_products_list(content_frame, username, search_query="", category=None):
    def refresh_product():

        for widget in content_frame.winfo_children():
            widget.destroy() # Removes everything in the content_frame

        products = database.get_products()
        if search_query:
            products = [product for product in products if search_query.lower() in product[1].lower()] # Filters products based on what is inside the search bar
        if category:
            products = [product for product in products if product[4] == category] # Filters products based on what category the user wants to display

        row = 0
        column = 0

        # Creates a frame for product image and other information to go into using PIL
        for product in products:
            product_frame = Frame(content_frame)
            product_frame.grid(row=row, column=column, padx=10, pady=10, sticky='nsew')

            image = Image.open(product[3])
            image = image.resize((150, 100), Image.LANCZOS)
            photo = ImageTk.PhotoImage(image)

            image_label = Label(product_frame, image=photo)
            image_label.image = photo
            image_label.grid(row=0, column=0, padx=10, pady=10, sticky='nsew')

            Label(product_frame, text=f"Name: {product[1]}").grid(row=1, column=0, sticky='w')
            Label(product_frame, text=f"Price: {product[2]}").grid(row=2, column=0, sticky='w')

            Button(product_frame,
               text="Add to basket",
               command=lambda p=product[0]: database.add_to_basket(username, p, 1)
               ).grid(row=3, column=0, sticky='w') # Button which calls the add_to_basket function from the database to add a product to the basket

            # If the user is an admin, a remove product button that allows an admin to remove a product from the database is displayed
            if is_admin(username):
                remove_button = Button(product_frame,
                   text="Remove Product",
                   command=lambda p=product[0]: remove_product_button(p, remove_button)
                )
                remove_button.grid(row=4, column=0, sticky='w')

            column += 1

            if column >= 4:
                column = 0
                row += 1

            for i in range(4):
                content_frame.grid_columnconfigure(i, weight=1, uniform="equal")
            for i in range(row + 1):
                content_frame.grid_rowconfigure(i, weight=1, uniform="equal")

    # Creates a function for removing products and then refreshes the frame
    def remove_product_button(product_id, button):
        database.remove_products(product_id=product_id)
        button.destroy()
        refresh_product()

    refresh_product()

# Creates a function for showing products depending on category
def populate_category(content_frame, username, category):
    populate_products_list(content_frame, username, category=category)


