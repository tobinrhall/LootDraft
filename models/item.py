class Item:
    def __init__(self, name, rarity, slot, stats, flavor_text="", item_level=1, item_tier="Crude"):
        self.name = name
        self.rarity = rarity
        self.slot = slot
        self.stats = stats
        self.flavor_text = flavor_text
        self.item_level = item_level
        self.item_tier = item_tier

    def __str__(self):
        if self.stats:
            stat_lines = "\n".join(
                [f"  - {stat}: {value}" for stat, value in self.stats.items()]
            )
        else:
            stat_lines = "  - None"

        return (
            f"{self.name}\n"
            f"Tier: {self.item_tier}\n"
            f"Item Level: {self.item_level}\n"
            f"Rarity: {self.rarity}\n"
            f"Slot: {self.slot}\n"
            f"Stats:\n{stat_lines}\n"
            f"{self.flavor_text}"
        )