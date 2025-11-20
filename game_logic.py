"""
Napoleon's Campaign - Game Logic Module

Contains core game mechanics, battle calculations, and state management.
"""

import random
from typing import Dict, List, Any, Optional
from data import get_event, get_victory_conditions, get_defeat_conditions, get_random_events, get_trait, get_general, get_artifact
from llm_client import LLMClient


def initialize_game(game_state: Dict[str, Any]) -> Dict[str, Any]:
    """Initialize a new game."""
    # Initialize LLM client
    if 'llm_client' not in game_state:
        game_state['llm_client'] = LLMClient()
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
        elif resource == "add_trait":
            trait_id = change
            if trait_id not in player.get("traits", []):
                player.setdefault("traits", []).append(trait_id)
        elif resource == "add_general":
            general_id = change
            if general_id not in player.get("generals", []):
                player.setdefault("generals", []).append(general_id)
        elif resource == "add_artifact":
            artifact_id = change
            if artifact_id not in player.get("artifacts", []):
                player.setdefault("artifacts", []).append(artifact_id)

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

    # Check if we should trigger a random event
    # Only trigger if we have a next historical event (don't interrupt end game)
    # and current event wasn't already a random one (prevent loops)
    if next_event_id and current_event.get("type") != "random":
        if random.random() < 0.3:  # 30% chance
            random_event = get_random_event(game_state)
            if random_event:
                # Store the actual next historical event to return to later
                # For simplicity in this linear structure, we might just insert it
                # But wait, our system relies on next_event_id from the *current* event choices usually.
                # If we insert a random event, that random event needs to know where to go next.
                # We can hack this by setting the random event's "next_event" to the calculated next_event_id
                
                # Deep copy to avoid modifying global data
                import copy
                event_copy = copy.deepcopy(random_event)
                
                # All choices in random event should lead to the original next historical event
                for choice in event_copy["choices"]:
                    if "consequences" not in choice:
                        choice["consequences"] = {}
                    choice["consequences"]["next_event"] = next_event_id
                
                game_state["current_event"] = event_copy
                return game_state

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


def get_random_event(game_state: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Get a random event, generated by LLM."""
    llm_client = game_state.get('llm_client')
    if not llm_client:
        llm_client = LLMClient()
        game_state['llm_client'] = llm_client
    
    # Create event trigger metadata
    event_trigger = {
        "id": f"random_{game_state['year']}_{game_state['turn_count']}",
        "type": "random",
        "year": game_state['year']
    }
    
    try:
        return llm_client.generate_event(game_state, event_trigger)
    except Exception as e:
        # Fallback to predefined random events if LLM fails
        print(f"LLM generation failed: {e}. Using fallback event.")
        events = get_random_events()
        if events:
            import random
            event_id = random.choice(list(events.keys()))
            return events[event_id]
        return None


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
    
    # Apply traits to maintenance
    for trait_id in player.get("traits", []):
        trait = get_trait(trait_id)
        if trait.get("effect_type") == "maintenance_reduction":
            maintenance_cost = int(maintenance_cost * (1 - trait["value"]))
        elif trait.get("effect_type") == "income_bonus":
            player["gold"] += trait["value"]
            
    # Apply generals to maintenance
    for general_id in player.get("generals", []):
        general = get_general(general_id)
        if general.get("status") == "active" and general.get("effect_type") == "logistics_bonus":
            maintenance_cost = int(maintenance_cost * (1 - general["value"]))

    # Apply artifacts to income
    for artifact_id in player.get("artifacts", []):
        artifact = get_artifact(artifact_id)
        if artifact.get("effect_type") == "income_bonus":
            player["gold"] += artifact["value"]

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
    player_traits: List[str] = None,
    player_generals: List[str] = None,
) -> Dict[str, Any]:
    """Resolve a battle between two forces."""
    if player_traits is None:
        player_traits = []
    if player_generals is None:
        player_generals = []

    # Calculate modifiers from traits
    attacker_modifier = 1.0
    casualty_modifier = 1.0
    
    for trait_id in player_traits:
        trait = get_trait(trait_id)
        if trait.get("effect_type") == "battle_bonus":
            attacker_modifier += trait["value"]
        elif trait.get("effect_type") == "battle_modifier":
            attacker_modifier += trait.get("strength_bonus", 0)
            casualty_modifier += trait.get("casualty_penalty", 0)
            
    # Calculate modifiers from generals
    active_generals = []
    for general_id in player_generals:
        general = get_general(general_id)
        if general.get("status") == "active":
            active_generals.append(general_id)
            if general.get("effect_type") in ["battle_bonus", "cavalry_bonus"]:
                attacker_modifier += general["value"]
            elif general.get("effect_type") == "defense_bonus":
                # If player is attacking, defense bonus might count less or not at all?
                # For simplicity, let's say it counts half when attacking
                attacker_modifier += general["value"] * 0.5

    # Simple battle calculation
    attacker_strength = (
        attacker_troops * (attacker_morale / 100) * (1 + random.uniform(-0.2, 0.2)) * attacker_modifier
    )
    defender_strength = (
        defender_troops
        * (defender_morale / 100)
        * (1 + random.uniform(-0.2, 0.2))
        * (1 + terrain_bonus)
    )

    if attacker_strength > defender_strength:
        # Attacker wins
        casualty_rate = random.uniform(0.05, 0.15) * casualty_modifier
        casualties = int(attacker_troops * casualty_rate)
        result = "victory"
    else:
        # Defender wins
        casualty_rate = random.uniform(0.10, 0.25) * casualty_modifier
        casualties = int(attacker_troops * casualty_rate)
        result = "defeat"
        
    # Check for general death/injury
    general_updates = []
    for general_id in active_generals:
        general = get_general(general_id)
        if random.random() < general.get("death_chance", 0):
            # General falls in battle!
            # In a real implementation we'd update the global state, but here we just return info
            # The caller needs to handle this. But wait, resolve_battle returns a dict.
            # We should probably return a list of events/messages.
            general_updates.append(f"{general['name']} has fallen in battle!")
            # We need a way to actually remove them from the player's active list or mark them dead.
            # Since we don't pass the full game_state here, we can't modify it directly easily.
            # But we can return it in the result.

    return {
        "result": result,
        "casualties": casualties,
        "attacker_strength": attacker_strength,
        "defender_strength": defender_strength,
        "general_updates": general_updates
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

    # Trait modifiers (passed via arguments? No, this function is standalone. 
    # We might need to refactor or just ignore traits here for now as it's not called with player state)
    # Actually, let's leave it for now.

    total_chance = (
        base_chance + gold_modifier + morale_modifier + ally_modifier + nation_modifier
    )
    return max(0.1, min(0.9, total_chance))  # Clamp between 10% and 90%
