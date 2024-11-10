from db_connection import db_connection         # To implement db connection
import re                                       # To validate user inputs
from validation import validation               # To access methods in file validation
from file_write import write_file               # To log errors
from cart import Cart                           # To access methods in cart file
from back_menu import go_back                   # To go back previous input every time
class checkout_sub:                             # Creating a class called checkout_sub
    def  __init__(self):                        # Creating __init__ method to implement db connection and creating objects for the respective classes
        db_obj = db_connection()
        self.db_connection = db_obj.db_connection
        self.cursor = db_obj.cursor
        self.write_file_obj=write_file()
        self.cart_obj=Cart()
        self.go_back_obj=go_back()
    def process_payment(self,user_email):       # Function to make payment for the product
        try : 
            if self.cart_obj.view_cart(user_email):     # Call function to view products in cart
                while True:
                    try : 
                        payment=input("Do you want to purchase items in the cart (yes/press any key to continue) : ").lower()   # again ask user wants to purchase
                        if payment=="yes":              # If user wish to purchase
                            while True:
                                prod_id_no=self.go_back_obj.get_input("Enter the IDs : (enter 'back' to go back) : ").split()   # Asks ids to purchase
                                if prod_id_no is None:      # To go back previous menu
                                    return
                                query_check="SELECT cart_ID FROM CARTDETAILS WHERE USER_EMAIL=%s"   # query to select ids in the cart
                                self.cursor.execute(query_check,(user_email,))
                                contents=self.cursor.fetchall()
                                lst=[str(content[0]) for content in contents]                       # Store the ids in cart  in list format
                                flag=False
                                while not flag:                                         # checks if the entered id is in the id columnn in cart
                                    for check in prod_id_no:
                                        if check not in lst:
                                            flag=True
                                    break
                                if flag:                                                # If user enters invalid id
                                    print("Please enter items in your cart!...")
                                if not flag:                                            # If user enters valid id in the cart
                                    break 
                            flag_quan = False
                            for quan_check in prod_id_no:                               # Loop thorugh each id
                                query_check_quan = "SELECT quantity FROM PRODUCTS WHERE ID=%s"  # query to select quantity from the products
                                self.cursor.execute(query_check_quan, (quan_check,))
                                quantity = self.cursor.fetchone()
                                if quantity and quantity[0] == 0:                       # checks if quantity is zero
                                    print("Sorry! ID:", quan_check, "Product out of stock...")
                                    flag_quan = True
                            if flag_quan:                                               # if zero go to start
                                continue
                            print("\nProduct selected...")                              # if not proceed
                            while True:
                                cash_on_online=input("\n1. Cash on delivery\n2. Online payment\n3. Exit\nEnter Your choice : ") # asks user payment way
                                if cash_on_online=="1":
                                    if self.cash_on(user_email,prod_id_no):         # Call function to go on cash on delivery
                                        return
                                elif cash_on_online=="2":
                                    if self.online_pay(user_email,prod_id_no):      # Call function to go on online payment
                                        return
                                elif cash_on_online=="3":                           # Exits from the payment
                                    print("Exiting...")
                                    break
                                else:                                               # If user enters invalid choice
                                    print("Invalid choice...")
                        else:                                                       # If user does not wants to purchase
                            print("Returning back...")
                            break
                    except :
                        break
        except Exception as e:
            self.write_file_obj.error_logging("Error in process payment :  "+str(e))        # To log errors
    def cash_on(self,user_email,prod_id_no):                                        # Function to make cash on delivery
        try  :
            print("==Cash On Delivery==")
            total_price=self.display(user_email,prod_id_no)                         # Call function to display total cost in the cart
            user_ch=input("Purchase (yes/press any key to continue) : ").lower()    # Ask users to purchase
            if user_ch=="yes":                                                      # if yes
                print("Thankyou! Your order has been confirmed...")
                self.update_transaction(user_email,prod_id_no,total_price)          # call function to update transaction in table
                self.update_products(prod_id_no)                                    # call function to update products quantity column
                return True
            else:                                                                   # If no to purchase
                print("Returning!...")
                return False
        except Exception as e:
            self.write_file_obj.error_logging("Error in cash on :  "+str(e))        # To log errors
    def online_pay(self,user_email,prod_id_no):                                     # Function to make online payment
        try :
            print("==Online Payment==")
            total_price=self.display(user_email,prod_id_no)                         # Call function to display total cost in the cart
            while True:
                user_ch=input("Purchase (yes/press any key to continue) : ").lower()    # Ask users to purchase
                if user_ch=="yes":
                    upi_=self.upi_id()                                              # Ask upi id from user
                    if upi_=="back":                                                # If go back 
                        continue
                    print("Thankyou! Your order has been confirmed...")
                    self.update_transaction(user_email,prod_id_no,total_price)      # call function to update transaction in table
                    self.update_products(prod_id_no)                                # call function to update products quantity column
                    return True
                else:
                    print("Returning!...")
                    return False
        except Exception as e:
            self.write_file_obj.error_logging("Error in online pay :  "+str(e))     # To log errors
    def display(self,user_email,prod_id_no):                                        # Function to display all details for payment
        try : 
            user_obj=validation()                                                   # Creating object for the class validation
            name=user_obj.valid_name()                                              # call valid_name() to get valid name
            mobile_number=user_obj.valid_mobile_number()                            # call valid_mobile_number() to get valid mobile_number
            address=user_obj.valid_address()                                        # call valid_address() to get valid address
            user_obj.otp_verify(user_email,mobile_number)                           # Call function to generate annd verify otp
            total_price=self.cost_cart(user_email,prod_id_no)                       # Function to display total cost in cart
            print("Total price to pay : ",sum(total_price))
            return total_price
        except Exception as e:
            self.write_file_obj.error_logging("Error in display checkout :  "+str(e))   # To log errors
    def cost_cart(self,user_email,prod_id_no):                                      # Function to display total cost in the cart
        try : 
            lst_price=[]                                                            # Empty list to store price of the products
            for each in prod_id_no:
                query="SELECT PRICE FROM PRODUCTS WHERE id=%s"                      # query to get price of product for each id
                self.cursor.execute(query,(each,))
                result=self.cursor.fetchone()
                result=str(result[0])                                               # Convert it to string to perform slicing operations
                lst_price.append(float(result))                                     # Append it to empty list with float type
            return lst_price
        except Exception as e:
            self.write_file_obj.error_logging("Error in cost_cart :  "+str(e))      # To log errors
    def upi_id(self):                                                               # Function to getb upi id from user
        try :
            while True:
                upi=self.go_back_obj.get_input("Enter Your upi ID : (enter 'back' to go back) : ")  # Get upi id from user
                if upi is None:                                                     # if user wants to go back
                    return "back"
                regix=r'^\w+@{1}[a-zA-Z]+'                                          # regix pattern for upi id validation
                if re.match(regix,upi):                                             # if matches
                    print("Processing payment...")
                    user_obj=validation()                                           # Call function to validation
                    user_obj.timer(3)
                    print("Payment Successfull!")
                    print("Thankyou! Your order has been confirmed...")
                    return upi
                else:                                                               # If upi id does not matches the regix pattern
                    print("Please enter valid upi ID...")
        except Exception as e:
            self.write_file_obj.error_logging("Error in upi_id checkout :  "+str(e))    # To log errors
    def update_transaction(self,user_email,prod_id_no,total_price):                 # Function to update purchase details
        try:
            for each in prod_id_no:
                query="SELECT PRICE FROM PRODUCTS WHERE id=%s"                      # query to select price of product
                self.cursor.execute(query,(each,))
                result=self.cursor.fetchone()
                result = float(result[0]) 
                query_update="INSERT INTO Purchase_details(USER_EMAIL,ID,amount,status,status_now) VALUES(%s,%s,%s,%s,NOW())"       # query to insert tranaction details to the table
                self.cursor.execute(query_update,(user_email,int(each),int(result),"Payment Successfull!"))                         # Insert it with "payment successfull"
                self.db_connection.commit()
        except Exception as e:  
            self.write_file_obj.error_logging("Error in update traansaction :  "+str(e))    # To log errors
    def update_products(self,prod_id_no):                                           # Function to update quantity of  the products
        try  :
            for each in prod_id_no:
                query_quan="UPDATE PRODUCTS SET QUANTITY=QUANTITY-1 WHERE ID=%s"    # query to update quantity of  the products
                self.cursor.execute(query_quan,(each,))
                self.db_connection.commit()
        except Exception as e:
            self.write_file_obj.error_logging("Error in update products quantity :  "+str(e))   # To log errors
