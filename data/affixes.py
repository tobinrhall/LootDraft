PREFIXES = [
    {
        "name": "Savage",
        "stat": "Strength",
        "min": 2,
        "max": 6,
        "tags": ["strength", "melee", "heavy"],
        "slots": ["Weapon", "Helmet", "Chest", "Boots", "Gloves", "Belt", "Amulet", "Ring"]
    },
    {
        "name": "Agile",
        "stat": "Dexterity",
        "min": 2,
        "max": 6,
        "tags": ["dexterity", "light"],
        "slots": ["Weapon", "Helmet", "Chest", "Boots", "Gloves", "Belt", "Amulet", "Ring"]
    },
    {
        "name": "Runed",
        "stat": "Intellect",
        "min": 2,
        "max": 6,
        "tags": ["intellect", "caster"],
        "slots": ["Weapon", "Helmet", "Chest", "Boots", "Gloves", "Belt", "Amulet", "Ring"]
    },
    {
        "name": "Stalwart",
        "stat": "Stamina",
        "min": 3,
        "max": 8,
        "tags": ["heavy", "strength", "armor"],
        "slots": ["Helmet", "Chest", "Boots", "Gloves", "Belt"]
    },
    {
        "name": "Brutal",
        "stat": "Attack Damage",
        "min": 2,
        "max": 5,
        "tags": ["weapon", "melee"],
        "slots": ["Weapon", "Amulet"]
    },
    {
        "name": "Arcane",
        "stat": "Spell Damage",
        "min": 2,
        "max": 5,
        "tags": ["weapon", "caster", "intellect"],
        "slots": ["Weapon", "Amulet", "Belt", "Ring"]
    },
    {
        "name": "Warding",
        "stat": "Armor",
        "min": 2,
        "max": 5,
        "tags": ["armor", "heavy", "light", "caster"],
        "slots": ["Helmet", "Chest", "Boots", "Gloves", "Belt"]
    },
    {
        "name": "Guarding",
        "stat": "Defense",
        "min": 1,
        "max": 4,
        "tags": ["armor", "heavy", "strength"],
        "slots": ["Helmet", "Chest", "Boots", "Gloves", "Belt", "Ring"]
    },
    {
        "name": "Shadowed",
        "stat": "Evade",
        "min": 1,
        "max": 4,
        "tags": ["armor", "light", "dexterity"],
        "slots": ["Helmet", "Chest", "Boots", "Gloves", "Belt", "Ring"]
    },
    {
        "name": "Slippery",
        "stat": "Dodge",
        "min": 1,
        "max": 4,
        "tags": ["armor", "light", "dexterity"],
        "slots": ["Helmet", "Chest", "Boots", "Gloves", "Belt", "Ring"]
    },
    {
        "name": "Swift",
        "stat": "Haste",
        "min": 1,
        "max": 3,
        "tags": ["dexterity", "light", "caster"],
        "slots": ["Weapon", "Helmet", "Chest", "Boots", "Gloves", "Amulet", "Ring"]
    },
    {
        "name": "Deadly",
        "stat": "Crit Chance",
        "min": 1,
        "max": 3,
        "tags": ["weapon", "melee", "dexterity"],
        "slots": ["Weapon", "Gloves", "Amulet", "Ring"]
    },
    {
        "name": "Crushing",
        "stat": "Crushing Blow",
        "min": 1,
        "max": 2,
        "tags": ["weapon", "melee", "strength"],
        "slots": ["Weapon", "Gloves", "Amulet"]
    },
    {
        "name": "Chilling",
        "stat": "Slow",
        "min": 1,
        "max": 2,
        "tags": ["weapon", "caster", "intellect"],
        "slots": ["Weapon", "Amulet", "Ring"]
    }
]

