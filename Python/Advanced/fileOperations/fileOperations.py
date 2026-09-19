# w (write mode)
# If the file already exists, it will be overwritten. If the file does not exist, a new file will be created. 

file = open("myNotes.txt", "w")
file.write("My name is Jef.\n")
file.write("I am learning Python.\n")
file.close()

# a (append mode)
# If the file already exists, the new data will be added to the end of the file
file = open("myNotes.txt", "a")
file.write("I am learning Generative AI.\n")
file.close()

# r (read mode)
# If the file does not exist, an error will be raised. You can read the content of the file using the read() method.
file = open("myNotes.txt", "r")
content = file.read()
print(content)
file.close()

# with in python is used to open a file and automatically close it after the block of code is executed. 
with open("myNotes.txt", "r") as file:
    content = file.read()
    print(content)

    file.seek(0)  # Move the cursor to the beginning of the file
    lines = file.readlines()
    print(lines)

try:
    with open("newFile.txt", "r") as file:
        content = file.read()
        print(content)
except FileNotFoundError:
    print("File not found. Please create the file and try again.")
finally:
    print("Execution completed.")