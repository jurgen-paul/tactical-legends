#!/usr/bin/env python3
"""
Tactical Legends: Rise of the Oistarian
Welcome, Squad Configuration & Tactical Combat Simulation Engine.
"""

from __future__ import annotations
import sys
import time
import random
import argparse
from dataclasses import dataclass, field
from typing import List, Dict, Optional

# ANSI Color codes for tactical terminal output
class Colors:
    CYAN = "\033[96m"
    BLUE = "\033[94m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    MAGENTA = "\033[95m"
    BOLD = "\033[1m"
    DIM = "\033[2m"
    RESET = "\033[0m"

    @classmethod
    def strip(cls, text: str) -> str:
        for attr in dir(cls):
            if not attr.startswith("__") and isinstance(getattr(cls, attr), str):
                text = text.replace(getattr(cls, attr), "")
        return text


@dataclass
class SquadMember:
    name: str
    role: str
    level: int
    hp: int = 100
    gear: List[str] = field(default_factory=list)

    def __post_init__(self) -> None:
        self.hp = 100 + (self.level * 10)

    def add_gear(self, item: str) -> None:
        self.gear.append(item)

    def display_status(self) -> None:
        gear_str = ", ".join(self.gear) if self.gear else "None"
        print(f"  {Colors.BOLD}{self.name}{Colors.RESET} [{self.role}] | HP: {Colors.GREEN}{self.hp}{Colors.RESET} | Level: {Colors.YELLOW}{self.level}{Colors.RESET}")
        print(f"  {Colors.DIM}Gear: {gear_str}{Colors.RESET}")


@dataclass
class Squad:
    name: str
    doctrine: str
    members: List[SquadMember] = field(default_factory=list)
    relics: List[str] = field(default_factory=list)
    level: int = 1
    xp: int = 0


def print_banner() -> None:
    print(Colors.CYAN + "=" * 55)
    print(f"   {Colors.BOLD}⚔️  TACTICAL LEGENDS: RISE OF THE OISTARIAN ⚔️{Colors.RESET}")
    print(Colors.CYAN + "=" * 55 + Colors.RESET)
    print("Prepare to command elite squads, forge relics, and shape the fate of Oistaria.\n")


def simulate_initialization(fast: bool = False) -> None:
    print(f"{Colors.BLUE}[*] Initializing battlefield simulation...{Colors.RESET}")
    units = ["Recon Scout", "Frontline Vanguard", "Combat Medic", "Heavy Breacher", "Tech Saboteur"]
    for i, unit in enumerate(units, start=1):
        print(f"  -> Loading unit {i}/5: {Colors.BOLD}{unit}{Colors.RESET}...")
        if not fast:
            time.sleep(0.15)
    print(f"\n{Colors.GREEN}[+] All units deployed. Tactical systems online.{Colors.RESET}")
    print(f"{Colors.DIM}Let the legend begin...{Colors.RESET}\n")


def safe_input(prompt: str, default: str = "") -> str:
    """Read input safely, returning default if EOF or non-interactive."""
    try:
        if not sys.stdin.isatty():
            return default
        user_val = input(prompt).strip()
        return user_val if user_val else default
    except (EOFError, KeyboardInterrupt):
        print()
        return default


def select_squad(auto: bool = False) -> Squad:
    squad_options = {
        1: ("Sand Reapers", "Stealth and Sabotage"),
        2: ("Stormfront Directive", "Heavy Armor and Brute Force"),
        3: ("EchoCore Vanguard", "Balanced Tactics and Relic Fusion"),
    }

    print(f"{Colors.BOLD}--- SELECT YOUR SQUAD ---{Colors.RESET}")
    for num, (name, doctrine) in squad_options.items():
        print(f"  [{num}] {Colors.CYAN}{name}{Colors.RESET} – {doctrine}")

    choice_idx = 3
    if not auto and sys.stdin.isatty():
        choice_str = safe_input(f"\nEnter squad number (1-3) [{choice_idx}]: ", default=str(choice_idx))
        try:
            choice_idx = int(choice_str)
            if choice_idx not in squad_options:
                choice_idx = 3
        except ValueError:
            choice_idx = 3

    chosen_name, chosen_doctrine = squad_options[choice_idx]
    print(f"\n{Colors.GREEN}[+] Selected Squad: {Colors.BOLD}{chosen_name}{Colors.RESET} ({chosen_doctrine})\n")

    # Default squad members
    members = [
        SquadMember("Commander Arin", "Leader", level=3),
        SquadMember("Scout Nyra", "Recon", level=2),
        SquadMember("Heavy Drax", "Breacher", level=4),
    ]

    return Squad(name=chosen_name, doctrine=chosen_doctrine, members=members)


def gear_assignment(squad: Squad, auto: bool = False) -> None:
    gear_options = {
        "1": "EchoCore Blade",
        "2": "Eden Alloy Shield",
        "3": "Surge Beacon Relic",
        "4": "Disruption Smoke Grenade",
    }

    print(f"{Colors.BOLD}--- ARMORY: SQUAD LOADOUT ASSIGNMENT ---{Colors.RESET}")
    for member in squad.members:
        member.display_status()
        default_choice = "1"
        if not auto and sys.stdin.isatty():
            print(f"Select gear for {Colors.BOLD}{member.name}{Colors.RESET}:")
            for k, v in gear_options.items():
                print(f"  [{k}] {v}")
            user_choice = safe_input(f"Enter gear choice (1-4) [1]: ", default="1")
            selected_gear = gear_options.get(user_choice, "Basic Tactical Vest")
        else:
            # Automatic sensible loadouts
            defaults = {
                "Commander Arin": "EchoCore Blade",
                "Scout Nyra": "Surge Beacon Relic",
                "Heavy Drax": "Eden Alloy Shield",
            }
            selected_gear = defaults.get(member.name, "EchoCore Blade")

        member.add_gear(selected_gear)
        print(f"  -> {member.name} equipped with {Colors.CYAN}{selected_gear}{Colors.RESET}\n")


def relic_crafting_console(squad: Squad, auto: bool = False) -> None:
    print(f"{Colors.BOLD}--- RELIC FORGE CONSOLE ---{Colors.RESET}")
    print(f"Available components: {Colors.YELLOW}EchoCore{Colors.RESET}, {Colors.YELLOW}Eden Alloy{Colors.RESET}")
    print("Combine components to forge advanced tactical relics.\n")

    recipe = "EchoCore + Eden Alloy"
    if not auto and sys.stdin.isatty():
        prompt_text = "Combine two components (e.g. EchoCore + Eden Alloy): "
        recipe = safe_input(prompt_text, default="EchoCore + Eden Alloy")

    recipe_lower = recipe.lower()
    if "echocore" in recipe_lower and "eden alloy" in recipe_lower:
        relic = "Surge Beacon"
        squad.relics.append(relic)
        print(f"{Colors.GREEN}[+] Relic Forged: {Colors.BOLD}{relic}{Colors.RESET}")
        print(f"    {Colors.DIM}Grants tactical line-of-sight and +15% squad morale reflex boost.{Colors.RESET}\n")
    else:
        print(f"{Colors.YELLOW}[!] Non-standard mixture. Relic unstable, forge idle.{Colors.RESET}\n")


def run_mission_briefing() -> None:
    print(f"{Colors.BOLD}--- MISSION BRIEFING: OPERATION SAND ECHO ---{Colors.RESET}")
    print(f"  {Colors.CYAN}Sector:{Colors.RESET} Vault of Eden, Subterranean Perimeter")
    print(f"  {Colors.CYAN}Objective:{Colors.RESET} Secure the ancient Surge Beacon and neutralize hostile Dominion patrols.")
    print(f"  {Colors.CYAN}Environment:{Colors.RESET} Nightfall, sandstorm descent, visual range reduced to 5 tiles.\n")


def combat_simulation(squad: Squad, auto: bool = False) -> bool:
    print(f"{Colors.BOLD}--- TACTICAL ENGAGEMENT: SQUAD VS. HOSTILE PATROL ---{Colors.RESET}")
    player_hp = 100
    enemy_hp = 100
    turn = 1

    while player_hp > 0 and enemy_hp > 0:
        print(f"{Colors.BOLD}Turn {turn}{Colors.RESET} | Squad HP: {Colors.GREEN}{player_hp}{Colors.RESET}/100 | Enemy HP: {Colors.RED}{enemy_hp}{Colors.RESET}/100")

        action = 1
        if not auto and sys.stdin.isatty():
            print("Choose your tactical action:")
            print("  [1] Tactical Strike (Standard Damage)")
            print("  [2] Defensive Maneuver (Reduce Incoming Damage)")
            print("  [3] Activate Relic (Surge Beacon / Heavy Pulse)")
            action_input = safe_input("Enter action (1-3) [1]: ", default="1")
            try:
                action = int(action_input)
            except ValueError:
                action = 1
        else:
            # Smart auto AI: use relic if available, else strike
            if "Surge Beacon" in squad.relics and turn % 2 == 1:
                action = 3
            else:
                action = 1

        damage_to_enemy = 0
        damage_to_player = random.randint(8, 16)

        if action == 1:
            damage_to_enemy = random.randint(18, 28)
            print(f"  ⚔️  Your squad delivers a coordinated strike for {Colors.CYAN}{damage_to_enemy} damage{Colors.RESET}!")
        elif action == 2:
            damage_to_player = max(2, damage_to_player // 2)
            print(f"  🛡️  Your squad takes fortified cover. Incoming damage dampened to {Colors.YELLOW}{damage_to_player}{Colors.RESET}!")
        elif action == 3:
            damage_to_enemy = 32
            print(f"  ⚡  {Colors.MAGENTA}Surge Beacon activated!{Colors.RESET} Overwhelming shockwave deals {Colors.BOLD}{damage_to_enemy} damage{Colors.RESET}!")
        else:
            print("  [!] Hesitation in command. Standard attack deployed.")
            damage_to_enemy = 15

        enemy_hp = max(0, enemy_hp - damage_to_enemy)

        if enemy_hp > 0:
            player_hp = max(0, player_hp - damage_to_player)
            print(f"  💥  Enemy retaliates with pulse fire for {Colors.RED}{damage_to_player} damage{Colors.RESET}.\n")
        else:
            print(f"  💥  Enemy patrol eliminated!\n")

        turn += 1

    victory = player_hp > 0
    if victory:
        print(f"{Colors.GREEN}{Colors.BOLD}[🏆 VICTORY] The Surge Beacon is secured! Oistaria rises again.{Colors.RESET}")
        xp_earned = random.randint(60, 90)
        squad.xp += xp_earned
        print(f"Experience Gained: {Colors.YELLOW}+{xp_earned} XP{Colors.RESET}")
        if squad.xp >= 100:
            squad.level += 1
            squad.xp -= 100
            print(f"{Colors.CYAN}⭐ LEVEL UP! Squad {squad.name} is now Rank {squad.level}!{Colors.RESET}")
    else:
        print(f"{Colors.RED}{Colors.BOLD}[☠️ DEFEAT] Your squad was overwhelmed. Tactical withdrawal initiated.{Colors.RESET}")

    return victory


def display_codex_entry() -> None:
    print(f"\n{Colors.BOLD}--- CODEX RECORD: SURGE BEACON ---{Colors.RESET}")
    print("An ancient tactical relic discovered within the Vault of Eden.")
    print("When linked with neural augments, it broadcasts continuous operational feedback,")
    print("illuminates enemy heat signatures through sandstorms, and inspires allied resolve.")
    print(f"{Colors.DIM}Recovered during Operation Sand Echo by independent tactical commanders.{Colors.RESET}\n")


def save_progress(squad: Squad) -> None:
    print(f"{Colors.BOLD}--- SAVING MISSION LOG & SQUAD STATE ---{Colors.RESET}")
    print(f"  Squad:   {Colors.CYAN}{squad.name}{Colors.RESET}")
    print(f"  Rank:    Level {squad.level}")
    print(f"  XP:      {squad.xp}/100")
    print(f"  Relics:  {', '.join(squad.relics) if squad.relics else 'None'}")
    print(f"{Colors.GREEN}[✓] State synchronized. Standing by for next deployment, Commander.{Colors.RESET}\n")


def main() -> None:
    parser = argparse.ArgumentParser(description="Tactical Legends CLI & Welcome Engine")
    parser.add_argument("--auto", action="store_true", help="Run in non-interactive demo mode")
    parser.add_argument("--fast", action="store_true", help="Skip loading delays")
    args = parser.parse_args()

    # Automatically enable auto mode if running without a TTY
    auto_mode = args.auto or not sys.stdin.isatty()

    print_banner()
    simulate_initialization(fast=args.fast or auto_mode)

    squad = select_squad(auto=auto_mode)
    gear_assignment(squad, auto=auto_mode)
    relic_crafting_console(squad, auto=auto_mode)

    run_mission_briefing()
    combat_simulation(squad, auto=auto_mode)

    display_codex_entry()
    save_progress(squad)


if __name__ == "__main__":
    main()
