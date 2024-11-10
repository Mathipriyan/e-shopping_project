import datetime             # Import datatime for accessing time functions
import mysql.connector      # Connecct it with database
import re                   # import re for validation
from products import timer  # import timer() function from products.py
from tabulate import tabulate  # Import tabulate for view in tabular format
from wishlist import wishlist   # Import wishlist to access methods in wishlist class
from file_write import write_file           # Import file_write to access methods in write_file class
from db_connection import db_connection     # To implement db_connection
from back_menu import go_back               # To go back prevoius meny every time
class Cart:                 # Creating cart class
    def __init__(self):     # Creating a constructor and create objects for the repective classes
        db_obj = db_connection()
        self.db_connection = db_obj.db_connection
        self.cursor = db_obj.cursor
        self.wishlist_obj=wishlist()
        self.file_write_obj= write_file()
        self.go_back_obj=go_back()
    def main(self,user_email):      # main() function to call every functions
        try :
            while True:
                ch=input("\n===Your cart===\n\n1. View Cart\n2. Add cart\n3. Remove cart\n4. Total cost\n5. Wishlist\n6. Exit\n\nEnter your choice : ")   # Asks user wish
                if ch=="1":
                    self.view_cart(user_email)          # call fucntion to view cart
                elif ch=="2":
                    self.add_cart(user_email)           # Call fucntion to add cart
                elif ch=="3":
                    self.remove_cart(user_email)        # Call fucntion to remove cart
                elif ch=="4":
                    self.total_cost(user_email)         # Call fucntion to view total cost
                elif ch=="5":
                    self.wishlist_obj.wishlist(user_email)          # Call fucntion to go to wishlist
                elif ch=="6":
                    print("Exiting...")
                    break
                else:
                    print("Invalid choice!...")
        except Exception as e:
            self.file_write_obj.error_logging("Error in main : "+str(e))
    def view_cart(self, user_email):                    # fucntion to view cart
        while True:
            try:
                query = """
                SELECT id,p.name, price, quantity, availability, color, description, Average_rating,c.quan 
                FROM PRODUCTS AS p, CARTDETAILS AS c 
                WHERE c.user_email=%s AND p.productid=c.product_id AND p.categoryid=c.category_id
                """                                     # get the product which is added to cart
                self.cursor.execute(query, (user_email,))
                results = self.cursor.fetchall()        # Store it in
                if results:                             # If any products found
                    self.display_details(results)       # Display it
                    self.total_cost(user_email)         # Call total_cost() to display total cost in that cart
                    return True
                else:                                   # if no products found
                    print("No products in the cart...")
                    global flag
                    flag=False
                    return False
                break
            except Exception as e:
                self.file_write_obj.error_logging("Error in view_cart: "+str(e))

    def remove_cart(self, user_email):      # Function to remove cart
        self.view_cart(user_email)          # Call fucntion to display the products in cart
        while True:
            try:
                ch = input("Do you want to remove any products (Yes/press any key to continue) : ").lower() # Asks wish to remove or not
                if ch == "yes":     # if yes to remove
                    while True:
                        prod_name = self.go_back_obj.get_input("Enter the product Name to Remove from your cart : (enter 'back' to go back) : ")     # Get product name
                        if prod_name is None:
                            break
                        query = """
                        SELECT Name 
                        FROM PRODUCTS, CARTDETAILS 
                        WHERE user_email=%s AND category_id=categoryid AND product_id=productid
                        """         # Get the products in that name
                        self.cursor.execute(query, (user_email,))
                        names = self.cursor.fetchall()      # store  it in
                        lst = [name[0] for name in names]   # fetch names one by one
                        if prod_name in lst:                # If entered product name is in the product table
                            query = """                     
                            DELETE c 
                            FROM CARTDETAILS AS c 
                            WHERE (c.product_id, c.category_id) IN (
                                SELECT p.productid, p.categoryid 
                                FROM PRODUCTS AS p 
                                WHERE p.Name = %s
                            ) AND c.user_email = %s
                            """                             # Query to delete the product with the respective name
                            self.cursor.execute(query, (prod_name, user_email))
                            self.db_connection.commit()     # Save the transaction
                            print("Product Removed from the cart...")
                            break
                        else:                               # If entered product name is not in the product table             
                            print("Product name not found...")
                else:           # If no to remove
                    print("Returning to main menu...")
                    timer(3)        # Call timer to delay 
                    break
            except Exception as e:
                self.file_write_obj.error_logging("Error in remove cart: "+str(e))

    def add_cart(self, user_email):                     # Function to add cart
        try:
            query="SELECT id,CategoryName,Name,Price,Quantity,Availability FROM PRODUCTS AS p,CATEGORIES AS c WHERE p.CategoryID=c.CategoryID"  # query to display all the products
            self.cursor.execute(query)
            results=self.cursor.fetchall()      # Store it
            headers=["ID","CategoryName","Name","Price","Quantity","Availability"]
            print(tabulate(results,headers=headers,tablefmt="fancy_grid"))      # Display it
            while True:
                id_=self.go_back_obj.get_input("Enter id : (enter 'back' to go back) : ")            # get id
                if id_ is None:
                    return
                query="SELECT * FROM PRODUCTS WHERE ID=%s"       # query to check if category id and product id is in the products table
                self.cursor.execute(query,(id_,))
                result_found=self.cursor.fetchall()
                if result_found:
                    while True:
                        quan=self.go_back_obj.get_input("Enter quantity : (enter 'back' to go back) : ")                 # get quantity of the product to add to cart
                        if quan is None:
                            break
                        try:
                            quan=int(quan)
                            if quan > 0:                          # if enntered quanntity  is greater than 0
                                query="INSERT INTO CARTDETAILS VALUES(%s,%s,%s,%s,%s)"             # insert the product into cartdetails table
                                query_now="SELECT categoryID,productID FROM PRODUCTS WHERE ID=%s"
                                self.cursor.execute(query_now,(id_,))
                                results=self.cursor.fetchall()
                                for result in results:
                                    cat_id,prod_id=result
                                self.cursor.execute(query,(user_email,cat_id,prod_id,int(id_),quan))
                                self.db_connection.commit()             # Save the transaction
                                print("Product added to cart..")
                                break
                            else:                                      # if the category and product index is not in the product table 
                                print("Please enter valid quantity!...")
                        except ValueError:
                            print("Please enter valid interger for quantity...")
                else:                                           # if enntered quanntity  is less than 0
                    print("Please enter valid id!...")
                    continue
                break
        except Exception as e:
            self.file_write_obj.error_logging("Error in add cart: "+ str(e))

    def total_cost(self, user_email):                       # Function to view total cost
        try:
            query_count = "SELECT SUM(QUAN) FROM CARTDETAILS WHERE USER_EMAIL=%s GROUP BY USER_EMAIL;"      # query to count the number of products in the cart
            query_sum = "SELECT SUM(PRICE)*SUM(quan) FROM CARTDETAILS, PRODUCTS  WHERE USER_EMAIL=%s AND categoryId=category_id AND product_id=productID;"  # query to calculate total cost in cart
            self.cursor.execute(query_count,(user_email,))
            count = self.cursor.fetchall()          # Store the count 
            print("\nTotal Products in your cart: ", count[0][0])       # display the count
            self.cursor.execute(query_sum, (user_email,))
            total_sum = self.cursor.fetchall()      # Store the total_cost
            print("Total price in your cart: ", total_sum[0][0], "\n")  # display it
        except Exception as e:
            self.file_write_obj.error_logging("Error in view_cart: " + str(e))

    def display_details(self, results):                 # function to display details of product
        try :
            headers = ["ID","Name", "Price", "Quantity", "Availability", "Color", "Description", "Average Rating","Quan"]        # headers for the table
            print(tabulate(results, headers=headers, tablefmt="simple"))        # display the product details in a table format
        except Exception as e:
            self.file_write_obj.error_logging("Error in display details: "+str(e))
