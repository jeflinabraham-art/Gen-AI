# enumerate in Python is a built-in function that allows you to loop over an iterable (like a list, tuple, or string) and get both the index and the value of each item in the iterable. It returns an enumerate object, which can be converted into a list of tuples containing the index and value pairs.

# Using a for loop to iterate through the list and get the index and value
position = 1
fruits = ["apple", "banana", "cherry"]
for fruit in fruits:
    print(f"{position}. {fruit}")
    position += 1

# Using enumerate() to get the index and value
for value in enumerate(fruits):
    # valuer is a tuple containing the index and the value of each item in the list.
    print(value)

# tuple unpacking
for index, fruit in enumerate(fruits):
    print(f"{index + 1}. {fruit}")
