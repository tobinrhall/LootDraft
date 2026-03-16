class Enemy:
    def __init__(self, name, level, health, attack, defense, dodge, is_boss=False):
        self.name = name
        self.level = level
        self.health = health
        self.attack = attack
        self.defense = defense
        self.dodge = dodge
        self.is_boss = is_boss

    def __str__(self):
        boss_text = "Boss" if self.is_boss else "Normal"
        return (
            f"{self.name} ({boss_text})\n"
            f"  Level: {self.level}\n"
            f"  Health: {self.health}\n"
            f"  Attack: {self.attack}\n"
            f"  Defense: {self.defense}\n"
            f"  Dodge: {self.dodge}"
        )