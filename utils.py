"""
Napoleon's Campaign - Utils Module

Contains utility functions, input validation, and helper methods.
"""

import json
import os
from typing import Dict, Any, Optional, Callable


def clear_screen() -> None:
    """Clear the terminal screen."""
    os.system("clear" if os.name == "posix" else "cls")


def validate_choice(choice: int, min_val: int, max_val: int) -> bool:
    """Validate that a choice is within the acceptable range."""
    return min_val <= choice <= max_val


def get_user_input(
    prompt: str, input_type: type = str, validator: Optional[Callable] = None
) -> Any:
    """Get user input with optional validation."""
    while True:
        try:
            user_input = input(prompt)
            if input_type == int:
                user_input = int(user_input)
            elif input_type == float:
                user_input = float(user_input)

            if validator and not validator(user_input):
                print("Invalid input. Please try again.")
                continue

            return user_input
        except (ValueError, TypeError):
            print(f"Please enter a valid {input_type.__name__}.")


def save_game(game_state: Dict[str, Any], filename: str = "napoleon_save.json") -> bool:
    """Save the current game state to a file."""
    try:
        with open(filename, "w") as f:
            json.dump(game_state, f, indent=2)
        return True
    except Exception as e:
        print(f"Error saving game: {e}")
        return False


def load_game(filename: str = "napoleon_save.json") -> Optional[Dict[str, Any]]:
    """Load a saved game state from a file."""
    try:
        if not os.path.exists(filename):
            return None

        with open(filename, "r") as f:
            game_state = json.load(f)
        return game_state
    except Exception as e:
        print(f"Error loading game: {e}")
        return None


def format_number(number: int) -> str:
    """Format a number with commas for readability."""
    return f"{number:,}"


def calculate_percentage(current: int, maximum: int) -> float:
    """Calculate percentage of current vs maximum."""
    if maximum == 0:
        return 0.0
    return (current / maximum) * 100


def clamp_value(value: int, min_val: int, max_val: int) -> int:
    """Clamp a value between minimum and maximum."""
    return max(min_val, min(max_val, value))


def get_season_name(season: str) -> str:
    """Get the display name for a season."""
    season_names = {
        "spring": "Spring",
        "summer": "Summer",
        "autumn": "Autumn",
        "winter": "Winter",
    }
    return season_names.get(season, season.title())


def calculate_battle_casualties(troops: int, intensity: str = "normal") -> int:
    """Calculate battle casualties based on intensity."""
    if intensity == "major":
        casualty_rate = random.uniform(0.15, 0.30)
    elif intensity == "siege":
        casualty_rate = random.uniform(0.05, 0.15)
    else:  # normal
        casualty_rate = random.uniform(0.08, 0.20)

    return int(troops * casualty_rate)


def generate_random_event() -> Optional[Dict[str, Any]]:
    """Generate a random event (for future expansion)."""
    events = [
        {
            "title": "Plague Outbreak",
            "description": "Disease spreads through your troops.",
            "effects": {"troops": -2000, "morale": -10},
        },
        {
            "title": "Economic Boom",
            "description": "Trade flourishes in your territories.",
            "effects": {"gold": 5000, "morale": 5},
        },
        {
            "title": "Desertion",
            "description": "Some troops desert due to poor conditions.",
            "effects": {"troops": -1000, "morale": -5},
        },
    ]

    # 20% chance of random event
    if random.random() < 0.2:
        return random.choice(events)

    return None


def calculate_historical_accuracy(game_state: Dict[str, Any]) -> int:
    """Calculate how closely the player follows historical events."""
    # Simplified calculation - in a full game this would be more complex
    base_accuracy = 100

    # Penalties for major deviations
    if "Egypt" in game_state["player"]["territories"]:
        base_accuracy -= 10  # Historical Egyptian campaign

    if game_state["year"] > 1815 and game_state["player"]["troops"] > 10000:
        base_accuracy += 20  # Survived to end

    return clamp_value(base_accuracy, 0, 100)


def get_resource_status(troops: int, gold: int, morale: int) -> str:
    """Get a status string for resource levels."""
    status_parts = []

    if troops < 10000:
        status_parts.append("⚠️  Low Troops")
    elif troops > 50000:
        status_parts.append("💪 Strong Army")

    if gold < 0:
        status_parts.append("💸 In Debt")
    elif gold > 50000:
        status_parts.append("💰 Wealthy")

    if morale < 30:
        status_parts.append("😞 Low Morale")
    elif morale > 80:
        status_parts.append("🎉 High Morale")

    if not status_parts:
        status_parts.append("✓ Stable")

    return " | ".join(status_parts)


def format_territory_list(territories: list) -> str:
    """Format a list of territories for display."""
    if not territories:
        return "None"

    if len(territories) <= 3:
        return ", ".join(territories)
    else:
        return f"{', '.join(territories[:3])} (+{len(territories) - 3} more)"


def create_backup_save(game_state: Dict[str, Any]) -> None:
    """Create a backup save file."""
    backup_filename = "napoleon_save_backup.json"
    save_game(game_state, backup_filename)


def validate_game_state(game_state: Dict[str, Any]) -> bool:
    """Validate that a game state has all required fields."""
    required_fields = ["year", "season", "player", "current_event", "game_over"]

    for field in required_fields:
        if field not in game_state:
            return False

    player_required = [
        "name",
        "troops",
        "gold",
        "morale",
        "territories",
        "allies",
        "enemies",
    ]
    for field in player_required:
        if field not in game_state["player"]:
            return False

    return True


def get_game_statistics(game_state: Dict[str, Any]) -> Dict[str, Any]:
    """Calculate and return game statistics."""
    player = game_state["player"]

    return {
        "years_played": game_state["year"] - 1796,
        "territories_controlled": len(player["territories"]),
        "allies_gained": len(player["allies"]),
        "enemies_remaining": len(player["enemies"]),
        "peak_troops": player["troops"],  # Would need tracking
        "total_gold_earned": player["gold"],  # Would need tracking
        "battles_won": 0,  # Would need tracking
        "historical_accuracy": game_state.get("historical_accuracy", 100),
    }


# Import random here to avoid circular imports
import random
