import pandas as pd

class Calculator:
    
    # Initialise the calculator with a and b, assign to self

    def __init__(self, a=0, b=0): 
        self.a = a
        self.b = b

    # Functions for the Calculator class

    def do_sum(self):
        return self.a + self.b
    
    def do_product(self):
        return self.a * self.b
    
    def do_subtract(self):
        return self.a - self.b
    
    def do_divide(self):
        return round((self.a / self.b),2)
    

# Function for prompting the user
## user can choose to sum two values together or visualise the times table up to 12 of an inputted number

def prompt_user():
    choice = input("Please input sum, tt, or ttdf:\n").lower()

    if choice == "sum":
        a = int(input("Please input number 'a':\n"))
        b = int(input("Please input number 'b':\n"))
        myCalc = Calculator(a,b)
        print(myCalc.do_product())
        choice = ""

    elif choice == "tt":
        b = int(input("Please input the times table you would like to see:\n"))
        a = 1
        print("Please see ", b, " times table below:\n")
        while (a < 13):
            myCalc = Calculator(a,b)
            print(myCalc.do_product())
            a = a + 1
        print("\n")

    elif choice == "ttdf":
        b = int(input("Please input the times table you would like to see:\n"))
        a = 1
        df = pd.DataFrame({'Position': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]})
        df['Result'] = df['Position'] * b
        print("Please see ", b, " times table below:\n",df)

    else:
        print('Invalid input!')



if __name__ == '__main__':
    prompt_user()