import random
from collections import Counter

# Define the 10 cards: Card 1 is the most common, Card 9 is rare, Card 10 is unique (very rare)
cards = [f"Card {i}" for i in range(1, 11)]

# Define weights for rarity: higher weight = more common. Unique has a very low weight.
# These can be adjusted as needed.
weights = [100, 80, 60, 40, 20, 10, 5, 2, 1, 0.1]  # Sum = 318.1, but random.choices normalizes automatically

def open_card():
    """
    Simulates opening a card pack and returns a randomly selected card based on rarity weights.
    """
    return random.choices(cards, weights=weights)[0]

# Example usage: Open a single card
if __name__ == "__main__":
    print("Opening a single card...")
    result = open_card()
    print(f"You got: {result}")
    
    # To demonstrate distribution, simulate 1000 openings and show frequencies
    openings = 10000
    print(f"\nSimulating {openings} openings to show approximate probabilities:")
    simulations = [open_card() for _ in range(openings)]
    counts = Counter(simulations)
    for card, count in sorted(counts.items()):
        percentage = (count / openings) * 100
        print(f"{card}: {count} times ({percentage:.2f}%)")

    # print(f"Simulations: {simulations}")