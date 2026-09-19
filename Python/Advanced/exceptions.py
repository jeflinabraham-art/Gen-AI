# exceptions

try:
    x = input("Enter a number: ")
    x = int(x)
    result = 10 / x
except ValueError:
    print("Invalid input! Please enter a valid number.")
except ZeroDivisionError:
    print("Error! Division by zero is not allowed.")
else:
    print("Result:", result)
finally:
    print("Execution completed.")
