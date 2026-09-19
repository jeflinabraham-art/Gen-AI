# dictionary in Python is a collection of key-value pairs. Each key is unique and is used to access the corresponding value. Dictionaries are mutable, meaning you can change their content without changing their identity.

dictionary = {
    "name": "John", 
    "age": 30, 
    "city": "New York"
}
print(dictionary)
print(dictionary["name"])

# adding a new key-value pair to the dictionary
dictionary["country"] = "USA"

print(dictionary.keys())
print(dictionary.values())

# removing a key-value pair from the dictionary using the pop() method. The pop() method removes the specified key and returns the corresponding value. If the key is not found, it raises a KeyError.
dictionary.pop("age")
print(dictionary)

# updating the value of an existing key in the dictionary
dictionary["name"] = "Jef"
print(dictionary)

# looping
# dictionary.items() returns a dictionary view containing (key, value) tuples.
print(dictionary.items())
for key, value in dictionary.items():
    print(f"{key}: {value}")

