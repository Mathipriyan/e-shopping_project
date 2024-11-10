from products import timer      # To access sleep() in timer() from products file
class go_back:                  # Creating class called go_back
    def get_input(self, prompt):
        while True:
            choice = input(prompt)      # Get choice
            if choice.lower() == "back": # If user enters back return 
                print("Returning back...")
                timer(3)
                return None
            if choice:                  # else return the entered choice
                return choice
            print("Invalid input. Type 'back' to return to the previous input or enter a valid option.")
