"""A module for managing global resources (Food, Wood, Gold) used by the game engine."""


class ResourcePool:
    """Manages basic resources like Food, Wood, and Gold."""
    def __init__(self, initial_food: int = 100, initial_wood: int = 50, initial_gold: int = 20):
        self.food = initial_food
        self.wood = initial_wood
        self.gold = initial_gold

    def spend(self, food: int, wood: int, gold: int) -> bool:
        """Checks and spends resources. Returns True if successful, False otherwise."""
        if food < 0 or wood < 0 or gold < 0:
            print("Error: Cannot spend negative resources.")
            return False
            
        if self.food >= food and self.wood >= wood and self.gold >= gold:
            self.food -= food
            self.wood -= wood
            self.gold -= gold
            print(f"\n[SUCCESS] Resources Spent:")
            print(f"  Food: {food}, Wood: {wood}, Gold: {gold}")
            return True
        else:
            print(f"\n[FAILED] Insufficient resources to spend. Need (F:{food}, W:{wood}, G:{gold})")
            return False

    def gain(self, food: int, wood: int, gold: int):
        """Adds resources to the pool."""
        self.food += food
        self.wood += wood
        self.gold += gold
        print(f"\n[SUCCESS] Resources Gained: Food: {food}, Wood: {wood}, Gold: {gold}")

    def display(self):
        """Displays current resource levels."""
        print("\n=======================================")
        print(f"CURRENT RESOURCES:")
        print(f"  FOOD: {self.food}")
        print(f"  WOOD: {self.wood}")
        print(f"  GOLD: {self.gold}")
        print("=======================================\n")

def gather_resources(pool: ResourcePool, base_size: int) -> tuple[int, int, int]:
    """Simulates gathering resources based on base size."""
    food_gained = base_size * 2
    wood_gained = base_size * 1
    gold_gained = base_size * 0.5
    pool.gain(int(food_gained), int(wood_gained), int(gold_gained))
    return food_gained, wood_gained, int(gold_gained)

