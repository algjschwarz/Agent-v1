"""A simple console-based calculator program that performs basic arithmetic operations (add, subtract, multiply, divide), including type hints and docstrings for better code quality. The run_calculator function now has a specified return type."""

def add(x: float, y: float) -> float:
    """Returns the sum of two numbers."""
    return x + y

def subtract(x: float, y: float) -> float:
    """Returns the difference between two numbers."""
    return x - y

def multiply(x: float, y: float) -> float:
    """Returns the product of two numbers."""
    return x * y

def divide(x: float, y: float) -> float | str:
    """
    Returns the division of two numbers.
    Returns an error string if division by zero is attempted.
    """
    if y == 0:
        return "Error! Division by zero is not possible."
    return x / y

def run_calculator() -> None:
    """Runs the main calculator loop and handles user input."""
    print("--- Simple Console Calculator ---")
    print("Select operation:")
    print("1. Add (+)")
    print("2. Subtract (-)")
    print("3. Multiply (*)")
    print("4. Divide (/)")

    while True:
        user_choice = input("\nEnter choice (1/2/3/4) or 'q' to quit: ")

        if user_choice.lower() == 'q':
            break
        
        if user_choice not in ('1', '2', '3', '4'):
            print("❌ Invalid choice. Please select an option from 1 to 4, or 'q' to quit.")
            continue

        try:
            num1 = float(input("Enter first number: "))
            num2 = float(input("Enter second number: "))
        except ValueError:
            print("❌ Invalid input. Please ensure you enter valid numbers.")
            continue

        result = None
        operator_symbol = ""
        
        if user_choice == '1':
            result = add(num1, num2)
            operator_symbol = "+"
        elif user_choice == '2':
            result = subtract(num1, num2)
            operator_symbol = "-"
        elif user_choice == '3':
            result = multiply(num1, num2)
            operator_symbol = "*"
        elif user_choice == '4':
            result = divide(num1, num2)
            operator_symbol = "/"
        
        print(f"\n✅ Result: {num1} {operator_symbol} {num2} = {result}")
        
        again = input("\nDo you want to perform another calculation? (yes/no): ")
        if again.lower() != 'yes':
            break

    print("\n👋 Calculator terminated. Goodbye!")

if __name__ == "__main__":
    run_calculator()