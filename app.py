from flask import Flask, render_template, request, redirect, url_for
import sqlite3
app = Flask(__name__)

def init_db():
    conn = sqlite3.connect("flex.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            price REAL NOT NULL,
            stock INTEGER NOT NULL,
            description TEXT
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

        cursor.execute("UPDATE products SET stock = ? WHERE id = ?", (new_stock, product_id))
        conn.commit()
        conn.close()

        order = {
            "product_name": product["name"],
            "price": product["price"]
        }

        return render_template("order_success.html", order=order)

    conn.close()
    return "Product not available"



if __name__ =="__main__":
    init_db()
    app.run(debug=True)