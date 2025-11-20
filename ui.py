"""
Napoleon's Campaign - UI Module

Handles all user interface and display logic.
"""

import os
from typing import Dict, List, Any


def clear_screen() -> None:
    """Clear the terminal screen."""
    os.system("clear" if os.name == "posix" else "cls")


def show_main_menu() -> int:
    """Display the main menu and get user choice."""
    print("\n" + "=" * 50)
    print("         NAPOLEON'S CAMPAIGN")
    print("=" * 50)
    print("1. Start New Campaign")
    print("2. Load Saved Game")
    print("3. View Instructions")
    print("4. Exit Game")
    print("=" * 50)

    while True:
        try:
            choice = int(input("\nEnter your choice (1-4): "))
            if 1 <= choice <= 4:
                return choice
            else:
                print("Please enter a number between 1 and 4.")
        except ValueError:
            print("Please enter a valid number.")


def show_status(game_state: Dict[str, Any]) -> None:
    """Display the current game status."""
    player = game_state["player"]

    print(f"\n{'=' * 60}")
    print(f"Year: {game_state['year']} | Season: {game_state['season'].title()}")
    print(f"Emperor: {player['name']}")
    print(
        f"Troops: {player['troops']:,} | Gold: {player['gold']:,} | Morale: {player['morale']}/100"
    )
    print(
        f"Territories: {len(player['territories'])} | Allies: {len(player['allies'])} | Enemies: {len(player['enemies'])}"
    )
    print(f"Turn: {game_state['turn_count']}")
    print(f"{'=' * 60}")


def show_event(event: Dict[str, Any]) -> None:
    """Display a historical event."""
    print(f"\n{'=' * 60}")
    print(f"HISTORICAL EVENT - {event['year']}")
    print(f"{event['title'].upper()}")
    print(f"{'=' * 60}")
    print(f"\n{event['description']}\n")

    print("Your choices:")
    for i, choice in enumerate(event["choices"], 1):
        print(f"{i}. {choice['text']}")

    print(f"{'=' * 60}")


def get_player_choice(event: Dict[str, Any]) -> int:
    """Get the player's choice for an event."""
    num_choices = len(event["choices"])

    while True:
        try:
            choice = int(input(f"\nEnter your choice (1-{num_choices}): "))
            if 1 <= choice <= num_choices:
                return choice - 1  # Convert to 0-based index
            else:
                print(f"Please enter a number between 1 and {num_choices}.")
        except ValueError:
            print("Please enter a valid number.")


def show_game_over(game_state: Dict[str, Any]) -> None:
    """Display the game over screen."""
    print(f"\n{'=' * 60}")
    print("GAME OVER")
    print(f"{'=' * 60}")

    if game_state.get("victory_condition"):
        print(f"\n🎉 VICTORY ACHIEVED: {game_state['victory_condition'].upper()} 🎉")
        print("\nYour leadership has shaped the destiny of Europe!")
    else:
        print("\n💔 DEFEAT 💔")
        print("\nThe empire has fallen. Your legacy will be debated for centuries.")

    print(f"\nFinal Statistics:")
    player = game_state["player"]
    print(f"- Troops: {player['troops']:,}")
    print(f"- Gold: {player['gold']:,}")
    print(f"- Morale: {player['morale']}/100")
    print(f"- Territories: {len(player['territories'])}")
    print(f"- Allies: {len(player['allies'])}")
    print(f"- Enemies: {len(player['enemies'])}")
    print(f"- Years in Power: {game_state['year'] - 1796}")
    print(f"- Historical Accuracy: {game_state['historical_accuracy']}%")

    print(f"\n{'=' * 60}")


def show_instructions() -> None:
    """Display detailed game instructions."""
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

    print("VICTORY CONDITIONS:")
    print("- Military: Control most of Europe")
    print("- Diplomatic: Form lasting alliances")
    print("- Historical: Follow Napoleon's actual path\n")

    print("DEFEAT CONDITIONS:")
    print("- Troops below 5,000")
    print("- Gold below 0")
    print("- Morale below 20")
    print("- Lose France\n")

    print("CONTROLS:")
    print("- Use number keys (1-4) to select options")
    print("- Type 'save' to save your progress")
    print("- Follow on-screen prompts\n")

    print("STRATEGY TIPS:")
    print("- Balance military expansion with economic stability")
    print("- High morale improves battle performance")
    print("- Allies provide diplomatic and military bonuses")
    print("- Historical accuracy unlocks special achievements\n")


def show_battle_result(
    attacker: str, defender: str, result: str, casualties: int
) -> None:
    """Display battle results."""
    print(f"\n{'=' * 40}")
    print(f"BATTLE RESULT")
    print(f"{'=' * 40}")
    print(f"{attacker} vs {defender}")
    print(f"Outcome: {result}")
    print(f"Casualties: {casualties:,}")
    print(f"{'=' * 40}\n")


def show_diplomacy_result(nation: str, result: str, gold_change: int = 0) -> None:
    """Display diplomacy results."""
    print(f"\n{'=' * 40}")
    print(f"DIPLOMACY RESULT")
    print(f"{'=' * 40}")
    print(f"Nation: {nation}")
    print(f"Result: {result}")
    if gold_change != 0:
        print(f"Gold Change: {'+' if gold_change > 0 else ''}{gold_change:,}")
    print(f"{'=' * 40}\n")


def show_resource_change(changes: Dict[str, int]) -> None:
    """Display resource changes after an event."""
    print("\nResource Changes:")
    for resource, change in changes.items():
        if change != 0:
            sign = "+" if change > 0 else ""
            print(f"  {resource.title()}: {sign}{change:,}")


def show_territories(territories: List[str]) -> None:
    """Display controlled territories."""
    if territories:
        print(f"\nControlled Territories ({len(territories)}):")
        for territory in territories:
            print(f"  • {territory}")
    else:
        print("\nNo territories controlled.")


def show_allies_and_enemies(allies: List[str], enemies: List[str]) -> None:
    """Display current diplomatic status."""
    if allies:
        print(f"\nAllies ({len(allies)}):")
        for ally in allies:
            print(f"  ✓ {ally}")

    if enemies:
        print(f"\nEnemies ({len(enemies)}):")
        for enemy in enemies:
            print(f"  ✗ {enemy}")


def show_historical_note(event_id: str) -> None:
    """Display educational historical notes."""
    notes = {
        "italian_campaign_1796": "Napoleon's first major victory established his reputation as a military genius.",
        "austerlitz_campaign_1805": "Considered Napoleon's masterpiece, this battle destroyed the Third Coalition.",
        "russian_campaign_1812": "The disastrous invasion led to the collapse of the Grande Armée.",
        "waterloo_1815": "The final defeat ended Napoleon's Hundred Days and his imperial ambitions.",
    }

    if event_id in notes:
        print(f"\n📚 Historical Note: {notes[event_id]}")


def show_loading_message(message: str = "Loading...") -> None:
    """Display a loading message."""
    print(f"\n{message}")


def show_error_message(message: str) -> None:
    """Display an error message."""
    print(f"\n❌ Error: {message}")


def show_success_message(message: str) -> None:
    """Display a success message."""
    print(f"\n✅ {message}")


def confirm_action(message: str) -> bool:
    """Get user confirmation for an action."""
    while True:
        response = input(f"\n{message} (y/n): ").lower()
        if response in ["y", "yes"]:
            return True
        elif response in ["n", "no"]:
            return False
        else:
            print("Please enter 'y' or 'n'.")
