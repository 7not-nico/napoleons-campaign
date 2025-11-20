"""
Napoleon's Campaign - Game Logic Module

Contains core game mechanics, battle calculations, and state management.
"""

import random
from typing import Dict, List, Any, Optional
from data import get_event, get_victory_conditions, get_defeat_conditions


def initialize_game(game_state: Dict[str, Any]) -> Dict[str, Any]:
    """Initialize a new game with starting conditions."""
    # Game is already initialized in data.py
    return game_state


def process_turn(game_state: Dict[str, Any], choice: Optional[int]) -> Dict[str, Any]:
    """Process a game turn based on player choice."""
    if choice is None:
        # Advance to next event if no choice needed
        game_state = advance_to_next_event(game_state)
    else:
        # Process the player's choice
        game_state = apply_choice_consequences(game_state, choice)

        # Advance to next event
        game_state = advance_to_next_event(game_state)

    # Update turn counter
    game_state["turn_count"] += 1

    # Apply seasonal effects
    game_state = apply_seasonal_effects(game_state)

    # Generate income
    game_state = generate_income(game_state)

    return game_state


def apply_choice_consequences(
    game_state: Dict[str, Any], choice_index: int
) -> Dict[str, Any]:
    """Apply the consequences of a player's choice."""
    current_event = game_state["current_event"]
    if not current_event or "choices" not in current_event:
        return game_state

    if choice_index >= len(current_event["choices"]):
        return game_state

    choice = current_event["choices"][choice_index]
    consequences = choice.get("consequences", {})

    player = game_state["player"]

    # Apply resource changes
    for resource, change in consequences.items():
        if resource == "troops":
            player["troops"] = max(0, player["troops"] + change)
        elif resource == "gold":
            player["gold"] = max(-10000, player["gold"] + change)  # Allow some debt
        elif resource == "morale":
            player["morale"] = max(0, min(100, player["morale"] + change))
        elif resource == "territories":
            if isinstance(change, list):
                for territory in change:
                    if territory not in player["territories"]:
                        player["territories"].append(territory)
        elif resource == "allies":
            if isinstance(change, list):
                for ally in change:
                    if ally not in player["allies"]:
                        player["allies"].append(ally)
                    # Remove from enemies if present
                    if ally in player["enemies"]:
                        player["enemies"].remove(ally)
        elif resource == "enemies":
            if isinstance(change, list):
                for enemy in change:
                    if enemy not in player["enemies"]:
                        player["enemies"].append(enemy)
                    # Remove from allies if present
                    if enemy in player["allies"]:
                        player["allies"].remove(enemy)
        elif resource == "next_event":
            # Will be handled by advance_to_next_event
            pass

    return game_state


def advance_to_next_event(game_state: Dict[str, Any]) -> Dict[str, Any]:
    """Advance to the next historical event."""
    current_event = game_state["current_event"]

    if not current_event:
        # Start with first event
        game_state["current_event"] = get_event("italian_campaign_1796")
        return game_state

    # Get next event from current event's consequences
    next_event_id = None

    # Check if current event has choices and find the selected choice
    if "choices" in current_event and len(current_event["choices"]) > 0:
        # This assumes the choice has already been processed
        # For now, we'll use a simple progression
        next_event_id = get_next_event_id(current_event["id"])

    if next_event_id:
        next_event = get_event(next_event_id)
        if next_event:
            game_state["current_event"] = next_event
            # Update year based on event
            if "year" in next_event:
                game_state["year"] = next_event["year"]
        else:
            game_state["current_event"] = None
    else:
        game_state["current_event"] = None

    return game_state


def get_next_event_id(current_event_id: str) -> Optional[str]:
    """Get the next event ID in the campaign sequence."""
    # Simple linear progression for now
    event_sequence = [
        "italian_campaign_1796",
        "austrian_counterattack_1796",
        "austrian_invasion_1796",
        "italian_alliance_1796",
        "castiglione_victory_1796",
        "arcole_bridge_1796",
        "mantua_siege_1796",
        "peace_negotiations_1797",
        "continued_war_1797",
        "egypt_campaign_1798",
        "battle_of_the_nile_1798",
        "siege_of_acre_1799",
        "return_to_france_1799",
        "coup_of_18_brumaire_1799",
        "consul_reforms_1800",
        "marengo_campaign_1800",
        "luneville_peace_1801",
        "concordat_with_church_1801",
        "amien_peace_1802",
        "crown_emperor_1804",
        "austerlitz_campaign_1805",
        "pressburg_peace_1805",
        "jena_auerstadt_1806",
        "berlin_decree_1806",
        "friedland_peace_1807",
        "peninsular_war_1808",
        "wagram_campaign_1809",
        "schonbrunn_peace_1809",
        "russian_campaign_1812",
        "retreat_from_moscow_1812",
        "leipzig_campaign_1813",
        "abdication_1814",
        "hundred_days_1815",
        "waterloo_1815",
        "final_exile_1815",
    ]

    try:
        current_index = event_sequence.index(current_event_id)
        if current_index + 1 < len(event_sequence):
            return event_sequence[current_index + 1]
    except ValueError:
        pass

    return None


