import re                                       # To validate user input
import random                                   # To generate random numbers
import time                                     # To access current time and sleep()
class validation:                               # Creating aclass called validation
    def valid_email(self):                                  
    # Validate email format using regular expression
        regex = r'^\w+@[a-zA-Z]+\.[a-zA-Z]{2,3}$'
        while True:
            email = input('Enter your email: ')
            if re.match(regex, email):
                ch=input("Do you want to re-enter email (yes/Press any key  to continue) : ")
                if ch=="yes":
                    continue
                else:
                    return email
            else:
                print("Please enter a valid email format.")
    def valid_name(self):
        # Validate name format using regular expression
        regex = r'^[a-zA-Z .]+$'
        while True:
            name = input("Enter your name: ")
            if re.match(regex, name):
                ch=input("Do you want to re-enter name (yes/Press any key  to continue) : ")
                if ch=="yes":
                    continue
                else:
                    return name
            else:
                print("Please enter a valid name format...")
    def valid_mobile_number(self):
        # Validate mobile number format using regular expression
        regex = r'^(\+91|91)?[ -]?(?!.*[0]{4})[9876]{1}\d{9}$'
        while True:
            mobile_number = input("Enter your mobile number: ")
            if re.match(regex, mobile_number):
                ch=input("Do you want to re-enter mobile  number (yes/Press any key  to continue) : ")
                if ch=="yes":
                    continue
                else:
                    return mobile_number
            else:
                print("Please enter a valid mobile number format..")
    def valid_address(self):
        # Validate address format using regular expression
        regex = r'^\d+\s*,?\s*[a-zA-Z\s,]+\s*,?\s*[a-zA-Z\s]+\s*,?\s*[a-zA-Z\s]+\s*,?\s*\d{6}$'
        while True:
            address = input("Please enter the address in the format 'House Number, Street, City, State, Pincode': ")
            if re.match(regex, address.strip()):
                ch=input("Do you want to re-enter address (yes/Press any key  to continue) : ")
                if ch=="yes":
                    continue
                else:
                    return address
            else:
                print("Please enter a valid address format...")
            
    def valid_password(self):
        # Validate password format using regular expression
        regex = r'^(?=.*[a-z]{4,6})(?=.*[A-Z]{4,6})(?=.*\d{2,4})(?=.*[^a-zA-Z0-9]{1,2}).{8,}$'
        while True:
            password = input('Enter your password: ')
            if re.fullmatch(regex, password):
                ch=input("Do you want to re-enter Password (yes/Press any key  to continue) : ")
                if ch=="yes":
                    continue
                else:
                    return password
            else:
                print("Please enter a valid password format...")
            
    def otp_verify(self, email, mobile_number):
        # Generate and verify OTP
        random_digit = random.randrange(100, 999)
        otp = email[0:2] + str(random_digit) + mobile_number[8:10]  # Generate OTP based on email, random 3 digit and mobile number
        self.timer(3)
        print("OTP:", otp)                                          # Display OTP for user
        while True:                                        # Maximum  attempt is 3 
            otp_input = input("Enter the OTP: ")
            if otp_input != otp:
                print("Incorrect OTP! Please try again..")
                continue
            else:
                print("\nOTP verified successfully...")
                break
    def mainmenu(self):                                     # Function to ask if user wants to go back mainmenu whenever
        ch=input("If you want to go back main menu (yes/Press any key to continue) : ").lower()
        if ch=="yes":
            self.timer(5)                                   # Delay 5 seconds
            self.main()
    def timer(self,count):                                  # Function to implement delay wherever requires
        print("Please wait! Processing..")
        while count > 0:
            if count == 1:
                print(count, end="\n")
            else:
                print(count, end="-")
            time.sleep(1)
            count -=1
