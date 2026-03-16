import random
from models.enemy import Enemy


class EnemyGenerator:
    def __init__(self):
        self.normal_names = [
            "Skeleton",
            "Bandit",
            "Cultist",
            "Raider",
            "Wraith",
            "Fallen Knight",
            "Ghoul",
            "Ash Stalker"
        ]

        self.boss_names = [
            "Bone Tyrant",
            "Blood Captain",
            "The Hollow Seer",
            "Grave Lord",
            "Ashen King"
        ]

    def is_boss_round(self, round_number):
        return round_number in [5, 10, 15, 20, 25]

    def get_difficulty_band(self, round_number):
        if round_number <= 10:
            return "early"
        elif round_number <= 15:
            return "mid"
        return "late"

    def get_enemy_level(self, round_number, is_boss=False):
        if is_boss:
            return round_number + 2

        min_level = max(1, round_number - 2)
        max_level = max(1, round_number)
        return random.randint(min_level, max_level)

    def build_enemy_stats(self, enemy_level, difficulty_band, is_boss=False):
        if difficulty_band == "early":
            health = 8 + (enemy_level * 4)
            attack = 2 + enemy_level
            defense = 1 + (enemy_level // 2)
            dodge = min(10, enemy_level)
        elif difficulty_band == "mid":
            health = 16 + (enemy_level * 6)
            attack = 3 + (enemy_level * 2)
            defense = 2 + (enemy_level // 2)
            dodge = min(16, enemy_level + 1)
        else:
            health = 24 + (enemy_level * 8)
            attack = 5 + (enemy_level * 2)
            defense = 3 + (enemy_level // 2)
            dodge = min(22, enemy_level + 3)

        if is_boss:
            health = round(health * 1.9)
            attack = round(attack * 1.35)
            defense = round(defense * 1.3)
            dodge = min(30, round(dodge * 1.2))

        return health, attack, defense, dodge

    def generate_enemy(self, round_number, is_boss=False):
        difficulty_band = self.get_difficulty_band(round_number)
        enemy_level = self.get_enemy_level(round_number, is_boss)

        if is_boss:
            name = random.choice(self.boss_names)
        else:
            name = random.choice(self.normal_names)

        health, attack, defense, dodge = self.build_enemy_stats(
            enemy_level,
            difficulty_band,
            is_boss
        )

        return Enemy(
            name=name,
            level=enemy_level,
            health=health,
            attack=attack,
            defense=defense,
            dodge=dodge,
            is_boss=is_boss
        )

    def generate_encounter(self, round_number):
        if self.is_boss_round(round_number):
            return [self.generate_enemy(round_number, is_boss=True)]

        enemy_count = random.randint(2, 4)
        return [self.generate_enemy(round_number, is_boss=False) for _ in range(enemy_count)]