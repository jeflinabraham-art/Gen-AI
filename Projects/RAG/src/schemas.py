from dataclasses import dataclass, field


# @dataclass: It automatically creates __init__() constructor and generates customized implementations of certain methods (like __repr__(), __eq__()) based on your class attributes.
@dataclass
class SourceCitation:
    filename: str
    page: int | None = None
    preview: str = ""


@dataclass
class RAGResponse:
    answer: str

    # Why not just use = []?
    # Because lists are mutable objects. If we use =[] as a default value, Python creates the list only once when the function is defined. Multiple objects that use this default will share the same list.
    # Modifying the list in one object can affect other objects unintentionally.

    # = field(default_factory=list): This creates a new empty list for every object, ensuring each object has its own independent list.

    # Use default_factory=list instead of =[] when defining list attributes in "dataclasses".
    sources: list[SourceCitation] = field(default_factory=list)
    num_chunks: int = 0



'''
without @dataclass

class Student:
    def __init__(self, name, age):
        self.name = name
        self.age = age

student1 = Student("John", 23)
student2 = Student("John", 23)

print(student1)
print(student1 == student2)



Output:
<__main__.Student object at 0x...>
False



Why?
__init__() → We had to write it ourselves to initialize attributes.
__repr__() → Python uses its default implementation, which displays the object's memory-related representation.
__eq__() → Python compares object identity by default. Both objects are different objects, so it returns False.
'''



'''
with @dataclass

from dataclasses import dataclass

@dataclass
class Student:
    name: str
    age: int


student1 = Student("John", 23)
student2 = Student("John", 23)

print(student1)
print(student1 == student2)

Output:
Student(name='John', age=23)
True

Why?

Python automatically generates useful implementations of:
__init__() → Initializes name and age.
__repr__() → Displays the object's attributes.
__eq__() → Compares attribute values instead of object identity.

@dataclass generates useful implementations tailored to your attributes.
'''
