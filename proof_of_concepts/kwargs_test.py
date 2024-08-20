# author - figueroa_90894@students.pupr.edu
# Testing double unpack of dictionary.

# Conclusion - It seems the double-unpack of kwargs in a function signature
# creates a dictionary view and modifies it to delete used named argument,
# instead of modifiying the original unpacked dictionary at the function call.

class Alpha:
    def __init__(self, arg1, arg2, *args, **kwargs):
        print("kwargs in alpha", kwargs)
        self.arg1 = arg1
        self.arg2 = arg2
        self.kwargs = kwargs

    def say(self):
        print("arg1", self.arg1)
        print("arg2", self.arg2)
        print("kwargs", self.kwargs)

# Unpacks succesfully and still saves kwargs
# BUT used entried are deleted, I dont want that.
# Somewhat successful
def test_one_double_pack_in_class():
    print("TEST - One Double Unpack in Class")
    
    d = {"acorn": 0, "berry": 1, "arg1": 4, "arg2": 5}
    print("d before", d)
   
    print("init alpha")
    a = Alpha(**d)          # double-unpack
    a.say()                 # elements in kwargs have been deleted
    
    print("d after", d)     # original dictionary is unmodified

# Unsuccessfull, did not unpack based on names
# Unpacked keys instead of values
def test_double_unpack_in_function():
    print("TEST - Double Unpack in Function")
    
    d = {"acorn": 0, "berry": 1, "arg1": 4, "arg2": 5}
    print("d before", d)
   
    # unpacks positionally, not name based
    # didnt even unpack values, only keys
    # not useful imo
    acorn, arg2, berry, arg1 = d

    print("acorn", acorn)
    print("berry", berry)
    print("arg1", arg1)
    print("arg2", arg2)
    
    print("d after", d)

# Succesful, unpacking two separate dictionaries
# still passes arguments correctly
def test_multi_dic_unpack():
    da = {"acorn": 0, "arg1": 4}
    db = {"arg2": 5, "berry": 1}
    print("da", da)
    print("db", db)

    print("init alpha")
    a = Alpha(**da, **db)
    print("\n\ninspect alpha")
    a.say()


def main():
    # test_one_double_pack_in_class()
    # test_double_unpack_in_function()
    test_multi_dic_unpack()

if __name__ == "__main__":
    main()