# Lists are mutable, ordered collections of items. They can contain elements of different data types, including other lists. Lists are defined using square brackets [] and can be modified after their creation.

my_list = [1,2,3,4,2]
my_list.append(5)
print(my_list)

# remove() removes the first occurrence of the specified value from the list. If the value is not found, it raises a ValueError.
my_list.remove(2)
print(my_list)

popped_element = my_list.pop()
print(f"Popped element: {popped_element}")
print(my_list)

my_list.insert(1, 10)
print(my_list)

# copying a list
my_list = [1, 2, 3, 4, 5]
print(f"Original list: {my_list}")

copy_list = my_list.copy()
print(f"Copied list: {copy_list}")
copy_list.pop()
print(f"Original list after popping from copied list: {my_list}")

copy_list.clear()
print(f"Copied list after clearing: {copy_list}")

copy_list = my_list
print(f"Copied list: {copy_list}")
copy_list.pop()
print(f"Original list after popping from copied list: {my_list}") 

# tuples are immutable, ordered collections of items. They can contain elements of different data types, including other tuples. Tuples are defined using parentheses () and cannot be modified after their creation.

my_tuple = (1, 2, 3, 4, 5)
print(f"Original tuple: {my_tuple}")

single_element_tuple = (1) 
# this is not a tuple, it's just an integer. To create a single-element tuple, you need to include a comma after the element, like this: (1,).
print(type(single_element_tuple))

single_element_tuple = (1,)
print(f"Single element tuple: {single_element_tuple}")

# unpacking a tuple
my_tuple = ("jef", 23, "Delhi")
name, age, city = my_tuple
print(f"Name: {name}, Age: {age}, City: {city}")
