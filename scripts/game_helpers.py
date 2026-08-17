"""Contains core functions for the Rock Paper Scissors game (input handling, computer choice generation, and determining the winner)."""

import random
from typing import Tuple

def get_player_choice() -> str:
    """Prompts the user for input and validates that the choice is 'rock', 'paper', or 'scissors'."""
    while True:
        print("\nPlease choose your move:")
        print("1. Rock")
        print("2. Paper")
        print("3. Scissors")
        choice = input("Enter choice (e.g., rock, paper, scissors): ").lower().strip()
        if choice in ['rock', 'paper', 'scissors']:
            return choice
        else:
            print("Invalid choice. Please enter 'rock', 'paper', or 'scissors'.")

def get_computer_choice() -> str:
    """Generates a random move for the computer."""
    choices = ["rock", "paper", "scissors"]
    return random.choice(choices)

def determine_winner(player_choice: str, computer_choice: str) -> Tuple[str, str]:
    """
    Compares two moves and determines the winner.
    Returns a tuple (winner_message, reason).
    """
    print("-" * 30)
    print(f"Player chose: {player_choice.capitalize()}")
    print(f"Computer chose: {computer_choice.capitalize()}")

    if player_choice == computer_choice:
        return "It's a tie!", "Haha, we matched!"

    # Winning conditions for the player
    elif (player_choice == "rock" and computer_choice == "scissors") or \
         (player_choice == "scissors" and computer_choice == "paper") or \
         (player_choice == "paper" and computer_choice == "rock"):
        return "You win!", "Rocks crush scissors, scissors cut paper, and paper covers rocks."
    # All other cases mean the computer wins
    else:
        return "Computer wins!", "Better luck next time!"
