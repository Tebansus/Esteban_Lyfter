# Decorator function that prints the arguments and keyword arguments of a function
def check_number(func):
    def wrapper(*args, **kwargs):
        for arg in args[1:]:
            try :
                float(arg)
                print("Argument: ", arg, " is a number")
                
            except ValueError:
                raise ValueError(f"Argument: {arg} isn't a valid number") from None
                
        return func(*args, **kwargs)
    return wrapper
# Test class to pass to the decorator
class test:
    @check_number
    def __init__(self, numbertopass, number2):
        self.numbertopass = numbertopass
        self.numbertopass = number2


def main():
    # Test the class
    test(1.2, "Hola")



if __name__ == "__main__":
    main()