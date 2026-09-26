class BankAccount:

    # class attributes
    bank_name = "hdfc_ltd"
    interest_rate = 7.0

    def __init__(self, name, balance):
        self.account_name = name
        self.account_balance= balance

    def __str__(self):
        return f"account name: {self.account_name}, account balance: {self.account_balance}"

    # instance methods: methods at object level. used when the method needs data belonging to a particular object.
    def deposit(self, amount):
        self.account_balance += amount
        print(f"{amount} Rs. deposited successfully.")
        print(f"current balance: {self.account_balance} Rs.\n")

    def withdraw(self, amount):
        if(amount > self.account_balance):
            print("insufficient balance")
        else:
            self.account_balance -= amount
            print(f"amount withdrawn: {amount} Rs.")
        print(f"current balance: {self.account_balance} Rs.\n")

    # class method: methods at class level. used for implementing functionalities applicable accross all objects.
    # a class method can be called through an instance too, and Python will still pass the class as cls, not the instance as self.
    @classmethod
    def change_intesrest_rate(cls, rate):
        cls.interest_rate = rate
        print(f"Interest rate updated to: {cls.interest_rate}%")

    # static method: A static method is simply a method inside a class that doesn't need the object (self) or the class (cls).
    @staticmethod
    def is_amount_valid(amount):
        if(amount > 0):
            return True
        return False



b1 = BankAccount("jeflin", 15000)
b2 = BankAccount("aryan", 25000)

# instance method
b1.deposit(2000)
b1.withdraw(500)

# class method
BankAccount.change_intesrest_rate(7.5)
b2.change_intesrest_rate(6.2)

# static method
amount = -10000
if(BankAccount.is_amount_valid(amount)):
    b3 = BankAccount("Yath", amount)
else:
    b3 = BankAccount("Yath", 0)
print(b3)

