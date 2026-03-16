CLASSES = {
    "Mage": {
        "base_stats": {
            "Stamina": 10,
            "Strength": 5,
            "Intellect": 15,
            "Dexterity": 10
        },
        "passive": {
            "name": "Arcane Fortune",
            "description": "+1 extra reroll at the start of a run",
            "type": "reroll_bonus",
            "value": 1
        },
        "loot_tags": ["caster", "intellect"],
        "starter_weapon": "Oak Staff"
    },
    "Warrior": {
        "base_stats": {
            "Stamina": 15,
            "Strength": 15,
            "Intellect": 5,
            "Dexterity": 8
        },
        "passive": {
            "name": "First Strike",
            "description": "Gets 1 free attack at the start of a fight",
            "type": "opening_attack",
            "value": 1
        },
        "loot_tags": ["strength", "melee", "heavy"],
        "starter_weapon": "Longsword"
    },
    "Rogue": {
        "base_stats": {
            "Stamina": 11,
            "Strength": 8,
            "Intellect": 7,
            "Dexterity": 15
        },
        "passive": {
            "name": "Fleet Shadow",
            "description": "+10% dodge chance",
            "type": "dodge_bonus_percent",
            "value": 10
        },
        "loot_tags": ["dexterity", "light"],
        "starter_weapon": "Dagger"
    }
}