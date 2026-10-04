#!/usr/bin/env python3
"""Tactical Legends - Unified Python Runtime Launcher v2.0

This is the single entrypoint for the entire game. All systems
(combat, AI, narrative, missions, squads) run through this bootstrap.
"""

import sys
import argparse
from pathlib import Path

from core import TacticalEngine, NarrativeEngine, RichConsoleUI
from core.narrative import DialogueTree


def boot_engine() -> TacticalEngine:
    """Initialize and boot the unified tactical engine."""
    print("[Boot] Initializing Tactical Legends Engine v2.0...")
    engine = TacticalEngine()
    print(f"[Boot] World state loaded: {len(engine.world.factions)} factions, {len(engine.world.relics)} relics, {len(engine.world.missions)} missions")
    return engine


def show_mission_briefing(engine: TacticalEngine):
    """Display full mission briefing with dialogue."""
    RichConsoleUI.render_banner()
    RichConsoleUI.render_world_state(engine.world.factions, engine.world.relics)

    mission = engine.world.missions[engine.current_mission_index]
    RichConsoleUI.render_mission_briefing(mission)

    # Show dialogue tree
    narrative = NarrativeEngine()
    briefing_dialogue = DialogueTree.create_mission_briefing_dialogue()
    narrative.register_dialogue(briefing_dialogue)

    print("[Dialogue] Mission Commander Briefing:\n")
    current_node = narrative.start_dialogue("mission_briefing")
    while current_node:
        print(f"[{current_node.speaker}] {current_node.text}\n")
        if current_node.choices:
            for i, choice in enumerate(current_node.choices, 1):
                print(f"  {i}. {choice.text}")
            break
        elif current_node.auto_advance:
            current_node = briefing_dialogue.start(current_node.auto_advance)
        else:
            break


def show_squad_roster(engine: TacticalEngine):
    """Display squad roster."""
    RichConsoleUI.render_banner()
    from core.squad import Squad, SquadMember

    squad = Squad("alpha", "Oistarian Vanguard", "United Resistance Coalition")
    for i, name in enumerate(["Echo-27", "Gunwafa", "Nyla Sera", "Korr Vex"], 1):
        member = SquadMember(f"member_{i}", name, f"CS-{i:02d}", name.split()[0], level=3)
        squad.members.append(member)

    RichConsoleUI.render_squad_roster(squad)


def show_factions(engine: TacticalEngine):
    """Display all factions."""
    RichConsoleUI.render_banner()
    for faction in engine.world.factions:
        RichConsoleUI.render_faction_dossier(faction)


def show_relics(engine: TacticalEngine):
    """Display all relics."""
    RichConsoleUI.render_banner()
    for relic in engine.world.relics:
        RichConsoleUI.render_relic_card(relic)


def run_battle_simulation(engine: TacticalEngine):
    """Run a simulated battle and show status updates."""
    RichConsoleUI.render_banner()

    for turn in range(1, 6):
        engine.turn = turn
        engine.morale = max(20, engine.morale - 5)
        engine.intel += 15

        battle_data = engine.run_battle_summary()
        RichConsoleUI.render_battle_status(battle_data)

        if turn == 5:
            print("[Simulation] Battle resolved. Mission complete.\n")


def run_interactive_menu(engine: TacticalEngine):
    """Run interactive command menu."""
    RichConsoleUI.render_banner()

    commands = {
        "1": ("Show Mission Briefing", lambda: show_mission_briefing(engine)),
        "2": ("Show Squad Roster", lambda: show_squad_roster(engine)),
        "3": ("Show World Factions", lambda: show_factions(engine)),
        "4": ("Show Relics", lambda: show_relics(engine)),
        "5": ("Run Battle Simulation", lambda: run_battle_simulation(engine)),
        "q": ("Quit", lambda: sys.exit(0)),
    }

    while True:
        print("\n[Menu] Tactical Legends Command Console")
        for key, (desc, _) in commands.items():
            print(f"  {key}. {desc}")

        choice = input("\nEnter command: ").strip().lower()
        if choice in commands:
            _, func = commands[choice]
            func()
        else:
            print("[Error] Unknown command")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Tactical Legends: Rise of OISTARIAN - Unified Python Runtime v2.0",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("--briefing", action="store_true", help="Show mission briefing")
    parser.add_argument("--squad", action="store_true", help="Show squad roster")
    parser.add_argument("--factions", action="store_true", help="Show world factions")
    parser.add_argument("--relics", action="store_true", help="Show relics catalog")
    parser.add_argument("--simulate", action="store_true", help="Run battle simulation")
    parser.add_argument("--status", action="store_true", help="Show engine status")
    parser.add_argument("--interactive", "-i", action="store_true", help="Run interactive menu (default)")

    args = parser.parse_args()
    engine = boot_engine()

    if args.briefing:
        show_mission_briefing(engine)
    elif args.squad:
        show_squad_roster(engine)
    elif args.factions:
        show_factions(engine)
    elif args.relics:
        show_relics(engine)
    elif args.simulate:
        run_battle_simulation(engine)
    elif args.status:
        RichConsoleUI.render_banner()
        status = engine.status_snapshot()
        RichConsoleUI.render_api_response(status)
    else:
        # Default: interactive menu
        run_interactive_menu(engine)


if __name__ == "__main__":
    main()
