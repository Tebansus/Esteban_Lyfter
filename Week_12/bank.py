# Write a class BankAccount that has the following attributes:
# balance
# The following methods:
# deposit:adds amount to the balance
# withdraw: subtracts amount from the balance
# __str__() : returns a string with the balance

class BankAccount:
    def __init__(self, balance):
        self.balance = balance

    def deposit(self, amount):
        self.balance += amount

    def withdraw(self, amount):
        if self.balance >= amount:
            self.balance -= amount
        else:
            print("Insufficient funds")

    def __str__(self):
        return f"Balance: {self.balance}"
# Write a class SavingsAccount that extends BankAccount and has the following attributes:
# min_balance (a float)
# The following methods:
# withdraw:subtracts amount from the balance. If the balance is less than min_balance, the amount is not subtracted and a message is printed that the withdrawal is not allowed. Indicate maximum allowed withdrawal amount.

class SavingsAccount(BankAccount):
    def __init__(self, balance, min_balance):
        super().__init__(balance)
        self.min_balance = min_balance
    def withdraw(self, amount):
        super().withdraw(amount)
        if self.balance < self.min_balance:
            self.balance += amount
            print("Cannot withdraw. Minimum balance reached. Please try again. Your maximum allowed withdrawal is", self.balance - self.min_balance)
# Test the classes by creating instances of BankAccount and SavingsAccount and calling the methods on them.
def main():
    test_bank_account = BankAccount(100)
    print(test_bank_account)
    test_bank_account.deposit(50)
    print(test_bank_account)
    test_bank_account.withdraw(200)
    print(test_bank_account)
    print("Now testing SavingsAccount")
    test_savings_account = SavingsAccount(100, 50)
    print(test_savings_account)
    test_savings_account.deposit(50)
    print(test_savings_account)
    test_savings_account.withdraw(110)
    print(test_savings_account)

if __name__ == "__main__":
    main()