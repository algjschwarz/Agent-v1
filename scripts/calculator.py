"""A simple command-line calculator that performs addition, subtraction, multiplication, and division on user inputs."""

def calculate(num1, num2, operation):
    """Performs the calculation based on the selected operation."""
    if operation == '+':
        return num1 + num2
    elif operation == '-':
        return num1 - num2
    elif operation == '*':
        return num1 * num2
    elif operation == '/':
        # Handle division by zero
        if num2 == 0:
            return "Error! Division by zero is not allowed."
        return num1 / num2
    else:
        return "Invalid operation selected."

def run_calculator():
    """Main function for the simple calculator program."""
    print("=============================")
    print("   Simple Command-Line Calculator  ")
    print("=============================")
    print("Available operations: +, -, *, /")
    
    while True:
        try:
            # Get user input for numbers and operation
            num1_str = input("\nEnter the first number (or 'quit' to exit): ")
            if num1_str.lower() == 'quit':
                break
            num1 = float(num1_str)

            operation = input("Enter the operator (+, -, *, /): ").strip()
            if operation not in ['+', '-', '*', '/']:
                print("Invalid operator. Please use +, -, *, or /.")
                continue

            num2_str = input("Enter the second number: ")
            if num2_str.lower() == 'quit':
                 break
            num2 = float(num2_str)

        except ValueError:
            print("\nInvalid input. Please ensure you enter valid numbers.")
            continue

        # Calculate and display result
        result = calculate(num1, num2, operation)
        print("-" * 40)
        print(f"Result: {num1} {operation} {num2} = {result}")
        print("-" * 40)

    print("Calculator closed. Goodbye!")


if __name__ == "__main__":
    run_calculator()