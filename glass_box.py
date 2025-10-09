"""A simple module to demonstrate glassbox unit testing."""

def FizzBuzz(n):
    if n % 3 == 0 and n % 5 == 0:
        return "FizzBuzz"
    elif n % 3 == 0:
        return "Fizz"
    elif n % 5 == 0:
        return "Buzz"
    else:
        return str(n)
    

if __name__ == "__main__":
    print("This is a FizzBuzz module.")
    print("Try calling FizzBuzz(n) with an integer n.")