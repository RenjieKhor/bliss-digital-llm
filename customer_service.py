from openai import OpenAI

class CustomerService:
    
    def __init__(self, api_key):
        self.client = OpenAI(api_key=api_key)
        self.messages = []
        self.customer_helped = False
        self.user_reply = ""
        self.ai_reply = ""
        self.role = "system"
        self.invoice_que = "@invoice"
        self.price_que = "@price"

    def init(self):
        #Start with preparing the AI with the initial data/messages
        self.messages = [
                {"role": "system", "content": "You are an online customer service."},
                {"role": "user", "content": f"Of the following text, convert the wishes into a json containing keys enclosed in single quotes for furniture type, amount of legs, color, material, length, width, height. If there is missing information to complete the json, keep asking questions to get this info. If all values for the keys are obtained, start the reply with the tag {self.invoice_que} (very important) followed by the json and a message implying what the price will be, but replace the currency sign and numeric value of the price by the tag {self.price_que}, all in one message (also very important). The most important rule is not to mention the json without those tags. If the customer is satisfied, he/she will say GERONIMO, reply with GERONIMO in capitals"},
                {"role": "system", "content": "okay."},
                {"role": "user", "content": "Start your roleplay, acting as if we never had this conversation."}
              ]
        completion = self.client.chat.completions.create(
                  model="gpt-3.5-turbo",
                  messages = self.messages
                )
        
        #Save the initial message of the AI
        self.ai_reply = completion.choices[0].message.content
        self.add_message(self.ai_reply)


    # A helper function for appending the replies to the list of messages
    def add_message(self, message):
        self.messages.append({"role":self.role, "content":message})


    # A function that handles the reply of the AI
    def handle_ai(self):
        self.role = "system"
        completion = self.client.chat.completions.create(
                  model="gpt-3.5-turbo",
                  messages = self.messages
                )
        
        self.ai_reply = completion.choices[0].message.content
        self.add_message(self.ai_reply)

        if self.invoice_que in self.ai_reply:
            self.handle_invoice()


    # A function that handles user input and saves their messages
    def handle_user(self):
        self.role = "user"
        self.user_reply = input(self.ai_reply + "\n")
        self.add_message(self.user_reply)


    # Return an invoice to the user by custom adding the reply
    def handle_invoice(self):
        self.ai_reply = self.ai_reply.replace(f"{self.invoice_que}", "")
        self.ai_reply = self.ai_reply.replace(f"{self.price_que}", "€200")
        print(self.ai_reply)
        exit()

    def run(self):
        while(not self.customer_helped):
            
            self.handle_user()
            self.handle_ai()

            # Exit criteria
            if("GERONIMO" in self.ai_reply):
                self.customer_helped = True