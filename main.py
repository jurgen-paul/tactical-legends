#!/usr/bin/env python3
"""Tactical Legends unified Python runtime.

This launcher acts as the single-language entrypoint for the project,
building the game around the Python engine rather than a mixed runtime.
"""

import argparse
import json
import sys
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any

from core import TacticalEngine
from core.combat import Combatant, Position, UnitClass
from core.ai import AIAgent

BASE_DIR = Path(__file__).resolve().parent


def build_demo_engine() -> TacticalEngine:
    """Create a ready-to-run engine instance for demo and server usage."""
    engine = TacticalEngine()
    engine.initialize()

    # Load a default mission and squad.
    squad = engine.squad_manager.create_default_squad()
    engine.active_squad = squad
    available_missions = engine.mission_manager.get_available_missions()
    if available_missions:
        engine.load_mission(available_missions[0].id)
        engine.start_mission()

    # Create a small combat demo board.
    combat = engine.combat_system
    player_units = [
        Combatant("p1", "Oistarian", UnitClass.TACTICAL_COMMANDER, "player", Position(1, 1), max_hp=120, hp=120, max_shields=60, shields=60, attack=18, defense=12, accuracy=0.9),
        Combatant("p2", "Gunwafa", UnitClass.HEAVY_ASSAULT, "player", Position(1, 3), max_hp=130, hp=130, max_shields=50, shields=50, attack=20, defense=10, accuracy=0.85),
        Combatant("p3", "Nyla", UnitClass.STEALTH_OPERATIVE, "player", Position(2, 2), max_hp=100, hp=100, max_shields=40, shields=40, attack=16, defense=9, accuracy=0.92),
    ]
    enemy_units = [
        Combatant("e1", "Dominion Enforcer", UnitClass.HEAVY_ASSAULT, "enemy", Position(7, 1), max_hp=100, hp=100, max_shields=45, shields=45, attack=17, defense=9, accuracy=0.8),
        Combatant("e2", "Holo Hunter", UnitClass.STEALTH_OPERATIVE, "enemy", Position(7, 4), max_hp=95, hp=95, max_shields=35, shields=35, attack=15, defense=8, accuracy=0.78),
    ]

    for unit in player_units + enemy_units:
        combat.add_combatant(unit)

    for enemy in enemy_units:
        ai_agent = AIAgent(enemy)
        ai_agent.set_behavior_tree(engine.ai_engine.create_enemy_behavior("normal"))
        engine.ai_engine.register_agent(enemy.id, ai_agent)

    return engine


APP_ENGINE = build_demo_engine()


class TacticalLegendsHandler(BaseHTTPRequestHandler):
    """Minimal Python HTTP API for the unified runtime."""

    def do_GET(self):  # noqa: N802
        if self.path in {"/", "/index.html"}:
            payload = {
                "status": "online",
                "system": "Tactical Legends Unified Python Runtime",
                "mission": APP_ENGINE.current_mission.name if APP_ENGINE.current_mission else None,
                "version": "1.0.0",
            }
            self.send_json(payload)
            return

        if self.path == "/api/health":
            self.send_json({
                "status": "online",
                "system": "Tactical Legends Python Engine",
                "python_version": sys.version,
                "state": APP_ENGINE.state.value,
            })
            return

        if self.path == "/api/squad":
            self.send_json(APP_ENGINE.active_squad.get_squad_summary() if APP_ENGINE.active_squad else {"members": []})
            return

        if self.path == "/api/mission":
            self.send_json(APP_ENGINE.current_mission.to_dict() if APP_ENGINE.current_mission else {})
            return

        if self.path == "/api/battle":
            self.send_json({
                "battle": "ready",
                "turn": APP_ENGINE.turn_number,
                "winner": APP_ENGINE.winner,
            })
            return

        self.send_json({"error": "Not found"}, status=404)

    def send_json(self, payload: Any, status: int = 200):
        body = json.dumps(payload, indent=2).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, format: str, *args: Any) -> None:  # noqa: A003
        sys.stderr.write(f"[TacticalServer] {args[0]} {args[1]} -> {args[2]}\n")


def run_server(port: int = 3000, host: str = "0.0.0.0"):
    print(f"\n[Server] Tactical Legends unified Python server starting on http://{host}:{port}")
    httpd = ThreadingHTTPServer((host, port), TacticalLegendsHandler)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n[Server] Shutting down cleanly.")
        httpd.server_close()


def print_mission_summary(engine: TacticalEngine):
    mission = engine.current_mission
    if not mission:
        print("[Mission] No mission loaded.")
        return
    print(f"\n[Mission] {mission.name}")
    print(f"[Mission] Environment: {mission.environment}")
    for objective in mission.objectives:
        print(f"  - {objective.name}: {'Complete' if objective.is_complete else 'In progress'}")


def print_squad_summary(engine: TacticalEngine):
    squad = engine.active_squad
    if not squad:
        print("[Squad] No squad loaded.")
        return
    print(f"\n[Squad] {squad.name} ({squad.faction})")
    for member in squad.members:
        print(f"  - {member.name} [{member.callsign}] | LVL {member.level} | HP {member.health}/{member.max_health}")


def run_demo_simulation(engine: TacticalEngine):
    if engine.combat_system and engine.combat_system.turn_order:
        # advance a few simulated turns
        for _ in range(3):
            current = engine.combat_system.get_current_combatant()
            if current is None:
                break
            for enemy in [c for c in engine.combat_system.grid.combatants.values() if c.team == "enemy" and c.is_alive]:
                enemy_ai = engine.ai_engine.agents.get(enemy.id)
                if enemy_ai:
                    enemy_ai.think(engine.combat_system)
            engine.combat_system.end_turn()
    print("[Simulation] Unified Python combat simulation complete.")
    print(engine.combat_system.combat_log[-5:])


def main():
    parser = argparse.ArgumentParser(description="Tactical Legends Unified Python Runtime")
    parser.add_argument("--server", action="store_true", help="Start the unified HTTP runtime")
    parser.add_argument("--port", type=int, default=3000, help="HTTP port for the unified server")
    parser.add_argument("--host", default="0.0.0.0", help="HTTP host for the unified server")
    parser.add_argument("--mission", action="store_true", help="Display the active mission briefing")
    parser.add_argument("--squad", action="store_true", help="Display the active squad roster")
    parser.add_argument("--simulate", action="store_true", help="Run a short Python battle simulation")
    parser.add_argument("--test", action="store_true", help="Run a lightweight runtime sanity check")
    args = parser.parse_args()

    engine = APP_ENGINE

    if args.test:
        assert engine.current_mission is not None
        assert engine.active_squad is not None
        print("[Test] Unified Python runtime sanity checks passed.")
        return

    if args.mission:
        print_mission_summary(engine)
        return

    if args.squad:
        print_squad_summary(engine)
        return

    if args.simulate:
        run_demo_simulation(engine)
        return

    if args.server:
        run_server(port=args.port, host=args.host)
        return

    # Default behavior: boot the unified runtime and show mission summary.
    print("[Runtime] Tactical Legends unified Python runtime booted.")
    print_mission_summary(engine)
    print_squad_summary(engine)


if __name__ == "__main__":
    main()
