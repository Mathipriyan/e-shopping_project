# import necessary packages and modules
from db_connection import db_connection
from tabulate import tabulate
import datetime
class admin:            # Creating class called admin
    def __init__(self):     # Implementing db connection
        db_obj = db_connection()
        self.db_connection = db_obj.db_connection
        self.cursor = db_obj.cursor
        self.status=""
        self.id=None
    def main(self):     # Main function all every function
        try :
            while True :
                print("\n===Admin===")  # Asks choice from user
                admin_ch=input("\n1. View all products\n2. Add products\n3. Remove products\n4. View Purchase Details\n5. Update order status\n6. View Cart Details\n7. View product reviews\n8. View product Ratings\n9. View Wishlist Details\n10. View Registered Users\n11. View Login details\n12. View logout details\n13. Exit\n\nEnter Your choice : ")
                if admin_ch=="1":
                    self.view_products()    # To view all products
                elif admin_ch=="2":
                    tup_content=self.add_products()     # To add any products
                    self.insert_products(tup_content)
                elif admin_ch=="3":
                    self.remove_products()              # To remove any products
                elif admin_ch=="4":
                    self.transaction_details()          # To display purchase details
                elif admin_ch=="5":
                    self.transaction_details()          # To update order status
                    self.update_order_status()
                elif admin_ch=="6":
                    self.view_cart_details()            # To display cart details
                elif admin_ch=="7":
                    self.view_product_reviews()         # To display product reviews
                elif admin_ch=="8":
                    self.view_ratings()                 # To display product ratings
                elif admin_ch=="9":
                    self.view_wishlist()                # To display wishlist details
                elif admin_ch=="10":
                    self.view_registered_users()        # To display registration details
                elif admin_ch=="11":
                    self.view_login_details()           # To display login details
                elif admin_ch=="12":
                    self.view_logout_details()          # To display logout details
                elif admin_ch=="13":
                    print("Exiting...")                 # To exit from admin
                    break
                else:
                    print("Invalid choice!...")         # If user enters invalid choice
        except Exception as e:
            self.error_logging("Error in admin main : " + str(e))
    # Function to view all products
    def view_products(self):
        try :
            query_prod="SELECT id,name,price,quantity,availability,color,description FROM products"
            self.cursor.execute(query_prod)
            results=self.cursor.fetchall()
            if results:
                header=['Product ID','Name','Price','Quantity','Availability','Description']
                print(tabulate(results,headers=header,tablefmt="fancy grid"))
            else:
                print("Product ratings not given yet!...")
        except Exception as e:
            self.error_logging("Error in view products : " + str(e))
    # Function to display purchase details
    def transaction_details(self):
        try :
            query="SELECT * FROM Purchase_details"
            self.cursor.execute(query)
            results=self.cursor.fetchall()
            header=['Email','ID','Amount','Status','Status_now','Transaction_id']
            if results:
                print(tabulate(results,headers=header,tablefmt="fancy_grid"))
            else:
                print("No products purchased...")
        except Exception as e:
            self.error_logging("Error in transaction details : " + str(e))
    # Function to update order status
    def update_order_status(self):
        try :
            self.id_=input("Enter the transaction id to update order status : ")
            query_check="SELECT * FROM PURCHASE_DETAILS WHERE TRANSACTION_ID = %s"
            self.cursor.execute(query_check,(self.id_,))
            result=self.cursor.fetchone()
            if result:
                status_dict={"1":"Order Processing","2":"Packaging","3":"In-Transit","4":"Out for Delivery","5":"Delivered"}
                for key,values in status_dict.items():
                    print(key,":",values)
                status_ch=input("Enter index to update order : ")
                if status_ch in "12345":
                    self.status=status_dict[status_ch]
                    self.update_status()
                else:
                    prinnt("Invalid index to update...")
            else:
                print("Transaction_id not found!...")
        except Exception as e:
            self.error_logging("Error in update order status : " + str(e))
    # Function to update using query
    def update_status(self):
        try :
            query_update="UPDATE PURCHASE_DETAILS SET Status=%s WHERE Transaction_id=%s"
            self.cursor.execute(query_update,(self.status,self.id_))
            self.db_connection.commit()
            print("Order Status updated!...")
        except Exception as e:
            self.error_logging("Error in update status : " + str(e))
    # Function to diplay cart details
    def view_cart_details(self):
        try :
            query_cart="SELECT * FROM CARTDETAILS"
            self.cursor.execute(query_cart)
            results=self.cursor.fetchall()
            if results:
                header=['Email','Category_ID','Product_ID','ID','Quantity']
                print(tabulate(results,headers=header,tablefmt="fancy grid"))
            else:
                print("Cart details not found!...")
        except Exception as e:
            self.error_logging("Error in view cart details : " + str(e))
    # Function to display product reviews
    def view_product_reviews(self):
        try :
            query_review="SELECT * FROM product_reviews"
            self.cursor.execute(query_review)
            results=self.cursor.fetchall()
            if results:
                header=['Product ID','Reviews','Review Category']
                print(tabulate(results,headers=header,tablefmt="fancy grid"))
            else:
                print("Product reviews not given yet!...")
        except Exception as e:
            self.error_logging("Error in view product reviews : " + str(e))
    # Function to display product ratings
    def view_ratings(self):
        try :
            query_ratings="SELECT id,name,no_of_ratings,total_ratings,average_rating FROM products"
            self.cursor.execute(query_ratings)
            results=self.cursor.fetchall()
            if results:
                header=['Product ID','Name','Number of Ratings','Total Ratings','Average Rating']
                print(tabulate(results,headers=header,tablefmt="fancy grid"))
            else:
                print("Product ratings not given yet!...")
        except Exception as e:
            self.error_logging("Error in view ratings : " + str(e))
    # Function to doisplay wishlist
    def view_wishlist(self):
        try :
            query_wishlist="SELECT * FROM wishlist"
            self.cursor.execute(query_wishlist)
            results=self.cursor.fetchall()
            if results:
                header=['Email','Category_ID','Product_ID']
                print(tabulate(results,headers=header,tablefmt="fancy grid"))
            else:
                print("Wishlist Details not found!...")
        except Exception as e:
            self.error_logging("Error in view wishlist : " + str(e))
    # Function to display registered users
    def view_registered_users(self):
        try :
            query_user="SELECT * FROM REG_DETAILS"
            self.cursor.execute(query_user)
            results=self.cursor.fetchall()
            if results:
                header=['Email','Name','Mobile Number','Address','Password','Time stamp']
                print(tabulate(results,headers=header,tablefmt="fancy grid"))
            else:
                print("User not registered yet!...")
        except Exception as e:
            self.error_logging("Error in view registered users : " + str(e))
    # Function to display login details
    def view_login_details(self):
        try :
            query_user="SELECT * FROM LOGIN_DETAILS"
            self.cursor.execute(query_user)
            results=self.cursor.fetchall()
            if results:
                header=['Email','Time stamp']
                print(tabulate(results,headers=header,tablefmt="fancy grid"))
            else:
                print("User not registered yet!...")
        except Exception as e:
            self.error_logging("Error in view login_details : " + str(e))
    # Function to display logout details
    def view_logout_details(self):
        try :
            query_user="SELECT * FROM LOGout_DETAILS"
            self.cursor.execute(query_user)
            results=self.cursor.fetchall()
            if results:
                header=['Email','Time stamp']
                print(tabulate(results,headers=header,tablefmt="fancy grid"))
            else:
                print("User not registered yet!...")
        except Exception as e:
            self.error_logging("Error in view logout details : " + str(e))
    # Function to add any products
    def add_products(self):
        try :
            product = {}
            product['cat_id']=int(input("Enter Category Id : "))
            product['Prod_id']=int(input("Enter Product Id : "))
            product['name'] = input("Enter product name: ")
            product['price'] = float(input("Enter product price: "))
            product['stock_quantity'] = int(input("Enter stock quantity: "))
            product['availability'] = input("Is the product available (yes/no)? ").lower()
            if product['availability']=="yes":
                product['availability']="in stock"
            else:
                product['availability']="out of stock"
            product['color'] = input("Enter product color: ")
            product['description'] = input("Enter product description: ")
            lst=[]
            for key,value in product.items():
                lst.append(value)
            tup=tuple(lst)
            print(tup)
            return tup
        except Exception as e:
            self.error_logging("Error in add products : " + str(e))
    # Function to remove any products
    def remove_products(self):
        try :
            self.view_products()
            id_=int(input("Enter the ID : "))
            query_delete="DELETE FROM PRODUCTS WHERE ID=%s"
            self.cursor.execute(query_delete,(id_,))
            self.db_connection.commit()
            print("ID :",id_,"Removed Successfully!")
        except Exception as e:
            self.error_logging("Error in view eemove products : " + str(e))
    # Function to insert product query
    def insert_products(self,tup_content):
        try :
            query_insert=" INSERT INTO PRODUCTS(CATEGORYID,PRODUCTID,NAME,PRICE,QUANTITY,AVAILABILITY,COLOR,DESCRIPTION) VALUES(%s,%s,%s,%s,%s,%s,%s,%s)"
            self.cursor.execute(query_insert,tup_content)
            self.db_connection.commit()
            print("Product Added Successfully!...")
        except Exception as e:
            self.error_logging("Error in insert products : " + str(e))
    # Function to log errors
    def error_logging(self,error):
        try :
            with open("Error_log_admin.txt","a") as error_fp:
                error_fp.write(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')+":"+error+"\n")
        except Exception as e:
            print("Error when error logging in admin : ",e)
'''if __name__=="__main__":
    admin_obj=admin()
    admin_obj.main()    
'''
