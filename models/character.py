from data.classes import CLASSES


class Character:
    def __init__(self, class_name):
        if class_name not in CLASSES:
            raise ValueError(f"Invalid class name: {class_name}")

        class_data = CLASSES[class_name]

        self.class_name = class_name
        self.base_stats = class_data["base_stats"].copy()
        self.passive = class_data["passive"]
        self.loot_tags = class_data["loot_tags"]

        self.equipment = {
            "Weapon": None,
            "Helmet": None,
            "Chest": None,
            "Boots": None,
            "Gloves": None,
            "Belt": None,
            "Amulet": None,
            "Ring": None
        }

        self.rerolls = 5 + self.get_reroll_bonus()

    def get_reroll_bonus(self):
        if self.passive["type"] == "reroll_bonus":
            return self.passive["value"]
        return 0

    def equip_item(self, item):
        slot = item.slot
        if slot not in self.equipment:
            raise ValueError(f"Invalid equipment slot: {slot}")

        old_item = self.equipment[slot]
        self.equipment[slot] = item
        return old_item

    def unequip_item(self, slot):
        if slot not in self.equipment:
            raise ValueError(f"Invalid equipment slot: {slot}")

        old_item = self.equipment[slot]
        self.equipment[slot] = None
        return old_item

    def get_total_stats(self):
        total_stats = self.base_stats.copy()

        for equipped_item in self.equipment.values():
            if equipped_item is None:
                continue

            for stat_name, stat_value in equipped_item.stats.items():
                if stat_name in total_stats:
                    total_stats[stat_name] += stat_value
                else:
                    total_stats[stat_name] = stat_value

        if self.passive["type"] == "dodge_bonus_percent":
            passive_stat = "Dodge Chance Bonus"
            total_stats[passive_stat] = total_stats.get(passive_stat, 0) + self.passive["value"]

        return total_stats

    def get_equipped_item(self, slot):
        if slot not in self.equipment:
            raise ValueError(f"Invalid equipment slot: {slot}")
        return self.equipment[slot]

    def compare_item_to_equipped(self, new_item):
        current_item = self.get_equipped_item(new_item.slot)

        current_stats = current_item.stats if current_item else {}
        new_stats = new_item.stats if new_item else {}

        all_stat_names = sorted(set(current_stats.keys()) | set(new_stats.keys()))
        comparison = {}

        for stat_name in all_stat_names:
            old_value = current_stats.get(stat_name, 0)
            new_value = new_stats.get(stat_name, 0)
            difference = new_value - old_value

            comparison[stat_name] = {
                "old": old_value,
                "new": new_value,
                "diff": difference
            }

        return {
            "slot": new_item.slot,
            "current_item": current_item,
            "new_item": new_item,
            "stat_deltas": comparison
        }

    def __str__(self):
        lines = [
            f"Class: {self.class_name}",
            f"Passive: {self.passive['name']} - {self.passive['description']}",
            f"Loot Bias: {', '.join(self.loot_tags)}",
            f"Rerolls: {self.rerolls}",
            "",
            "Equipped Items:"
        ]

        for slot, item in self.equipment.items():
            if item is None:
                lines.append(f"  - {slot}: Empty")
            else:
                lines.append(f"  - {slot}: {item.name} ({item.rarity}, ilvl {item.item_level})")

        lines.append("")
        lines.append("Total Stats:")

        total_stats = self.get_total_stats()
        for stat_name, stat_value in total_stats.items():
            lines.append(f"  - {stat_name}: {stat_value}")

        return "\n".join(lines)