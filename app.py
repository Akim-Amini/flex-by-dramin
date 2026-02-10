from flask import Flask, render_template
app = Flask(__name__)

@app.route("/")
def home():
    return render_template("base.html")

@app.route("/admin")
def admin_dashboard():
    return render_template("admin/dashboard.html")

@app.route("/admin/add-product")
def add_product():
    return render_template("admin/add_product.html")


if __name__ =="__main__":
    app.run(debug=True)