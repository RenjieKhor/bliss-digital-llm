from customer_service import CustomerService
from dotenv import dotenv_values
from flask import Flask

app = Flask(__name__)

secrets = dotenv_values(".env")

customer_service = CustomerService(secrets["OPENAI_KEY"])

if __name__ == "__main__":
    app.run(debug=True)