#!/usr/bin/env python3
"""
Tactical Legends: Rise of OISTARIAN
Master Python System & Application Engine

Unified entrypoint supporting:
- Full Web Server mode (port 3000) with REST API & Static Asset Serving
- Interactive CLI Turn-Based Combat Simulation
- Automated Tactical AI Battle Engine
- Squad Roster & Gear Management
- Mission Briefing & Codex Inspections
- Cinematic Voice Script Generator
"""

import sys
import os
import json
import argparse
import mimetypes
from typing import Any, Dict, List, Optional
from pathlib import Path
from http.server import HTTPServer, SimpleHTTPRequestHandler
from socketserver import ThreadingMixIn

# Import tactical sub-modules
from tactical_legends import TacticalGame, Position, Combatant, TileType
from SquadMember import get_default_squad, SquadMember
from soundNvoiceManager import SoundNVoiceManager
from coe import CathedralOfEchoes
from vault_of_eden import VaultOfEdenEncounter
from typescript_engine import generate_procedural_operative, RelicFusionEngine, FogOfWarGrid
from html_portal import render_html_page

BASE_DIR = Path(__file__).resolve().parent
PUBLIC_DIR = BASE_DIR / "public"
RESOURCE_DIR = BASE_DIR / "resource"


class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """Multi-threaded HTTP server for handling concurrent web requests."""
    daemon_threads = True