SUFFIXES = [
    {
        "name": "of the Bear",
        "stat": "Strength",
        "min": 2,
        "max": 6,
        "tags": ["strength", "melee", "heavy"],
        "slots": ["Weapon", "Helmet", "Chest", "Boots", "Gloves", "Belt", "Amulet", "Ring"]
    },
    {
        "name": "of the Fox",
        "stat": "Dexterity",
        "min": 2,
        "max": 6,
        "tags": ["dexterity", "light"],
        "slots": ["Weapon", "Helmet", "Chest", "Boots", "Gloves", "Belt", "Amulet", "Ring"]
    },
    {
        "name": "of the Magus",
        "stat": "Intellect",
        "min": 2,
        "max": 6,
        "tags": ["intellect", "caster"],
        "slots": ["Weapon", "Helmet", "Chest", "Boots", "Gloves", "Belt", "Amulet", "Ring"]
    },
    {
        "name": "of the Ox",
        "stat": "Stamina",
        "min": 3,
        "max": 8,
        "tags": ["heavy", "strength", "armor"],
        "slots": ["Helmet", "Chest", "Boots", "Gloves", "Belt", "Amulet", "Ring"]
    },
    {
        "name": "of Slaying",
        "stat": "Attack Damage",
        "min": 2,
        "max": 5,
        "tags": ["weapon", "melee"],
        "slots": ["Weapon", "Amulet"]
    },
    {
        "name": "of Sorcery",
        "stat": "Spell Damage",
        "min": 2,
        "max": 5,
        "tags": ["weapon", "caster", "intellect"],
        "slots": ["Weapon", "Amulet", "Belt", "Ring"]
    },
    {
        "name": "of the Bulwark",
        "stat": "Armor",
        "min": 2,
        "max": 5,
        "tags": ["armor", "heavy", "light", "caster"],
        "slots": ["Helmet", "Chest", "Boots", "Gloves", "Belt"]
    },
    {
        "name": "of Guarding",
        "stat": "Defense",
        "min": 1,
        "max": 4,
        "tags": ["armor", "heavy", "strength"],
        "slots": ["Helmet", "Chest", "Boots", "Gloves", "Belt", "Ring"]
    },
    {
        "name": "of Evasion",
        "stat": "Evade",
        "min": 1,
        "max": 4,
        "tags": ["armor", "light", "dexterity"],
        "slots": ["Helmet", "Chest", "Boots", "Gloves", "Belt", "Ring"]
    },
    {
        "name": "of Reflexes",
        "stat": "Dodge",
        "min": 1,
        "max": 4,
        "tags": ["armor", "light", "dexterity"],
        "slots": ["Helmet", "Chest", "Boots", "Gloves", "Belt", "Ring"]
    },
    {
        "name": "of Quickness",
        "stat": "Haste",
        "min": 1,
        "max": 3,
        "tags": ["dexterity", "light", "caster"],
        "slots": ["Weapon", "Helmet", "Chest", "Boots", "Gloves", "Amulet", "Ring"]
    },
    {
        "name": "of Precision",
        "stat": "Crit Chance",
        "min": 1,
        "max": 3,
        "tags": ["weapon", "melee", "dexterity"],
        "slots": ["Weapon", "Gloves", "Amulet", "Ring"]
    },
    {
        "name": "of Sundering",
        "stat": "Crushing Blow",
        "min": 1,
        "max": 2,
        "tags": ["weapon", "melee", "strength"],
        "slots": ["Weapon", "Gloves", "Amulet"]
    },
    {
        "name": "of Frost",
        "stat": "Slow",
        "min": 1,
        "max": 2,
        "tags": ["weapon", "caster", "intellect"],
        "slots": ["Weapon", "Amulet", "Ring"]
    }
]

FLAVOR_TEXTS = [
    "A relic from a forgotten battlefield.",
    "Its surface hums with ancient power.",
    "Crafted in darkness, meant for war.",
    "Legends whisper of its previous owner.",
    "You feel stronger just holding it.",
    "It carries the weight of ancient battles.",
    "Power coils within its frame.",
    "Its presence alone inspires caution."
]