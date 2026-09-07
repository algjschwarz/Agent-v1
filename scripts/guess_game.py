"""A Python script for a simple 'Guess the Number' game where the user attempts to guess a random number between 1 and 100."""

import random

def guess_the_number() -> None:
    """
    A simple 'Guess the Number' game.
    The player has to guess a number between 1 and 100.
    """
    print("Welcome to the Guess the Number Game!")
    print("I'm thinking of a number between 1 and 100.")

    secret_number = random.randint(1, 100)
    attempts = 0

    while True:
        try:
            # The input() function inside the script will prompt the user interactively.
            guess = int(input("Enter your guess: "))
            attempts += 1

            if guess < 1 or guess > 100:
                print("Please guess a number within the specified range (1-100).")
                continue

            if guess < secret_number:
                print("Too low! Try again.")
            elif guess > secret_number:
                print("Too high! Try again.")
            else:
                print(f"\n🎉 Congratulations! You guessed the number {secret_number} correctly!")
                print(f"It took you {attempts} attempts.")
                break
        except ValueError:
            print("Invalid input. Please enter a whole number.")

if __name__ == "__main__":
    guess_the_number()