class TacticalLegendsHTTPHandler(SimpleHTTPRequestHandler):
    """Custom HTTP handler serving web portal files and Tactical REST APIs."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(BASE_DIR), **kwargs)

    def do_GET(self):
        # API Endpoints
        if self.path == "/api/health":
            self.send_json_response({
                "status": "online",
                "system": "Tactical Legends Python Engine",
                "version": "1.0.0",
                "python_version": sys.version
            })
            return

        if self.path == "/api/squad":
            squad = get_default_squad()
            self.send_json_response(squad.get_squad_summary())
            return

        if self.path == "/api/voice" or self.path == "/api/voice/manifest":
            vm = SoundNVoiceManager()
            self.send_json_response(vm.to_manifest())
            return

        if self.path == "/api/operation":
            op_file = BASE_DIR / "operation_sand_echo.json"
            if op_file.exists():
                try:
                    content = op_file.read_text(encoding="utf-8").split("\n\nvoice_lines")[0]
                    self.send_json_response(json.loads(content))
                    return
                except Exception as e:
                    self.send_json_response({"error": str(e)}, status=500)
                    return
            self.send_json_response({"operation": "Sand Echo", "status": "Ready"})
            return

        if self.path == "/api/coe":
            engine = CathedralOfEchoes()
            engine.record_action("spared_enemy")
            engine.complete_mission_echoes_of_judgment()
            self.send_json_response(engine.to_dict())
            return

        if self.path == "/api/eden":
            encounter = VaultOfEdenEncounter(morality_score=75, prior_civilian_rescue=True)
            self.send_json_response(encounter.run_full_simulation())
            return

        if self.path == "/api/ts/operative":
            op = generate_procedural_operative()
            self.send_json_response(op.to_dict())
            return

        if self.path == "/api/codex":
            codex_file = RESOURCE_DIR / "CODEX.json"
            if codex_file.exists():
                try:
                    content = codex_file.read_text(encoding="utf-8").split("\n\nC#")[0]
                    self.send_json_response(json.loads(content))
                    return
                except Exception as e:
                    self.send_json_response({"error": str(e)}, status=500)
                    return
            self.send_json_response({"factions": [], "relics": []})
            return

        if self.path == "/trailer" or self.path == "/trailer.html":
            self.serve_file(BASE_DIR / "trailer.html", "text/html")
            return

        if self.path == "/" or self.path == "/index.html":
            self.serve_file(BASE_DIR / "index.html", "text/html")
            return

        # Check in public directory first, then root
        target_path = PUBLIC_DIR / self.path.lstrip("/")
        if target_path.exists() and target_path.is_file():
            mime_type, _ = mimetypes.guess_type(str(target_path))
            self.serve_file(target_path, mime_type or "application/octet-stream")
            return

        root_target = BASE_DIR / self.path.lstrip("/")
        if root_target.exists() and root_target.is_file():
            mime_type, _ = mimetypes.guess_type(str(root_target))
            self.serve_file(root_target, mime_type or "application/octet-stream")
            return

        # Fallback to 404
        fallback_404 = BASE_DIR / "404.html"
        if fallback_404.exists():
            self.serve_file(fallback_404, "text/html", status=404)
        else:
            self.send_error(404, "File Not Found")

    def do_POST(self):
        if self.path == "/api/battle/simulate":
            game = TacticalGame()
            result = game.simulate_automated_battle()
            self.send_json_response(result)
            return

        if self.path == "/api/ts/relic/fuse":
            fusion = RelicFusionEngine()
            res = fusion.fuse("EchoCore", "EdenAlloy")
            self.send_json_response(res)
            return

        self.send_error(404, "Unknown POST Endpoint")

    def serve_file(self, file_path: Path, content_type: str, status: int = 200):
        try:
            data = file_path.read_bytes()
            self.send_response(status)
            self.send_header("Content-Type", content_type)
            self.send_header("Content-Length", str(len(data)))
            self.send_header("Cache-Control", "public, max-age=0")
            self.end_headers()
            self.wfile.write(data)
        except Exception as e:
            self.send_error(500, f"Error reading file: {e}")

    def send_json_response(self, data: Any, status: int = 200):
        body = json.dumps(data, indent=2).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, format, *args):
        # Compact access logs
        sys.stderr.write(f"[TacticalServer] {args[0]} {args[1]} -> {args[2]}\n")


def run_web_server(port: int = 3000, host: str = "0.0.0.0"):
    server_address = (host, port)
    httpd = ThreadedHTTPServer(server_address, TacticalLegendsHTTPHandler)
    print(f"\n=======================================================")
    print(f"⚔️  TACTICAL LEGENDS PYTHON HTTP SERVER RUNNING")
    print(f"🌐  URL: http://{host}:{port}/")
    print(f"🎙️  AI Trailer: http://{host}:{port}/trailer")
    print(f"📡  REST API:   http://{host}:{port}/api/health")
    print(f"=======================================================\n")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n[TacticalServer] Server shutting down safely.")
        httpd.server_close()


def print_mission():
    op_file = BASE_DIR / "operation_sand_echo.json"
    if op_file.exists():
        try:
            content = op_file.read_text(encoding="utf-8").split("\n\nvoice_lines")[0]
            data = json.loads(content)
            print("\n=======================================================")
            print(f"🎯 OPERATION: {data.get('operation_name', 'SAND ECHO').upper()}")
            print(f"📍 Sector: {data.get('sector', 'CH-03')} | Environment: {data.get('environment', 'Desert')}")
            print(f"📜 Objective: {data.get('primary_objective', 'Retrieve Echo Core Relic')}")
            print("=======================================================\n")
            print("Hazards & Battlefield Traits:")
            for h in data.get("tactical_hazards", []):
                print(f"  • {h}")
            return
        except Exception:
            pass
    print("\n🎯 OPERATION SAND ECHO // SECTOR CH-03")
    print("Objective: Secure the Echo Core Relic inside Vault Eden.")


def print_squad():
    squad = get_default_squad()
    print("\n=======================================================")
    print(f"🛡️  ACTIVE SQUAD ROSTER: {squad.name.upper()}")
    print("=======================================================\n")
    for m in squad.members:
        print(f"[{m.id}] {m.name} ({m.class_type.value})")
        print(f"    HP: {m.health}/{m.max_health} | Shields: {m.shields}/{m.max_shields} | AP: {m.action_points}")
        print(f"    Traits: {', '.join(m.traits)}")
        if m.gear:
            gear_str = ", ".join(f"{slot}: {item.name}" for slot, item in m.gear.items())
            print(f"    Gear: {gear_str}")
        print()


def print_codex():
    codex_file = RESOURCE_DIR / "CODEX.json"
    print("\n=======================================================")
    print("📜 TACTICAL LEGENDS CODEX & FACTIONS")
    print("=======================================================\n")
    if codex_file.exists():
        try:
            content = codex_file.read_text(encoding="utf-8").split("\n\nC#")[0]
            data = json.loads(content)
            print("Factions Active:")
            for f in data.get("Factions", []):
                print(f"  🛡️ {f.get('Name', 'Unknown')} - {f.get('Description', '')[:80]}...")
            print("\nRelics Cataloged:")
            for r in data.get("Relics", [])[:6]:
                print(f"  🗝️ {r.get('Name', 'Relic')} [{r.get('Type', 'Ancient')}]: {r.get('Effect', '')}")
            return
        except Exception as e:
            print(f"Error parsing codex: {e}")
    print("Codex database online. Ready for query.")


def run_tests():
    print("\n=======================================================")
    print("🧪 RUNNING TACTICAL LEGENDS PYTHON SYSTEM TESTS")
    print("=======================================================\n")

    # Test 1: Squad calculations
    squad = get_default_squad()
    assert len(squad.members) >= 4, "Squad must have 4 default members"
    oistarian = squad.members[0]
    initial_shields = oistarian.shields
    dmg = oistarian.take_damage(20)
    assert oistarian.shields < initial_shields, "Shields should absorb damage"
    print("✅ Test 1 Passed: SquadMember damage mitigation & shield absorption")

    # Test 2: Grid & Combatant
    game = TacticalGame()
    assert game.map.width == 10 and game.map.height == 10, "Grid must be 10x10"
    p1 = game.combatants[0]
    assert p1.is_alive, "Unit should start alive"
    print("✅ Test 2 Passed: TacticalGrid coordinate system & combatant initialization")

    # Test 3: Automated Battle Simulation
    sim_result = game.simulate_automated_battle()
    assert sim_result["game_over"] is True or sim_result["turns_taken"] >= 1, "Simulation must execute turns"
    print(f"✅ Test 3 Passed: Combat simulation resolved in {sim_result['turns_taken']} turns (Winner: {sim_result['winner']})")

    # Test 4: Voice & Audio Manager
    vm = SoundNVoiceManager()
    manifest = vm.to_manifest()
    assert len(manifest["items"]) == 8, "Voice manifest must have 8 scenes"
    print("✅ Test 4 Passed: SoundNVoiceManager scene orchestration verified")

    print("\n🎉 ALL TESTS PASSED! Python system is 100% operational.")


def run_cli_combat():
    """Interactive command-line tactical game."""
    game = TacticalGame()
    print("\n=======================================================")
    print("⚔️  TACTICAL LEGENDS // CLI COMBAT SIMULATOR")
    print("=======================================================\n")
    print("Operatives: [O] Oistarian, [Z] Zoe, [J] Jax")
    print("Enemies:    [D] Dominion Enforcer, [H] Holo Hunter, [M] Mecha Sentry")
    print("Terrain:    [#] Cover (+8 Def), [~] Hazard (15 Dmg), [*] Objective\n")

    while not game.game_over and game.turn <= 25:
        print(f"\n--- SQUAD TURN {game.turn} ---")
        print(game.render_map_ascii())

        players = [c for c in game.combatants if c.team == "player" and c.is_alive]
        if not players:
            break

        print("\nActive Operatives:")
        for idx, p in enumerate(players):
            print(f"  [{idx + 1}] {p.name} at ({p.pos.x}, {p.pos.y}) | HP: {p.hp}/{p.max_hp} | Shields: {p.shields}/{p.max_shields} | AP: {p.ap}")

        # Automated or step through
        print("\nOptions: [1-3] Select unit, [a] Auto-complete turn, [q] Quit to menu")
        try:
            choice = input("Enter command: ").strip().lower()
        except (EOFError, KeyboardInterrupt):
            print("\nExiting combat...")
            break

        if choice == "q":
            break
        elif choice == "a" or not choice:
            # Let AI execute player turn
            for player in players:
                enemies = [c for c in game.combatants if c.team == "enemy" and c.is_alive]
                if not enemies:
                    break
                closest = min(enemies, key=lambda e: player.pos.distance_to(e.pos))
                if player.pos.distance_to(closest.pos) <= 4.0 and player.ap >= 2:
                    game.attack_unit(player, closest)
                elif player.ap >= 1:
                    dx = 1 if closest.pos.x > player.pos.x else (-1 if closest.pos.x < player.pos.x else 0)
                    dy = 1 if closest.pos.y > player.pos.y else (-1 if closest.pos.y < player.pos.y else 0)
                    game.move_unit(player, player.pos.x + dx, player.pos.y + dy)
            game.end_turn()
        elif choice in ["1", "2", "3"]:
            unit_idx = int(choice) - 1
            if unit_idx < len(players):
                unit = players[unit_idx]
                print(f"\nSelected {unit.name}. [m] Move (x, y), [f] Fire at closest enemy, [c] Cancel")
                act = input("Action: ").strip().lower()
                if act == "f":
                    enemies = [c for c in game.combatants if c.team == "enemy" and c.is_alive]
                    if enemies:
                        closest = min(enemies, key=lambda e: unit.pos.distance_to(e.pos))
                        game.attack_unit(unit, closest)
                    else:
                        print("No enemies remaining.")
                elif act.startswith("m"):
                    try:
                        coords = input("Enter target x y (e.g. 3 4): ").split()
                        tx, ty = int(coords[0]), int(coords[1])
                        game.move_unit(unit, tx, ty)
                    except Exception as e:
                        print(f"Invalid coordinate: {e}")

    print("\n=== COMBAT RESOLUTION ===")
    if game.winner == "player":
        print("🏆 VICTORY! All Dominion hostiles eliminated.")
    elif game.winner == "enemy":
        print("💀 DEFEAT! Squad was wiped out.")
    else:
        print("Tactical retreat / simulation finished.")


def main():
    parser = argparse.ArgumentParser(
        description="Tactical Legends: Rise of OISTARIAN - Master Python Engine",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("--server", action="store_true", help="Start the Python HTTP Web Server on port 3000")
    parser.add_argument("--port", type=int, default=3000, help="Web server port (default: 3000)")
    parser.add_argument("--host", type=str, default="0.0.0.0", help="Web server host (default: 0.0.0.0)")
    parser.add_argument("--cli", "--play", action="store_true", help="Launch interactive CLI tactical battle simulator")
    parser.add_argument("--simulate", action="store_true", help="Run automated AI vs AI combat simulation")
    parser.add_argument("--json-sim", action="store_true", help="Output battle simulation as pure JSON (for Node/API bridge)")
    parser.add_argument("--mission", action="store_true", help="Display Operation Sand Echo briefing")
    parser.add_argument("--squad", action="store_true", help="Display active squad roster & stats")
    parser.add_argument("--codex", action="store_true", help="Display Codex factions & relics catalog")
    parser.add_argument("--voice", action="store_true", help="Display voice scripts and trailer audio manifest")
    parser.add_argument("--coe", action="store_true", help="Run Cathedral of Echoes (COE) moral consequence demo")
    parser.add_argument("--eden", action="store_true", help="Run Vault of Eden symphonic tactical encounter demo")
    parser.add_argument("--ts", action="store_true", help="Run TypeScript-to-Python unified systems test and demos")
    parser.add_argument("--portal", action="store_true", help="Generate and export the Python HTML Portal")
    parser.add_argument("--test", action="store_true", help="Execute Python unit & integration tests")

    args = parser.parse_args()

    if args.portal:
        from html_portal import export_html
        export_html(BASE_DIR / "index.html")
        return

    if args.ts:
        from typescript_engine import run_tests as run_ts_tests
        run_ts_tests()
        return

    if args.coe:
        from coe import run_demo
        run_demo()
        return

    if args.eden:
        from vault_of_eden import main as run_eden
        run_eden()
        return

    if args.json_sim:
        game = TacticalGame()
        res = game.simulate_automated_battle()
        print(json.dumps(res))
        return

    if args.test:
        run_tests()
        return

    if args.mission:
        print_mission()
        return

    if args.squad:
        print_squad()
        return

    if args.codex:
        print_codex()
        return

    if args.voice:
        vm = SoundNVoiceManager()
        vm.print_script()
        return

    if args.simulate:
        game = TacticalGame()
        print("=== TACTICAL BATTLEFIELD MAP ===")
        print(game.render_map_ascii())
        res = game.simulate_automated_battle()
        print(f"\nWinner: {res['winner'].upper()} (Turns: {res['turns_taken']})")
        print("Combat Log:")
        for log in res["final_log"][-6:]:
            print(f"  {log}")
        return

    if args.cli:
        run_cli_combat()
        return

    if args.server:
        run_web_server(port=args.port, host=args.host)
        return

    # If no flags passed, start the Web Server by default
    run_web_server(port=args.port, host=args.host)


if __name__ == "__main__":
    main()
