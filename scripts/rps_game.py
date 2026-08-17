"""A text-based game of Rock, Paper, Scissors where the user plays against the computer (which chooses randomly)."""

import random

def get_computer_choice():
    """Randomly selects 'rock', 'paper', or 'scissors' for the computer."""
    return random.choice(['rock', 'paper', 'scissors'])

def determine_winner(user_choice, computer_choice):
    """Determines the winner based on the rules of the game."""
    # Check for a tie
    if user_choice == computer_choice:
        return "It's a Tie!"
    
    # Define winning conditions (User wins)
    elif (user_choice == 'rock' and computer_choice == 'scissors') or \
         (user_choice == 'scissors' and computer_choice == 'paper') or \
         (user_choice == 'paper' and computer_choice == 'rock'):
        return "You Win!"
    else:
        return "Computer Wins!"

def play_game():
    """Main function to run the Rock, Paper, Scissors game."""
    print("=============================")
    print("   Rock, Paper, Scissors!  ")
    print("=============================")
    
    while True:
        user_input = input("\nEnter your choice (rock, paper, scissors) or 'quit' to exit: ").lower()
        if user_input == 'quit':
            print("Thanks for playing! Goodbye.")
            break
        
        if user_input not in ['rock', 'paper', 'scissors']:
            print("Invalid choice. Please enter rock, paper, or scissors.")
            continue

        # Get computer's move
        computer_choice = get_computer_choice()
        
        # Determine and display the winner
        winner = determine_winner(user_input, computer_choice)
        
        print("-" * 30)
        print(f"You chose: {user_input.capitalize()}")
        print(f"Computer chose: {computer_choice.capitalize()}")
        print(f"\n--- Result: {winner} ---")

if __name__ == "__main__":
    play_game()