class Calculator:
    
    # Initialise the calculator with a and b, assign to self

    def __init__(self, a, b): 
        self.a = a
        self.b = b

    def do_sum(self):
        return self.a + self.b
    
    def do_product(self):
        return self.a * self.b
    
    def do_subtract(self):
        return self.a - self.b
    
    def do_divide(self):
        return round((self.a / self.b),2)

a = int(input("Please input number 'a':\n"))

b = int(input("Please input number 'b':\n"))

myCalc = Calculator(a,b)
print(myCalc.do_product())



