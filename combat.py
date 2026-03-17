import random


def get_player_combat_stats(character):
    stats = character.get_total_stats()

    attack_damage = stats.get("Attack Damage", 0)
    spell_damage = stats.get("Spell Damage", 0)
    strength = stats.get("Strength", 0)
    dexterity = stats.get("Dexterity", 0)
    intellect = stats.get("Intellect", 0)
    crit = stats.get("Crit Chance", 0)
    haste = stats.get("Haste", 0)
    crushing = stats.get("Crushing Blow", 0)
    slow = stats.get("Slow", 0)
    armor = stats.get("Armor", 0)
    defense = stats.get("Defense", 0)
    dodge = stats.get("Dodge", 0)
    evade = stats.get("Evade", 0)
    dodge_bonus = stats.get("Dodge Chance Bonus", 0)
    stamina = stats.get("Stamina", 0)

    physical_power = attack_damage + strength + (dexterity // 2)
    magical_power = spell_damage + intellect
    base_offense = physical_power + magical_power

    offense = base_offense + haste

    return {
        "physical_power": physical_power,
        "magical_power": magical_power,
        "base_offense": base_offense,
        "haste_bonus": haste,
        "crit_stat": crit,
        "crushing_bonus": crushing * 2,
        "mitigation": armor + defense + (stamina // 2),
        "dodge_chance": dodge + evade + dodge_bonus,
        "slow_power": slow,
        "crushing_power": crushing,
        "offense_pre_rolls": offense
    }


def calculate_enemy_team_score(enemies, player_stats):
    total_score = 0
    enemy_breakdown = []

    for enemy in enemies:
        enemy_score = enemy.attack + enemy.defense + (enemy.health // 4) + (enemy.level * 2)

        if enemy.is_boss:
            enemy_score += 10

        enemy_breakdown.append({
            "name": enemy.name,
            "level": enemy.level,
            "score": enemy_score,
            "is_boss": enemy.is_boss
        })

        total_score += enemy_score

    slow_reduction = player_stats["slow_power"] * 2
    total_score -= slow_reduction

    crushing_reduction = 0
    if any(enemy.is_boss for enemy in enemies):
        crushing_reduction = player_stats["crushing_power"] * 3
        total_score -= crushing_reduction

    total_score = max(1, total_score)

    return total_score, enemy_breakdown, slow_reduction, crushing_reduction


def auto_fight(character, enemies, rng=None):
    rng = rng if rng is not None else random.Random()

    player_stats = get_player_combat_stats(character)

    crit_roll = rng.randint(1, 100)
    crit_triggered = crit_roll <= min(60, player_stats["crit_stat"] * 4)
    crit_bonus = max(2, player_stats["crit_stat"] * 2) if crit_triggered else 0

    offense = player_stats["offense_pre_rolls"] + crit_bonus + player_stats["crushing_bonus"]
    base_player_score = offense + player_stats["mitigation"]

    enemy_score, enemy_breakdown, slow_reduction, crushing_reduction = calculate_enemy_team_score(
        enemies,
        player_stats
    )

    player_score = base_player_score

    dodge_roll = rng.randint(1, 100)
    dodged = dodge_roll <= min(50, player_stats["dodge_chance"])
    dodge_bonus_applied = 6 if dodged else 0
    player_score += dodge_bonus_applied

    passive_bonus = 0
    if character.passive["type"] == "opening_attack":
        passive_bonus += 6
    elif character.passive["type"] == "reroll_bonus":
        passive_bonus += 2

    player_score += passive_bonus

    boss_present = any(enemy.is_boss for enemy in enemies)
    boss_bonus = 3 if boss_present else 0
    player_score += boss_bonus

    victory = player_score >= enemy_score

    return {
        "victory": victory,
        "player_score": player_score,
        "enemy_score": enemy_score,
        "dodged": dodged,
        "boss_present": boss_present,
        "crit_triggered": crit_triggered,
        "player_breakdown": {
            "physical_power": player_stats["physical_power"],
            "magical_power": player_stats["magical_power"],
            "base_offense": player_stats["base_offense"],
            "haste_bonus": player_stats["haste_bonus"],
            "crit_bonus": crit_bonus,
            "crushing_bonus": player_stats["crushing_bonus"],
            "mitigation": player_stats["mitigation"],
            "dodge_bonus_applied": dodge_bonus_applied,
            "passive_bonus": passive_bonus,
            "boss_bonus": boss_bonus
        },
        "enemy_breakdown": enemy_breakdown,
        "enemy_modifiers": {
            "slow_reduction": slow_reduction,
            "crushing_reduction": crushing_reduction
        }
    }