def apply_seasonal_effects(game_state: Dict[str, Any]) -> Dict[str, Any]:
    """Apply seasonal effects on resources."""
    season = game_state["season"]
    player = game_state["player"]

    if season == "winter":
        # Winter penalties
        player["morale"] = max(0, player["morale"] - 5)
        # Higher maintenance costs
        maintenance_cost = len(player["territories"]) * 200
        player["gold"] = max(-10000, player["gold"] - maintenance_cost)

    elif season == "spring":
        # Spring bonuses
        player["morale"] = min(100, player["morale"] + 2)

    elif season == "summer":
        # Summer bonuses for campaigning
        pass

    elif season == "autumn":
        # Autumn harvest bonuses
        harvest_bonus = len(player["territories"]) * 100
        player["gold"] += harvest_bonus

    # Advance season
    seasons = ["spring", "summer", "autumn", "winter"]
    current_season_index = seasons.index(season)
    game_state["season"] = seasons[(current_season_index + 1) % 4]

    return game_state


def generate_income(game_state: Dict[str, Any]) -> Dict[str, Any]:
    """Generate income from territories and other sources."""
    player = game_state["player"]

    # Base income from territories
    territory_income = len(player["territories"]) * 500
    player["gold"] += territory_income

    # Ally bonuses
    ally_bonus = len(player["allies"]) * 200
    player["gold"] += ally_bonus

    # Troop maintenance costs
    maintenance_cost = (player["troops"] // 1000) * 100
    player["gold"] -= maintenance_cost

    return game_state


def check_game_over(game_state: Dict[str, Any]) -> Dict[str, Any]:
    """Check if the game should end."""
    player = game_state["player"]
    defeat_conditions = get_defeat_conditions()

    # Check defeat conditions
    if player["troops"] < defeat_conditions["military_defeat"]["threshold"]:
        game_state["game_over"] = True
        game_state["victory_condition"] = None
        return game_state

    if player["gold"] < defeat_conditions["economic_defeat"]["threshold"]:
        game_state["game_over"] = True
        game_state["victory_condition"] = None
        return game_state

    if player["morale"] < defeat_conditions["political_defeat"]["threshold"]:
        game_state["game_over"] = True
        game_state["victory_condition"] = None
        return game_state

    if "France" not in player["territories"]:
        game_state["game_over"] = True
        game_state["victory_condition"] = None
        return game_state

    # Check victory conditions
    victory_conditions = get_victory_conditions()

    # Military victory
    if (
        len(player["territories"])
        >= victory_conditions["military_victory"]["requirements"]["territories_count"]
        and player["morale"]
        >= victory_conditions["military_victory"]["requirements"]["morale"]
    ):
        game_state["game_over"] = True
        game_state["victory_condition"] = "Military Victory"
        return game_state

    # Diplomatic victory
    if (
        len(player["allies"])
        >= victory_conditions["diplomatic_victory"]["requirements"]["allies_count"]
    ):
        game_state["game_over"] = True
        game_state["victory_condition"] = "Diplomatic Victory"
        return game_state

    # Historical victory (simplified)
    if (
        game_state["year"] >= 1815
        and game_state["historical_accuracy"]
        >= victory_conditions["historical_victory"]["requirements"][
            "historical_accuracy"
        ]
    ):
        game_state["game_over"] = True
        game_state["victory_condition"] = "Historical Victory"
        return game_state

    return game_state


def resolve_battle(
    attacker_troops: int,
    defender_troops: int,
    attacker_morale: int = 100,
    defender_morale: int = 100,
    terrain_bonus: int = 0,
) -> Dict[str, Any]:
    """Resolve a battle between two forces."""
    # Simple battle calculation
    attacker_strength = (
        attacker_troops * (attacker_morale / 100) * (1 + random.uniform(-0.2, 0.2))
    )
    defender_strength = (
        defender_troops
        * (defender_morale / 100)
        * (1 + random.uniform(-0.2, 0.2))
        * (1 + terrain_bonus)
    )

    if attacker_strength > defender_strength:
        # Attacker wins
        casualty_rate = random.uniform(0.05, 0.15)
        casualties = int(attacker_troops * casualty_rate)
        result = "victory"
    else:
        # Defender wins
        casualty_rate = random.uniform(0.10, 0.25)
        casualties = int(attacker_troops * casualty_rate)
        result = "defeat"

    return {
        "result": result,
        "casualties": casualties,
        "attacker_strength": attacker_strength,
        "defender_strength": defender_strength,
    }


def calculate_diplomacy_success(
    target_nation: str, current_gold: int, current_morale: int, allies_count: int
) -> float:
    """Calculate success chance for diplomatic actions."""
    base_chance = 0.5

    # Gold influence
    gold_modifier = min(0.3, current_gold / 50000)  # Max 30% bonus

    # Morale influence
    morale_modifier = (current_morale - 50) / 100  # -0.5 to +0.5

    # Allies influence
    ally_modifier = allies_count * 0.05  # 5% per ally

    # Nation-specific modifiers
    nation_modifiers = {
        "Austria": -0.2,  # Historical rival
        "Britain": -0.3,  # Major enemy
        "Russia": -0.1,  # Distant power
        "Prussia": -0.1,  # Potential ally
        "Spain": 0.1,  # Natural ally
        "Kingdom of Sardinia": 0.2,  # Small, easy to influence
    }

    nation_modifier = nation_modifiers.get(target_nation, 0)

    total_chance = (
        base_chance + gold_modifier + morale_modifier + ally_modifier + nation_modifier
    )
    return max(0.1, min(0.9, total_chance))  # Clamp between 10% and 90%
