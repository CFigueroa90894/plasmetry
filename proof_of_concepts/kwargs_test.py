class Alpha:
    def __init__(self, arg1, arg2, *args, **kwargs):
        self.arg1 = arg1
        self.arg2 = arg2
        self.kwargs = kwargs

    def say(self):
        print("arg1", self.arg1)
        print("arg2", self.arg2)
        print("kwargs", self.kwargs)

def test():
    print("init alpha")
    d = {"acorn": 0, "berry": 1, "arg1": 4, "arg2": 5}
    a = Alpha(**d)
    a.say()

def main():
    test()

if __name__ == "__main__":
    main()