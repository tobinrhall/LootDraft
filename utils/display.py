def print_item(item):
    print("\n" + "=" * 40)
    print("ITEM GENERATED")
    print("=" * 40)
    print(item)
    print("=" * 40 + "\n")


def print_character(character):
    print("\n" + "=" * 40)
    print("CHARACTER SHEET")
    print("=" * 40)
    print(character)
    print("=" * 40 + "\n")


def print_encounter(round_number, enemies):
    print("\n" + "=" * 40)
    print(f"ROUND {round_number} ENCOUNTER")
    print("=" * 40)

    for index, enemy in enumerate(enemies, start=1):
        print(f"Enemy {index}")
        print(enemy)
        print("-" * 30)

    print("=" * 40 + "\n")


def print_combat_result(result):
    print("\n" + "=" * 40)
    print("COMBAT RESULT")
    print("=" * 40)
    print(f"Victory: {'Yes' if result['victory'] else 'No'}")
    print(f"Player Score: {result['player_score']}")
    print(f"Enemy Score: {result['enemy_score']}")
    print(f"Dodged Key Hit: {'Yes' if result['dodged'] else 'No'}")
    print(f"Critical Burst: {'Yes' if result['crit_triggered'] else 'No'}")
    print(f"Boss Fight: {'Yes' if result['boss_present'] else 'No'}")
    print("=" * 40 + "\n")


def print_item_comparison(comparison):
    print("\n" + "=" * 40)
    print(f"ITEM COMPARISON - {comparison['slot']}")
    print("=" * 40)

    current_item = comparison["current_item"]
    new_item = comparison["new_item"]

    if current_item is None:
        print("Currently Equipped: Empty")
    else:
        print(f"Currently Equipped: {current_item.name}")

    print(f"Candidate Item: {new_item.name}")
    print("-" * 40)

    for stat_name, values in comparison["stat_deltas"].items():
        diff = values["diff"]

        if diff > 0:
            diff_text = f"+{diff}"
        elif diff < 0:
            diff_text = str(diff)
        else:
            diff_text = "0"

        print(
            f"{stat_name}: "
            f"{values['old']} -> {values['new']} "
            f"({diff_text})"
        )

    print("=" * 40 + "\n")