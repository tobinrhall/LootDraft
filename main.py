from generator.item_generator import ItemGenerator
from generator.enemy_generator import EnemyGenerator
from models.character import Character
from utils.display import (
    print_item,
    print_character,
    print_encounter,
    print_combat_result,
    print_item_comparison
)
from combat import auto_fight
GAME_VERSION = "0.1 Prototype"
def choose_class():
    valid_classes = ["Mage", "Warrior", "Rogue"]

    print("Choose your class:")
    for index, class_name in enumerate(valid_classes, start=1):
        print(f"{index}. {class_name}")

    while True:
        choice = input("Enter class name or number: ").strip()

        if choice in ["1", "2", "3"]:
            return valid_classes[int(choice) - 1]

        for class_name in valid_classes:
            if choice.lower() == class_name.lower():
                return class_name

        print("Invalid choice. Please choose Mage, Warrior, or Rogue.")


def ask_to_equip(character, item):
    current_item = character.get_equipped_item(item.slot)

    if current_item is None:
        comparison = character.compare_item_to_equipped(item)
        print_item_comparison(comparison)

        print(f"{item.slot} slot is empty. Equipping {item.name}.")
        character.equip_item(item)
        return

    comparison = character.compare_item_to_equipped(item)
    print_item_comparison(comparison)

    while True:
        choice = input("Replace current item? (y/n): ").strip().lower()

        if choice == "y":
            character.equip_item(item)
            print(f"{item.name} equipped.")
            return
        if choice == "n":
            print(f"Kept current {item.slot}.")
            return

        print("Please enter y or n.")

def show_item_choices(choices):
    print("\nChoose one item:\n")
    for i, item in enumerate(choices, start=1):
        print(f"Option {i}")
        print_item(item)


def run_draft_round(generator, character, item_level_wave, label="Draft Round"):
    print(f"\n=== {label} ===")

    choices = generator.generate_item_choices(
        count=3,
        class_tags=character.loot_tags,
        wave=item_level_wave
    )

    show_item_choices(choices)

    while True:
        selection = input("Select item (1-3) or 's' to skip: ").strip().lower()

        if selection == "s":
            print("You discard the items.\n")
            return

        if selection in ["1", "2", "3"]:
            chosen_item = choices[int(selection) - 1]
            ask_to_equip(character, chosen_item)
            return

        print("Invalid choice.")


def run_opening_draft(item_generator, character, opening_rounds=5):
    print("\n===== OPENING DRAFT PHASE =====")

    for draft_number in range(1, opening_rounds + 1):
        run_draft_round(
            item_generator,
            character,
            item_level_wave=draft_number,
            label=f"Opening Draft {draft_number}/{opening_rounds}"
        )
        print_character(character)

    print("===== OPENING DRAFT COMPLETE =====\n")


def run_game():
    item_generator = ItemGenerator()
    enemy_generator = EnemyGenerator()

    class_name = choose_class()
    character = Character(class_name)

    print_character(character)

    # Opening draft before any combat
    run_opening_draft(item_generator, character, opening_rounds=5)

    max_rounds = 25

    for round_number in range(1, max_rounds + 1):
        print(f"\n===== COMBAT ROUND {round_number} =====\n")
        print_character(character)

        enemies = enemy_generator.generate_encounter(round_number)
        print_encounter(round_number, enemies)

        input("Press Enter to auto-fight...")

        result = auto_fight(character, enemies)
        print_combat_result(result)

        if not result["victory"]:
            print(f"You were defeated on round {round_number}.")
            return

        print(f"You survived round {round_number}!")

        # Reward draft after each successful combat, except after final victory
        if round_number < max_rounds:
            run_draft_round(
                item_generator,
                character,
                item_level_wave=round_number + 1,
                label=f"Post-Combat Reward for Round {round_number}"
            )

    print("You conquered all 25 rounds. Victory!")


def main():
    while True:
        print("\n=== ACTION RPG DRAFT RUN ===")
        print("1. Start Run")
        print("2. Quit")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            run_game()
        elif choice == "2":
            print("Goodbye, adventurer.")
            break
        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()