"""
Entry point for the Elias game.
This module initializes and starts the game.
"""

import sys
import pygame
from aliace_game.game import EliasGame

def main():
    """Main function to run the game."""
    # Check if user wants to start in management mode
    if len(sys.argv) > 1 and sys.argv[1] == "--manage":
        # For now, we'll just note this in the documentation
        # In a full implementation, we would pass a parameter to the game
        print("To access word management, modify the code to set initial screen to SCREEN_MANAGE")
        return
        
    # Create and run the game
    game = EliasGame()
    game.run()

if __name__ == "__main__":
    main()