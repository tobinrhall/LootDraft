import random

from models.item import Item
from data.base_items import BASE_ITEMS
from data.affixes import PREFIXES, SUFFIXES, FLAVOR_TEXTS
from data.rarities import RARITIES
from data.item_levels import ITEM_LEVELS


class ItemGenerator:
    def __init__(self):
        self.base_items = BASE_ITEMS
        self.prefixes = PREFIXES
        self.suffixes = SUFFIXES
        self.flavor_texts = FLAVOR_TEXTS
        self.rarities = RARITIES
        self.item_levels = ITEM_LEVELS

    def roll_rarity(self, min_rarity=None):
        rarity_order = ["Common", "Magic", "Rare", "Legendary"]

        rarity_names = list(self.rarities.keys())
        rarity_weights = [self.rarities[rarity]["weight"] for rarity in rarity_names]

        if min_rarity is None:
            return random.choices(rarity_names, weights=rarity_weights, k=1)[0]

        min_index = rarity_order.index(min_rarity)
        allowed = rarity_order[min_index:]

        filtered_names = [r for r in rarity_names if r in allowed]
        filtered_weights = [self.rarities[r]["weight"] for r in filtered_names]

        return random.choices(filtered_names, weights=filtered_weights, k=1)[0]

    def roll_item_level(self, wave=1):
        min_level = max(1, 1 + (wave // 2))
        max_level = min(self.item_levels["max_level"], 5 + (wave * 2))
        return random.randint(min_level, max_level)

    def get_item_tier(self, item_level):
        for tier in self.item_levels["tiers"]:
            if tier["min"] <= item_level <= tier["max"]:
                return tier["name"]
        return "Crude"

    def roll_slot(self):
        return random.choice(list(self.base_items.keys()))

    def roll_base_item(self, slot, class_tags=None):
        items = self.base_items[slot]

        if not class_tags:
            return random.choice(items)

        weighted_items = []
        for item in items:
            item_tags = set(item["tags"])
            overlap = len(item_tags.intersection(set(class_tags)))
            weight = 1 + (overlap * 3)
            weighted_items.append(weight)

        return random.choices(items, weights=weighted_items, k=1)[0]

    def get_base_item_by_name(self, base_item_name):
        for slot, items in self.base_items.items():
            for item in items:
                if item["name"] == base_item_name:
                    return slot, item
        return None, None

    def affix_matches_item(self, affix, base_item, slot):
        item_tags = set(base_item["tags"])
        affix_tags = set(affix["tags"])
        slot_match = slot in affix["slots"]
        tag_match = len(item_tags.intersection(affix_tags)) > 0
        return slot_match and tag_match

    def get_valid_affixes(self, affix_pool, base_item, slot):
        valid_affixes = []

        for affix in affix_pool:
            if self.affix_matches_item(affix, base_item, slot):
                valid_affixes.append(affix)

        return valid_affixes

    def choose_weighted_affix(self, affixes, class_tags=None):
        if not affixes:
            return None

        if not class_tags:
            return random.choice(affixes)

        weights = []
        class_tag_set = set(class_tags)

        for affix in affixes:
            affix_tags = set(affix["tags"])
            overlap = len(affix_tags.intersection(class_tag_set))
            weight = 1 + (overlap * 3)
            weights.append(weight)

        return random.choices(affixes, weights=weights, k=1)[0]

    def roll_affixes(self, rarity, base_item, slot, class_tags=None):
        num_affixes = self.rarities[rarity]["num_affixes"]

        chosen_prefixes = []
        chosen_suffixes = []

        valid_prefixes = self.get_valid_affixes(self.prefixes, base_item, slot)
        valid_suffixes = self.get_valid_affixes(self.suffixes, base_item, slot)

        if num_affixes >= 1 and valid_prefixes:
            prefix = self.choose_weighted_affix(valid_prefixes, class_tags)
            if prefix:
                chosen_prefixes.append(prefix)

        if num_affixes >= 2 and valid_suffixes:
            suffix = self.choose_weighted_affix(valid_suffixes, class_tags)
            if suffix:
                chosen_suffixes.append(suffix)

        if num_affixes >= 3:
            extra_pool = valid_prefixes + valid_suffixes

            already_chosen_names = {
                affix["name"] for affix in chosen_prefixes + chosen_suffixes
            }

            remaining_affixes = [
                affix for affix in extra_pool
                if affix["name"] not in already_chosen_names
            ]

            extra_affix = self.choose_weighted_affix(remaining_affixes, class_tags)

            if extra_affix:
                if extra_affix in valid_prefixes:
                    chosen_prefixes.append(extra_affix)
                else:
                    chosen_suffixes.append(extra_affix)

        return chosen_prefixes, chosen_suffixes

    def build_name(self, base_item, prefixes, suffixes):
        prefix_names = " ".join(prefix["name"] for prefix in prefixes)
        suffix_names = " ".join(suffix["name"] for suffix in suffixes)

        if prefix_names and suffix_names:
            return f"{prefix_names} {base_item['name']} {suffix_names}"
        elif prefix_names:
            return f"{prefix_names} {base_item['name']}"
        elif suffix_names:
            return f"{base_item['name']} {suffix_names}"
        else:
            return base_item["name"]

    def get_level_multiplier(self, item_level):
        return 1 + ((item_level - 1) * 0.08)

    def build_base_stats(self, base_item, item_level):
        stats = {}
        multiplier = self.get_level_multiplier(item_level)

        for stat_name, stat_range in base_item["base_stats"].items():
            min_value, max_value = stat_range
            rolled_value = random.randint(min_value, max_value)
            scaled_value = max(1, round(rolled_value * multiplier))
            stats[stat_name] = scaled_value

        return stats

    def add_affix_stats(self, stats, affixes, item_level):
        multiplier = self.get_level_multiplier(item_level)

        for affix in affixes:
            stat_name = affix["stat"]
            rolled_value = random.randint(affix["min"], affix["max"])
            scaled_value = max(1, round(rolled_value * multiplier))

            if stat_name in stats:
                stats[stat_name] += scaled_value
            else:
                stats[stat_name] = scaled_value

    def build_item_from_base(self, slot, base_item, class_tags=None, wave=1, min_rarity=None):
        item_level = self.roll_item_level(wave)
        item_tier = self.get_item_tier(item_level)
        rarity = self.roll_rarity(min_rarity=min_rarity)
        prefixes, suffixes = self.roll_affixes(rarity, base_item, slot, class_tags)

        name = self.build_name(base_item, prefixes, suffixes)
        stats = self.build_base_stats(base_item, item_level)
        self.add_affix_stats(stats, prefixes, item_level)
        self.add_affix_stats(stats, suffixes, item_level)

        flavor_text = random.choice(self.flavor_texts)

        return Item(
            name=name,
            rarity=rarity,
            slot=slot,
            stats=stats,
            flavor_text=flavor_text,
            item_level=item_level,
            item_tier=item_tier
        )

    def generate_item(self, class_tags=None, wave=1, min_rarity=None):
        slot = self.roll_slot()
        base_item = self.roll_base_item(slot, class_tags)
        return self.build_item_from_base(
            slot=slot,
            base_item=base_item,
            class_tags=class_tags,
            wave=wave,
            min_rarity=min_rarity
        )

    def generate_item_choices(self, count=3, class_tags=None, wave=1, min_rarity=None):
        return [
            self.generate_item(class_tags=class_tags, wave=wave, min_rarity=min_rarity)
            for _ in range(count)
        ]

    def generate_starter_item(self, base_item_name, class_tags=None):
        slot, base_item = self.get_base_item_by_name(base_item_name)

        if slot is None or base_item is None:
            raise ValueError(f"Could not find base item named: {base_item_name}")

        return self.build_item_from_base(
            slot=slot,
            base_item=base_item,
            class_tags=class_tags,
            wave=1,
            min_rarity="Magic"
        )