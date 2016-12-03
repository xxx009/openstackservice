class Add:
    def __init__(self, num1, num2):
        self.num1 = num1
        self.num2 = num2
        print "Sum of", self.num1,"and",self.num2, "is:"

    def __call__(self):
        return (self.num1 + self.num2)


add = Add(1,2)
print add()


