def add(a, b):
    return a + b


def subtract(a, b):
    return a - b


def multiply(a, b):
    return a * b


def divide(a, b):
    if b == 0:
        raise ZeroDivisionError("Cannot divide by zero.")
    return a / b


def main():
    print("Welcome to the calculator")
    print("1 add")
    print("2 subtract")
    print("3 multiply")
    print("4 divide")

    choice = int(input("enter your choice: "))
    x = int(input("enter value X: "))
    y = int(input("enter value Y: "))

    if choice == 1:
        result = add(x, y)
    elif choice == 2:
        result = subtract(x, y)
    elif choice == 3:
        result = multiply(x, y)
    elif choice == 4:
        result = divide(x, y)
    else:
        print("invalid choice")
        return

    print("result:", result)


if __name__ == "__main__":
    main()


