"""The main game engine. It uses the ResourcePool from resources.py to manage a turn-based strategy game."""

from resources import ResourcePool, gather_resources
import time

class Civilization:
    """Represents a player's civilization."""
    def __init__(self, name: str, starting_resources: ResourcePool):
        self.name = name
        self.resources = starting_resources
        self.population = 10
        self.military_strength = 5
        self.is_defeated = False

    def display_status(self) -> None:
        """Prints the current status of the civilization."""
        print("\n" + "="*40)
        print(f"    Civilization Status: {self.name.upper()}")
        print("="*40)
        print(f"Population: {self.population}")
        print(f"Military Strength: {self.military_strength}")
        self.resources.display()
        print("="*40)

    def develop(self) -> bool:
        """Action: Develop technology/infrastructure, costing resources."""
        COST_FOOD = 10
        COST_WOOD = 5
        COST_GOLD = 15
        
        if self.resources.spend(COST_FOOD, COST_WOOD, COST_GOLD):
            self.population += 2
            self.military_strength += 3
            print(f"[{self.name}] SUCCESSFULLY developed new infrastructure! Pop increased, Military boosted.")
            return True
        else:
            print(f"[{self.name}] Cannot develop: Insufficient resources.")
            return False

    def attack(self, target: 'Civilization') -> bool:
        """Action: Attack another civilization."""
        print(f"\n[{self.name}] is preparing to engage {target.name}...")
        
        # Combat logic: Uses a combination of military strength and population scaling.
        attack_modifier = 1 + (self.population // 10)
        combat_strength = self.military_strength * attack_modifier
        
        target_defense = target.military_strength * 0.8 + (target.population // 10)
        
        print(f"  -> {self.name} Combat Power: {combat_strength:.0f}")
        print(f"  -> {target.name} Defense: {target_defense:.0f}")

        if combat_strength > target_defense * 1.2:
            # Victory
            print(f"*** VICTORY! {target.name} is defeated! ***")
            target.is_defeated = True
            self.resources.gain(10, 10, 30) # Loot
            self.military_strength += 5
            return True
        elif combat_strength < target_defense * 0.8:
            # Defeat
            print(f"!!! DEFEAT! {self.name} was repelled by {target.name}. Lost morale/soldiers. !!!")
            self.military_strength = max(1, self.military_strength - 4)
            return False
        else:
            # Stalemate/Damage
            print("--- SKIRMISH! Both sides suffer damage. ---")
            self.military_strength = max(1, self.military_strength - 2)
            target.military_strength = max(1, target.military_strength - 2)
            return True


def main_game_loop() -> None:
    """
    Initializes and runs the turn-based strategy game. 
    The game progresses until one civilization is defeated.
    """
    print("***************************************************")
    print("*       ADVANCED TURN-BASED STRATEGY SIM        *")
    print("***************************************************")

    # Setup Resources
    initial_res = ResourcePool(food=100, wood=80, gold=50)
    
    # Setup Civilizations
    civ_A = Civilization("Aethelgard", initial_res.copy())
    civ_B = Civilization("Borealis", initial_res.copy())
    
    # Give a slight advantage to one player for testing:
    civ_B.resources.gain(50, 50, 50)
    civ_B.military_strength += 2

    current_turn = 1
    
    while not (civ_A.is_defeated or civ_B.is_defeated):
        print("\n" + "#"*60)
        print(f"== TURNING ON: TURN {current_turn} ==")
        print("#"*60)
        
        # --- Resource Gathering Phase ---
        print("\n--- 1. RESOURCE GATHERING PHASE ---")
        gather_resources(civ_A)
        gather_resources(civ_B)

        # --- Action Phase ---
        print("\n--- 2. ACTION PHASE (CIV A) ---")
        # Example Turn Action for Civ A: Attempt to develop, then attack B
        civ_A.display_status()
        civ_A.develop()
        civ_A.attack(civ_B)

        print("\n--- 3. ACTION PHASE (CIV B) ---")
        # Example Turn Action for Civ B