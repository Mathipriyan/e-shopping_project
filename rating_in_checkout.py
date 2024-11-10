from file_write import write_file               # To take error log
from db_connection import db_connection         # To implement db connection
from back_menu import go_back                   # To go back previous input every time
class rating:                                   # Creating a classs called rating
    def __init__(self):                         # Creating __init__ method to implement db connection and creating objects for  the respective classes
        db_obj = db_connection()
        self.db_connection = db_obj.db_connection
        self.cursor = db_obj.cursor
        self.write_file_obj=write_file()
        self.go_back_obj=go_back()
    def review_category(self,review):           # Function to return review category
        try :
            # List of positive words
            positive_words = [                      
                "amazing", "great", "fantastic", "excellent", "awesome",
                "wonderful", "perfect", "best", "positive", "happy",
                "satisfied", "love", "liked", "good", "recommend",
                "enjoyed", "superb", "impressive", "delight", "pleasant"
            ]
            # List of negative words
            negative_words = [
                "terrible", "awful", "bad", "disappointed", "poor",
                "horrible", "worst", "negative", "hate", "unhappy",
                "dissatisfied", "problem", "issue", "complain", "regret",
                "dislike", "inferior", "unimpressed", "annoying", "frustrating"
            ]
            review_temp=review.lower().split()                          # Convert to lower case and fetch every words
            if any(word in positive_words for word in review_temp):     # Checks if any word matches with postive list return 'positive'
                return "positive"
            elif any(word in negative_words for word in review_temp):   # Checks if any word matches with negative list return 'negative'
                return "negative"
            else:
                return "neutral"                                        # else return neutral
        except Exception as e:                                      
            self.write_file_obj.error_logging("Error in review category :  "+str(e))        # Logging errors
    def rate_products(self,user_email,id_in):               # Function to rate and review the product
        try:
            ch = input("\nAre You wish to Rate and review the purchased product (Yes/Press any key to continue) : ").lower()        # Ask user wish
            if ch == "yes":     # If  yes to rate the product
                while True:
                    id_=input("Enter the IDs to rate and review : (IDs seperated by spaces) : ").split()    # Get ids from the user
                    id_=list(id_)                                                                           # Convert to list
                    flag=False
                    for each_id in id_:                                 # Checks if any of the id is nnot in delivered products
                        if each_id not in id_in:
                            flag=True
                            break
                    if flag:
                        print("Please enter ID Delivered...")           # if user enters invalid id
                    if not flag:                                        # If user enters valid id
                        break                                           
                for each in id_:                                        # Loop thorugh each id
                    print("For ID : ",each)
                    while True:
                        rate = self.go_back_obj.get_input("Enter the Ratings out of 5 : (enter 'back' to go back) : ")       # Get rating out of 5
                        if rate is None:                                    # To go back prevoius menu
                            self.rate_products(user_email,id_in)
                        if rate in "12345":                                 # Checks if user enters rating between  1 and 5
                            review = self.go_back_obj.get_input("Enter Review : (enter 'back' to go back) : ")              # Get review
                            if review is None:                 # To go back prevoius menu             
                                self.rate_products(user_email,id_in)
                            user_rev=self.review_category(review)           # Get the review category
                            query_1 = "UPDATE PRODUCTS SET no_of_ratings=no_of_ratings+1 WHERE ID=%s"  # Update number of ratings in products table
                            query_2 = "UPDATE PRODUCTS SET Total_Ratings=Total_ratings+%s WHERE ID=%s" # update the total rating in products table
                            query_3 = "UPDATE PRODUCTS SET average_rating=Total_Ratings/no_of_ratings WHERE ID=%s" # Update also the average rating in products table
                            query_4 = "INSERT INTO product_reviews VALUES(%s,%s,%s)"                                          # Insert the review in product_reviewws table
                            self.cursor.execute(query_4, (each, review,user_rev))
                            self.cursor.execute(query_1, (each,))
                            self.cursor.execute(query_2, (rate,each))
                            self.cursor.execute(query_3, (each,))
                            self.db_connection.commit()         # Save the transaction
                            print("Thank you for your precious time! Enjoy your product...")
                            break
                        else:
                            print("Please Enter the rating out of 5...")
                
            else:           # If no to rate the product
                print("Thank you! Enjoy your product...")
        except Exception as e:
            self.write_file_obj.error_logging("Error in rate products : "+str(e))       # To log errors
