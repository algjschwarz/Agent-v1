"""A script using Object-Oriented Programming (OOP) to simulate a simple predator-prey ecosystem (e.g., rabbits and foxes) over time. Great for demonstrating basic biological modeling."""

# ecosystem_sim.py

import random
from typing import Tuple

class Organism:
    """Base class for living organisms."""
    def __init__(self, population: int, max_growth: float):
        self.population = population
        self.max_growth_rate = max_growth

    def check_survival(self, environment_stress: float = 0.0) -> float:
        """Calculates the natural decline due to environment stress."""
        decline = self.population * (environment_stress / 100.0)
        self.population = max(0, self.population - int(decline))
        return self.population

class Prey(Organism):
    """Represents the food source (e.g., Rabbits)."""
    def __init__(self, population: int):
        # Prey are highly reproductive, so they have a high base growth rate
        super().__init__(population, max_growth=1.5)

    def reproduce(self):
        """Increases population based on current size and inherent growth rate."""
        growth = self.population * self.max_growth_rate * random.uniform(0.9, 1.1)
        self.population = int(self.population + growth)
        print(f"[Prey] Reproduction: Population increased by {int(growth):,}.")

class Predator(Organism):
    """Represents the consumer (e.g., Foxes)."""
    def __init__(self, population: int):
        # Predators have lower reproductive rate but benefit from prey
        super().__init__(population, max_growth=0.8)

    def hunt(self, prey_pop: int, efficiency: float) -> Tuple[int, float]:
        """
        Simulates hunting successful kills.
        Returns (kills, energy_spent).
        """
        # Kills are limited by both predator population and prey availability
        potential_kills = min(self.population * 0.5, int(prey_pop * 0.5))
        actual_kills = int(potential_kills * efficiency)
        
        # Each kill boosts the population slightly (survival benefit)
        self.population += int(actual_kills * 0.05) 
        
        return actual_kills, actual_kills * 1.5

def simulate_cycle(prey: Prey, predator: Predator, cycle: int, stress: float) -> None:
    """Runs one full cycle of the ecosystem simulation."""
    
    print(f"\n--- Cycle {cycle} ---")

    # 1. Environmental Stress & Natural Decline
    prey.check_survival(stress)
    predator.check_survival(stress)

    # 2. Prey Reproduction
    prey.reproduce()

    # 3. Predator Hunting
    kills, energy_spent = predator.hunt(prey.population, efficiency=0.6)
    print(f"[Predator] Successfully hunted {kills:,} prey. Energy spent: {int(energy_spent):,}.")

    # 4. Resource Impact (Prey Loss)
    prey.population = max(0, prey.population - kills)
    
    # 5. Reproduction/Growth based on success
    predator.reproduce()
    
    print(f"Summary: Prey Pop={prey.population:,} | Predator Pop={predator.population:,}")


def run_simulation(cycles: int) -> None:
    """Initializes and runs the simulation for a given number of cycles."""
    print("=================================================")
    print("🦊 ECOLOGICAL ECOSYSTEM SIMULATOR 🐰")
    print("=================================================")
    
    # Initialize starting populations
    rabbits = Prey(population=1000)
    foxes = Predator(population=100)
    
    # Define base environment stress (low = stable, high = disaster)
    environment_stress = 5.0 

    for i in range(1, cycles + 1):
        simulate_cycle(rabbits, foxes, i, environment_stress)
        
        # Simple check to stop simulation if one population collapses entirely
        if rabbits.population == 0 and foxes.population == 0:
            print("\\n[SIMULATION STOPPED] All life extinguished.")
            break
        if rabbits.population == 0 and foxes.population > 0:
            print("\\n[WARNING] No food source remaining. Predators are starving.")
            break
        if foxes.population == 0 and rabbits.population > 0:
            print("\\n[INFO] Predators are absent. Prey population may boom.")


if __name__ == "__main__":
    # Run the simulation for 15 cycles to observe boom/bust cycles
    run_simulation(cycles=15)