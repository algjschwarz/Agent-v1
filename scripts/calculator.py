"""A simple command-line calculator application written in Python. Includes type hinting and docstrings as required by the file writing tool. """

from typing import Union

def add(x: float, y: float) -> float:
    """Adds two numbers."""
    return x + y

def subtract(x: float, y: float) -> float:
    """Subtracts two numbers."""
    return x - y

def multiply(x: float, y: float) -> float:
    """Multiplies two numbers."""
    return x * y

def divide(x: float, y: float) -> Union[float, str]:
    """Divides two numbers. Handles division by zero."""
    if y == 0:
        return "Error! Cannot divide by zero."
    return x / y

def calculator() -> None:
    """Runs the main calculator interface loop."""
    print("Simple Command Line Calculator")
    while True:
        print("\nSelect operation:")
        print("1. Add (+)")
        print("2. Subtract (-)")
        print("3. Multiply (*)")
        print("4. Divide (/)")
        print("5. Exit")

        choice = input("Enter choice (1/2/3/4/5): ")

        if choice == '5':
            print("Exiting calculator. Goodbye!")
            break

        if choice in ('1', '2', '3', '4'):
            try:
                num1 = float(input("Enter first number: "))
                num2 = float(input("Enter second number: "))
            except ValueError:
                print("Invalid input. Please enter a valid number.")
                continue

            if choice == '1':
                result = add(num1, num2)
                print(f"Result: {num1} + {num2} = {result}")
            elif choice == '2':
                result = subtract(num1, num2)
                print(f"Result: {num1} - {num2} = {result}")
            elif choice == '3':
                result = multiply(num1, num2)
                print(f"Result: {num1} * {num2} = {result}")
            elif choice == '4':
                result = divide(num1, num2)
                print(f"Result: {num1} / {num2} = {result}")
        else:
            print("Invalid choice. Please select an option from 1 to 5.")

if __name__ == "__main__":
    calculator()
