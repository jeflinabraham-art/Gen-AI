# self in Python OOP is a reference to the current instance of the class. When you create an object of a class, self allows you to refer to that specific instance.

class Student:

    def __init__(self, name, age):

        # Create an attribute called name on this object and give it this value.
        self.name = name

        # Create an attribute called age on this object and give it this value.
        self.age = age

    def display(self):
        print(f"Name: {self.name}, Age: {self.age}")

# student1 = Student("Alice", 20)
# student1.display()



class Car:
    # class attribute
    wheels = 4

    def __init__(self, brand_name):
        # instance attribute
        self.brand = brand_name

car1 = Car("Toyota")
print(car1.brand)
print(car1.wheels)