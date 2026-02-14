from flask import Flask, render_template, request, redirect, url_for
import sqlite3
app = Flask(__name__)

def init_db():
    conn = sqlite3.connect("flex.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id INTEGER,
            product_name TEXT,
            price REAL,
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

        conn = sqlite3.connect("flex.db")
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
    conn = sqlite3.connect("flex.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()

    conn.close()

    return render_template("admin/products.html", products=products)


@app.route("/shop")
def shop():
    conn = sqlite3.connect("flex.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()

    conn.close()

    return render_template("shop.html", products=products)


@app.route("/order/<int:product_id>")
def order_product(product_id):
    conn = sqlite3.connect("flex.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM products WHERE id = ?", (product_id,))
    product = cursor.fetchone()

    if product and product["stock"] > 0:
        new_stock = product["stock"] - 1

        # Update stock
        cursor.execute("UPDATE products SET stock = ? WHERE id = ?", (new_stock, product_id))

        # Insert order into database
        cursor.execute("""
            INSERT INTO orders (product_id, product_name, price)
            VALUES (?, ?, ?)
        """, (product_id, product["name"], product["price"]))

        conn.commit()
        conn.close()

        order = {
            "product_name": product["name"],
            "price": product["price"]
        }

        return render_template("order_success.html", order=order)

    conn.close()
    return "Product not available"

@app.route("/admin/orders")
def view_orders():
    conn = sqlite3.connect("flex.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM orders ORDER BY order_date DESC")
    orders = cursor.fetchall()

    conn.close()

    return render_template("admin/orders.html", orders=orders)


if __name__ =="__main__":
    init_db()
    app.run(debug=True)