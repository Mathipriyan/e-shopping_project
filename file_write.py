import datetime                             # To access current date and time
import pickle                               # To load and dump data to file
class write_file:    
    def error_logging(self, error):         # Function to log errors
        try:
            with open("Error_log_products.txt", "a") as error_fp:       # open error log products file in append mode
                error_fp.write(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')+":"+error+"\n")        # Write the error in that file with timestamp
        except Exception as e:
            print("Error while logging: ", e)
    def write_to_file_reg(self, reg_details_user):
        # Write user registration details to file
        try:
            with open("User details.dat", 'ab') as fp:              # Append in binary mode
                pickle.dump(reg_details_user, fp)                   # Dump the data in binary format
        except Exception as e:
            self.error_logging("Write to File Error: " + str(e))
    def write_to_file_login(self, login_dict):
        # Write login details to file
        try:
            with open("Login details.dat", "ab") as login_fp:        # Append in binary mode
                pickle.dump(login_dict, login_fp)                    # Dump  the data in binary format
        except Exception as e:
            self.error_logging("Write to Login File Error: " + str(e))
    def write_to_file_logout(self,logout_dict):
        # Write login details to file
        try:
            with open("Login details.dat","ab") as logout_fp:       # Append in binary mode
                pickle.dump(logout_dict,logout_fp)                  # Dump  the data in binary format
        except Exception as e:
            self.error_logging("Write to Login File Error: " + str(e))
    def write_to_file_pass_changed(self,pass_change):
        # Write password updated details to file
        try :
            with open("Password changes.dat","ab") as pass_ch_fp:   # Append in binary mode
                pickle.dump(pass_change,pass_ch_fp)                 # Dump  the data in binary format
        except Exception as e:
            self.error_logging("Write to Login File Error: " + str(e))
    def write_to_file_profile_update(self,profile_change):
        # Write profilee updates details to file
        try :
            with open("Profile updates.dat","ab") as profile_ch_fp: # Append in binary mode
                pickle.dump(profile_change,profile_ch_fp)           # Dump  the data in binary format
        except Exception as e:
            self.error_logging("Write to Login File Error: " + str(e))
