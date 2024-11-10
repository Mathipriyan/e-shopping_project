# Importing necessary packages
import re                                               # To validate user inputs
import random                                           # To generate random numbers
import datetime                                         # To access current date and time functions
import time                                             # To access sleep() 
import pickle                                           # To load and dump data to file
from Product_details import product_management          # To access methods in product_management
from db_connection import db_connection                 # To implement db connection
from file_write import write_file                       # To log any errors to file
from insert_details import user_details                 # To access methods in insert_details
# Creating a class for User Authentication System
class UserAuthenticationSystem: 
    def __init__(self):                                 # Creating __init__ method to implement db connection and creating objects for respective classes
        db_obj = db_connection()
        self.db_connection = db_obj.db_connection
        self.cursor = db_obj.cursor
        self.write_obj=write_file()
        self.insert_obj=user_details()
        # Initialize instance variables
        self.reg_details_user = None                    # Variable to store user registration details
        self.login_dict = None                          # Variable to store login details
        self.logout_dict = None                         # Variable to store logout details
        self.email_mobile=None                          # Variable to store email of the user
        self.pass_change=None
        self.profile_change=None
        self.lst_questions=["1. What is your all time favorite movie ? ","2. Name of the first game you've played ? ","3. Name your first acheivement ? "]   #To ask some security questions
    def main(self):
        # Main menu function to interact with users
        try :
            while True:
                print("\n===User Authentication System===\n\n1. Register\n2. Login\n3. Forgot password\n4. View and update profile informations\n5. Exit\n")
                ch = input("Enter your choice: ")
                if ch == "1":
                    self.register_user()                        # Call method to register a new user
                elif ch == "2": 
                    self.login_user()                           # Call method to login a user
                elif ch == "3":
                    self.forgot_password()                      # Call method to reset password
                elif ch =="4":
                    self.viewprofile()                          # Call method to view and update profile info
                elif ch == "5":
                    print("\nExiting...\n")                       # Exit the program
                    break
                else:
                    print("\nInvalid choice.. Please try again!")
        except Exception as e:
            self.error_logging("Error in main Userauthentication : " + str(e))
    def mainmenu(self):                                     # Function to ask if user wants to go back mainmenu whenever
        try:
            ch=input("If you want to go back main menu (yes/Press any key to continue) : ").lower()
            if ch=="yes":
                self.timer(5)                                   # Delay 5 seconds
                return True
        except Exception as e:
            self.error_logging("Error in Mainmenu :" + str(e))
    def timer(self,count):                                  # Function to implement delay wherever requires
        try :
            print("Please wait! Processing..")
            while count > 0:
                if count == 1:
                    print(count, end="\n")
                else:
                    print(count, end="-")
                time.sleep(1)
                count -=1
        except Exception as e:
            self.error_logging("Error in Timer :" + str(e))
    def register_user(self):
        # Function to register a new user
        try :
            print("\n===Register====\n")
            if self.mainmenu():
                return 
            self.user_validation()                                                   # Validate user input
            self.security_ans=self.security_questions()                              # To get security answers from the user
            self.otp_verify(self.email, self.mobile_number)                          # Generate and Verify OTP
            self.reg_details_user = self.user_details_dict(self.email, self.name, self.mobile_number, self.address, self.password,self.security_ans)  # Create user details dictionary
            self.write_obj.write_to_file_reg(self.reg_details_user)                           # Write user details to file
            self.insert_obj.dict_tuple_reg(self.reg_details_user)
        except Exception as e:
            self.error_logging("Error in register_user :" + str(e))
    def user_validation(self):
        # Validate user input for registration
        try:
            self.email = self.valid_email()                  # Validate and store email
            self.unique_email(self.email)                    # Check if email is unique
            self.name = self.valid_name()                    # Validate and store name
            self.mobile_number = self.valid_mobile_number()  # Validate and store mobile number
            self.unique_mobile_number(self.mobile_number)    # Check if mobile number is unique
            self.address = self.valid_address()              # Validate and store address
            self.password = self.valid_password()            # Validate and store password
            self.confirm_password(self.password)             # Confirm password
        except Exception as e:
            self.error_logging("Error in user_validation : " + str(e))  # Error logging
    def valid_email(self):                                  
    # Validate email format using regular expression
        try  :
            regex = r'^\w+@[a-zA-Z]+\.[a-zA-Z]{2,3}$'
            count=0
            while count<4:
                email = input('Enter your email: ')
                if re.match(regex, email):
                    ch=input("Do you want to re-enter email (yes/Press any key  to continue) : ")
                    if ch=="yes":
                        count+=1
                        continue
                    else:
                        return email
                else:
                    print("Please enter a valid email format.")
                    count+=1
            else:
                print("Limit exceeded! Please  try  again...")
                self.main()
        except Exception as e:
            self.error_logging("Error in valid_email :" + str(e))
    def unique_email(self, email):
        # Check if email is unique or not
        try:
            with open("User details.dat", "rb") as fp:
                while True:
                    try:
                        reg_details_dict = pickle.load(fp)                              # Load the dumped data to  dictionary
                        if 'Email' in reg_details_dict and reg_details_dict['Email'] == email:
                            print("Email has already been taken.")
                            self.email = self.valid_email()                             # Ask user to enter a new email
                            return False
                    except EOFError:
                        break
                    except Exception as e:
                        self.error_logging("Error in unique_email : " + str(e))
            return True
        except FileNotFoundError:
            return True
    def valid_name(self):
        # Validate name format using regular expression
        try  :
            regex = r'^[a-zA-Z .]+$'
            count=0
            while count<4:
                name = input("Enter your name: ")
                if re.match(regex, name):
                    ch=input("Do you want to re-enter name (yes/Press any key  to continue) : ")
                    if ch=="yes":
                        count+=1
                        continue
                    else:
                        return name
                else:
                    print("Please enter a valid name format...")
                    count+=1
            else:
                print("Limit exceeded! Please  try  again...")
                self.main()
        except Exception as e:
            self.error_logging("Error in valid_name :" + str(e))
    def valid_mobile_number(self):
        # Validate mobile number format using regular expression
        try :
            regex = r'^(\+91|91)?[ -]?(?!.*[0]{4})[9876]{1}\d{9}$'
            count=0
            while count<4:
                mobile_number = input("Enter your mobile number: ")
                if re.match(regex, mobile_number):
                    ch=input("Do you want to re-enter mobile  number (yes/Press any key  to continue) : ")
                    if ch=="yes":
                        count+=1
                        continue
                    else:
                        return mobile_number
                else:
                    print("Please enter a valid mobile number format..")
                    count+=1
            else:
                print("Limit exceeded! Please  try  again...")
                self.main()
        except Exception as e:
            self.error_logging("Error in valid_mobile_number : " + str(e))
    def unique_mobile_number(self, mobile_number):
        # Check if mobile number is unique or not
        try:
            with open("User details.dat", "rb") as fp:
                while True:
                    try:
                        reg_details_dict = pickle.load(fp)                          # Load dumped data to dictionary
                        if 'Mobile_number' in reg_details_dict and reg_details_dict['Mobile_number'] == mobile_number:
                            print("Mobile number has already been taken.")
                            self.mobile_number = self.valid_mobile_number()         # Ask user to enter a new mobile number
                            return False
                    except EOFError:
                        break
                    except Exception as e:
                        self.error_logging("Error in unique_mobile_number : " + str(e))
            return True
        except FileNotFoundError:
            return True
    def valid_address(self):
        # Validate address format using regular expression
        try :
            count=0
            regex = r'^\d+\s*,?\s*[a-zA-Z\s,]+\s*,?\s*[a-zA-Z\s]+\s*,?\s*[a-zA-Z\s]+\s*,?\s*\d{6}$'
            while count<4:
                address = input("Please enter the address in the format 'House Number, Street, City, State, Pincode': ")
                if re.match(regex, address.strip()):
                    ch=input("Do you want to re-enter address (yes/Press any key  to continue) : ")
                    if ch=="yes":
                        count+=1
                        continue
                    else:
                        return address
                else:
                    print("Please enter a valid address format...")
                    count+=1
            else:
                print("Limit exceeded! Please  try  again...")
                self.main()
        except Exception as e:
            self.error_logging("Error in valid_address :" + str(e))
    def valid_password(self):
        # Validate password format using regular expression
        try :
            count=0
            regex = r'^(?=.*[a-z]{4,6})(?=.*[A-Z]{4,6})(?=.*\d{2,4})(?=.*[^a-zA-Z0-9]{1,2}).{8,}$'
            while count<4:
                password = input('Enter your password: ')
                if re.fullmatch(regex, password):
                    ch=input("Do you want to re-enter Password (yes/Press any key  to continue) : ")
                    if ch=="yes":
                        continue
                    else:
                        return password
                else:
                    print("Please enter a valid password format...")
                    count+=1
            else:
                print("Limit exceeded! Please  try  again...")
                self.main()
        except Exception as e:
            self.error_logging("Error in valid_password :" + str(e))
    def confirm_password(self, password):
        # Confirm password entered by user
        try :
            count = 0
            while count < 3:                                                # Maximum attempt is 3
                confirm_password = input("Confirm password: ")
                count += 1
                if confirm_password != password:
                    print("Passwords do not match! Please re-enter...")
                    continue
                print("\nPassword confirmed...")
                break
            else:
                print("Password confirmation limit exceeded! Please try again...")
        except Exception as e:
            self.error_logging("Error in confirm_password :" + str(e))
    def otp_verify(self, email, mobile_number):
        # Generate and verify OTP
        try:
            random_digit = random.randrange(100, 999)
            otp = email[0:2] + str(random_digit) + mobile_number[8:10]  # Generate OTP based on email, random 3 digit and mobile number
            self.timer(3)
            print("OTP:", otp)                                          # Display OTP for user
            count = 0
            while count < 3:                                        # Maximum  attempt is 3 
                otp_input = input("Enter the OTP: ")
                if otp_input != otp:
                    print("Incorrect OTP! Please try again..")
                    count += 1
                    continue
                else:
                    print("\nOTP verified successfully...")
                    break
            else:
                print("OTP verification limit exceeded! New otp will be sent...")
                self.otp_verify(self.email, self.mobile_number)
        except Exception as e:
            self.error_logging("Error in otp_verify :" + str(e))
    def security_questions(self):
        # Fnction to get security answers
        try :
            lst_ans=[]
            print("\nPlease answer below security questions ! ...\n")
            for question in self.lst_questions:
                print(question)
                ans=input()
                lst_ans.append(ans)
            print("Thankyou !")
            return lst_ans
        except Exception as e:
            self.error_logging("Error in security_questions :" + str(e))
    def user_details_dict(self, email, name, mobile_number, address, password,lst_answers):
        # Create dictionary with user details
        try:
            details_dict = {
                "Email": email,
                "Name": name,
                "Mobile_number": mobile_number,
                "Address": address,
                "Password": password,
                "Security_answers":lst_answers,
                "Registration_timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")     # Mentioning time_stamp 
            }
            self.timer(5)
            print("Registration successful!...")
            return details_dict
        except Exception as e:
            self.error_logging("Error in user_details_dict :" + str(e))
    def login_user(self):
        # Function to authenticate and login a user
        try :
            print("\n===Login===\n")
            if self.mainmenu():
                return
            if not self.login_verification_display():
                return  
            else:                
                self.write_obj.write_to_file_login(self.login_dict)                   # Write login details to file
                self.insert_obj.dict_tuple_login(self.login_dict)
                self.product_management_obj=product_management()            # Creating object for prodyct_managemnet class
                self.product_management_obj.main(self.email_mobile)         # Calling main() in databse module
                self.logout(self.email_mobile)                              # Calling logout() to user logging out
                self.write_obj.write_to_file_logout(self.logout_dict)                 # Writing logout details in file
                self.insert_obj.dict_tuple_logout(self.logout_dict) 
        except Exception as e:
            self.error_logging("Error in login_user :" + str(e))

    def login_verification_display(self):                           # Function to verify login credentials
        try:
            flag = False
            while not flag:                                         # Whenever user gives invalid credentials
                self.email_mobile = input("Enter your email/mobile: ")   # Get email from user    
                while True:
                    ch = input("Re-enter email (yes/Press any key to continue): ").lower() 
                    if ch == "yes":
                        self.email_mobile = input("Enter your email/mobile: ")
                    else:
                        break
                password = input("Enter your password: ")           # Gwt password from user
                query="SELECT email FROM Admin_products WHERE email=%s and pass_wd=%s"
                self.cursor.execute(query,(self.email_mobile,password))
                results=self.cursor.fetchall()
                if results:
                    from admin_place import admin
                    admin_obj=admin()
                    admin_obj.main()
                    return False
                with open("User details.dat", "rb") as fp:          # Open the file in read binary mode
                    while True:
                        try:
                            reg_details_dict = pickle.load(fp)      # Store the file content in a dictionary
                            if ('Email' in reg_details_dict and reg_details_dict['Email'] == self.email_mobile) or ('Mobile_number' in reg_details_dict and reg_details_dict['Mobile_number'] == self.email_mobile):
                                if reg_details_dict['Password'] == password:        # checks if email/mobile and password are correct
                                    self.timer(5)
                                    print("\nLogged in successfully.")
                                    self.login_dict = {             # Dictionary to store logging in details
                                        "Login Details : "
                                        "login_mobile": self.email_mobile,
                                        "login_timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                                    }
                                    flag = True                     # To break the loop
                                    return True
                                else:
                                    break  # Break inner loop to retry email/mobile input
                        except EOFError:                            # If end of file reached breaks
                            break
                        except Exception as e:
                            self.error_logging("Login Verification Error: " + str(e))
                if not flag:                                        # If credentails are wrong
                    print("Invalid user! Please try again...")
        except Exception as e:
            self.error_logging("Error in login_verification_display :" + str(e))
    def verify_sec_ans(self,reg_details_dict):                  # Function to verify security ans to change new password
        try :
            for question in self.lst_questions:                 # Display questions one by one
                print(question,end="\n")
            while True : 
                ch=input("Enter the index of any questions to answer : ")       # Asks any of the questions from user
                if ch in "123":                                                 # If in the index
                    print(self.lst_questions[int(ch)-1])                        # Displays the user given question
                    ans=input()                                                 # Get answer
                    if ans in reg_details_dict['Security_answers']:             # if ans is correct
                        print("Verified Successfully!...")
                        break
                    else:                                                       # if it gets wrong
                        print("Incorrect answer!...")
                else:
                    print("Invalid index!...")
        except Exception as e:
            self.error_logging("Error in verify_sec_ans : " + str(e))
    def forgot_password(self):                                                  # Function to forgot password and change new password
        try:
            if self.mainmenu():
                return
            while True:
                email_mobile = input("Enter your email/mobile: ")               #  Enter email/mobile from user
                flag = False   
                with open("User details.dat", "rb+") as fp:                         # Open the file in binary read write
                    lines = []                                                      # To append the overwritten contents
                    while True:
                        try:
                            reg_details_dict = pickle.load(fp)                      # Load the data to a dictionary
                            if (reg_details_dict['Email'] == email_mobile or 
                                reg_details_dict['Mobile_number'] == email_mobile): # Checks if the email/mobile are correct
                                self.verify_sec_ans(reg_details_dict)               # Verify the security answers
                                self.otp_verify(reg_details_dict['Email'], reg_details_dict['Mobile_number'])   # Get otp 
                                print("OTP verified. Please set a new password.")
                                new_password = self.valid_password()                # Set new password
                                self.confirm_password(new_password)                 # Confirm the new 
                                reg_details_dict['Password'] = new_password         # Overwrite the new password in dictionary
                                flag = True         
                            lines.append(reg_details_dict)                          # Append the dictionary one by one to the list 
                        except EOFError:
                            break
                        except Exception as e:
                            self.error_logging("Forgot Password Error: " + str(e))
                    fp.seek(0)                                                      # Sets the cursor to beginning of file
                    fp.truncate(0)                                                  # Delete only the content of file
                    for line in lines:
                        pickle.dump(line, fp)                                       # Dump the list to the file with new password
                if flag:
                    print("Password reset successful!")
                    self.pass_change = {                                            # Dictionary to store user logout details
                        "Password Changed : "
                        "login_mobile": email_mobile,
                        "login_timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        }
                    self.write_obj.write_to_file_pass_changed(self.pass_change)
                    break                                                           # Exit the while loop if password reset successful
                    
                else:
                    print("Invalid email/mobile! Please try again.")
        except Exception as e:
            self.error_logging("Error in forgot_password : " + str(e))
        
    def logout(self,email_mobile):
        # Function to log out user
        try:
            while True:
                log_out = input("\nEnter 'yes' to Log out: ").lower()               
                if log_out == "yes":
                    self.timer(3)
                    self.logout_dict = {                                            # Dictionary to store user logout details
                                        "Logout Details : "
                                        "login_mobile": self.email_mobile,
                                        "login_timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                                    }
                    print("User logged out successfully...")
                    break
                else:
                    print("Invalid input! Please try again...")
                    continue
        except Exception as e:
            self.error_logging("Error in logout : " + str(e))
    def viewprofile(self):                                                  # Function to view and update profile informations
        try :
            if self.mainmenu():
                return
            while True:
                flag=False
                email_prompt=input("Enter Your email : ")                   # Get email and password to view
                passwd_prompt=input("Enter your password : ")
                with open("User Details.dat","rb+") as fp:                  # Open the file in read and write binary mode
                    lines=[]                                                # To append the contents
                    while True:
                        try :
                            container=pickle.load(fp)                       # Store the content in a seperate variable
                            if email_prompt==container['Email'] and passwd_prompt==container['Password']:   # Checks if the given email/password correct
                                self.timer(3)
                                # Displays the profile information of the respective user
                                print("\nName :",container['Name'])             
                                print("Mobile Number :",container['Mobile_number'])
                                print("Address :",container['Address'])
                                flag=True
                                ch=input("\nDo you want to update the profile (yes/press any key to continue) : ").lower()  # Asks if user wants to update
                                if ch=="yes":                               # If yes, update the profile info
                                    new_name=self.valid_name()
                                    new_mobile=self.valid_mobile_number()
                                    new_address=self.valid_address()
                                    container['Name']=new_name
                                    container['Mobile_number']=new_mobile
                                    container['Address']=new_address
                                    self.timer(3)
                                    print("Profile Updated Successfully!...")
                                    self.profile_change = {                                            # Dictionary to store user logout details
                                        "Profile Updated : "
                                        "login_mobile": email_prompt,
                                        "login_timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                                        }
                                    self.write_obj.write_to_file_profile_update(self.profile_change)
                                else:
                                    self.timer(3)
                            lines.append(container)                         # append the updated profile information to the empty list 
                        except EOFError:
                            break
                    fp.seek(0)                                              # Set cursor to the beginning of the file
                    fp.truncate()                                           # Delete all the old contents
                    for line in lines:                                      # Iterarte through each line
                        pickle.dump(line,fp)                                # Write the new content to the file
                if not flag:
                    print("Invalid credentials! Please try again...")
                if flag:
                    break
        except Exception as e:
            self.error_logging("Error in view_profile : " + str(e))              
        
    def error_logging(self, error):
        # Log errors to error log file
        try:
            with open("Error log.txt", "a") as error_fp:
                error_fp.write(str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")) + ": " + error + "\n")    # Write the respective error with timestamp
        except Exception as e:
            print("Error while logging: ", e)
if __name__ == "__main__":
    auth_system = UserAuthenticationSystem()                        # Creating object for the class
    auth_system.main()                                              # Call the main() method
with open("User details.dat", "rb") as load_:
    while True:    
        try:
            print(pickle.load(load_))  # Load and print each user details
        except EOFError:
            break
with open("Login details.dat","rb") as fp1:
    while True:
        try:
            print(pickle.load(fp1))
        except EOFError :
            break
with open("password changes.dat","rb") as pass_fp:
    while True:
        try :
            print(pickle.load(pass_fp))
        except EOFError:
            break
with open("profile updates.dat","rb") as profile_fp:
    while True:
        try :
            print(pickle.load(profile_fp))
        except EOFError:
            break

    
