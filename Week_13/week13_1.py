# Decorator function that prints the arguments and keyword arguments of a function
def print_parameters(func):
    def wrapper(*args, **kwargs):
        for arg in args:
            print("Function Argument: ", arg)
        for key, value in kwargs.items():
            print(f"Keyword Argument {key}: {value}")
        
        result = func(*args, **kwargs)
        print("Function output is: ", result)
        return result
    return wrapper
class test:
    @print_parameters
    def __init__(self, numbertopass, stringtopass):
        self.numbertopass = numbertopass
        self.stringtopass = stringtopass


def main():
    # Test the class
    test(1, "Hello")



if __name__ == "__main__":
    main()