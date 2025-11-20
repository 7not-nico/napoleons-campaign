#!/usr/bin/env python3
"""
Napoleon's Campaign - Test Script

Tests the game functionality without user interaction.
"""

from data import get_initial_game_state, get_event
from game_logic import process_turn, check_game_over
from ui import show_status


def test_basic_gameplay():
    """Test basic game functionality."""
    print("=== NAPOLEON'S CAMPAIGN - TEST ===\n")

    # Initialize game
    game_state = get_initial_game_state()
    print("✅ Game initialized successfully")

    # Show initial status
    print("\n--- Initial Game State ---")
    show_status(game_state)

    # Test first event
    current_event = game_state["current_event"]
    if current_event:
        print(f"\n✅ First event loaded: {current_event['title']}")
        print(f"Year: {current_event['year']}")
        print(f"Choices available: {len(current_event['choices'])}")

        # Simulate making a choice (choice 0 = first option)
        print("\n--- Processing first choice ---")
        game_state = process_turn(game_state, 0)
        print("✅ Choice processed successfully")

        # Show updated status
        print("\n--- Updated Game State ---")
        show_status(game_state)

    # Test game over conditions
    game_state = check_game_over(game_state)
    if not game_state["game_over"]:
        print("\n✅ Game continues (not over)")
    else:
        print(f"\n✅ Game ended: {game_state.get('victory_condition', 'Defeat')}")

    print("\n=== TEST COMPLETED SUCCESSFULLY ===")


if __name__ == "__main__":
    test_basic_gameplay()
