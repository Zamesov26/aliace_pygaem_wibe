"""
Entry point for the Elias game.
This module initializes and starts the game.
"""

from aliace_game.game import EliasGame

if __name__ == "__main__":
    # Create and run the game
    game = EliasGame()
    game.run()