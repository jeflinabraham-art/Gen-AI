import time
import threading

def print_numbers():
    for i in range(1, 6):
        print(i)
        time.sleep(1)  # Sleep for 1 second

def print_letters():
    for char in "abcde":
        print(char)
        time.sleep(2)  # Sleep for 2 seconds

# print_numbers()
# print_letters()

print("Starting threads...")
thread1 = threading.Thread(target=print_numbers)
thread2 = threading.Thread(target=print_letters)

# start() is used to start the thread's activity.
thread1.start()
thread2.start()

# join() is used to wait for the thread to complete its execution.
# The main thread should wait until these threads finish.
thread1.join()
thread2.join()
print("Both threads have completed.")


#                  Main thread
#                      │
#           ┌──────────┴──────────┐
#           ↓                     ↓
#       thread1                thread2
#           │                     │
#   print_numbers()         print_letters()
#           │                     │
#        1, 2, 3...            a, b, c...


# passing arguments to a thread
def greet(name):
    print(f"Hello, {name}!")

thread3 = threading.Thread(target=greet, args=("Alice",))
thread3.start()
