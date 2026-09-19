def my_add(a, b):
    return a + b

result = my_add(5, 3)
print("Result of addition:", result)


# args in Python allows you to pass a variable number of arguments to a function.
def my_add(*args):
    return sum(args)
result = my_add(1, 2, 3, 4, 5)
print("Result of addition with variable arguments:", result, "\n")


#keyword arguments means that you can pass arguments to a function by explicitly naming them, rather than relying on their position in the argument list. This allows for more flexibility and clarity when calling functions, especially when dealing with functions that have many parameters or optional parameters.

# kwargs in Python allows you to pass a variable number of keyword arguments to a function. It collects the keyword arguments into a dictionary.
def my_function(**kwargs):
    for key, value in kwargs.items():
        print(f"{key}: {value}")

my_function(name="Alice", age=30, city="New York")


# another example of using *args and **kwargs together in a function definition. 
def show_data(*args, **kwargs):
    print("\nPositional arguments:", args)
    print("Keyword arguments:", kwargs)
    print("Sum of positional arguments:", sum(args))
    for k, v in kwargs.items():
        print(f"{k} -> {v}")

show_data(1, 2, 3, name="Alice", age=30, city="New York")