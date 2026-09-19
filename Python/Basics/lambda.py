x = 10
# Python creates an object representing 10 somewhere in memory.
# x → a variable/reference pointing to that object.
# id(x) gives the memory address of the object.
# so, x isn't literally "the number 10." It's a reference to the object containing 10.

y = x
print("memory address of x:", id(x))
print("memory address of y:", id(y))
# Both x and y refer to the same object.

x = 20
print("memory address of x after reassignment:", id(x))
# The object 10 wasn't changed. We simply changed where x points.


# lambda functions are small anonymous functions defined using the lambda keyword. Lambda functions are often used for short, simple operations that can be defined in a single line of code.

# A lambda function is called anonymous because the function itself is created without giving it a name.


def add1(a, b):
    return a + b
# Python creates a function object and gives that function the name add1.


add2 = lambda x, y: x + y
# Python creates an anonymous function object. 'add2' is a variable/reference pointing to the function.


result = add2(5, 3)
print("\nResult of addition using lambda function:", result)

# map() is a built-in function that applies a given function to each item of an iterable (like a list) and returns an iterator. The map() function takes two arguments: the function to apply and the iterable to process.
numbers = [1, 2, 3, 4, 5]
squared_numbers = list(map(lambda x: x**2, numbers))
print("Squared numbers using map and lambda:", squared_numbers)

# filter() is a built-in function that constructs an iterator from elements of an iterable for which a function returns true. The filter() function takes two arguments: the function to apply and the iterable to process.
even_numbers = list(filter(lambda x: x % 2 == 0, numbers))
print("Even numbers using filter and lambda:", even_numbers)

# reduce() is a function from the functools module that applies a rolling computation to sequential pairs of values in an itera  ble. It takes two arguments: a function and an iterable. The function should take two arguments and return a single value.
from functools import reduce
total = reduce(lambda x, y: x + y, numbers)
print("Sum of numbers using reduce and lambda:", total)