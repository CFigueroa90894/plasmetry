# author - figueroa_90894@students.pupr.edu
# Testing whether grandchildren that do not override grandparents abstract
# methods can be instantiated if: their parents did not override it and 
# are not explicit marked as abstract.

# Conclusion - child cannot be instantiated even if it did not directly
# inherit from an abstract class.

from abc import ABC, abstractmethod

class GrandParent(ABC):
    def __init__(self):
        self.name = "grandparent"

    @abstractmethod
    def hello(self):
        raise NotImplementedError
    
    def who(self):
        print(f"i am {self.name}")
    

class Parent(GrandParent):
    def __init__(self):
        self.name = "parent"


class Child(Parent):
    def __init__(self):
        self.name = "child"


def create_grandparent():
    g = GrandParent()
    g.who()

def create_parent():
    p = Parent()
    p.who()

def create_child():
    c = Child()
    c.who()

def main():
    # create_grandparent()
    # create_parent()
    create_child()

if __name__ == "__main__":
    main()