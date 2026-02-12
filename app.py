from flask import Flask, render_template, request, redirect, url_for
app = Flask(__name__)

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

        product = {
            "name": name,
            "price": price,
            "stock": stock,
            "description": description
        }

        products.append(product)

        return redirect(url_for("view_products"))

    return render_template("admin/add_product.html")

@app.route("/admin/products")
def view_products():
    return render_template("admin/products.html", products=products)

@app.route("/shop")
def shop():
    return render_template("shop.html", products=products)

@app.route("/order/<int:product_index>")
def order_product(product_index):
    if product_index < len(products):
        product = products[product_index]

        if int(product["stock"]) > 0:
            product["stock"] = str(int(product["stock"]) - 1)

            order = {
                "product_name": product["name"],
                "price": product["price"]
            }

            orders.append(order)

            return render_template("order_success.html", order=order)

    return "Product not available"



if __name__ =="__main__":
    app.run(debug=True)