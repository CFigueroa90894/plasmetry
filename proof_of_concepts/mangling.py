# author - figueroa_90894@students.pupr.edu
# Testing if mangled functions in parent class can still be called
# from children without overriding them.

# Conclusion - no you cannot, prints a very dense error message,
# seems to break other stuff in the interpreter.

class Parent:
    def __init__(self):
        self.name = "parent"

    def _who(self):
        print(f"i am {self.name}")


class Child(Parent):
    def __init__(self):
        self.name = "child"

def test():
    print("init child")
    child = Child()
    print("who? expect child")
    child.__who()

if __name__ == "__main__":
    test()
    