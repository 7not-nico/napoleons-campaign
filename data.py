"""
Napoleon's Campaign - Game Data Module

Contains all game data structures, historical events, and initial game state.
"""

from typing import Dict, List, Any
from roguelike_data import TRAITS, RANDOM_EVENTS, GENERALS, ARTIFACTS


def get_initial_game_state() -> Dict[str, Any]:
    """Return the initial game state for a new campaign."""
    return {
        "year": 1796,
        "season": "spring",
        "player": {
            "name": "Napoleon Bonaparte",
            "troops": 50000,
            "gold": 10000,
            "morale": 100,
            "territories": ["France"],
            "allies": [],
            "enemies": ["Austria", "Britain", "Russia", "Prussia"],
            "traits": [],
            "generals": [],
            "artifacts": []  # Unique items found
        },
        "npcs": {},  # NPC instances by ID
        "goals": [],  # Player-defined objectives
        "current_event": get_event("italian_campaign_1796"),
        "game_over": False,
        "victory_condition": None,
        "historical_accuracy": 100,  # Track how closely player follows history
        "turn_count": 0,
    }


def get_event(event_id: str) -> Dict[str, Any]:
    """Get a specific historical event by ID."""
    events = get_all_events()
    return events.get(event_id, {})


def get_all_events() -> Dict[str, str]:
    """Return all historical events in the game."""
    return {
        "italian_campaign_1796": {
            "id": "italian_campaign_1796",
            "year": 1796,
            "title": "The Italian Campaign",
            "description": """The French Directory has appointed you to command the Army of Italy.
The Austrian Empire threatens French borders. You have 50,000 troops under your command.
The Italian peninsula offers rich resources and strategic advantages.

Will you launch an aggressive offensive or proceed cautiously?""",
            "choices": [
                {
                    "text": "Launch aggressive offensive against Austrian forces",
                    "consequences": {
                        "troops": -8000,  # Casualties
                        "gold": 5000,  # War booty
                        "morale": 15,  # Victory boost
                        "territories": ["Northern Italy"],
                        "enemies": [],  # No change
                        "next_event": "austrian_counterattack_1796",
                    },
                },
                {
                    "text": "Build fortifications and wait for reinforcements",
                    "consequences": {
                        "troops": 5000,  # Reinforcements arrive
                        "gold": -2000,  # Fortification costs
                        "morale": -5,  # Perceived as weak
                        "territories": [],
                        "enemies": [],
                        "next_event": "austrian_invasion_1796",
                    },
                },
                {
                    "text": "Negotiate with local Italian states for alliances",
                    "consequences": {
                        "troops": 2000,  # Local recruits
                        "gold": 1000,  # Trade agreements
                        "morale": 5,  # Diplomatic success
                        "territories": [],
                        "allies": ["Kingdom of Sardinia"],
                        "next_event": "italian_alliance_1796",
                    },
                },
            ],
        },
        "austrian_counterattack_1796": {
            "id": "austrian_counterattack_1796",
            "year": 1796,
            "title": "Austrian Counterattack",
            "description": """Your victory at Lodi has opened the path to Milan, but the Austrians
are massing forces for a counterattack. Field Marshal Beaulieu commands
40,000 Austrian troops against your 42,000 French soldiers.

The terrain favors defense, but you could outflank their positions.""",
            "choices": [
                {
                    "text": "Hold defensive positions at the Adda River",
                    "consequences": {
                        "troops": -3000,
                        "gold": 0,
                        "morale": 10,
                        "territories": [],
                        "next_event": "castiglione_victory_1796",
                    },
                },
                {
                    "text": "Launch flanking maneuver around their right",
                    "consequences": {
                        "troops": -5000,
                        "gold": 3000,
                        "morale": 20,
                        "territories": ["Lombardy"],
                        "next_event": "arcole_bridge_1796",
                    },
                },
            ],
        },
        "austrian_invasion_1796": {
            "id": "austrian_invasion_1796",
            "year": 1796,
            "title": "Austrian Invasion",
            "description": """While you waited, the Austrians have invaded northern Italy.
Your defensive positions are strong, but the enemy has numerical superiority.
The Directory demands action - they question your aggressive reputation.""",
            "choices": [
                {
                    "text": "Counterattack immediately despite odds",
                    "consequences": {
                        "troops": -12000,
                        "gold": 0,
                        "morale": -10,
                        "territories": [],
                        "next_event": "defensive_stand_1796",
                    },
                },
                {
                    "text": "Withdraw to stronger defensive positions",
                    "consequences": {
                        "troops": -2000,
                        "gold": -1000,
                        "morale": -15,
                        "territories": [],
                        "next_event": "mantua_siege_1796",
                    },
                },
            ],
        },
        "italian_alliance_1796": {
            "id": "italian_alliance_1796",
            "year": 1796,
            "title": "Italian Alliances",
            "description": """Your diplomatic efforts have paid off. Several Italian states
have agreed to support France in exchange for protection and reforms.
However, Austria still threatens from the north.""",
            "choices": [
                {
                    "text": "March north to confront Austrians",
                    "consequences": {
                        "troops": 3000,
                        "gold": 2000,
                        "morale": 10,
                        "territories": [],
                        "next_event": "austrian_counterattack_1796",
                    },
                },
                {
                    "text": "Consolidate control of allied territories",
                    "consequences": {
                        "troops": 5000,
                        "gold": 4000,
                        "morale": 5,
                        "territories": ["Tuscany", "Modena"],
                        "next_event": "papal_states_1797",
                    },
                },
            ],
        },
        "castiglione_victory_1796": {
            "id": "castiglione_victory_1796",
            "year": 1796,
            "title": "Victory at Castiglione",
            "description": """Your defensive strategy worked perfectly. The Austrians attacked
your prepared positions and suffered heavy casualties. Beaulieu has retreated
north, leaving northern Italy under French control.""",
            "choices": [
                {
                    "text": "Pursue the retreating Austrians",
                    "consequences": {
                        "troops": -2000,
                        "gold": 4000,
                        "morale": 15,
                        "territories": ["Venetia"],
                        "next_event": "peace_negotiations_1797",
                    },
                },
                {
                    "text": "Secure current gains and reorganize",
                    "consequences": {
                        "troops": 1000,
                        "gold": 2000,
                        "morale": 5,
                        "territories": [],
                        "next_event": "mantua_siege_1796",
                    },
                },
            ],
        },
        "arcole_bridge_1796": {
            "id": "arcole_bridge_1796",
            "year": 1796,
            "title": "The Bridge at Arcola",
            "description": """Your flanking maneuver caught the Austrians off guard, but they
have retreated to the strategic Bridge at Arcola. Alvinzi commands their forces
and has fortified the position. The bridge is narrow - only infantry can cross.""",
            "choices": [
                {
                    "text": "Direct assault across the bridge",
                    "consequences": {
                        "troops": -6000,
                        "gold": 0,
                        "morale": -5,
                        "territories": [],
                        "next_event": "rivoli_victory_1797",
                    },
                },
                {
                    "text": "Wait for artillery and attack at night",
                    "consequences": {
                        "troops": -3000,
                        "gold": -1000,
                        "morale": 10,
                        "territories": ["Venetia"],
                        "next_event": "peace_negotiations_1797",
                    },
                },
            ],
        },
        "mantua_siege_1796": {
            "id": "mantua_siege_1796",
            "year": 1796,
            "title": "Siege of Mantua",
            "description": """The fortress of Mantua holds out against your forces. Austrian
garrisons inside are well-supplied, but your army controls the surrounding
countryside. A prolonged siege will cost supplies but weaken the enemy.""",
            "choices": [
                {
                    "text": "Maintain the siege until surrender",
                    "consequences": {
                        "troops": -1000,
                        "gold": -3000,
                        "morale": 5,
                        "territories": ["Mantua"],
                        "next_event": "peace_negotiations_1797",
                    },
                },
                {
                    "text": "Offer generous surrender terms",
                    "consequences": {
                        "troops": 0,
                        "gold": -1000,
                        "morale": -5,
                        "territories": ["Mantua"],
                        "next_event": "peace_negotiations_1797",
                    },
                },
            ],
        },
        "peace_negotiations_1797": {
            "id": "peace_negotiations_1797",
            "year": 1797,
            "title": "Peace of Campo Formio",
            "description": """Austria seeks peace after their defeats. Emperor Francis offers
to cede Belgium and Lombardy to France, and recognize the Cisalpine Republic.
Britain remains at war, but the continent might have peace.""",
            "choices": [
                {
                    "text": "Accept the peace terms",
                    "consequences": {
                        "troops": 5000,
                        "gold": 8000,
                        "morale": 20,
                        "territories": ["Belgium", "Lombardy"],
                        "enemies": ["Austria"],  # Remove Austria from enemies
                        "next_event": "egypt_campaign_1798",
                    },
                },
                {
                    "text": "Demand more concessions",
                    "consequences": {
                        "troops": 0,
                        "gold": 0,
                        "morale": -10,
                        "territories": [],
                        "next_event": "continued_war_1797",
                    },
                },
            ],
        },
        "continued_war_1797": {
            "id": "continued_war_1797",
            "year": 1797,
            "title": "Continued War with Austria",
            "description": """Austria has rejected your demands and fighting continues.
Archduke Charles has taken command and is proving a formidable opponent.
The war drags on with heavy casualties on both sides.""",
            "choices": [
                {
                    "text": "Seek peace on original terms",
                    "consequences": {
                        "troops": -3000,
                        "gold": 3000,
                        "morale": -5,
                        "territories": ["Belgium"],
                        "enemies": ["Austria"],
                        "next_event": "egypt_campaign_1798",
                    },
                },
                {
                    "text": "Continue the offensive",
                    "consequences": {
                        "troops": -8000,
                        "gold": -2000,
                        "morale": 5,
                        "territories": ["Belgium", "Lombardy"],
                        "next_event": "egypt_campaign_1798",
                    },
                },
            ],
        },
        "egypt_campaign_1798": {
            "id": "egypt_campaign_1798",
            "year": 1798,
            "title": "The Egyptian Campaign",
            "description": """The Directory has approved your plan to strike at British trade
routes by invading Egypt. This will disrupt British commerce with India and
establish a French presence in the Middle East. However, it means leaving
Europe undefended.""",
            "choices": [
                {
                    "text": "Launch the Egyptian expedition",
                    "consequences": {
                        "troops": -5000,
                        "gold": -5000,
                        "morale": 10,
                        "territories": ["Egypt"],
                        "next_event": "battle_of_the_nile_1798",
                    },
                },
                {
                    "text": "Focus on European consolidation",
                    "consequences": {
                        "troops": 2000,
                        "gold": 3000,
                        "morale": 5,
                        "territories": [],
                        "next_event": "coup_of_18_brumaire_1799",
                    },
                },
            ],
        },
        "battle_of_the_nile_1798": {
            "id": "battle_of_the_nile_1798",
            "year": 1798,
            "title": "Battle of the Nile",
            "description": """British Admiral Nelson has found your fleet at anchor in Aboukir Bay.
His ships attack at night, catching your navy unprepared. The battle rages
through the night with heavy losses on both sides.""",
            "choices": [
                {
                    "text": "Fight to the last ship",
                    "consequences": {
                        "troops": -2000,
                        "gold": 0,
                        "morale": -15,
                        "territories": [],
                        "next_event": "siege_of_acre_1799",
                    },
                },
                {
                    "text": "Abandon the fleet and save the army",
                    "consequences": {
                        "troops": -1000,
                        "gold": -2000,
                        "morale": -10,
                        "territories": ["Egypt"],
                        "next_event": "siege_of_acre_1799",
                    },
                },
            ],
        },
        "siege_of_acre_1799": {
            "id": "siege_of_acre_1799",
            "year": 1799,
            "title": "Siege of Acre",
            "description": """Your army marches north to confront Ottoman forces at Acre.
The fortress is strongly defended by British and Turkish troops under
Sir Sidney Smith. Your artillery has been delayed by desert conditions.""",
            "choices": [
                {
                    "text": "Press the siege despite difficulties",
                    "consequences": {
                        "troops": -4000,
                        "gold": -3000,
                        "morale": -10,
                        "territories": [],
                        "next_event": "return_to_france_1799",
                    },
                },
                {
                    "text": "Withdraw back to Egypt",
                    "consequences": {
                        "troops": -1000,
                        "gold": -1000,
                        "morale": -5,
                        "territories": ["Egypt"],
                        "next_event": "return_to_france_1799",
                    },
                },
            ],
        },
        "return_to_france_1799": {
            "id": "return_to_france_1799",
            "year": 1799,
            "title": "Return to France",
            "description": """News reaches you of political chaos in France. The Directory
is unpopular and ineffective. Royalist uprisings threaten the Republic.
Your presence in France could be crucial for its survival.""",
            "choices": [
                {
                    "text": "Return immediately to France",
                    "consequences": {
                        "troops": 10000,
                        "gold": 0,
                        "morale": 15,
                        "territories": [],
                        "next_event": "coup_of_18_brumaire_1799",
                    },
                },
                {
                    "text": "Complete objectives in Egypt first",
                    "consequences": {
                        "troops": -2000,
                        "gold": -1000,
                        "morale": -10,
                        "territories": [],
                        "next_event": "coup_of_18_brumaire_1799",
                    },
                },
            ],
        },
        "coup_of_18_brumaire_1799": {
            "id": "coup_of_18_brumaire_1799",
            "year": 1799,
            "title": "Coup of 18 Brumaire",
            "description": """The Directory has lost all credibility. With military support
and political allies, you can seize power. The alternative is continued
chaos that could lead to royalist restoration or Jacobin terror.""",
            "choices": [
                {
                    "text": "Seize power as First Consul",
                    "consequences": {
                        "troops": 0,
                        "gold": 5000,
                        "morale": 25,
                        "territories": [],
                        "next_event": "consul_reforms_1800",
                    },
                },
                {
                    "text": "Support establishment of a triumvirate",
                    "consequences": {
                        "troops": 0,
                        "gold": 2000,
                        "morale": 5,
                        "territories": [],
                        "next_event": "consul_reforms_1800",
                    },
                },
                {
                    "text": "Allow elections to proceed",
                    "consequences": {
                        "troops": 0,
                        "gold": 0,
                        "morale": -20,
                        "territories": [],
                        "next_event": "political_chaos_1800",
                    },
                },
            ],
        },
        "consul_reforms_1800": {
            "id": "consul_reforms_1800",
            "year": 1800,
            "title": "Consular Reforms",
            "description": """As First Consul, you have broad powers to reform France.
The economy is in shambles, the military needs reorganization,
and political stability must be restored.""",
            "choices": [
                {
                    "text": "Focus on military reorganization",
                    "consequences": {
                        "troops": 15000,
                        "gold": -3000,
                        "morale": 10,
                        "territories": [],
                        "next_event": "marengo_campaign_1800",
                    },
                },
                {
                    "text": "Implement economic reforms",
                    "consequences": {
                        "troops": 0,
                        "gold": 10000,
                        "morale": 15,
                        "territories": [],
                        "next_event": "marengo_campaign_1800",
                    },
                },
                {
                    "text": "Establish the Napoleonic Code",
                    "consequences": {
                        "troops": 0,
                        "gold": -1000,
                        "morale": 20,
                        "territories": [],
                        "next_event": "marengo_campaign_1800",
                    },
                },
            ],
        },
        "marengo_campaign_1800": {
            "id": "marengo_campaign_1800",
            "year": 1800,
            "title": "Battle of Marengo",
            "description": """Austria has renewed hostilities, invading Italy once more.
General Melas commands 100,000 Austrians against your 60,000 French troops.
The outcome will determine control of Italy and possibly the war itself.""",
            "choices": [
                {
                    "text": "Confront Melas directly at Marengo",
                    "consequences": {
                        "troops": -8000,
                        "gold": 6000,
                        "morale": 20,
                        "territories": ["Northern Italy"],
                        "next_event": "luneville_peace_1801",
                    },
                },
                {
                    "text": "Attempt to outflank Austrian positions",
                    "consequences": {
                        "troops": -6000,
                        "gold": 8000,
                        "morale": 25,
                        "territories": ["Northern Italy", "Piedmont"],
                        "next_event": "luneville_peace_1801",
                    },
                },
            ],
        },
        "luneville_peace_1801": {
            "id": "luneville_peace_1801",
            "year": 1801,
            "title": "Peace of Lunéville",
            "description": """Austria sues for peace after Marengo. The terms are favorable:
France gains the left bank of the Rhine and confirms Italian possessions.
Britain remains isolated but continues the war at sea.""",
            "choices": [
                {
                    "text": "Accept the peace terms",
                    "consequences": {
                        "troops": 5000,
                        "gold": 10000,
                        "morale": 15,
                        "territories": ["Left Bank Rhineland"],
                        "enemies": ["Austria"],
                        "next_event": "concordat_with_church_1801",
                    },
                }
            ],
        },
        "concordat_with_church_1801": {
            "id": "concordat_with_church_1801",
            "year": 1801,
            "title": "Concordat with the Church",
            "description": """Religious conflict divides France. The Catholic Church opposes
the Revolution's legacy. A concordat could reconcile the Church with the state,
but it risks alienating revolutionary supporters.""",
            "choices": [
                {
                    "text": "Negotiate a concordat with Pope Pius VII",
                    "consequences": {
                        "troops": 0,
                        "gold": 2000,
                        "morale": 10,
                        "territories": [],
                        "next_event": "amien_peace_1802",
                    },
                },
                {
                    "text": "Maintain strict separation of church and state",
                    "consequences": {
                        "troops": 0,
                        "gold": 0,
                        "morale": -10,
                        "territories": [],
                        "next_event": "amien_peace_1802",
                    },
                },
            ],
        },
        "amien_peace_1802": {
            "id": "amien_peace_1802",
            "year": 1802,
            "title": "Peace of Amiens",
            "description": """Britain finally agrees to peace. The Treaty of Amiens ends
10 years of war. France retains most of its conquests, and Britain
recognizes the French Republic. But how long will this peace last?""",
            "choices": [
                {
                    "text": "Celebrate and consolidate gains",
                    "consequences": {
                        "troops": 10000,
                        "gold": 15000,
                        "morale": 20,
                        "territories": [],
                        "enemies": ["Britain"],
                        "next_event": "crown_emperor_1804",
                    },
                }
            ],
        },
        "crown_emperor_1804": {
            "id": "crown_emperor_1804",
            "year": 1804,
            "title": "Coronation as Emperor",
            "description": """The Senate and people demand you become Emperor. This will
establish a new dynasty and provide stability. However, it contradicts
republican principles and could provoke renewed war with monarchies.""",
            "choices": [
                {
                    "text": "Accept the imperial crown",
                    "consequences": {
                        "troops": 0,
                        "gold": 5000,
                        "morale": 30,
                        "territories": [],
                        "next_event": "austerlitz_campaign_1805",
                    },
                },
                {
                    "text": "Remain First Consul for life",
                    "consequences": {
                        "troops": 0,
                        "gold": 0,
                        "morale": -15,
                        "territories": [],
                        "next_event": "austerlitz_campaign_1805",
                    },
                },
            ],
        },
        "austerlitz_campaign_1805": {
            "id": "austerlitz_campaign_1805",
            "year": 1805,
            "title": "Battle of Austerlitz",
            "description": """The Third Coalition forms against you: Austria, Russia, and Britain.
Tsar Alexander and Emperor Francis command 85,000 troops against your
65,000 French soldiers on the Pratzen Heights. Victory here could end the war.""",
            "choices": [
                {
                    "text": "Lure them into attacking your center",
                    "consequences": {
                        "troops": -5000,
                        "gold": 12000,
                        "morale": 25,
                        "territories": ["Austria"],
                        "enemies": ["Austria", "Russia"],
                        "next_event": "pressburg_peace_1805",
                    },
                },
                {
                    "text": "Attack their flanks aggressively",
                    "consequences": {
                        "troops": -8000,
                        "gold": 10000,
                        "morale": 20,
                        "territories": ["Austria"],
                        "next_event": "pressburg_peace_1805",
                    },
                },
            ],
        },
        "pressburg_peace_1805": {
            "id": "pressburg_peace_1805",
            "year": 1805,
            "title": "Peace of Pressburg",
            "description": """Austria is defeated and sues for peace. The Treaty of Pressburg
dissolves the Holy Roman Empire and creates the Confederation of the Rhine
under French protection. Napoleon is now the dominant power in Europe.""",
            "choices": [
                {
                    "text": "Accept Austrian surrender",
                    "consequences": {
                        "troops": 5000,
                        "gold": 20000,
                        "morale": 20,
                        "territories": ["Confederation of Rhine"],
                        "next_event": "jena_auerstadt_1806",
                    },
                }
            ],
        },
        "jena_auerstadt_1806": {
            "id": "jena_auerstadt_1806",
            "year": 1806,
            "title": "Battles of Jena and Auerstadt",
            "description": """Prussia challenges your dominance, forming the Fourth Coalition
with Britain, Russia, and Sweden. King Frederick William III commands
150,000 Prussians against your 180,000 French troops.""",
            "choices": [
                {
                    "text": "Divide your forces to surround them",
                    "consequences": {
                        "troops": -6000,
                        "gold": 15000,
                        "morale": 20,
                        "territories": ["Prussia"],
                        "enemies": ["Prussia"],
                        "next_event": "berlin_decree_1806",
                    },
                },
                {
                    "text": "Concentrate forces for decisive battle",
                    "consequences": {
                        "troops": -4000,
                        "gold": 18000,
                        "morale": 25,
                        "territories": ["Prussia"],
                        "next_event": "berlin_decree_1806",
                    },
                },
            ],
        },
        "berlin_decree_1806": {
            "id": "berlin_decree_1806",
            "year": 1806,
            "title": "Berlin Decree",
            "description": """With Prussia defeated, you issue the Berlin Decree, establishing
the Continental System to blockade British trade. All European ports must
close to British ships. This will economically isolate Britain.""",
            "choices": [
                {
                    "text": "Implement the Continental System strictly",
                    "consequences": {
                        "troops": 0,
                        "gold": -5000,
                        "morale": 5,
                        "territories": [],
                        "next_event": "friedland_peace_1807",
                    },
                },
                {
                    "text": "Allow limited exemptions for allies",
                    "consequences": {
                        "troops": 0,
                        "gold": 2000,
                        "morale": 10,
                        "territories": [],
                        "next_event": "friedland_peace_1807",
                    },
                },
            ],
        },
        "friedland_peace_1807": {
            "id": "friedland_peace_1807",
            "year": 1807,
            "title": "Treaties of Tilsit",
            "description": """Russia is defeated at Friedland. Tsar Alexander seeks peace.
The Treaties of Tilsit divide Europe between France and Russia, and
establish the Duchy of Warsaw. Britain stands alone against you.""",
            "choices": [
                {
                    "text": "Form alliance with Russia",
                    "consequences": {
                        "troops": 10000,
                        "gold": 10000,
                        "morale": 15,
                        "territories": ["Duchy of Warsaw"],
                        "allies": ["Russia"],
                        "next_event": "peninsular_war_1808",
                    },
                }
            ],
        },
        "peninsular_war_1808": {
            "id": "peninsular_war_1808",
            "year": 1808,
            "title": "Peninsular War",
            "description": """Portugal refuses to join the Continental System. You invade
the Iberian peninsula to enforce compliance. Spain initially cooperates,
but popular resistance grows. British forces land to support insurgents.""",
            "choices": [
                {
                    "text": "Install your brother Joseph as King of Spain",
                    "consequences": {
                        "troops": -10000,
                        "gold": -8000,
                        "morale": -10,
                        "territories": ["Spain"],
                        "next_event": "wagram_campaign_1809",
                    },
                },
                {
                    "text": "Withdraw and focus on other fronts",
                    "consequences": {
                        "troops": 5000,
                        "gold": 3000,
                        "morale": -5,
                        "territories": [],
                        "next_event": "wagram_campaign_1809",
                    },
                },
            ],
        },
        "wagram_campaign_1809": {
            "id": "wagram_campaign_1809",
            "year": 1809,
            "title": "Battle of Wagram",
            "description": """Austria renews war in the Fifth Coalition. Archduke Charles
commands 150,000 Austrians against your 180,000 French troops.
The Danube River complicates maneuvers.""",
            "choices": [
                {
                    "text": "Cross the Danube and attack their center",
                    "consequences": {
                        "troops": -7000,
                        "gold": 15000,
                        "morale": 15,
                        "territories": ["Illyria"],
                        "next_event": "schonbrunn_peace_1809",
                    },
                },
                {
                    "text": "Wait for reinforcements before attacking",
                    "consequences": {
                        "troops": -5000,
                        "gold": 12000,
                        "morale": 10,
                        "territories": ["Illyria"],
                        "next_event": "schonbrunn_peace_1809",
                    },
                },
            ],
        },
        "schonbrunn_peace_1809": {
            "id": "schonbrunn_peace_1809",
            "year": 1809,
            "title": "Peace of Schönbrunn",
            "description": """Austria is defeated again. The Treaty of Schönbrunn annexes
additional territories and reduces Austria to a second-rate power.
France now controls most of continental Europe.""",
            "choices": [
                {
                    "text": "Accept the peace terms",
                    "consequences": {
                        "troops": 8000,
                        "gold": 25000,
                        "morale": 20,
                        "territories": ["Illyria", "Tyrol"],
                        "next_event": "russian_campaign_1812",
                    },
                }
            ],
        },
        "russian_campaign_1812": {
            "id": "russian_campaign_1812",
            "year": 1812,
            "title": "Invasion of Russia",
            "description": """Russia violates the Continental System by trading with Britain.
You launch the largest invasion in history: 600,000 men against Russia.
The vast distances and harsh winter will test your Grande Armée.""",
            "choices": [
                {
                    "text": "Advance rapidly to Moscow",
                    "consequences": {
                        "troops": -200000,
                        "gold": -15000,
                        "morale": -40,
                        "territories": [],
                        "enemies": ["Russia"],
                        "next_event": "retreat_from_moscow_1812",
                    },
                },
                {
                    "text": "Advance cautiously and secure supply lines",
                    "consequences": {
                        "troops": -150000,
                        "gold": -10000,
                        "morale": -30,
                        "territories": ["Lithuania"],
                        "next_event": "retreat_from_moscow_1812",
                    },
                },
                {
                    "text": "Negotiate with Russia instead",
                    "consequences": {
                        "troops": 0,
                        "gold": 5000,
                        "morale": -10,
                        "territories": [],
                        "next_event": "leipzig_campaign_1813",
                    },
                },
            ],
        },
        "retreat_from_moscow_1812": {
            "id": "retreat_from_moscow_1812",
            "year": 1812,
            "title": "The Great Retreat",
            "description": """Moscow burns and Kutuzov avoids battle. Winter comes early,
temperatures drop to -30°C. Your army starves and freezes during the retreat.
Only 40,000 of 600,000 men survive to reach the Berezina River.""",
            "choices": [
                {
                    "text": "Continue the retreat to France",
                    "consequences": {
                        "troops": -10000,
                        "gold": 0,
                        "morale": -25,
                        "territories": [],
                        "next_event": "leipzig_campaign_1813",
                    },
                }
            ],
        },
        "leipzig_campaign_1813": {
            "id": "leipzig_campaign_1813",
            "year": 1813,
            "title": "Battle of Leipzig",
            "description": """The Sixth Coalition forms: Austria, Prussia, Russia, Sweden, Britain.
Over 300,000 allied troops face your 200,000 French soldiers.
This is the "Battle of the Nations" - defeat means the end of your empire.""",
            "choices": [
                {
                    "text": "Fight defensive battle in Leipzig",
                    "consequences": {
                        "troops": -30000,
                        "gold": 0,
                        "morale": -20,
                        "territories": [],
                        "next_event": "abdication_1814",
                    },
                },
                {
                    "text": "Withdraw to more defensible positions",
                    "consequences": {
                        "troops": -20000,
                        "gold": -5000,
                        "morale": -15,
                        "territories": [],
                        "next_event": "abdication_1814",
                    },
                },
            ],
        },
        "abdication_1814": {
            "id": "abdication_1814",
            "year": 1814,
            "title": "First Abdication",
            "description": """Coalition forces enter Paris. Your marshals urge you to continue
fighting, but the Senate demands your abdication. You could fight on or
accept exile to Elba with the title of Emperor.""",
            "choices": [
                {
                    "text": "Abdicate and accept exile to Elba",
                    "consequences": {
                        "troops": 0,
                        "gold": 0,
                        "morale": -50,
                        "territories": ["Elba"],
                        "next_event": "hundred_days_1815",
                    },
                },
                {
                    "text": "Continue fighting to the end",
                    "consequences": {
                        "troops": -50000,
                        "gold": 0,
                        "morale": -30,
                        "territories": [],
                        "next_event": "final_defeat_1814",
                    },
                },
            ],
        },
        "hundred_days_1815": {
            "id": "hundred_days_1815",
            "year": 1815,
            "title": "The Hundred Days",
            "description": """You escape Elba and return to France. The people and army rally
to you. Louis XVIII flees. You raise a new army of 200,000 men to face
the Seventh Coalition: Britain, Austria, Russia, Prussia.""",
            "choices": [
                {
                    "text": "March north to confront the coalition",
                    "consequences": {
                        "troops": 0,
                        "gold": 0,
                        "morale": 30,
                        "territories": [],
                        "next_event": "waterloo_1815",
                    },
                }
            ],
        },
        "waterloo_1815": {
            "id": "waterloo_1815",
            "year": 1815,
            "title": "Battle of Waterloo",
            "description": """The decisive battle. Wellington commands 68,000 Anglo-Allied
troops on a ridge. Blücher's Prussians approach from the east.
Rain has made the ground muddy. Your 72,000 French troops must break through.""",
            "choices": [
                {
                    "text": "Attack Wellington's center immediately",
                    "consequences": {
                        "troops": -25000,
                        "gold": 0,
                        "morale": -60,
                        "territories": [],
                        "next_event": "final_exile_1815",
                    },
                },
                {
                    "text": "Wait for the ground to dry",
                    "consequences": {
                        "troops": -30000,
                        "gold": 0,
                        "morale": -70,
                        "territories": [],
                        "next_event": "final_exile_1815",
                    },
                },
                {
                    "text": "Withdraw and negotiate peace",
                    "consequences": {
                        "troops": -10000,
                        "gold": 0,
                        "morale": -40,
                        "territories": ["Elba"],
                        "next_event": "final_exile_1815",
                    },
                },
            ],
        },
        "final_exile_1815": {
            "id": "final_exile_1815",
            "year": 1815,
            "title": "Final Exile",
            "description": """Defeated at Waterloo, you surrender to the British. The Coalition
sends you to Saint Helena, a remote island in the South Atlantic.
You will spend your remaining years in exile, dictating your memoirs.""",
            "choices": [
                {
                    "text": "Accept your fate",
                    "consequences": {
                        "troops": 0,
                        "gold": 0,
                        "morale": -100,
                        "territories": ["Saint Helena"],
                        "next_event": None,
                    },
                }
            ],
        },
    }


