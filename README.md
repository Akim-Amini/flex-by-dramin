Flex by Dramin

Flex by Dramin is a web-based business management system built using Flask (Python).
The project is designed to support real-world business operations such as product listing, customer orders, installment payments, delivery management, and business record tracking.

This project is also a learning-focused system, helping the developer improve skills in web development, backend logic, databases, and system design.

Project Motivation

I am both:

a businessman (selling jerseys and other goods), and

a Computer Science student

This project helps me:

digitize my business operations

manage customers efficiently

track installment payments

practice real-world software development skills

The system is designed to be scalable, meaning it is not limited to jerseys only and can support other products in the future.

Features (Current & Planned)
Admin (Business Owner)

Upload new products (e.g. jerseys)

Update product stock automatically after sales

View all customer orders

Register customers taking products on installment

Track installment payments (2-week period)

Identify customers who delay or fail to pay

Manage delivery status around Mangochi town

View business records (sales, stock, customers)

Customers

View available products

Place orders

Choose installment payment option

Track order and delivery status

Delivery Management

Free delivery within Mangochi town

Track delivered and pending orders

Technology Stack

Backend: Python (Flask)

Frontend: HTML, CSS (Bootstrap later)

Database: SQLite (for development)

Version Control: Git & GitHub

IDE: PyCharm

Operating System: Windows

Project Structure
Flex_By_Dramin/
│
├── static/
│   └── css/
│       └── style.css
│
├── templates/
│   └── index.html
│
├── app.py          # Main Flask application
├── main.py         # Entry/testing file
├── .gitignore
└── README.md

Installation & Setup

Clone the repository:

git clone https://github.com/Akim-Amini/flex-by-dramin.git


Navigate into the project:

cd flex-by-dramin


Create and activate virtual environment:

python -m venv .venv
.venv\Scripts\activate


Install dependencies:

pip install flask


Run the application:

python app.py


Open browser and visit:

http://127.0.0.1:5000/

Future Enhancements

User authentication (Admin & Customers)

Database integration with MySQL/PostgreSQL

Installment payment reminders

Reports & analytics dashboard

Mobile-friendly UI

SMS/WhatsApp payment follow-up notifications

Developer

Akim Amini
Computer Science Student & Entrepreneur
Brand: Flex by Dramin

License

This project is for learning and personal business use.
Further licensing will be added in future versions.