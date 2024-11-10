import mysql.connector               # Importing to implenet db connection
class db_connection:
    def __init__(self):             # Connect to database in __init__ method
        self.db_connection = mysql.connector.connect(
        host="localhost",
        username="root",
        password="Madhar@20",
        database="product_management"
        )       # Connect it with database
        self.cursor = self.db_connection.cursor()   # Store the connection in self.cursor attribute
if __name__=="__main__":
    db_obj=db_connection()
