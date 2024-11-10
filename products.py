import time                 # To access sleep()
def product_store(self):    # Function to store products
    self.products = {
                1: {
                    1: {"Name": "Samsung Galaxy S21", "Price": "Rs.69999", "Quantity": 50, "Availability": "In Stock",
                        "Color": "Phantom Gray", "Description": "Flagship smartphone with 5G capability and advanced camera features."},
                    2: {"Name": "iPhone 13 Pro", "Price": "Rs.99900", "Quantity": 20, "Availability": "In Stock",
                        "Color": "Graphite", "Description": "Apple's latest flagship smartphone with ProMotion display and A15 Bionic chip."}
                },
                2: {
                    1: {"Name": "Apple Watch Series 7", "Price": "Rs.41900", "Quantity": 15, "Availability": "In Stock",
                        "Color": "Midnight", "Description": "Latest generation Apple smartwatch with larger display and advanced health monitoring."},
                    2: {"Name": "Samsung Galaxy Watch 4", "Price": "Rs.28999", "Quantity": 25, "Availability": "In Stock",
                        "Color": "Black", "Description": "Samsung's premium smartwatch with extensive fitness tracking features."}
                },
                3: {
                    1: {"Name": "JBL Charge 5", "Price": "Rs.17999", "Quantity": 12, "Availability": "In Stock",
                        "Color": "Squad", "Description": "Portable Bluetooth speaker with powerful bass and IPX7 waterproof rating."},
                    2: {"Name": "Bose SoundLink Mini II", "Price": "Rs.19990", "Quantity": 8, "Availability": "In Stock",
                        "Color": "Carbon", "Description": "Compact Bluetooth speaker known for its balanced sound and portability."}
                },
                4: {
                    1: {"Name": "Apple AirPods Pro", "Price": "Rs.24900", "Quantity": 25, "Availability": "In Stock",
                        "Color": "White", "Description": "Apple's premium noise-cancelling earbuds with Transparency mode."},
                    2: {"Name": "Samsung Galaxy Buds Pro", "Price": "Rs.15990", "Quantity": 18, "Availability": "In Stock",
                        "Color": "Phantom Black", "Description": "Samsung's true wireless earbuds with intelligent active noise cancellation."}
                }
    }

def timer(count):       # FUnction to delay for needed seconds
    print("Please wait! Loading..")
    while count > 0:
        if count == 1:
            print(count, end="\n")
        else:
            print(count, end="-")
        time.sleep(1)
        count -=1
def mainmenu(self):     # Function to go back mainmenu()
    ch=input("If you want to go back main menu (yes/Press any key to continue) : ").lower()
    if ch=="yes":
        timer(3)
        self.main()
    
