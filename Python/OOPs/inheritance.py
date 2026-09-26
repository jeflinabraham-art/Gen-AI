# Parent class
class BankAccount:

    # Constructor of the parent class
    def __init__(self, name, balance):
        self.name = name
        self.balance = balance

    # Method defined in the parent class
    def deposit(self, amount):
        if amount > 0:
            self.balance += amount
            print(f"₹{amount} deposited successfully.")
        else:
            print("Please enter a positive amount to deposit.")

    # Method defined in the parent class
    def withdraw(self, amount):
        if amount > self.balance:
            print("Insufficient balance.")
        elif amount <= 0:
            print("Please enter a positive amount to be withdrawn.")
        else:
            self.balance -= amount
            print(f"₹{amount} withdrawn successfully.")

    # Method defined in the parent class
    def show_balance(self):
        print(f"Account holder: {self.name}")
        print(f"Balance: ₹{self.balance}")


# CHILD CLASS

# SavingsAccount inherits from BankAccount
# SavingsAccount automatically gets:
#   - __init__()
#   - deposit()
#   - withdraw()
#   - show_balance()
# from BankAccount.
#
class SavingsAccount(BankAccount):

    # Child class has its own constructor
    def __init__(self, name, balance, interest_rate):

        # Call the parent's constructor
        # This initializes:
        #   self.name
        #   self.balance
        super().__init__(name, balance)

        # This attribute belongs specifically to SavingsAccount
        self.interest_rate = interest_rate

    # Method defined in child class
    def add_interest(self):

        # Calculate interest
        interest = self.balance * self.interest_rate / 100

        # Add interest to the balance
        self.balance += interest
        print(f"Interest added: ₹{interest}")


    # Method overriding

    # BankAccount already has show_balance().
    # Here we define show_balance() again. This is called METHOD OVERRIDING.
    def show_balance(self):

        # Call the parent's show_balance() first
        super().show_balance()

        # Then add SavingsAccount-specific information
        print(f"Interest rate: {self.interest_rate}%")


# CREATE AN OBJECT OF THE CHILD CLASS
account = SavingsAccount(
    "Jeflin",
    15000,
    5
)
# INHERITED METHOD
# deposit() is NOT defined inside SavingsAccount.
# Python finds it in the parent class BankAccount
# and executes it.
account.deposit(3000)

# ANOTHER INHERITED METHOD
# withdraw() also comes from BankAccount.
account.withdraw(1000)


# CHILD-CLASS METHOD
# add_interest() is defined specifically inside
# SavingsAccount.
account.add_interest()

# OVERRIDDEN METHOD
# SavingsAccount has its own show_balance(),
# so Python uses the child version.
account.show_balance()

