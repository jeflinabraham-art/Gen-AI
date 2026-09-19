my_lst = [1, 2, 2, 3, 3, 4, 5, 5, 5, 6]
my_set = set(my_lst)
print(my_set)

my_set.add(7)
print(my_set)

my_set.remove(2)
print(my_set)

my_set.discard(10)  # discard() does not raise an error if the element is not found
print(my_set)

a = {1, 2, 3}
b = {3, 4, 5}
print(f"Union of a and b: {a | b}")
print(f"Intersection of a and b: {a & b}")