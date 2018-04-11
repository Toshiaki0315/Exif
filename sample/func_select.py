class f():
    __b = 0
    def __init__(self, a):
        self.__b = a

    def a(self):
        print("Call Func a " , self.__b)
        self.__b += 10

    def b(self):
        print("Call Func b ", self.__b)
        self.__b += 20

    def select(self):
        func_lists = {"a":self.a, "b":self.b}

        func_lists["a"]()
        func_lists["b"]()
        func_lists["a"]()

func = f(3)
func.select()