"""A program that takes user input from the console and checks if the input is 'hi'. If it is, it prints 'hi' back to the console."""

def main() -> None:
    """Reads user input from the console and prints 'hi' if the input is 'hi'."""
    try:
        user_input = input("Please enter something: ")
        if user_input.strip().lower() == "hi":
            print("hi")
        else:
            print("The input was not 'hi'.")
    except EOFError:
        print("\nProgram finished.")

if __name__ == "__main__":
    main()