nums = [1,2,3,4,5]
print(nums)

# when file is run directly, the value of __name__ is set to "__main__". When the file is imported as a module, the value of __name__ is set to the name of the module.
print(__name__)

print("Hello from _first.py!")

if __name__ == "__main__":
    print("This code is running directly.")