from file_write import write_file               # To take error log
from products import timer                      # To access timer() 
import datetime                                 # To access current date and time
from db_connection import db_connection         # To implement db_connection
from back_menu import go_back                   # To go back prevoius input every time
from tabulate import tabulate                   # To display detailsin a tabular format
class wishlist:                                 # Creating a class called wishlist
    def __init__(self):                         # Creating __init__ method to implement db_connection and creating objects for the respective class
        db_obj = db_connection()
        self.db_connection = db_obj.db_connection
        self.cursor = db_obj.cursor
        self.file_write_obj= write_file()
        self.go_back_obj=go_back()
    def wishlist(self,user_email):              # Main funnction to user_choice
        while True:
            try :
                ch=input("\n===Wishlist===\n\n1. Like products\n2. View Liked products\n3. Remove liked products\n4. Exit\n\nEnter Your choice : ") # Asks choice from user
                if ch=="1":
                    self.like_products(user_email)              # Call function to like products
                elif ch=="2":
                    self.view_liked_products(user_email)        # Call function to view liked products
                elif ch=="3":
                    self.remove_liked_products(user_email)      # Call function to  remove liked products
                elif ch=="4":
                    print("Exiting...")                         # To exit from wishlist
                    break
                else:
                    print("Invalid choice!...")                 # If user enters invalid choice
            except Exception as e:
                self.file_write_obj.error_logging("Error in wishlist: "+str(e))
    def like_products(self,user_email):                 # Function to like products
        try :
            query="SELECT id,CategoryName,p.CategoryID,ProductID,Name,Price,Quantity,Availability FROM PRODUCTS AS p,CATEGORIES AS c WHERE p.CategoryID=c.CategoryID"  # query to display all the products to like
            self.cursor.execute(query)
            results=self.cursor.fetchall()                  # store it in
            headers=["ID","CategoryName","ProductID","Name","Price","Quantity","Availability"]
            print(tabulate(results,headers=headers,tablefmt="fancy_grid"))    # display it
            while True:
                id_=self.go_back_obj.get_input("Enter id : (enter 'back' to go back) : ")            # get id
                if id_ is None:
                   return 
                query_select="SELECT * FROM PRODUCTS WHERE ID=%s"       # query to check if category id and product id is in the products table
                self.cursor.execute(query_select,(id_,))
                result_found=self.cursor.fetchall()
                if result_found:
                    query="INSERT INTO Wishlist VALUES(%s,%s,%s)"                  # insert the liked products in like_products table
                    query_now="SELECT categoryID,productID FROM PRODUCTS WHERE ID=%s"
                    self.cursor.execute(query_now,(id_,))
                    results=self.cursor.fetchall()
                    for result in results:
                        cat_id,prod_id=result
                    self.cursor.execute(query,(user_email,cat_id,prod_id))
                    self.db_connection.commit()                                         # Save the transaction
                    print("Product liked..")
                    break
                else:                                                               # if category id and product id is not in the products table                
                    print("Invalid category or product id...")
        except Exception as e:
            self.file_write_obj.error_logging("Error in like products: "+str(e))
    def view_liked_products(self,user_email):                   # Function to view liked products
        try :
            query = "SELECT id,Name,price,quantity,Availability,color,description,average_rating FROM PRODUCTS AS p, Wishlist AS c WHERE c.user_email=%s and p.productid=c.product_id and p.categoryid=c.category_id"
            self.cursor.execute(query, (user_email,))
            results = self.cursor.fetchall()            # Store it in
            if results:                                 # if liked products found
                print("Your Liked Products...")
                self.display_details(results)           # call function to display it
            else:                                       # if liked products does not found
                print("No Liked Products found...")
        except Exception as e:
            self.file_write_obj.error_logging("Error in view liked products: "+str(e))
    def remove_liked_products(self, user_email):      # Function to remove cart
        self.view_liked_products(user_email)          # Call fucntion to display the products in cart
        while True:
            try:
                ch = input("Do you want to remove any products (Yes/press any key to continue) : ").lower() # Asks wish to remove or not
                if ch == "yes":     # if yes to remove
                    while True:
                        prod_name = self.go_back_obj.get_input("Enter the product Name to Remove from your wishlist : (enter 'back' to go back) : ")     # Get product name
                        if prod_name is None:
                            break
                        query = """
                        SELECT Name 
                        FROM PRODUCTS, Wishlist
                        WHERE user_email=%s AND category_id=categoryid AND product_id=productid
                        """         # Get the products in that name
                        self.cursor.execute(query, (user_email,))
                        names = self.cursor.fetchall()      # store  it in
                        lst = [name[0] for name in names]   # fetch names one by one
                        if prod_name in lst:                # If entered product name is in the product table
                            query = """                     
                            DELETE c 
                            FROM Wishlist AS c 
                            WHERE (c.product_id, c.category_id) IN (
                                SELECT p.productid, p.categoryid 
                                FROM PRODUCTS AS p 
                                WHERE p.Name = %s
                            ) AND c.user_email = %s
                            """                             # Query to delete the product with the respective name
                            self.cursor.execute(query, (prod_name, user_email))
                            self.db_connection.commit()     # Save the transaction
                            print("Product Removed from Wishlist...")
                            break
                        else:                               # If entered product name is not in the product table             
                            print("Product name not found...")
                else:           # If no to remove
                    print("Returning to Wishlist...")
                    timer(3)        # Call timer to delay 
                    break
            except Exception as e:
                self.file_write_obj.error_logging("Error in remove liked products : "+str(e))
    def display_details(self, results):                 # function to display details of product
        try :
            headers = ["ID","Name", "Price", "Quantity", "Availability", "Color", "Description", "Average Rating","Quan"]        # headers for the table
            print(tabulate(results, headers=headers, tablefmt="simple"))        # display the product details in a table format
        except Exception as e:
            self.file_write_obj.error_logging("Error in display details: "+str(e))
