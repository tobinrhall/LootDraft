import tkinter as tk
from tkinter import ttk, messagebox

from generator.item_generator import ItemGenerator
from generator.enemy_generator import EnemyGenerator
from models.character import Character
from combat import auto_fight
from data.classes import CLASSES
from utils.app_state import load_app_state, save_app_state


RARITY_COLORS = {
    "Common": "#d9d9d9",
    "Magic": "#66a3ff",
    "Rare": "#ffd24d",
    "Legendary": "#ff9933"
}


class ToolTip:
    def __init__(self, widget, text_func):
        self.widget = widget
        self.text_func = text_func
        self.tipwindow = None

        widget.bind("<Enter>", self.show_tip)
        widget.bind("<Leave>", self.hide_tip)

    def show_tip(self, event=None):
        text = self.text_func()
        if not text:
            return

        if self.tipwindow is not None:
            return

        x = self.widget.winfo_rootx() + 20
        y = self.widget.winfo_rooty() + 20

        self.tipwindow = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(True)
        tw.wm_geometry(f"+{x}+{y}")

        label = tk.Label(
            tw,
            text=text,
            justify="left",
            background="#ffffe0",
            relief="solid",
            borderwidth=1,
            font=("Arial", 9),
            padx=6,
            pady=4
        )
        label.pack()

    def hide_tip(self, event=None):
        if self.tipwindow is not None:
            self.tipwindow.destroy()
            self.tipwindow = None


