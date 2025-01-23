from tkinter import Label, ttk
import database


def populate_basket(content_frame, username):
    def refresh_basket(): # Function for deleting and then re-adding what is inside the basket for when basket items are added or removed
        for widget in content_frame.winfo_children():
            widget.destroy()


        basket_items = database.get_basket(username)
        total_price = 0


        for item in basket_items:
            create_str = f"{item[0]} - ${item[1]} * {item[2]} = ${item[4]}"
            Label(content_frame, text=create_str).pack(pady=10)
            total_price += item[4] # Calculates total price of basket

            remove_basket = ttk.Button(content_frame,
                               text="Remove From Basket", style='TButton',
                               command=lambda p=item[3]: remove_basket_button(p, remove_basket, username)
                               )
            remove_basket.pack(pady=1) # Removes individual item from basket

        order_button = ttk.Button(content_frame, text="Order", style='TButton', command=order)
        order_button.pack(pady=20, anchor='s') # Adds basket items into order table

        Label(content_frame, text=f"Total: ${total_price}").pack(pady=20)

        discount_code="BR1CKS4NDM0RT4R" # assigns discount code relative to the QR code

        # Function that, if the entry is equal to the discount code, displays the total price after discount
        def discount_apply():
            user_code = discount_entry.get().strip()

            if user_code == discount_code:
                Label(content_frame, text=f"Total after discount: ${total_price - (total_price * 0.1)}").pack(pady=20)

        # Creates an entry for the discount code
        discount_entry = ttk.Entry(content_frame, style='TEntry')
        discount_entry.pack(pady=10, padx=10, anchor='s')

        #Creates a button for applying the discount code using the discount_apply command
        apply_button = ttk.Button(content_frame, style='TButton', command=discount_apply, text="Apply Discount")
        apply_button.pack(pady=10, padx=10, anchor='s')


    # Creates a function for removing items from the basket using parameters from the database, the button is then destroyed and basket is refreshed
    def remove_basket_button(product_id, button, username):
        database.remove_from_basket(product_id=product_id, username=username)
        button.destroy()
        refresh_basket()

    # Creates a function that runs moves to basket to order, prints to console that items have been ordered and then refreshes the basket
    def order():
        database.move_basket_to_orders(username)
        print("Items have been ordered.")
        refresh_basket()




    refresh_basket()









