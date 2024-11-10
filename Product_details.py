from products import timer                                      # Import timer function from products.py
import mysql.connector                                          # Import mysql.connector for database connection
from tabulate import tabulate                                   # Import tabulate module for viewing in table formats
from cart import Cart                                           # Import the cart class in cart.py module
import re                                                       # Import re for validation
from checkout import checkout                                   # Import checkout for access methods in class checkout
from file_write import write_file                               # Import file_write ro access methos in class write_file
from db_connection import db_connection                         # Implement db_connection to implement db_connection
from back_menu import go_back                                   # Import back_menu to go back previous menu every time
from payment_process import checkout_sub
class product_management:           # Creating a class which contains all the methods
    def __init__(self):             # Creating a constructor 
        db_obj = db_connection()
        self.db_connection = db_obj.db_connection
        self.cursor = db_obj.cursor
        self.temp = None  # refers category id  
        self.choice = None  # refers product id
        self.cart_obj = Cart()   # Creating object for class cart
        self.write_file_obj=write_file()
        self.go_back_obj=go_back()
        self.payment_obj=checkout_sub()
    def __del__(self):
        self.db_connection.close()
        self.cursor.close()

    def main(self, user_email):  # main which contains all functions to be called
        while True:
            print("\n===Main Menu===\n\n1. Display Categories\n2. Display Products\n3. View Product Details\n4. Search Products\n5. Your Cart\n6. Checkout\n7. Exit\n")
            ch = input("Enter Your Choice : ")
            if ch == "1":
                self.display_category()  # Call function to display categories...
            elif ch == "2":
                self.display_products()  # Call function to display products...
            elif ch == "3":
                self.product_details(user_email)  # Call function to view product details...
            elif ch == "4":
                self.search_products()  # Call function to search product by name...
            elif ch == "5":
                self.view_cart(user_email)  # Delegate to cart class for cart details
            elif ch=="6":
                checkout_obj=checkout()
                checkout_obj.main(user_email)
            elif ch == "7":
                print("Exiting...")  # If user wants to exit...
                break
            else:  # if user entered invalid choice...
                print("Invalid choice! Please Try again..")

    def display_category(self):  # To Display categories...
        categories = [
            ["1.", "Smartphones"],
            ["2.", "Smartwatches"],
            ["3.", "Speakers"],
            ["4.", "Earbuds"]
        ]
        header = ["S.No", "Categories"]     # Headers for the table
        print(tabulate(categories, headers=header, tablefmt="fancy_grid"))  # Display it in a table  format

    def display_products(self):     # To display products
        self.display_category()     # Call function to display  categories
        try:
            while True:
                choice = self.go_back_obj.get_input("Enter the Category index to view products (enter 'back' to go back) : ")      # Get the category index
                if choice is None:
                    return True
                print("\n")
                self.temp = choice                                                  # Store the index for further use
                query = "select productid, name, price, quantity, availability from products where categoryID=%s"   # retrive all the products in that category
                self.cursor.execute(query, (choice,))
                results = self.cursor.fetchall()                # Store it in results variable
                if results:                                     # Display the product details if found
                    headers = ["Product ID", "Name", "Price", "Quantity", "Availability"]
                    print(tabulate(results, headers=headers, tablefmt="grid"))
                    break
                else:                                           # To solve invalid category index
                    print("Category index not found!..\n")
        except Exception as e:                                      
            self.write_file_obj.error_logging("Error in display products : "+str(e))

    def product_details(self, user_email):                      # Function to disp\lay the details of the product
        if self.display_products():                                 # Call function to display categories and as well products
            return
        try:
            while True:
                choice = self.go_back_obj.get_input("Enter the product index to view product details (enter 'back' to go back) : ")    # Get the product index
                if choice is None:
                    break
                print("\n")
                query = "select id,name, price, quantity, availability, color, description, average_rating from products where categoryId=%s and productID=%s" # Retrive product details based on the categoryy and product index
                self.cursor.execute(query, (self.temp, choice))         
                results = self.cursor.fetchall()        # Store it
                if results:                             # If found, display the whole product details
                    self.display_details(results)
                    self.view_review(self.temp, choice) # call function to view review for the product or not
                    ch_1=self.go_back_obj.get_input("Add to cart (Yes/press any key to continue) (enter 'back' to go back) : ")     # Asks user to add cart
                    if ch_1 is None:                    # if user wish to go back
                        continue
                    if ch_1.lower()=="yes":
                        while True:
                            quan=self.go_back_obj.get_input("Enter quantity : (enter 'back' to go back) : ")                 # get quantity of the product to add to cart
                            if quan is None:
                                return
                            try :
                                quan=int(quan)
                                if quan > 0:               # If quan is greater than zero
                                    query_id="SELECT ID FROM PRODUCTS WHERE CATEGORYID=%s AND PRODUCTID=%s"     # query to get id of the respective product
                                    self.cursor.execute(query_id,(self.temp,choice))
                                    id_s=self.cursor.fetchone()
                                    query_cart="INSERT INTO CARTDETAILS VALUES(%s,%s,%s,%s,%s)"                 # Insert the product details to cart table
                                    self.cursor.execute(query_cart,(user_email,self.temp,choice,int(id_s[0]),quan))
                                    self.db_connection.commit()
                                    print("Product added to cart..")
                                    break
                            except ValueError:
                                print("Please enter a valid integer from quantity...")
                    ch_2=self.go_back_obj.get_input("Add to Wishlist (Yes/press any key to continue) (enter 'back' to go back) : ") # Asks user to add to wishlist
                    if ch_2 is None:                    # IF user wish to go back
                        continue
                    if ch_2.lower()=="yes":
                        query_wishlist="INSERT INTO Wishlist VALUES(%s,%s,%s)"  # Insert the product details to wishlist table
                        self.cursor.execute(query_wishlist,(user_email,self.temp,choice))
                        self.db_connection.commit()
                        print("Product added to Wishlist..")
                    query_idk="SELECT ID FROM PRODUCTS WHERE CATEGORYID=%s AND PRODUCTID=%s"     # query to get id of the respective product
                    self.cursor.execute(query_idk,(self.temp,choice))
                    id_s=self.cursor.fetchone()
                    if not self.purchasing(user_email,int(id_s[0])): # call function to user purchase the product or not
                        continue
                    else:
                        break
                else:                                   # If not found
                    print("Product index not found!..\n")
        except Exception as e:
            self.write_file_obj.error_logging("Error in products details : "+str(e))

    def display_details(self, results):                 # function to display product details
        try:
            headers = ["ID","Name", "Price", "Quantity", "Availability", "Color", "Description", "Average Rating"]       # Headers for the table
            print(tabulate(results, headers=headers, tablefmt="grid"))                                        # Display it in a table format
        except Exception as e:
            self.write_file_obj.error_logging("Error in display details : "+str(e))

    def view_review(self, cat_id, prod_id):             # Fuction to view review for the product or not
        try:
            while True:
                rev_tag = input("Wish to see the review for the product (yes/any key to continue) : ").lower()  # Get user wish
                if rev_tag == "yes":            # If yes to see review
                    query = "SELECT ID FROM products WHERE categoryID=%s and productID=%s"        # Retrive the review of the  respective product
                    self.cursor.execute(query, (cat_id, prod_id))
                    results = self.cursor.fetchone()        # Store it
                    query_rev="SELECT reviews from product_reviews WHERE review_ID=%s"
                    self.cursor.execute(query_rev,(results[0],))
                    review_content=self.cursor.fetchall()
                    if review_content:                 # If any review found
                        headers = ["Review"]
                        print("\nReviews given...\n")
                        print(tabulate(review_content, headers=headers, tablefmt="grid"))      # Display the review
                        break
                    else:                       # If no reviews found
                        print("No Reviews yet..")
                        break
                else:                       # If user does not wish to see the review
                    break
        except Exception as e:
            self.write_file_obj.error_logging("Error in view review : "+str(e))

    def search_products(self):          # Function to search product
        try:
            while True:
                ch = input("\n1. Name\n2. Price\n3. Exit\n\nEnter Your choice : ")       # Asks user to search product by name or price
                if ch == "1":                                                   # if name
                    choice = self.go_back_obj.get_input("Enter the product name to search : (enter 'back' to go back) : ")       # get name
                    if choice is None:
                        continue
                    print("\n")
                    query_1 = "select id,name, price, quantity, availability, color, description, average_rating from products where name LIKE CONCAT('%', %s, '%')"   # retrivve the product details based on the name
                    self.cursor.execute(query_1, (choice,))
                    results = self.cursor.fetchall()            # Store it in
                    if results:                                 # If any products found
                        print("Products under", choice, "are listed below...")
                        self.display_details(results)           # Call function to display it
                    else:                                       # If no products found
                        print("Name not found!..\n")
                elif ch == "2":                                 # If price
                    self.display_category()                     # To display categories
                    cat_tag = self.go_back_obj.get_input("Enter Category index to search : (enter 'back' to go back) : ")    # get the category index
                    if cat_tag is None:
                        continue
                    if cat_tag in "1234":
                        self.temp = cat_tag                     # Store it for further use
                        price_tag = self.go_back_obj.get_input("Enter the price amount : (enter 'back' to go back) : ")  # Get the price
                        if price_tag is None:
                            continue
                        regix = r'^\d+$'                        # Regic for price validation
                        if re.match(regix, price_tag):          # If valid
                            query_2 = "SELECT id,name, price, quantity, availability, color, description, average_rating FROM PRODUCTS WHERE categoryID=%s and Price<=%s"  # Get the products under the given price
                            self.cursor.execute(query_2, (self.temp, price_tag))
                            results = self.cursor.fetchall()            # store it in
                            if results:                         # If any products found
                                print("\nProducts Under", price_tag, "are listed below...")
                                self.display_details(results)       # Display it
                            else:                               # if no products found
                                print("No products within the specified price range...")
                        else:                           
                            print("Invalid price input...")
                    else:                                       # if user enters invalid category index
                        print("Category Index not found...")
                elif ch=="3":
                    print("Exiting...")
                    break
                else:
                    print("Invalid choice...")
        except Exception as e:
            self.write_file_obj.error_logging("Error in search products : "+str(e))
    def purchasing(self,user_email,id_s):                       # Function to purchase the product
        while True:
            pay_ch=self.go_back_obj.get_input("Do you wish to purchase the product (yes/any key to continue) : (enter 'back' to go back) : ")        # Asks user to yes or not to purchase
            if pay_ch is None:
                return False
            if pay_ch.lower()=="yes":              
                cash_on_online=input("\n1. Cash on delivery\n2. Online payment\n3. Exit\n\nEnter Your choice : ") # asks user payment way
                if cash_on_online=="1":
                   self.payment_obj.cash_on(user_email,id_s)    # Call function to go on cash on delivery
                   return True
                elif cash_on_online=="2":
                    self.payment_obj.online_pay(user_email,id_s)    # Call function to  go on online payment
                    return True
                elif cash_on_online=="3":                           # Exits from the payment
                    print("Exiting...")
                    return True
                else:                                               # If user enters invalid choice
                    print("Invalid choice...")
            else:
                print("Returning!...")
                return
    def view_cart(self, user_email):        # Functioon to view cart
        self.cart_obj.main(user_email)       # Call the main() in cart.py with user email
'''email_mobile = input("Enter Your email : ")
product_management_obj = product_management()
product_management_obj.main(email_mobile)'''

