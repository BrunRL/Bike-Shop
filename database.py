import sqlite3


# Connects to sql and creates users.db file
def create_connection():
    conn = sqlite3.connect("users.db")
    return conn

# Creates a table for users
def create_table():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT,
            age INT,
            admin BOOL
        )
    """)
    conn.commit()
    conn.close()

# Function to add users to the user table
def add_user(username, password, age, admin):
    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO users (username, password, age, admin) VALUES (?, ?, ?, ?)", (username, password, age, admin))
        conn.commit()
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()
    return True

# Function to see if a user has admin permissions which gives the user access to other parts of the application
def is_admin(username):
    try:
        conn = create_connection()
        cursor = conn.cursor()

        query = "SELECT admin FROM users WHERE username = ?"
        cursor.execute(query, (username,))
        result = cursor.fetchone()

        if result is None:
            return False

        return bool(result[0])
    except Exception as e:
        print(f"Error: {e}")
        return False
    finally:
        if conn:
            conn.close()

# Function for defining a verified user, selecting username, password and age values from the database
def verify_user(username, password, age):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ? AND password = ? AND age = ?", (username, password, age))
    user = cursor.fetchone()
    conn.close()
    return user is not None

# Creates a table in the database for products
def create_product_table():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("""
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                price REAL,
                image_path TEXT,
                category TEXT
            )
        """)
    conn.commit()
    conn.close()

# Creates a table in the database for the basket
def create_basket_table():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("""
            CREATE TABLE IF NOT EXISTS basket (
                username TEXT NOT NULL,
                product_id INTEGER NOT NULL,
                quantity INTEGER NOT NULL,
                PRIMARY KEY (username, product_id)  -- Composite primary key
            )
        """)
    conn.commit()
    conn.close()

# Creates a table in the database for orders
def create_orders_table():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("""
            CREATE TABLE IF NOT EXISTS orders (
                username TEXT NOT NULL,
                product_id INTEGER NOT NULL,
                quantity INTEGER NOT NULL,
                PRIMARY KEY (username, product_id)
            )
        """)
    conn.commit()
    conn.close()

# Function for moving items from the basket into the orders table
def move_basket_to_orders(username):
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT username, product_id, quantity FROM basket WHERE username = ?", (username,))
    basket_items = cursor.fetchall()

    for item in basket_items:
        username, product_id, quantity = item
        cursor.execute("""
            INSERT or IGNORE INTO orders (username, product_id, quantity)
            VALUES (?, ?, ?)
        """, (username, product_id, quantity))

    cursor.execute("DELETE FROM basket WHERE username = ?", (username,))

    conn.commit()
    conn.close()

# Creates a function for adding products into the product table
def add_product(name, price, image_path, category):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO products (name, price, image_path, category) VALUES (?, ?, ?, ?)",
                   (name, price, image_path, category))
    conn.commit()
    conn.close()

# Function for pulling values out of products table
def get_products():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT *FROM products")
    products = cursor.fetchall()
    conn.close()
    return products

# Function for removing products from the product table
def remove_products(product_id):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM products WHERE id = ?", (product_id,))
    conn.commit()
    conn.close()

# Function for adding username, product id and quantity values into the basket table
def add_to_basket(username, product_id, quantity):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("""INSERT INTO basket (username, product_id, quantity) VALUES (?, ?, ?)
                   ON CONFLICT (username, product_id) DO UPDATE SET quantity=quantity+excluded.quantity""",
                   (username, product_id, quantity))
    conn.commit()
    conn.close()

# Pulls all values from the basket table depending on the current user
def get_basket(username):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("""
    SELECT p.name, p.price, b.quantity, p.id, (p.price * b.quantity) AS total
    FROM basket b
    JOIN products p on b.product_id = p.id
    WHERE b.username = ?
    """, (username,))

    basket_items = cursor.fetchall()
    conn.close()
    return basket_items

# Function for removing an item from basket depending on user/product id
def remove_from_basket(product_id, username):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM basket WHERE product_id = ? AND username = ?", (product_id, username))
    conn.commit()
    conn.close()

if __name__ == '__main__':
    create_table()
    create_product_table()
    create_basket_table()
    create_orders_table()

    add_user(username="admin", password="Admin123*", age="18", admin="true")

    add_product("Bike 43", 80, "image/Bike 43.png", category="Bike")
    add_product("Wishbone", 30, "image/Wishbone.png", category="Bike")
    add_product("Endurance Pro", 100, "image/Endurance Pro.png", category="Bike")
    add_product("Carrera Axle", 225, "image/Carrera Axle.png", category="Bike")
    add_product("Carrera Hellcat", 410, "image/Carrera Hellcat.png", category="Bike")
    add_product("GSX-8S", 8300, "image/GSX-8S.png", category="Bike")
    add_product("Trail Helmet", 10, "image/Trail Helmet.png", category="Helmet")
    add_product("Scorpion Shell Helmet", 30, "image/Scorpion Shell Helmet.png", category="Helmet")
    add_product("Ultra Helmet", 45, "image/Ultra Helmet.png", category="Helmet")
    add_product("Front Bike Light 500 Lumen", 25, "image/Front Bike Light.png", category="Light")

