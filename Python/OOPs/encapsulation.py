class BankAccount:
    def __init__(self, name, balance):
        self.account_holder = name
        self.balance = balance

    def __str__(self):
        return f"account owner: {self.account_holder}, balance: {self.balance}"

    def deposit(self, amount):
        if(amount > 0):
            self.balance += amount
        else:
            print("please enter a positive amount to deposit")

    def withdraw(self, amount):
        if(amount > self.balance):
            print("insufficient balance amount")
        else:
            self.balance -= amount

acc1 = BankAccount("Jeflin", 15000)
acc1.deposit(3000)
acc1.withdraw(1000)

# balance can be accessed from outside, can also change its value (DANGER!!)
acc1.balance = 0
print(acc1)



class BankAccount_Protected:
    def __init__(self, name, balance):
        self.account_holder = name
        self.__balance = balance

    def __str__(self):
        return f"account owner: {self.account_holder}, balance: {self.__balance}"

    def deposit(self, amount):
        if(amount > 0):
            self.__balance += amount
        else:
            print("please enter a positive amount to deposit")

    def withdraw(self, amount):
        if(amount > self.__balance):
            print("insufficient balance amount")
        else:
            self.__balance -= amount

acc2 = BankAccount_Protected("Jeflin", 25000)
acc2.deposit(1000)
acc2.withdraw(500)

# value of balance wont be updated
acc2.__balance = 0
print(acc2)

# just in case if u want to update (unethical and not recommended)
acc2._BankAccount_Protected__balance = 10
print(acc2)

