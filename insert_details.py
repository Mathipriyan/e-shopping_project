from db_connection import db_connection             # To  implement db connection
from file_write import write_file                   # To log errors
class user_details:                                 # Creating class called user_details
    def __init__(self):                             # Creating __init__ method to impement db connection
        db_obj = db_connection()
        self.db_connection = db_obj.db_connection
        self.cursor = db_obj.cursor
        self.write_file_obj=write_file()
    def dict_tuple_reg(self,dict_):                     # Function to insert user details to table
        try :
            lst=[]
            for key,value in dict_.items():         # Convert the dict to  a tuple  format
                lst.append(value)
            del lst[5]
            tup_=tuple(lst)
            query_insert="INSERT INTO REG_DETAILS VALUES(%s,%s,%s,%s,%s,%s)"   # query to insert the details to table
            self.cursor.execute(query_insert,tup_)
            self.db_connection.commit()
        except Exception as e:
            self.write_file_obj.error_logging("Error in dict tuple reg :  "+str(e))        # To log errors
    def dict_tuple_login(self,dict_):
        try :
            lst=[]
            for key,value in dict_.items():         # Convert the dict to  a tuple  format
                lst.append(value)
            tup_=tuple(lst)
            query_insert="INSERT INTO LOGIN_DETAILS VALUES(%s,%s)"   # query to insert the details to table
            self.cursor.execute(query_insert,tup_)
            self.db_connection.commit()
        except Exception as e:
            self.write_file_obj.error_logging("Error in dict tuple login :  "+str(e))        # To log errors
    def dict_tuple_logout(self,dict_):
        try :
            lst=[]
            for key,value in dict_.items():         # Convert the dict to  a tuple  format
                lst.append(value)
            tup_=tuple(lst)
            query_insert="INSERT INTO LOGOUT_DETAILS VALUES(%s,%s)"   # query to insert the details to table
            self.cursor.execute(query_insert,tup_)
            self.db_connection.commit()
        except Exception as e:
            self.write_file_obj.error_logging("Error in dict tuple login :  "+str(e))        # To log errors