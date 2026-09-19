# strings in python

# basic string methods
name = "John Doe John"
print("length of name:", len(name))
print("name in uppercase:", name.upper())
print("name in lowercase:", name.lower())
print("name with replaced substring:", name.replace("John", "Jane"))
print("name split into words:", name.split(" "))

message = "  Learn Python Programming  "
print("message with leading/trailing whitespace removed:", message.strip())
print("position of P in message:", message.find("P"))

# slicing
print("first character of name:", name[0])
print("last character of name:", name[-1])
print("first 5 characters of name:", name[:5])
print("characters from index 2 to 5:", name[2:6])
print("skip every second character of name:", name[::2])
print("reversed name:", name[::-1])



# In Python, strings are immutable means:
# Once a string object is created, you cannot change the characters inside that same string object.

s = "Hello"
print("memory address of s:", id(s))

# s[0] = "h" 
# This will raise an error because strings are immutable in Python

s = "hello"
# The original memory object wasn't changed.
# The variable s simply started referring to a different object.

print("memory address of s:", id(s))

# fstring
name = "John"
age = 30
print(f"Hello, my name is {name} and I am {age} years old.")

a = 2
b = 5
print(f"{a} X {b} = {a * b}")