def get_victory_conditions() -> Dict[str, Dict]:
    """Return all possible victory conditions."""
    return {
        "military_victory": {
            "name": "Military Victory",
            "description": "Control 75% of European territories",
            "requirements": {"territories_count": 15, "morale": 80},
        },
        "diplomatic_victory": {
            "name": "Diplomatic Victory",
            "description": "Form alliances with 5+ nations",
            "requirements": {"allies_count": 5, "peace_years": 5},
        },
        "historical_victory": {
            "name": "Historical Victory",
            "description": "Follow Napoleon's actual path closely",
            "requirements": {"historical_accuracy": 80, "survive_to_1815": True},
        },
    }


def get_defeat_conditions() -> Dict[str, Dict]:
    """Return all defeat conditions."""
    return {
        "military_defeat": {
            "name": "Military Defeat",
            "description": "Troops fall below 5,000",
            "threshold": 5000,
        },
        "economic_defeat": {
            "name": "Economic Collapse",
            "description": "Gold falls below 0",
            "threshold": 0,
        },
        "political_defeat": {
            "name": "Political Defeat",
            "description": "Morale falls below 20",
            "threshold": 20,
        },
        "territorial_defeat": {
            "name": "Territorial Loss",
            "description": "Lose control of France",
            "territory": "France",
        },
    }


