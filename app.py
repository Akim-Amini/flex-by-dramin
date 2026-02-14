from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import os

app = Flask(__name__)

DATABASE = os.path.join("database", "flex.db")

def init_db():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    # Products table with description
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            description TEXT,
            price REAL,
            stock INTEGER
        )
    """)

    # Orders table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id INTEGER,
            product_name TEXT,
            price REAL,
            customer_name TEXT,
            customer_phone TEXT,
            customer_location TEXT,
            order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(product_id) REFERENCES products(id)
        )
    """)

    conn.commit()
    conn.close()

products = []

orders = []

@app.route("/")
def home():
    return render_template("base.html")

@app.route("/admin")
def admin_dashboard():
    return render_template("admin/dashboard.html")

@app.route("/admin/add-product", methods=["GET", "POST"])
def add_product():
    if request.method == "POST":
        name = request.form["name"]
        price = request.form["price"]
        stock = request.form["stock"]
        description = request.form["description"]

        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO products (name, price, stock, description)
            VALUES (?, ?, ?, ?)
        """, (name, price, stock, description))

        conn.commit()
        conn.close()

        return redirect(url_for("view_products"))

    return render_template("admin/add_product.html")

@app.route("/admin/products")
def view_products():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()

    conn.close()

    return render_template("admin/products.html", products=products)


@app.route("/shop")
def shop():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()

    conn.close()

    return render_template("shop.html", products=products)


@app.route("/order/<int:product_id>",methods=["GET", "POST"])
def order_product(product_id):
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM products WHERE id = ?", (product_id,))
    product = cursor.fetchone()

    if product and product["stock"] > 0:
        customer_name = request.form["customer_name"]
        customer_phone = request.form["customer_phone"]
        customer_location = request.form["customer_location"]

        new_stock = product["stock"] - 1

        cursor.execute("UPDATE products SET stock = ? WHERE id = ?", (new_stock, product_id))

        cursor.execute("""
            INSERT INTO orders 
            (product_id, product_name, price, customer_name, customer_phone, customer_location)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            product_id,
            product["name"],
            product["price"],
            customer_name,
            customer_phone,
            customer_location
        ))

        conn.commit()
        conn.close()

        order = {
            "product_name": product["name"],
            "price": product["price"],
            "customer_name": customer_name
        }

        return render_template("order_success.html", order=order)

    conn.close()
    return "Product not available"

@app.route("/admin/orders")
def view_orders():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM orders ORDER BY order_date DESC")
    orders = cursor.fetchall()

    conn.close()

    return render_template("admin/orders.html", orders=orders)


if __name__ =="__main__":
    init_db()
    app.run(debug=True)