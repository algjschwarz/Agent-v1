"""A simple, modular, turn-based console strategy game demonstrating resource conflict and territory control."""

import random
import time

# =====================================================================
# CORE GAME COMPONENTS
# =====================================================================

class Player:
    """Represents a participant in the game."""
    def __init__(self, name: str):
        self.name = name
        self.resources = 10
        self.units = 2
        self.controlled_territories = set()

    def display_status(self) -> str:
        """Returns a formatted string of the player's current status."""
        return (f"\n--- {self.name}'s Status ---\n"
                f"Resources: {self.resources}\n"
                f"Units: {self.units}\n"
                f"Controlled Territories: {len(self.controlled_territories)}\n")

    def gain_resources(self, amount: int):
        """Increases the player's resources."""
        self.resources += amount
        print(f"✅ {self.name} gained {amount} resources.")

    def spend_resources(self, amount: int) -> bool:
        """Decreases the player's resources if enough are available."""
        if self.resources >= amount:
            self.resources -= amount
            print(f"➖ {self.name} spent {amount} resources.")
            return True
        else:
            print(f"❌ {self.name} failed action: Insufficient resources (Needed: {amount}, Have: {self.resources}).")
            return False

class Territory:
    """Represents a location on the map."""
    def __init__(self, name: str, is_resource_rich: bool = False):
        self.name = name
        self.is_resource_rich = is_resource_rich
        self.owner: str | None = None
        self.defenses = 1 if is_resource_rich else 0

    def __str__(self) -> str:
        """String representation for display."""
        owner_status = f" (Owner: {self.owner})" if self.owner else ""
        resource_status = " [💰 RICH]" if self.is_resource_rich else ""
        return f"'{self.name}'{resource_status}{owner_status}"

class Game:
    """Manages the game state, players, and turn sequence."""
    def __init__(self, player_names: list[str]):
        self.players = [Player(name) for name in player_names]
        self.territories: list[Territory] = self._setup_map()
        self.current_turn = 1

    def _setup_map(self) -> list[Territory]:
        """Initializes the map of territories."""
        # Creating a set of predefined territories
        return [
            Territory("Capital City", is_resource_rich=True),
            Territory("Whispering Woods", is_resource_rich=False),
            Territory("Iron Mines", is_resource_rich=True),
            Territory("River Crossing", is_resource_rich=False)
        ]

    def display_game_state(self) -> None:
        """Prints the current state of the map and player status."""
        print("\n" + "="*60)
        print(f"*** GAME STATE - TURN {self.current_turn} ***")
        print("="*60)
        
        # 1. Territory Display
        print("\n[🗺️ MAP STATUS]")
        for t in self.territories:
            print(f"  - {t}")
        
        # 2. Player Status Display
        print("\n[👤 PLAYER STATUS]")
        for player in self.players:
            print(player.display_status())

    def run_turn(self) -> None:
        """Executes one full turn of the game, allowing player actions."""
        print("\n" + "#"*20 + "\n✨ STARTING TURN ACTIONS ✨")
        
        # Loop through each player to allow actions
        for player in self.players:
            print(f"\n\n>>> {player.name}'s Turn:")
            
            # Action 1: Claim/Expand Territory
            self.expand_territory(player)
            
            # Action 2: Attack (Basic Conflict Simulation)
            self.attack_random_target(player)
        
        self.current_turn += 1
        time.sleep(1)

    def expand_territory(self, player: Player):
        """Allows a player to claim a new territory."""
        available_territories = [t for t in self.territories if t.owner is None]
        if not available_territories:
            print(f"    -> {player.name}: All territories are currently claimed.")
            return

        print("    -> {player.name}: Territory Expansion.")
        
        # Simulate resource cost and selection
        if player.spend_resources(5):
            # Simple random claim for demonstration
            target = random.choice(available_territories)
            target.owner = player.name
            player.controlled_territories.add(target.name)
            print(f"    -> SUCCESS: {player.name} has claimed the {target.name}!")
        else:
            print(f"    -> FAILURE: {player.name} could not afford expansion.")

    def attack_random_target(self, attacker: Player):
        """Simulates a random attack on a non-allied, owned territory."""
        
        # Targets are territories owned by others and not already owned by the attacker
        potential_targets = [
            t for t in self.territories 
            if t.owner is not None and t.owner != attacker.name
        ]

        if not potential_targets:
            print("    -> {attacker.name}: No enemy territories found to attack.")
            return

        target = random.choice(potential_targets)
        print(f"    -> {attacker.name}: Military Action (Attacking {target.name}).")

        # Combat Logic (Simplified)
        attacker_units = attacker.units
        defender_defenses = target.defenses
        
        print(f"    -> Combat initiated! Attacker Units: {attacker_units}, Defender Defenses: {defender_defenses}.")
        time.sleep(0.5)

        if attacker_units > defender_defenses * 1.5:
            print(f"    -> VICTORY! {attacker.name} successfully conquered {target.name}!")
            
            # Transfer ownership
            old_owner = target.owner
            target.owner = attacker.name
            attacker.controlled_territories.add(target.name)
            if old_owner:
                 # Simple punishment for old owner (lose some units/resources)
                 old_player = next((p for p in self.players if p.name == old_owner), None)
                 if old_player:
                     old_player.units = max(1, old_player.units - 1)
                     old_player.resources = max(0, old_player.resources - 3)
                     print(f"    -> CONQUERED: {old_owner} was hit hard! Lost 1 unit and 3 resources.")
            
            attacker.gain_resources(5) # Reward
        else:
            print(f"    -> DEFEAT: {attacker.name}'s attack failed at {target.name}. Retreat!")
            attacker.units = max(1, attacker.units - 1) # Penalty for failure

# =====================================================================
# MAIN EXECUTION
# =====================================================================

if __name__ == "__main__":
    # Initialize the game with player names
    player_names = ["PlayerA", "PlayerB", "PlayerC"]
    game = Game(player_names)

    print("************************************************************")
    print("✨ WELCOME TO THE RESOURCE CONFLICT STRATEGY GAME ✨")
    print("************************************************************")
    time.sleep(1)
    
    # Display initial state
    game.display_game_state()

    # Run a few turns to demonstrate functionality
    try:
        print("\n\n[Running 3 Demonstration Turns. Press Ctrl+C to stop early.]")
        for _ in range(3):
            game.run_turn()
    except KeyboardInterrupt:
        print("\n\nGame interrupted by user. Exiting.")
    finally:
        game.display_game_state()
        print("\n*** GAME ENDED ***")

