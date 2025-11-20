#!/usr/bin/env python3
"""
Napoleon's Campaign - A CLI Strategy Game

A text-based strategy game where you play as Napoleon Bonaparte,
making historical decisions that shape the fate of Europe.
"""

import sys
import os
from game_logic import initialize_game, process_turn, check_game_over
from ui import (
    show_main_menu,
    show_status,
    show_event,
    get_player_choice,
    show_game_over,
)
from data import get_initial_game_state
from utils import clear_screen, save_game, load_game, validate_choice


def main():
    """Main game entry point and loop."""
    clear_screen()
    print("=== NAPOLEON'S CAMPAIGN ===")
    print("A historical strategy game\n")

    game_state = None

    while True:
        choice = show_main_menu()

        if choice == 1:  # Start New Campaign
            game_state = get_initial_game_state()
            run_game_loop(game_state)

        elif choice == 2:  # Load Saved Game
            game_state = load_game()
            if game_state:
                run_game_loop(game_state)
            else:
                print("No saved game found.")

        elif choice == 3:  # View Instructions
            show_instructions()

        elif choice == 4:  # Exit
            print("Thank you for playing Napoleon's Campaign!")
            sys.exit(0)

        input("\nPress Enter to continue...")


def run_game_loop(game_state):
    """Main game loop handling turns and events."""
    while not game_state["game_over"]:
        clear_screen()

        # Show current game status
        show_status(game_state)

        # Process current event
        current_event = game_state["current_event"]
        if current_event:
            show_event(current_event)

            # Get player choice
            choice = get_player_choice(current_event)

            # Process the choice and update game state
            game_state = process_turn(game_state, choice)

            # Check for game over conditions
            game_state = check_game_over(game_state)

        # If no current event, advance to next one
        else:
            game_state = process_turn(game_state, None)

        # Allow saving at any time
        if (
            input("\nType 'save' to save game, or press Enter to continue: ").lower()
            == "save"
        ):
            save_game(game_state)
            print("Game saved!")

    # Game over screen
    show_game_over(game_state)


def show_instructions():
    """Display game instructions."""
    clear_screen()
    print("=== NAPOLEON'S CAMPAIGN - INSTRUCTIONS ===\n")

    print("OVERVIEW:")
    print("You are Napoleon Bonaparte, commanding France through")
    print("the turbulent years of the French Revolution and Napoleonic Wars.\n")

    print("GAMEPLAY:")
    print("- Make strategic decisions at key historical moments")
    print("- Manage your troops, gold, morale, and territories")
    print("- Fight battles and form diplomatic alliances")
    print("- Your choices determine the fate of Europe\n")

    print("RESOURCES:")
    print("- TROOPS: Military strength for battles")
    print("- GOLD: Economic power and army maintenance")
    print("- MORALE: Public support and army effectiveness")
    print("- TERRITORIES: Land control and resource generation\n")

    print("CONTROLS:")
    print("- Use number keys (1-4) to select options")
    print("- Type 'save' to save your progress")
    print("- Follow on-screen prompts\n")

    print("OBJECTIVE:")
    print("Lead France to victory through military conquest,")
    print("diplomatic alliances, or historical accuracy.\n")


if __name__ == "__main__":
    main()
