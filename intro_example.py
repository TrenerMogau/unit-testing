def simple_func(name="World"):
    return f"Hello, {name}!"

def returnFalse():
    return False

def returnTrue():
    return True


if __name__ == "__main__":
    print(simple_func())  # Default case
    print(simple_func("Alice"))  # Custom name