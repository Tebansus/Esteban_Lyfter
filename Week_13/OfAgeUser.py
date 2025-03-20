from datetime import date
import sys
#Define a decorator check_of_Age that checks if the user is of age and is a valid user. If the user is not of age or is not a valid user, the decorator should raise a ValueError with the message "User isn't a valid, of age user". 
def check_of_Age(func):
    def wrapper(user):
        # Check if the user is of age and is a valid user      
        if  isinstance(user, User) and user.age >= 18:
            print("User is valid and of age")
        # Else, raise a ValueError        
        else:
            raise ValueError(f"User isn't a valid, of age user") from None
        
                
        
        return func(user)
    return wrapper


# Define a class User that has a property 'age' that gives the age of the user
class User:
    dateofbirth: date
    def __init__(self, dateofbirth):
        self.dateofbirth = dateofbirth
    
    @property
    def age(self):
        today = date.today()
        return today.year - self.dateofbirth.year - ((today.month, today.day) < (self.dateofbirth.month, self.dateofbirth.day))

# Usage Testing the decorator
# Define a function example_function that takes a User instance as an argument and prints the user's age
@check_of_Age
def example_function(user):
    print(f"User's age is: {user.age}")
# main function that tests the example_function with a User instance
def main():
    try:
        # Test the function with a User instance
        user = User(date(2001, 1, 1))
        example_function(user)
    # Catch the ValueError exception and print the error message
    except ValueError as e:
        print(e)
        sys.exit(1)  # Exit the program with a status code of 1

if __name__ == "__main__":
    main()