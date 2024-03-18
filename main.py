from customer_service import CustomerService

customer_service = CustomerService("YOUR_API_KEY")

if __name__ == "__main__":
    customer_service.init()
    customer_service.run()