# Dunder = double underscore.

# Dunder methods are special methods that Python automatically invokes when you use certain built-in operations on your objects. They are also called special methods or magic methods.

# our class is essentially teaching Python how your Book object should behave with built-in operations.

from operator import call


class Book:
    def __init__(self, title, author):
        self.title = title
        self.author = author

    # what should print(object) show?
    def __str__(self):
        return f"{self.title} by {self.author}"

    # what happens when you call len(object)?
    def __len__(self):
        return len(self.title)

    # what does == mean for our object?
    def __eq__(self, other):
        if isinstance(other, Book):
            return self.title == other.title and self.author == other.author
        return False

b1 = Book("1984", "George Orwell")
b2 = Book("To Kill a Mockingbird", "Harper Lee")
b3 = Book("1984", "George Orwell")

# without __str__
# print(b1)
# Output: <__main__.Book object at 0x000...>

print(b1)
print(len(b1))
print(b1 == b2)
print(b1 == b3)

print("\n")

# addition

class Wallet:
    def __init__(self, amount):
        self.amount = amount

    def __str__(self):
        return f"{self.amount}"

    def __add__(self, other):
        if isinstance(other, Wallet):
            return Wallet(self.amount + other.amount)
        return "type of other is not Wallet"

    # def __str__(self):
    #     return f"Wallet with amount: {self.amount}"

w1 = Wallet(100)
w2 = Wallet(500)
print(w1 + w2)

w3 = Wallet(150)
print(w1 + w2 + w3)