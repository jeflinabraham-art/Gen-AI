x = 0

# global keyword in Python is used to declare a variable as global, allowing it to be accessed and modified from within a function. 
# When you use the global keyword, you are telling Python that you want to use the variable defined in the global scope, rather than creating a new local variable with the same name.

def increment():
    global x
    x += 1
    print("Value of x inside increment():", x)

increment()
increment()
increment()