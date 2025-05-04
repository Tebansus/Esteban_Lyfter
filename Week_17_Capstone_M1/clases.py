# is none decorator to check if the arguments are not None or empty.
def is_not_none(func):
    def wrapper(*args, **kwargs):
        for argss in args[1:]:
            if argss == None or argss == "":
                raise ValueError("None value is not allowed one or more fields.") 
        return func(*args, **kwargs)
    return wrapper
# Decorator to validate the transaction details.
# It checks if the amount is a number, not negative, and if the type is a string and not empty or whitespace.
def transaction_validador(func):
    def wrapper(*args, **kwargs):
        
        try:
            amount = float(args[2])
        except (ValueError, TypeError):
            raise ValueError("Amount must be a number")        
       
        if amount < 0:
            raise ValueError("Amount cannot be negative")            

        if not isinstance(args[3], str):
            raise ValueError("type must be a string")
        if not args[3] or args[3].strip == "":
            raise ValueError("parameter cannot be empty or whitespace")
        return func(*args, **kwargs)
    return wrapper
# This function checks if the category is not None, is a string, and is not empty or whitespace.
def category_check(func):
    def wrapper(*args, **kwargs):
       
        if not isinstance(args[1], str):
            raise ValueError("Category must be a string")
        if not args[1] or args[1].strip() == "" or " " in args[1].strip():
            raise ValueError("Category cannot be empty or have whitespace in between")
        return func(*args, **kwargs)
    return wrapper
# Transaction class to represent a financial transaction.
# It includes the date, amount, type of transaction (income or expense), and category.
class Transaction:
    @is_not_none
    @transaction_validador
    def __init__(self, date, amount, type_transaction, category):
        self.date = date
        self.amount = float(amount)
        self.type_transaction = type_transaction
        self.category = category
# Category class to represent a financial category.
class Category:
    @is_not_none
    @category_check
    def __init__(self, name):
        self.name = name


    