class ARPGGUI:
    def __init__(self, root, version):
        self.root = root
        self.root.title(f"ARPG Draft Builder - {version}")
        self.root.geometry("1550x980")

        self.item_generator = ItemGenerator()
        self.enemy_generator = EnemyGenerator()

        self.character = None
        self.round_number = 1
        self.max_rounds = 25
        self.current_items = []

        self.phase = "idle"
        self.opening_draft_total = 5
        self.opening_draft_current = 0

        self.selected_class = tk.StringVar(value="Warrior")
        self.equipment_slot_labels = {}
        self.next_reward_min_rarity = None
        self.last_combat_result = None
        self.pending_enemies = []
        self.current_preview_item = None

        self.app_state = load_app_state()

        self.create_layout()
        self.show_start_screen()
        
    def restart_to_intro(self):
        self.character = None
        self.round_number = 1
        self.current_items = []
        self.phase = "idle"
        self.opening_draft_current = 0
        self.next_reward_min_rarity = None
        self.last_combat_result = None
        self.pending_enemies = []
        self.current_preview_item = None

        self.hide_boss_banner()

        self.character_text.delete("1.0", tk.END)
        self.comparison_text.delete("1.0", tk.END)
        self.log_text.delete("1.0", tk.END)

        self.clear_item_cards()

        for slot_name, widgets in self.equipment_slot_labels.items():
            widgets["label"].config(text="Empty")
            widgets["frame"].config(bg="#f0f0f0", highlightthickness=0)
            widgets["title"].config(bg="#f0f0f0")
            widgets["icon"].config(bg="#f0f0f0")
            widgets["label"].config(bg="#f0f0f0")

        self.phase_text.config(text="No active run")
        self.status_label.config(
            text=f"Status: Idle | Best: {self.app_state.get('best_round', 0)}"
        )

        self.show_start_screen()
    # -------------------------
    # Layout
    # -------------------------

    def create_layout(self):
        self.main_frame = ttk.Frame(self.root, padding=10)
        self.main_frame.pack(fill="both", expand=True)

        self.main_frame.columnconfigure(0, weight=2)
        self.main_frame.columnconfigure(1, weight=2)
        self.main_frame.columnconfigure(2, weight=2)
        self.main_frame.rowconfigure(2, weight=1)

        self.create_top_bar()
        self.create_boss_banner()

        self.left_panel = ttk.Frame(self.main_frame)
        self.left_panel.grid(row=2, column=0, sticky="nswe", padx=(0, 10))

        self.center_panel = ttk.Frame(self.main_frame)
        self.center_panel.grid(row=2, column=1, sticky="nswe", padx=(0, 10))

        self.right_panel = ttk.Frame(self.main_frame)
        self.right_panel.grid(row=2, column=2, sticky="nswe")

        self.bottom_panel = ttk.Frame(self.main_frame)
        self.bottom_panel.grid(row=3, column=0, columnspan=3, sticky="ew", pady=(10, 0))

        self.create_character_panel()
        self.create_item_panel()
        self.create_comparison_panel()
        self.create_log_panel()

    def create_top_bar(self):
        top_bar = ttk.Frame(self.main_frame)
        top_bar.grid(row=0, column=0, columnspan=3, sticky="ew", pady=(0, 10))

        ttk.Label(top_bar, text="Class:").pack(side="left", padx=(0, 5))

        class_box = ttk.Combobox(
            top_bar,
            textvariable=self.selected_class,
            values=["Mage", "Warrior", "Rogue"],
            state="readonly",
            width=12
        )
        class_box.pack(side="left", padx=(0, 15))

        self.start_button = ttk.Button(top_bar, text="Start Run", command=self.start_run)
        self.start_button.pack(side="left", padx=(0, 10))

        self.legend_button = ttk.Button(top_bar, text="Stat Legend", command=self.show_stat_legend)
        self.legend_button.pack(side="left", padx=(0, 10))

        self.history_button = ttk.Button(top_bar, text="Run History", command=self.show_run_history)
        self.history_button.pack(side="left", padx=(0, 10))

        self.status_label = ttk.Label(top_bar, text="Status: Idle", font=("Arial", 11, "bold"))
        self.status_label.pack(side="right")

    def create_boss_banner(self):
        self.boss_banner = tk.Label(
            self.main_frame,
            text="⚠ BOSS ROUND ⚠",
            font=("Arial", 16, "bold"),
            bg="#8b0000",
            fg="white",
            pady=8
        )

    def show_boss_banner(self, text="⚠ BOSS ROUND ⚠", bg="#8b0000"):
        self.boss_banner.config(text=text, bg=bg)
        self.boss_banner.grid(row=1, column=0, columnspan=3, sticky="ew", pady=(0, 10))

    def hide_boss_banner(self):
        self.boss_banner.grid_forget()

    # -------------------------
    # Start Screen
    # -------------------------

    def show_start_screen(self):
        self.start_screen = tk.Toplevel(self.root)
        self.start_screen.title("Welcome")
        self.start_screen.geometry("520x420")
        self.start_screen.transient(self.root)
        self.start_screen.grab_set()

        frame = ttk.Frame(self.start_screen, padding=20)
        frame.pack(fill="both", expand=True)

        ttk.Label(
            frame,
            text="ARPG Draft Builder",
            font=("Arial", 20, "bold")
        ).pack(pady=(10, 20))

        ttk.Label(
            frame,
            text="Build your gear. Survive the arena.",
            font=("Arial", 11)
        ).pack(pady=(0, 20))

        best_round = self.app_state.get("best_round", 0)
        best_class = self.app_state.get("best_class", "None")

        ttk.Label(
            frame,
            text=f"Best Run: Round {best_round} ({best_class})",
            font=("Arial", 12, "bold")
        ).pack(pady=(0, 20))

        ttk.Label(frame, text="Choose Class:").pack()
        class_box = ttk.Combobox(
            frame,
            textvariable=self.selected_class,
            values=["Mage", "Warrior", "Rogue"],
            state="readonly",
            width=15
        )
        class_box.pack(pady=(5, 20))

        class_descriptions = (
            "Mage — high Intellect, extra reroll\n"
            "Warrior — high Strength/Stamina, opening attack bonus\n"
            "Rogue — high Dexterity, dodge bonus"
        )
        ttk.Label(frame, text=class_descriptions, justify="center").pack(pady=(0, 20))

        ttk.Button(frame, text="Start Adventure", command=self.begin_from_start_screen).pack(ipadx=12, ipady=6)

    def begin_from_start_screen(self):
        self.start_screen.destroy()
        self.start_run()

    # -------------------------
    # Character Panel
    # -------------------------

    def create_character_panel(self):
        ttk.Label(self.left_panel, text="Character", font=("Arial", 14, "bold")).pack(pady=5)

        self.character_text = tk.Text(self.left_panel, width=34, height=14, wrap="word")
        self.character_text.pack(fill="x", pady=(0, 10))

        ttk.Label(self.left_panel, text="Equipment Layout", font=("Arial", 13, "bold")).pack(pady=(5, 8))

        equip_frame = ttk.Frame(self.left_panel)
        equip_frame.pack(fill="both", expand=True)

        for col in range(3):
            equip_frame.columnconfigure(col, weight=1)

        self.create_slot_box(equip_frame, "Helmet", 0, 1)
        self.create_slot_box(equip_frame, "Weapon", 1, 0)
        self.create_slot_box(equip_frame, "Chest", 1, 1)
        self.create_slot_box(equip_frame, "Ring", 1, 2)
        self.create_slot_box(equip_frame, "Gloves", 2, 0)
        self.create_slot_box(equip_frame, "Belt", 2, 1)
        self.create_slot_box(equip_frame, "Amulet", 2, 2)
        self.create_slot_box(equip_frame, "Boots", 3, 1)

    def create_slot_box(self, parent, slot_name, row, col):
        frame = tk.Frame(parent, bd=2, relief="groove", padx=6, pady=6, bg="#f0f0f0")
        frame.grid(row=row, column=col, padx=6, pady=6, sticky="nsew")

        title = tk.Label(frame, text=slot_name, font=("Arial", 10, "bold"), bg="#f0f0f0")
        title.pack()

        icon = tk.Label(frame, text=self.get_slot_icon(slot_name), font=("Arial", 18), bg="#f0f0f0")
        icon.pack(pady=(4, 4))

        label = tk.Label(
            frame,
            text="Empty",
            wraplength=120,
            justify="center",
            bg="#f0f0f0"
        )
        label.pack()

        self.equipment_slot_labels[slot_name] = {
            "frame": frame,
            "label": label,
            "title": title,
            "icon": icon
        }

        ToolTip(frame, lambda s=slot_name: self.get_equipped_slot_tooltip(s))
        ToolTip(title, lambda s=slot_name: self.get_equipped_slot_tooltip(s))
        ToolTip(icon, lambda s=slot_name: self.get_equipped_slot_tooltip(s))
        ToolTip(label, lambda s=slot_name: self.get_equipped_slot_tooltip(s))

        frame.bind("<Enter>", lambda event, s=slot_name: self.preview_equipped_slot(s))
        frame.bind("<Button-1>", lambda event, s=slot_name: self.compare_preview_to_slot(s))
        title.bind("<Button-1>", lambda event, s=slot_name: self.compare_preview_to_slot(s))
        icon.bind("<Button-1>", lambda event, s=slot_name: self.compare_preview_to_slot(s))
        label.bind("<Button-1>", lambda event, s=slot_name: self.compare_preview_to_slot(s))

    def get_slot_icon(self, slot_name):
        icons = {
            "Weapon": "⚔",
            "Helmet": "⛑",
            "Chest": "🛡",
            "Boots": "👢",
            "Gloves": "🧤",
            "Belt": "▬",
            "Amulet": "📿",
            "Ring": "◌"
        }
        return icons.get(slot_name, "?")

    def update_equipment_layout(self):
        if not self.character:
            return

        for slot_name, widgets in self.equipment_slot_labels.items():
            item = self.character.get_equipped_item(slot_name)

            if item is None:
                widgets["label"].config(text="Empty")
                widgets["frame"].config(bg="#f0f0f0", highlightthickness=0)
                widgets["title"].config(bg="#f0f0f0")
                widgets["icon"].config(bg="#f0f0f0")
                widgets["label"].config(bg="#f0f0f0")
            else:
                widgets["label"].config(text=f"{item.name}\n({item.rarity})")
                color = RARITY_COLORS.get(item.rarity, "#f0f0f0")
                widgets["frame"].config(bg=color, highlightthickness=0)
                widgets["title"].config(bg=color)
                widgets["icon"].config(bg=color)
                widgets["label"].config(bg=color)

        self.highlight_matching_slot()

    def highlight_matching_slot(self):
        for slot_name, widgets in self.equipment_slot_labels.items():
            widgets["frame"].config(highlightthickness=0)

        if self.current_preview_item is None:
            return

        slot = self.current_preview_item.slot
        if slot in self.equipment_slot_labels:
            self.equipment_slot_labels[slot]["frame"].config(
                highlightbackground="green",
                highlightcolor="green",
                highlightthickness=3
            )

    def get_equipped_slot_tooltip(self, slot_name):
        if not self.character:
            return ""

        item = self.character.get_equipped_item(slot_name)

        if item is None:
            return f"{slot_name}\nEmpty"

        lines = [
            slot_name,
            item.name,
            f"Rarity: {item.rarity}",
            f"Tier: {item.item_tier}",
            f"Item Level: {item.item_level}",
            ""
        ]

        for stat_name, stat_value in item.stats.items():
            lines.append(f"{stat_name}: {stat_value}")

        return "\n".join(lines)

    def preview_equipped_slot(self, slot_name):
        if not self.character:
            return

        item = self.character.get_equipped_item(slot_name)
        lines = [f"Equipped Slot Preview: {slot_name}", ""]

        if item is None:
            lines.append("Currently Empty")
        else:
            lines.append(item.name)
            lines.append(f"Rarity: {item.rarity}")
            lines.append(f"Tier: {item.item_tier}")
            lines.append(f"Item Level: {item.item_level}")
            lines.append("")
            lines.append("Stats:")
            for stat_name, stat_value in item.stats.items():
                lines.append(f"  {stat_name}: {stat_value}")

        self.render_plain_text("\n".join(lines))

    def compare_preview_to_slot(self, slot_name):
        if not self.character or self.current_preview_item is None:
            return

        if self.current_preview_item.slot != slot_name:
            self.render_plain_text(
                f"Selected draft item goes in {self.current_preview_item.slot}.\n\n"
                f"You clicked {slot_name}."
            )
            return

        comparison = self.character.compare_item_to_equipped(self.current_preview_item)
        self.render_item_comparison(self.current_preview_item, comparison)

    # -------------------------
    # Center Panel
    # -------------------------

    def create_item_panel(self):
        ttk.Label(self.center_panel, text="Draft / Combat Flow", font=("Arial", 14, "bold")).pack(pady=5)

        self.phase_text = ttk.Label(self.center_panel, text="No active run", font=("Arial", 11))
        self.phase_text.pack(pady=(0, 8))

        self.center_mode_frame = ttk.Frame(self.center_panel)
        self.center_mode_frame.pack(fill="both", expand=True)

        self.draft_frame = ttk.Frame(self.center_mode_frame)
        self.draft_frame.pack(fill="both", expand=True)

        self.item_frames = []

        for i in range(3):
            outer = tk.Frame(self.draft_frame, bd=2, relief="groove", padx=6, pady=6)
            outer.pack(fill="x", pady=4)

            header = tk.Label(outer, text=f"Option {i + 1}", font=("Arial", 11, "bold"))
            header.pack(anchor="w")

            text = tk.Text(outer, height=8, width=48, wrap="word")
            text.pack(fill="x", pady=4)

            btn_frame = ttk.Frame(outer)
            btn_frame.pack(fill="x")

            preview_button = ttk.Button(
                btn_frame,
                text="Preview",
                command=lambda i=i: self.preview_item(i)
            )
            preview_button.pack(side="left", padx=(0, 5))

            choose_button = ttk.Button(
                btn_frame,
                text="Choose Item",
                command=lambda i=i: self.choose_item(i)
            )
            choose_button.pack(side="left", padx=(0, 5))

            skip_button = ttk.Button(
                btn_frame,
                text="Skip",
                command=self.skip_draft_choice
            )
            skip_button.pack(side="left")

            self.item_frames.append({
                "outer": outer,
                "header": header,
                "text": text,
                "preview_button": preview_button,
                "choose_button": choose_button,
                "skip_button": skip_button
            })

            ToolTip(outer, lambda i=i: self.get_item_tooltip(i))
            ToolTip(header, lambda i=i: self.get_item_tooltip(i))
            ToolTip(text, lambda i=i: self.get_item_tooltip(i))

        self.combat_ready_frame = ttk.Frame(self.center_mode_frame)

        self.combat_ready_label = ttk.Label(
            self.combat_ready_frame,
            text="Combat Ready",
            font=("Arial", 16, "bold")
        )
        self.combat_ready_label.pack(pady=(40, 20))

        self.combat_ready_info = ttk.Label(
            self.combat_ready_frame,
            text="",
            font=("Arial", 11),
            justify="center"
        )
        self.combat_ready_info.pack(pady=(0, 20))

        self.next_button = ttk.Button(
            self.combat_ready_frame,
            text="Continue Combat",
            command=self.continue_after_draft
        )
        self.next_button.pack(ipadx=20, ipady=10)

    def format_item_card_text(self, item):
        lines = [
            f"{item.name}",
            f"Slot: {item.slot}",
            f"Rarity: {item.rarity}    Tier: {item.item_tier}",
            f"Item Level: {item.item_level}",
            "",
            "Stats:"
        ]

        for stat_name, stat_value in item.stats.items():
            lines.append(f"  {stat_name}: {stat_value}")

        return "\n".join(lines)

    def get_item_tooltip(self, index):
        if not self.current_items or index >= len(self.current_items):
            return ""

        item = self.current_items[index]

        lines = [
            item.name,
            f"Rarity: {item.rarity}",
            f"Tier: {item.item_tier}",
            f"Item Level: {item.item_level}",
            f"Slot: {item.slot}",
            ""
        ]

        for stat_name, stat_value in item.stats.items():
            lines.append(f"{stat_name}: {stat_value}")

        return "\n".join(lines)

    def show_draft_view(self):
        self.combat_ready_frame.pack_forget()
        self.draft_frame.pack(fill="both", expand=True)

    def show_combat_ready_view(self, message_text, button_text="Continue Combat", button_command=None):
        self.draft_frame.pack_forget()
        self.combat_ready_info.config(text=message_text)

        self.next_button.config(text=button_text)

        if button_command is None:
            self.next_button.config(command=self.continue_after_draft)
        else:
            self.next_button.config(command=button_command)

        self.combat_ready_frame.pack(fill="both", expand=True)

    def clear_item_cards(self):
        self.current_items = []
        self.current_preview_item = None

        for widgets in self.item_frames:
            widgets["text"].delete("1.0", tk.END)
            widgets["outer"].config(bg=self.root.cget("bg"))
            widgets["header"].config(bg=self.root.cget("bg"))
            widgets["text"].config(bg="white")

        self.highlight_matching_slot()

    # -------------------------
    # Comparison Panel
    # -------------------------

    def create_comparison_panel(self):
        ttk.Label(self.right_panel, text="Comparison / Encounter", font=("Arial", 14, "bold")).pack(pady=5)

        self.comparison_text = tk.Text(self.right_panel, width=48, height=34, wrap="word")
        self.comparison_text.pack(fill="both", expand=True)

        self.comparison_text.tag_configure("positive", foreground="green")
        self.comparison_text.tag_configure("negative", foreground="red")
        self.comparison_text.tag_configure("neutral", foreground="black")
        self.comparison_text.tag_configure("heading", font=("Arial", 10, "bold"))

    def render_plain_text(self, text):
        self.comparison_text.delete("1.0", tk.END)
        self.comparison_text.insert(tk.END, text)

    def render_item_comparison(self, item, comparison):
        self.comparison_text.delete("1.0", tk.END)

        self.comparison_text.insert(tk.END, "Candidate Item\n", "heading")
        self.comparison_text.insert(tk.END, f"{item.name}\n")
        self.comparison_text.insert(tk.END, f"Rarity: {item.rarity}\n")
        self.comparison_text.insert(tk.END, f"Tier: {item.item_tier}\n")
        self.comparison_text.insert(tk.END, f"Item Level: {item.item_level}\n")
        self.comparison_text.insert(tk.END, f"Slot: {item.slot}\n\n")

        self.comparison_text.insert(tk.END, "Currently Equipped:\n", "heading")
        current_item = comparison["current_item"]
        if current_item is None:
            self.comparison_text.insert(tk.END, "  Empty\n\n")
        else:
            self.comparison_text.insert(
                tk.END,
                f"  {current_item.name} ({current_item.rarity}, ilvl {current_item.item_level})\n\n"
            )

        self.comparison_text.insert(tk.END, "Stat Comparison:\n", "heading")

        for stat_name, values in comparison["stat_deltas"].items():
            diff = values["diff"]
            if diff > 0:
                diff_text = f"+{diff}"
                tag = "positive"
            elif diff < 0:
                diff_text = str(diff)
                tag = "negative"
            else:
                diff_text = "0"
                tag = "neutral"

            self.comparison_text.insert(
                tk.END,
                f"  {stat_name}: {values['old']} -> {values['new']} ",
                "neutral"
            )
            self.comparison_text.insert(tk.END, f"({diff_text})\n", tag)

    # -------------------------
    # Log Panel
    # -------------------------

    def create_log_panel(self):
        ttk.Label(self.bottom_panel, text="Run Log", font=("Arial", 12, "bold")).pack(anchor="w")

        self.log_text = tk.Text(self.bottom_panel, height=10, wrap="word")
        self.log_text.pack(fill="x", expand=True)

    # -------------------------
    # Run Control
    # -------------------------

    def start_run(self):
        class_name = self.selected_class.get().strip()
        if class_name not in ["Mage", "Warrior", "Rogue"]:
            messagebox.showerror("Invalid Class", "Please choose Mage, Warrior, or Rogue.")
            return

        self.character = Character(class_name)
        self.round_number = 1
        self.phase = "opening_draft"
        self.opening_draft_current = 1
        self.next_reward_min_rarity = None
        self.last_combat_result = None
        self.pending_enemies = []

        self.log_text.delete("1.0", tk.END)
        self.comparison_text.delete("1.0", tk.END)

        self.hide_boss_banner()
        self.next_button.config(text="Continue Combat", command=self.continue_after_draft)

        self.log(f"Started new run as {class_name}.")
        self.log("Opening draft phase begins.")

        starter_weapon_name = CLASSES[class_name]["starter_weapon"]
        starter_item = self.item_generator.generate_starter_item(
            starter_weapon_name,
            class_tags=self.character.loot_tags
        )
        self.character.equip_item(starter_item)
        self.log(f"Starter item equipped: {starter_item.name}")

        self.update_character_display()
        self.update_equipment_layout()
        self.update_status()
        self.show_draft_choices()

    def update_status(self):
        if self.phase == "opening_draft":
            status = f"Opening Draft {self.opening_draft_current}/{self.opening_draft_total}"
        elif self.phase == "reward_draft":
            status = f"Reward Draft after Round {self.round_number}"
        elif self.phase == "awaiting_combat":
            status = f"Ready for Combat Round {self.round_number}"
        elif self.phase == "game_over":
            status = "Game Over"
        elif self.phase == "victory":
            status = "Victory"
        else:
            status = "Idle"

        best_round = self.app_state.get("best_round", 0)
        self.status_label.config(text=f"Status: {status} | Best: {best_round}")
        self.phase_text.config(text=status)

    def update_best_run(self):
        if self.round_number > self.app_state.get("best_round", 0):
            self.app_state["best_round"] = self.round_number
            self.app_state["best_class"] = self.character.class_name if self.character else "None"
            save_app_state(self.app_state)

    # -------------------------
    # Draft Flow
    # -------------------------

    def show_draft_choices(self):
        if not self.character:
            return

        self.hide_boss_banner()
        self.show_draft_view()

        wave_value = self.round_number
        if self.phase == "opening_draft":
            wave_value = self.opening_draft_current

        self.current_items = self.item_generator.generate_item_choices(
            count=3,
            class_tags=self.character.loot_tags,
            wave=wave_value,
            min_rarity=self.next_reward_min_rarity
        )

        if self.next_reward_min_rarity is not None:
            self.log(f"Special reward draft: {self.next_reward_min_rarity}+ items guaranteed.")
            self.show_boss_banner("★ BOSS REWARD DRAFT: RARE OR BETTER ★", "#6b4f00")
            self.next_reward_min_rarity = None

        for i, widgets in enumerate(self.item_frames):
            item = self.current_items[i]
            text_widget = widgets["text"]
            outer = widgets["outer"]

            text_widget.delete("1.0", tk.END)
            text_widget.insert(tk.END, self.format_item_card_text(item))

            rarity_color = RARITY_COLORS.get(item.rarity, "#d9d9d9")
            outer.config(bg=rarity_color)
            widgets["header"].config(bg=rarity_color)
            text_widget.config(bg=rarity_color)

        self.preview_item(0)

    def preview_item(self, index):
        if not self.character or not self.current_items:
            return

        item = self.current_items[index]
        self.current_preview_item = item
        self.highlight_matching_slot()

        comparison = self.character.compare_item_to_equipped(item)
        self.render_item_comparison(item, comparison)

    def choose_item(self, index):
        if not self.character or not self.current_items:
            return

        item = self.current_items[index]
        current = self.character.get_equipped_item(item.slot)

        if current is not None:
            replace = messagebox.askyesno(
                "Replace Item?",
                f"Replace {current.name} with {item.name}?"
            )
            if not replace:
                self.log(f"Kept current {item.slot}.")
                return

        self.character.equip_item(item)
        self.log(f"Equipped {item.name} in {item.slot}.")
        self.update_character_display()
        self.update_equipment_layout()

        self.clear_item_cards()

        if self.phase == "opening_draft":
            if self.opening_draft_current < self.opening_draft_total:
                self.opening_draft_current += 1
                self.update_status()
                self.show_draft_choices()
            else:
                self.phase = "awaiting_combat"
                self.update_status()
                self.show_encounter_preview()
                self.show_combat_ready_view(
                    f"Opening draft complete.\n\nReady for Combat Round {self.round_number}."
                )
        elif self.phase == "reward_draft":
            self.phase = "awaiting_combat"
            self.round_number += 1

            if self.round_number > self.max_rounds:
                self.phase = "victory"
                self.update_best_run()
                self.update_status()
                self.show_run_summary(victory=True)
                messagebox.showinfo("Victory", "You conquered all 25 rounds!")
                self.log("Victory! You conquered all 25 rounds.")
                return

            self.update_status()
            self.show_encounter_preview()
            self.show_combat_ready_view(
                f"Reward draft complete.\n\nReady for Combat Round {self.round_number}."
            )

    def skip_draft_choice(self):
        if not self.character:
            return

        self.log("Skipped draft reward.")
        self.clear_item_cards()

        if self.phase == "opening_draft":
            if self.opening_draft_current < self.opening_draft_total:
                self.opening_draft_current += 1
                self.update_status()
                self.show_draft_choices()
            else:
                self.phase = "awaiting_combat"
                self.update_status()
                self.show_encounter_preview()
                self.show_combat_ready_view(
                    f"Opening draft complete.\n\nReady for Combat Round {self.round_number}."
                )
        elif self.phase == "reward_draft":
            self.phase = "awaiting_combat"
            self.round_number += 1

            if self.round_number > self.max_rounds:
                self.phase = "victory"
                self.update_best_run()
                self.update_status()
                self.show_run_summary(victory=True)
                messagebox.showinfo("Victory", "You conquered all 25 rounds!")
                self.log("Victory! You conquered all 25 rounds.")
                return

            self.update_status()
            self.show_encounter_preview()
            self.show_combat_ready_view(
                f"Reward skipped.\n\nReady for Combat Round {self.round_number}."
            )

    def continue_after_draft(self):
        if self.phase != "awaiting_combat":
            return
        self.run_combat_round()

    # -------------------------
    # Combat Flow
    # -------------------------

    def show_encounter_preview(self):
        enemies = self.enemy_generator.generate_encounter(self.round_number)
        self.pending_enemies = enemies

        if any(enemy.is_boss for enemy in enemies):
            self.show_boss_banner()
        else:
            self.hide_boss_banner()

        lines = []
        lines.append(f"Upcoming Combat Round {self.round_number}\n")

        for idx, enemy in enumerate(enemies, start=1):
            boss_text = "Boss" if enemy.is_boss else "Normal"
            lines.append(f"Enemy {idx}: {enemy.name} ({boss_text})")
            lines.append(f"  Level: {enemy.level}")
            lines.append(f"  Health: {enemy.health}")
            lines.append(f"  Attack: {enemy.attack}")
            lines.append(f"  Defense: {enemy.defense}")
            lines.append(f"  Dodge: {enemy.dodge}")
            lines.append("")

        self.render_plain_text("\n".join(lines))
        self.log(f"Prepared encounter for round {self.round_number}.")

    def run_combat_round(self):
        if not self.pending_enemies:
            self.show_encounter_preview()

        enemies = self.pending_enemies
        result = auto_fight(self.character, enemies)
        self.last_combat_result = result

        enemy_names = ", ".join(enemy.name for enemy in enemies)
        self.log(f"Round {self.round_number} encounter: {enemy_names}")
        self.log(
            f"Combat result: {'Victory' if result['victory'] else 'Defeat'} | "
            f"Player Score {result['player_score']} vs Enemy Score {result['enemy_score']}"
        )

        if result["dodged"]:
            self.log("You dodged a key hit.")
        if result.get("crit_triggered"):
            self.log("Critical burst triggered.")
        if result["boss_present"]:
            self.log("Boss fight completed.")

        self.show_fight_summary(result, enemies)

        if not result["victory"]:
            self.phase = "game_over"
            self.update_best_run()
            self.update_status()
            self.show_combat_ready_view(
                f"You were defeated on round {self.round_number}.",
                button_text="Start Over",
                button_command=self.restart_to_intro
            )
            self.show_run_summary(victory=False)
            messagebox.showinfo("Run Ended", f"You were defeated on round {self.round_number}.")
            return

        if self.round_number == self.max_rounds:
            self.phase = "victory"
            self.update_best_run()
            self.update_status()
            self.show_combat_ready_view(
                "Victory!\n\nYou conquered all 25 rounds!",
                button_text="Start Over",
                button_command=self.restart_to_intro
            )
            self.show_run_summary(victory=True)
            messagebox.showinfo("Victory", "You conquered all 25 rounds!")
            self.log("Victory! You conquered all 25 rounds.")
            return

        self.phase = "reward_draft"

        if result["boss_present"]:
            self.next_reward_min_rarity = "Rare"
            self.log("Boss reward unlocked: next draft is guaranteed Rare or better.")

        self.update_best_run()
        self.update_status()
        self.log(f"Round {self.round_number} cleared. Reward draft begins.")
        self.show_draft_choices()

    # -------------------------
    # Summary / Popups
    # -------------------------

    def show_fight_summary(self, result, enemies):
        lines = []
        lines.append(f"Fight Summary - Round {self.round_number}\n")

        lines.append("Enemies:")
        for enemy in enemies:
            boss_text = "Boss" if enemy.is_boss else "Normal"
            lines.append(
                f"  {enemy.name} ({boss_text}) - "
                f"Lvl {enemy.level}, HP {enemy.health}, ATK {enemy.attack}, DEF {enemy.defense}, DODGE {enemy.dodge}"
            )

        lines.append("")
        lines.append("Player Breakdown:")
        pb = result["player_breakdown"]
        lines.append(f"  Physical Power: {pb['physical_power']}")
        lines.append(f"  Magical Power: {pb['magical_power']}")
        lines.append(f"  Base Offense: {pb['base_offense']}")
        lines.append(f"  Haste Bonus: {pb['haste_bonus']}")
        lines.append(f"  Crit Bonus: {pb['crit_bonus']}")
        lines.append(f"  Crushing Bonus: {pb['crushing_bonus']}")
        lines.append(f"  Mitigation: {pb['mitigation']}")
        lines.append(f"  Dodge Bonus Applied: {pb['dodge_bonus_applied']}")
        lines.append(f"  Passive Bonus: {pb['passive_bonus']}")
        lines.append(f"  Boss Bonus: {pb['boss_bonus']}")

        lines.append("")
        lines.append("Enemy Breakdown:")
        for enemy_data in result["enemy_breakdown"]:
            boss_text = "Boss" if enemy_data["is_boss"] else "Normal"
            lines.append(
                f"  {enemy_data['name']} ({boss_text}) - "
                f"Level {enemy_data['level']} Score Contribution: {enemy_data['score']}"
            )

        lines.append("")
        lines.append("Enemy Modifiers:")
        lines.append(f"  Slow Reduction: {result['enemy_modifiers']['slow_reduction']}")
        lines.append(f"  Crushing Reduction: {result['enemy_modifiers']['crushing_reduction']}")

        lines.append("")
        lines.append(f"Final Player Score: {result['player_score']}")
        lines.append(f"Final Enemy Score: {result['enemy_score']}")
        lines.append(f"Critical Burst: {'Yes' if result['crit_triggered'] else 'No'}")
        lines.append(f"Dodged Key Hit: {'Yes' if result['dodged'] else 'No'}")
        lines.append(f"Victory: {'Yes' if result['victory'] else 'No'}")

        messagebox.showinfo("Fight Summary", "\n".join(lines))

    def show_run_summary(self, victory=False):
        if not self.character:
            return

        summary = tk.Toplevel(self.root)
        summary.title("Run Summary")
        summary.geometry("700x700")

        title_text = "Victory Summary" if victory else "Run Summary"
        title = ttk.Label(summary, text=title_text, font=("Arial", 16, "bold"))
        title.pack(pady=10)

        text = tk.Text(summary, wrap="word")
        text.pack(fill="both", expand=True, padx=10, pady=10)

        lines = []
        lines.append(f"Class: {self.character.class_name}")
        lines.append(f"Result: {'Victory' if victory else 'Defeat'}")
        lines.append(f"Rounds Reached: {self.round_number}")
        lines.append("")

        lines.append("Equipped Items:")
        for slot, item in self.character.equipment.items():
            if item is None:
                lines.append(f"  {slot}: Empty")
            else:
                lines.append(f"  {slot}: {item.name} ({item.rarity}, ilvl {item.item_level})")

        lines.append("")
        lines.append("Final Stats:")
        total_stats = self.character.get_total_stats()
        for stat_name, stat_value in total_stats.items():
            lines.append(f"  {stat_name}: {stat_value}")

        text.insert(tk.END, "\n".join(lines))
        text.config(state="disabled")

    def show_run_history(self):
        history = tk.Toplevel(self.root)
        history.title("Run History")
        history.geometry("900x600")

        frame = ttk.Frame(history, padding=10)
        frame.pack(fill="both", expand=True)

        text = tk.Text(frame, wrap="word")
        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=text.yview)
        text.config(yscrollcommand=scrollbar.set)

        scrollbar.pack(side="right", fill="y")
        text.pack(side="left", fill="both", expand=True)

        log_contents = self.log_text.get("1.0", tk.END)
        text.insert(tk.END, log_contents)
        text.config(state="disabled")

    # -------------------------
    # Character Display
    # -------------------------

    def update_character_display(self):
        if not self.character:
            return

        self.character_text.delete("1.0", tk.END)
        self.character_text.insert(tk.END, str(self.character))

    # -------------------------
    # Utilities
    # -------------------------

    def log(self, text):
        self.log_text.insert(tk.END, text + "\n")
        self.log_text.see(tk.END)

    def show_stat_legend(self):
        legend = (
            "Strength — increases physical power\n"
            "Dexterity — improves agility and crit potential\n"
            "Intellect — increases magical power\n"
            "Stamina — improves survivability\n\n"
            "Attack Damage — boosts physical offense\n"
            "Spell Damage — boosts magical offense\n"
            "Armor — reduces incoming damage\n"
            "Defense — increases toughness\n"
            "Dodge — chance to avoid damage\n"
            "Evade — additional avoidance\n"
            "Crit Chance — chance to trigger burst damage\n"
            "Haste — increases offensive pressure\n"
            "Crushing Blow — stronger against bosses\n"
            "Slow — weakens enemy effectiveness"
        )
        messagebox.showinfo("Stat Legend", legend)