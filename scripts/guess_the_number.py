"""A simple game where the user tries to guess a randomly selected number between 1 and 100 within a set number of attempts."""

import random

def guess_the_number():
    """A simple game where the user tries to guess a randomly selected number."""
    print("=============================")
    print("   Welcome to Guess The Number!  ")
    print("=============================")
    
    # Generate a random number between 1 and 100
    secret_number = random.randint(1, 100)
    max_attempts = 7
    attempts = 0

    while attempts < max_attempts:
        try:
            guess = int(input("Enter your guess (1-100): "))
        except ValueError:
            print("Invalid input. Please enter a whole number.")
            continue

        attempts += 1

        if guess == secret_number:
            print(f"\n*** Congratulations! You guessed the number {secret_number} in {attempts} attempts! ***")
            return
        elif abs(guess - secret_number) < 10:
            print("You are very close!")
        elif guess < secret_number:
            print("Too low! Try a higher number.")
        else:
            print("Too high! Try a lower number.")

    print("\n=============================")
    print(f"Game Over! You ran out of attempts. The correct number was {secret_number}.")
    print("=============================")

if __name__ == "__main__":
    guess_the_number()