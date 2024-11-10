# Importing necessary packages
import mysql.connector                                            # To implement db connection
from cart import Cart                                             # To  accesss methods from the cart module
from tabulate import tabulate                                    # To display details in a tabular format
from validation import validation                                # To access methods from validation module
import re                                                        # To validate inputs
from db_connection import db_connection                          # To implement db connection
from file_write import write_file                                # To write error logs
from payment_process import checkout_sub                         # To implement methods from payment_process
from rating_in_checkout import rating                            # To implement methods from rating_in_checkout
from back_menu import go_back                                     # To go back previous menu
class checkout:                                                   # Creatinng a class called checkout
    def __init__(self):                             # Creating __init__ method to  implement db connection and creating objects fro respective classes
        db_obj = db_connection()
        self.db_connection = db_obj.db_connection
        self.cursor = db_obj.cursor
        self.cart_obj=Cart()
        self.write_file_obj=write_file()
        self.checkout_sub_obj=checkout_sub()
        self.rating_obj=rating()
        self.go_back_obj=go_back()
    def main(self,user_email):                      # Main function to call every functions
        try :  
            while True:
                ch=input("\n1. Purchase Product\n2. View order status\n3. Delivered orders\n4. Cancel order\n5. Return products\n6. Exit\n\nEnter Your choice : ")  # Get user choice from user
                if ch=="1":
                    self.checkout_sub_obj.process_payment(user_email)   #  Call payment_process module to proceeed payment
                elif ch=="2":
                    self.view_order_status(user_email)                  # To view order status
                elif ch=="3":
                    id_content=self.display_delivered(user_email)       # Get ids of delivered orders
                    self.rating_obj.rate_products(user_email,id_content)    # To rate and review the products
                elif ch=="4":
                    self.cancel_order(user_email)                       # To cancel the order
                elif ch=="5":
                    self.return_products(user_email)                    # To return orders
                elif ch=="6":
                    print("Exiting...")                                 # To exit from checkout
                    break
                else:
                    print("Invalid choice...")                          # If user enters invvalid choice
        except Exception as e:
            self.write_file_obj.error_logging("Error in main checkout :  "+str(e))  # To log errors
    def view_order_status(self,user_email):                             # Function to view order status
        try :
            query_view="SELECT * FROM purchase_details WHERE USER_EMAIL=%s AND Status!=%s and status!=%s and status!=%s"    # query to get purchase details for the respective user email
            self.cursor.execute(query_view,(user_email,"Delivered","Returned","Cancelled"))
            result=self.cursor.fetchall()
            if result:                                                     # If found
                header=['Email','ID','Amount paid','Order status','paid date','Transaction ID'] 
                print(tabulate(result,headers=header,tablefmt="fancy grid"))    # Display the details in a tabular format 
                return True
            else:
                print("No products Ordered yet!...")                            # If no products found
                return False
        except Exception as e:
            self.write_file_obj.error_logging("Error in view order status :  "+str(e))      # To log  errors
    def display_delivered(self,user_email):                                     # Function to display delivered products
        try :
            query_view="SELECT * FROM purchase_details WHERE USER_EMAIL=%s AND Status=%s"   # query to get delivered products based on user email
            self.cursor.execute(query_view,(user_email,"Delivered"))
            result=self.cursor.fetchall()
            if result:                                                          # If found
                header=['Email','ID','Amount paid','Order status','paid date','Transaction ID']
                print(tabulate(result,headers=header,tablefmt="fancy grid"))                # Display delivered products n a tabular format
                id_in = [str(row[1]) for row in result]                                     # Get only the id_s of the product
                return id_in
            else:                                                               # If no delivered products found
                print("No Delivered products found!...")
                return
        except Exception as e:
            self.cart_obj.error_logging("Error in view order status :  "+str(e))    # If not found
    def cancel_order(self,user_email):                                          # Function to cancel order
        try : 
            if self.view_order_status(user_email):                              # Checks if  return of view order status is true
                while True:
                    cancel_ch=self.go_back_obj.get_input("Enter the Transaction id to cancel the order : (enter 'back' to go back) : ") # asks  trnsaction id of the products from the user
                    if cancel_ch is None:                                       # To go back previous menu
                        return
                    query_trans_id="SELECT * FROM PURCHASE_DETAILS WHERE USER_EMAIL=%s and STATUS!=%s and status!=%s and status!=%s"        # query to get purchased products
                    self.cursor.execute(query_trans_id,(user_email,"Delivered","Returned","Cancelled"))
                    results=self.cursor.fetchall()
                    trans_ids=[str(row[5]) for row in results]                  # To get of the product
                    if cancel_ch in trans_ids:
                        query_insert="UPDATE PURCHASE_DETAILS SET status=%s WHERE Transaction_id=%s"    # query to update order status  to "cancelled"
                        self.cursor.execute(query_insert,("Cancelled",cancel_ch))
                        self.db_connection.commit()
                        print("Order Cancelled!...")
                        break
                    else:                                                       # If user enters invalid id
                        print("Please enter the valid transaction id to cancel the order... " )
        except Exception as e:
            self.write_file_obj.error_logging("Error in cancel order :  "+str(e))       # To log errors
    def return_products(self,user_email):                                       # Function to return products
        try :
            if self.display_delivered(user_email):                              # if display_delivered return true
                while True :
                    print("Note : 'We will only return half of the amount as refund !' ")
                    return_ch=self.go_back_obj.get_input("Enter the transaction id to return product : (enter 'back' to go back) : ")   # asks the transacttionn id of the products
                    if return_ch is None:                                       # To go back previous menu
                        return
                    query_view="SELECT * FROM purchase_details WHERE USER_EMAIL=%s AND Status=%s"   # get delivered products
                    self.cursor.execute(query_view,(user_email,"Delivered"))
                    result=self.cursor.fetchall()
                    trans_ids=[str(row[5]) for row in result]                   # get only the ids
                    if return_ch in trans_ids:
                        query_date="SELECT * FROM PURCHASE_DETAILS WHERE transaction_id = %s and DATEDIFF(NOW(),status_now) <= 7"   # checks if the delivered date crosses 7 days
                        self.cursor.execute(query_date,(return_ch,))
                        results=self.cursor.fetchone()
                        if results:
                            query_refund="SELECT amount/2 FROM PURCHASE_DETAILS WHERE TRANSACTION_ID=%s"        # Get half amount of price as refund
                            self.cursor.execute(query_refund,(return_ch,))
                            refund=self.cursor.fetchone()
                            print("\nProduct Returned.\nYour refund",refund[0],"will be sent in few minutes!\nThank you...")
                            query_update="UPDATE PURCHASE_DETAILS SET status=%s WHERE Transaction_id=%s"           # To  update order status to "returned"
                            self.cursor.execute(query_update,("Returned",int(return_ch)))
                            self.db_connection.commit()
                            break
                        else:                                                       # If date  crosses 7  days
                            print("Returns are not accepted after 7 days from delivery.")
                    else:
                        print("Transaction id not found!...")
        except Exception as e:
            self.write_file_obj.error_logging("Error in return products :  "+str(e))    # To log errors

            