def get_random_events() -> Dict[str, Any]:
    """Return all random events."""
    return RANDOM_EVENTS


def get_trait(trait_id: str) -> Dict[str, Any]:
    """Get trait data by ID."""
    return TRAITS.get(trait_id, {})


def get_general(general_id: str) -> Dict[str, Any]:
    """Get general data by ID."""
    return GENERALS.get(general_id, {})


def get_artifact(artifact_id: str) -> Dict[str, Any]:
    """Get artifact data by ID."""
    return ARTIFACTS.get(artifact_id, {})


# Map Data
MAP_DIMENSIONS = (90, 30)  # Width, Height

TERRITORY_NODES = {
    "France":  {"x": 35, "y": 12, "w": 14, "h": 5, "label": "FRA"},
    "Spain":   {"x": 15, "y": 20, "w": 12, "h": 4, "label": "SPA"},
    "Britain": {"x": 30, "y": 2,  "w": 12, "h": 4, "label": "GBR"},
    "Germany": {"x": 55, "y": 10, "w": 12, "h": 4, "label": "GER"},
    "Austria": {"x": 60, "y": 18, "w": 12, "h": 4, "label": "AUS"},
    "Russia":  {"x": 75, "y": 8,  "w": 12, "h": 6, "label": "RUS"},
    "Italy":   {"x": 45, "y": 22, "w": 12, "h": 4, "label": "ITA"},
    "Prussia": {"x": 60, "y": 4,  "w": 12, "h": 4, "label": "PRU"},
}

MAP_CONNECTIONS = [
    ("France", "Spain"),
    ("France", "Britain"),
    ("France", "Germany"),
    ("France", "Italy"),
    ("Germany", "Austria"),
    ("Germany", "Russia"),
    ("Germany", "Prussia"),
    ("Austria", "Italy"),
    ("Austria", "Russia"),
    ("Prussia", "Russia"),
]
