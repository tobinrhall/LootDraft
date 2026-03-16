BASE_ITEMS = {
    "Weapon": [
        {
            "name": "Longsword",
            "tags": ["weapon", "melee", "strength"],
            "base_stats": {
                "Attack Damage": (8, 12),
                "Strength": (2, 5),
                "Crit Chance": (1, 3)
            }
        },
        {
            "name": "War Axe",
            "tags": ["weapon", "melee", "strength"],
            "base_stats": {
                "Attack Damage": (10, 14),
                "Strength": (3, 6),
                "Crushing Blow": (1, 2)
            }
        },
        {
            "name": "Dagger",
            "tags": ["weapon", "melee", "dexterity"],
            "base_stats": {
                "Attack Damage": (6, 10),
                "Dexterity": (3, 6),
                "Haste": (1, 3)
            }
        },
        {
            "name": "Oak Staff",
            "tags": ["weapon", "caster", "intellect"],
            "base_stats": {
                "Spell Damage": (10, 15),
                "Intellect": (3, 7),
                "Haste": (1, 2)
            }
        }
    ],
    "Helmet": [
        {
            "name": "Iron Helm",
            "tags": ["armor", "heavy", "strength"],
            "base_stats": {
                "Armor": (4, 8),
                "Strength": (2, 4),
                "Defense": (1, 3)
            }
        },
        {
            "name": "Shadow Hood",
            "tags": ["armor", "light", "dexterity"],
            "base_stats": {
                "Armor": (2, 5),
                "Dexterity": (2, 5),
                "Evade": (1, 3)
            }
        },
        {
            "name": "Sage Crown",
            "tags": ["armor", "caster", "intellect"],
            "base_stats": {
                "Armor": (2, 4),
                "Intellect": (3, 6),
                "Haste": (1, 2)
            }
        }
    ],
    "Chest": [
        {
            "name": "Breastplate",
            "tags": ["armor", "heavy", "strength"],
            "base_stats": {
                "Armor": (8, 14),
                "Stamina": (4, 8),
                "Defense": (2, 4)
            }
        },
        {
            "name": "Leather Jerkin",
            "tags": ["armor", "light", "dexterity"],
            "base_stats": {
                "Armor": (5, 9),
                "Dexterity": (3, 6),
                "Dodge": (1, 3)
            }
        },
        {
            "name": "Mystic Robe",
            "tags": ["armor", "caster", "intellect"],
            "base_stats": {
                "Armor": (3, 6),
                "Intellect": (4, 8),
                "Spell Damage": (2, 5)
            }
        }
    ],
    "Boots": [
        {
            "name": "War Boots",
            "tags": ["armor", "heavy", "strength"],
            "base_stats": {
                "Armor": (3, 6),
                "Stamina": (2, 5),
                "Defense": (1, 2)
            }
        },
        {
            "name": "Tracker Boots",
            "tags": ["armor", "light", "dexterity"],
            "base_stats": {
                "Armor": (2, 5),
                "Dexterity": (2, 5),
                "Dodge": (1, 3)
            }
        },
        {
            "name": "Silken Slippers",
            "tags": ["armor", "caster", "intellect"],
            "base_stats": {
                "Armor": (1, 3),
                "Intellect": (2, 5),
                "Haste": (1, 2)
            }
        }
    ],
    "Gloves": [
        {
            "name": "Iron Gauntlets",
            "tags": ["armor", "heavy", "strength"],
            "base_stats": {
                "Armor": (3, 6),
                "Strength": (2, 4),
                "Defense": (1, 2)
            }
        },
        {
            "name": "Shadow Grips",
            "tags": ["armor", "light", "dexterity"],
            "base_stats": {
                "Armor": (2, 4),
                "Dexterity": (2, 5),
                "Crit Chance": (1, 2)
            }
        },
        {
            "name": "Silk Handwraps",
            "tags": ["armor", "caster", "intellect"],
            "base_stats": {
                "Armor": (1, 3),
                "Intellect": (2, 5),
                "Haste": (1, 2)
            }
        }
    ],
    "Belt": [
        {
            "name": "War Belt",
            "tags": ["armor", "heavy", "strength"],
            "base_stats": {
                "Armor": (3, 6),
                "Stamina": (3, 6),
                "Strength": (2, 4)
            }
        },
        {
            "name": "Hunter's Belt",
            "tags": ["armor", "light", "dexterity"],
            "base_stats": {
                "Armor": (2, 4),
                "Dexterity": (2, 5),
                "Dodge": (1, 2)
            }
        },
        {
            "name": "Mystic Sash",
            "tags": ["armor", "caster", "intellect"],
            "base_stats": {
                "Armor": (1, 3),
                "Intellect": (3, 6),
                "Spell Damage": (1, 3)
            }
        }
    ],
    "Amulet": [
        {
            "name": "Bronze Amulet",
            "tags": ["jewelry", "strength", "melee"],
            "base_stats": {
                "Strength": (2, 5),
                "Stamina": (2, 5),
                "Attack Damage": (1, 3)
            }
        },
        {
            "name": "Jeweled Charm",
            "tags": ["jewelry", "dexterity", "light"],
            "base_stats": {
                "Dexterity": (2, 5),
                "Crit Chance": (1, 3),
                "Haste": (1, 2)
            }
        },
        {
            "name": "Rune Pendant",
            "tags": ["jewelry", "caster", "intellect"],
            "base_stats": {
                "Intellect": (3, 6),
                "Spell Damage": (2, 4),
                "Haste": (1, 2)
            }
        }
    ],
    "Ring": [
        {
            "name": "Iron Ring",
            "tags": ["jewelry", "strength", "heavy"],
            "base_stats": {
                "Strength": (2, 4),
                "Defense": (1, 2),
                "Stamina": (2, 4)
            }
        },
        {
            "name": "Band of Precision",
            "tags": ["jewelry", "dexterity", "light"],
            "base_stats": {
                "Dexterity": (2, 4),
                "Crit Chance": (1, 3),
                "Dodge": (1, 2)
            }
        },
        {
            "name": "Signet Loop",
            "tags": ["jewelry", "caster", "intellect"],
            "base_stats": {
                "Intellect": (2, 5),
                "Spell Damage": (1, 3),
                "Haste": (1, 2)
            }
        }
    ]
}