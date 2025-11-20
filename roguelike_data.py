"""
Napoleon's Campaign - Roguelike Data Module

Contains definitions for Traits and Random Events.
"""

TRAITS = {
    "artillery_expert": {
        "name": "Artillery Expert",
        "description": "Your mastery of cannons gives +20% combat strength.",
        "effect_type": "battle_bonus",
        "value": 0.20
    },
    "logistics_master": {
        "name": "Logistics Master",
        "description": "Efficient supply lines reduce army maintenance by 30%.",
        "effect_type": "maintenance_reduction",
        "value": 0.30
    },
    "charismatic_leader": {
        "name": "Charismatic Leader",
        "description": "Your presence inspires troops, increasing morale recovery by 50%.",
        "effect_type": "morale_recovery",
        "value": 0.50
    },
    "diplomat": {
        "name": "Diplomat",
        "description": "Skilled negotiator. +20% chance of diplomatic success.",
        "effect_type": "diplomacy_bonus",
        "value": 0.20
    },
    "reckless": {
        "name": "Reckless",
        "description": "Aggressive tactics increase casualties by 10% but give +10% strength.",
        "effect_type": "battle_modifier",
        "strength_bonus": 0.10,
        "casualty_penalty": 0.10
    },
    "wealthy_patron": {
        "name": "Wealthy Patron",
        "description": "Personal connections provide +500 gold income per turn.",
        "effect_type": "income_bonus",
        "value": 500
    }
}

RANDOM_EVENTS = {
    "supply_shortage": {
        "id": "supply_shortage",
        "title": "Supply Shortage",
        "description": "Bad weather and partisan attacks have disrupted your supply lines. Your troops are hungry and ammunition is low.",
        "type": "random",
        "choices": [
            {
                "text": "Purchase supplies at high cost",
                "consequences": {
                    "gold": -2000,
                    "morale": 5,
                }
            },
            {
                "text": "Forage from the local countryside",
                "consequences": {
                    "morale": -10,
                    "gold": 500, # Looting
                }
            }
        ]
    },
    "local_uprising": {
        "id": "local_uprising",
        "title": "Local Uprising",
        "description": "Locals in a captured territory have taken up arms against your garrison!",
        "type": "random",
        "choices": [
            {
                "text": "Crush the rebellion ruthlessly",
                "consequences": {
                    "troops": -1000,
                    "morale": -5,
                    "gold": 1000, # Confiscated goods
                    "add_trait": "reckless" # Chance to become reckless
                }
            },
            {
                "text": "Negotiate and offer concessions",
                "consequences": {
                    "gold": -1000,
                    "morale": 5,
                    "add_trait": "diplomat" # Practice diplomacy
                }
            }
        ]
    },
    "mercenary_offer": {
        "id": "mercenary_offer",
        "title": "Mercenary Company",
        "description": "A veteran Swiss mercenary company offers their services for the right price.",
        "type": "random",
        "choices": [
            {
                "text": "Hire them (5,000 troops)",
                "consequences": {
                    "gold": -3000,
                    "troops": 5000,
                }
            },
            {
                "text": "Decline the offer",
                "consequences": {}
            }
        ]
    },
    "military_academy": {
        "id": "military_academy",
        "title": "Military Academy Inspection",
        "description": "You visit a military academy to inspect the new officer cadets.",
        "type": "random",
        "choices": [
            {
                "text": "Emphasize artillery training",
                "consequences": {
                    "gold": -500,
                    "add_trait": "artillery_expert"
                }
            },
            {
                "text": "Focus on logistics and supply",
                "consequences": {
                    "gold": -500,
                    "add_trait": "logistics_master"
                }
            }
        ]
    },
    "scandal": {
        "id": "scandal",
        "title": "Political Scandal",
        "description": "Rumors of corruption in your administration are spreading in Paris.",
        "type": "random",
        "choices": [
            {
                "text": "Suppress the rumors",
                "consequences": {
                    "gold": -1000,
                    "morale": -5
                }
            },
            {
                "text": "Address the public directly",
                "consequences": {
                    "morale": 5,
                    "add_trait": "charismatic_leader"
                }
            }
        ]
    },
    "recruit_ney": {
        "id": "recruit_ney",
        "title": "The Bravest of the Brave",
        "description": "General Michel Ney has distinguished himself in recent battles. He requests a command in your army.",
        "type": "random",
        "choices": [
            {
                "text": "Grant him a command",
                "consequences": {
                    "gold": -1000,
                    "add_general": "ney"
                }
            },
            {
                "text": "We have enough commanders",
                "consequences": {
                    "morale": -2
                }
            }
        ]
    },
    "find_rosetta": {
        "id": "find_rosetta",
        "title": "Discovery in Egypt",
        "description": "Your scholars have found a curious stone slab in Rashid (Rosetta). It appears to hold the key to hieroglyphs.",
        "type": "random",
        "choices": [
            {
                "text": "Send it to the Louvre",
                "consequences": {
                    "morale": 5,
                    "add_artifact": "rosetta_stone"
                }
            },
            {
                "text": "Sell it to private collectors",
                "consequences": {
                    "gold": 5000,
                    "morale": -5
                }
            }
        ]
    }
}

GENERALS = {
    "ney": {
        "name": "Michel Ney",
        "description": "The Bravest of the Brave. Leads from the front.",
        "effect_type": "battle_bonus",
        "value": 0.25,
        "death_chance": 0.15, # High risk
        "status": "active"
    },
    "davout": {
        "name": "Louis-Nicolas Davout",
        "description": "The Iron Marshal. Unshakable defense.",
        "effect_type": "defense_bonus",
        "value": 0.30,
        "death_chance": 0.05,
        "status": "active"
    },
    "murat": {
        "name": "Joachim Murat",
        "description": "Dashing cavalry commander. Devastating charges.",
        "effect_type": "cavalry_bonus", # treated as battle bonus for now
        "value": 0.20,
        "death_chance": 0.10,
        "status": "active"
    },
    "berthier": {
        "name": "Louis-Alexandre Berthier",
        "description": "Chief of Staff. Master of organization.",
        "effect_type": "logistics_bonus", # maintenance reduction
        "value": 0.25,
        "death_chance": 0.01,
        "status": "active"
    },
    "lannes": {
        "name": "Jean Lannes",
        "description": "The Roland of the Army. Exceptional vanguard leader.",
        "effect_type": "battle_bonus",
        "value": 0.20,
        "death_chance": 0.10,
        "status": "active"
    }
}

ARTIFACTS = {
    "rosetta_stone": {
        "name": "Rosetta Stone",
        "description": "Unlocks ancient knowledge. +10% Diplomatic Success.",
        "effect_type": "diplomacy_bonus",
        "value": 0.10
    },
    "imperial_eagle": {
        "name": "Imperial Eagle",
        "description": "Symbol of the Empire. +1 Morale per turn.",
        "effect_type": "morale_regen",
        "value": 1
    },
    "code_civil": {
        "name": "Code Civil Draft",
        "description": "The foundation of modern law. +200 Gold income per turn.",
        "effect_type": "income_bonus",
        "value": 200
    },
    "austrian_cannon": {
        "name": "Captured Austrian Cannon",
        "description": "Fine artillery piece. +5% Battle Strength.",
        "effect_type": "battle_bonus",
        "value": 0.05
    }
}
