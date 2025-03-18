# Decorator function that prints the arguments and keyword arguments of a function. Check if the first argument is self, if it is, ignore it and check the rest of the arguments, so that it can work with class functions.
import inspect
def check_number(func):
    sig = inspect.signature(func)
    params = list(sig.parameters.values())
    is_method = params and params[0].name == 'self'

    def wrapper(*args, **kwargs):
        args_to_check = args[1:] if is_method else args
        
        # Check arguments
        for arg in args_to_check:
            try:
                float(arg)
                print(f"Argument: {arg} is a number")
            except ValueError:
                raise ValueError(f"Argument: {arg} isn't a valid number") from None
        
        # Check keyword arguments
        for value in kwargs.values():
            try:
                float(value)
                print(f"Argument: {value} is a number")
            except ValueError:
                raise ValueError(f"Argument: {value} isn't a valid number") from None
        
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