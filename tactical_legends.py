#!/usr/bin/env python3
"""
Tactical Legends: Rise of OISTARIAN - Core Game Engine
A robust turn-based tactical simulation system featuring grid-based combat,
squad tactics, cover mechanics, relic buffs, and adaptive AI.
"""

import math
import random
import json
from dataclasses import dataclass, field
from enum import Enum
from typing import List, Dict, Tuple, Optional, Any
from pathlib import Path


class TileType(Enum):
    EMPTY = "."
    COVER = "#"
    HAZARD = "~"
    OBJECTIVE = "*"


@dataclass
class Position:
    x: int
    y: int

    def distance_to(self, other: 'Position') -> float:
        return math.sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2)

    def manhattan_to(self, other: 'Position') -> int:
        return abs(self.x - other.x) + abs(self.y - other.y)


@dataclass
class Combatant:
    id: str
    name: str
    team: str  # "player" or "enemy"
    hp: int
    max_hp: int
    shields: int
    max_shields: int
    ap: int
    max_ap: int
    attack_power: int
    defense: int
    pos: Position
    symbol: str
    is_alive: bool = True
    traits: List[str] = field(default_factory=list)

    def take_damage(self, amount: int) -> Dict[str, Any]:
        damage_absorbed_by_shield = 0
        damage_to_hp = 0

        mitigated = max(1, amount - (self.defense // 3))

        if self.shields > 0:
            if self.shields >= mitigated:
                self.shields -= mitigated
                damage_absorbed_by_shield = mitigated
            else:
                damage_absorbed_by_shield = self.shields
                damage_to_hp = mitigated - self.shields
                self.shields = 0
                self.hp = max(0, self.hp - damage_to_hp)
        else:
            damage_to_hp = mitigated
            self.hp = max(0, self.hp - damage_to_hp)

        if self.hp <= 0:
            self.is_alive = False

        return {
            "target": self.name,
            "damage_dealt": mitigated,
            "shield_damage": damage_absorbed_by_shield,
            "hp_damage": damage_to_hp,
            "remaining_hp": self.hp,
            "remaining_shields": self.shields,
            "killed": not self.is_alive
        }

    def reset_ap(self):
        self.ap = self.max_ap


class TacticalGrid:
    def __init__(self, width: int = 10, height: int = 10):
        self.width = width
        self.height = height
        self.grid: List[List[TileType]] = [[TileType.EMPTY for _ in range(width)] for _ in range(height)]
        self._init_terrain()

    def _init_terrain(self):
        # Place fixed cover and hazards
        covers = [(2, 2), (2, 3), (7, 6), (7, 7), (4, 4), (5, 5)]
        for x, y in covers:
            if x < self.width and y < self.height:
                self.grid[y][x] = TileType.COVER

        hazards = [(4, 2), (4, 3), (5, 6), (5, 7)]
        for x, y in hazards:
            if x < self.width and y < self.height:
                self.grid[y][x] = TileType.HAZARD

        # Extraction objective
        self.grid[self.height - 1][self.width - 1] = TileType.OBJECTIVE

    def is_valid_move(self, x: int, y: int, combatants: List[Combatant]) -> bool:
        if not (0 <= x < self.width and 0 <= y < self.height):
            return False
        if self.grid[y][x] == TileType.COVER:
            return False
        for c in combatants:
            if c.is_alive and c.pos.x == x and c.pos.y == y:
                return False
        return True


class TacticalGame:
    def __init__(self, width: int = 10, height: int = 10):
        self.map = TacticalGrid(width, height)
        self.combatants: List[Combatant] = []
        self.turn = 1
        self.current_team = "player"
        self.battle_log: List[str] = []
        self.game_over = False
        self.winner: Optional[str] = None
        self._init_combatants()

    def _init_combatants(self):
        # Player Fireteam
        self.combatants.append(Combatant(
            id="p1", name="OISTARIAN", team="player",
            hp=140, max_hp=140, shields=75, max_shields=75,
            ap=4, max_ap=4, attack_power=38, defense=20,
            pos=Position(1, 1), symbol="O", traits=["NeuroPulse Kinetic Arm", "Eden Resonance"]
        ))
        self.combatants.append(Combatant(
            id="p2", name="Zoe", team="player",
            hp=90, max_hp=90, shields=40, max_shields=40,
            ap=4, max_ap=4, attack_power=28, defense=12,
            pos=Position(0, 2), symbol="Z", traits=["Holo Decoy", "Digital Glitch"]
        ))
        self.combatants.append(Combatant(
            id="p3", name="Jax", team="player",
            hp=150, max_hp=150, shields=80, max_shields=80,
            ap=3, max_ap=3, attack_power=30, defense=25,
            pos=Position(2, 0), symbol="J", traits=["Bulwark Shield"]
        ))

        # Enemy Squad (Dominion Patrol)
        self.combatants.append(Combatant(
            id="e1", name="Dominion Enforcer", team="enemy",
            hp=110, max_hp=110, shields=50, max_shields=50,
            ap=3, max_ap=3, attack_power=26, defense=16,
            pos=Position(7, 8), symbol="D"
        ))
        self.combatants.append(Combatant(
            id="e2", name="Holo Hunter", team="enemy",
            hp=85, max_hp=85, shields=30, max_shields=30,
            ap=4, max_ap=4, attack_power=32, defense=10,
            pos=Position(8, 7), symbol="H"
        ))
        self.combatants.append(Combatant(
            id="e3", name="Mecha Sentry", team="enemy",
            hp=130, max_hp=130, shields=60, max_shields=60,
            ap=3, max_ap=3, attack_power=24, defense=22,
            pos=Position(9, 9), symbol="M"
        ))

    def move_unit(self, unit: Combatant, target_x: int, target_y: int) -> bool:
        if unit.ap < 1:
            self.log(f"{unit.name} has insufficient Action Points to move.")
            return False

        dist = unit.pos.manhattan_to(Position(target_x, target_y))
        if dist > 2:
            self.log(f"Target coordinates too far for {unit.name} (Max move: 2 cells).")
            return False

        if not self.map.is_valid_move(target_x, target_y, self.combatants):
            self.log(f"Movement to ({target_x}, {target_y}) obstructed.")
            return False

        unit.pos.x = target_x
        unit.pos.y = target_y
        unit.ap -= 1

        # Check hazard tile
        if self.map.grid[target_y][target_x] == TileType.HAZARD:
            hazard_dmg = unit.take_damage(15)
            self.log(f"⚠️ {unit.name} triggered a Sandstorm Hazard! Took 15 hazard damage.")

        self.log(f"🏃 {unit.name} moved to ({target_x}, {target_y}). [AP remaining: {unit.ap}]")
        return True

    def attack_unit(self, attacker: Combatant, target: Combatant) -> bool:
        if attacker.ap < 2:
            self.log(f"{attacker.name} needs 2 AP to attack. (Current AP: {attacker.ap})")
            return False

        dist = attacker.pos.distance_to(target.pos)
        max_range = 4.5
        if dist > max_range:
            self.log(f"{target.name} is out of weapon range ({dist:.1f} > {max_range}).")
            return False

        attacker.ap -= 2
        # Calculate cover bonus
        target_defense = target.defense
        for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            cx, cy = target.pos.x + dx, target.pos.y + dy
            if 0 <= cx < self.map.width and 0 <= cy < self.map.height:
                if self.map.grid[cy][cx] == TileType.COVER:
                    target_defense += 8
                    break

        dmg_result = target.take_damage(attacker.attack_power)
        log_msg = (f"💥 {attacker.name} fired upon {target.name} for {dmg_result['damage_dealt']} DMG! "
                   f"(HP: {target.hp}/{target.max_hp}, Shields: {target.shields}/{target.max_shields})")
        if dmg_result['killed']:
            log_msg += f" ☠️ {target.name} WAS NEUTRALIZED!"
        self.log(log_msg)

        self.check_victory()
        return True

    def end_turn(self):
        # Switch turn
        if self.current_team == "player":
            self.current_team = "enemy"
            self.log(f"\n--- ENEMY SQUAD TURN (Turn {self.turn}) ---")
            self.run_enemy_ai()
            self.current_team = "player"
            self.turn += 1
            for c in self.combatants:
                c.reset_ap()
            self.log(f"\n--- SQUAD TURN {self.turn} ---")
        self.check_victory()

    def run_enemy_ai(self):
        living_enemies = [c for c in self.combatants if c.team == "enemy" and c.is_alive]
        living_players = [c for c in self.combatants if c.team == "player" and c.is_alive]

        for enemy in living_enemies:
            if not living_players:
                break
            # Find closest player
            closest_player = min(living_players, key=lambda p: enemy.pos.distance_to(p.pos))
            dist = enemy.pos.distance_to(closest_player.pos)

            # Attack if in range
            if dist <= 4.0 and enemy.ap >= 2:
                self.attack_unit(enemy, closest_player)

            # Move towards player if AP remains
            if enemy.ap >= 1 and enemy.is_alive:
                dx = 1 if closest_player.pos.x > enemy.pos.x else (-1 if closest_player.pos.x < enemy.pos.x else 0)
                dy = 1 if closest_player.pos.y > enemy.pos.y else (-1 if closest_player.pos.y < enemy.pos.y else 0)
                target_x = enemy.pos.x + dx
                target_y = enemy.pos.y + dy
                self.move_unit(enemy, target_x, target_y)

                # Re-check attack after move
                if enemy.pos.distance_to(closest_player.pos) <= 3.5 and enemy.ap >= 2 and closest_player.is_alive:
                    self.attack_unit(enemy, closest_player)

    def check_victory(self):
        players_alive = any(c.team == "player" and c.is_alive for c in self.combatants)
        enemies_alive = any(c.team == "enemy" and c.is_alive for c in self.combatants)

        if not enemies_alive:
            self.game_over = True
            self.winner = "player"
            self.log("🏆 MISSION SUCCESSFUL! All hostile forces neutralized.")
        elif not players_alive:
            self.game_over = True
            self.winner = "enemy"
            self.log("💀 MISSION FAILED! All squad operatives eliminated.")

    def log(self, message: str):
        self.battle_log.append(message)

    def render_map_ascii(self) -> str:
        lines = []
        header = "   " + " ".join(f"{i}" for i in range(self.map.width))
        lines.append(header)
        lines.append("  +" + "--" * self.map.width + "+")

        for y in range(self.map.height):
            row_str = f"{y:02d}|"
            for x in range(self.map.width):
                # Check for unit
                unit = next((c for c in self.combatants if c.is_alive and c.pos.x == x and c.pos.y == y), None)
                if unit:
                    row_str += f"{unit.symbol} "
                else:
                    row_str += f"{self.map.grid[y][x].value} "
            row_str += "|"
            lines.append(row_str)

        lines.append("  +" + "--" * self.map.width + "+")
        return "\n".join(lines)

    def simulate_automated_battle(self) -> Dict[str, Any]:
        """Runs a complete simulation until resolution and returns full telemetry."""
        while not self.game_over and self.turn < 20:
            players = [c for c in self.combatants if c.team == "player" and c.is_alive]
            enemies = [c for c in self.combatants if c.team == "enemy" and c.is_alive]

            for player in players:
                while player.ap >= 1 and player.is_alive and not self.game_over:
                    enemies = [c for c in self.combatants if c.team == "enemy" and c.is_alive]
                    if not enemies:
                        break
                    closest = min(enemies, key=lambda e: player.pos.distance_to(e.pos))
                    dist = player.pos.distance_to(closest.pos)
                    if dist <= 4.5 and player.ap >= 2:
                        self.attack_unit(player, closest)
                    elif player.ap >= 1:
                        dx = 1 if closest.pos.x > player.pos.x else (-1 if closest.pos.x < player.pos.x else 0)
                        dy = 1 if closest.pos.y > player.pos.y else (-1 if closest.pos.y < player.pos.y else 0)
                        target_x = player.pos.x + dx
                        target_y = player.pos.y + dy
                        if not self.move_unit(player, target_x, target_y):
                            # Try alternate step if direct route blocked
                            if not self.move_unit(player, player.pos.x + dx, player.pos.y):
                                if not self.move_unit(player, player.pos.x, player.pos.y + dy):
                                    player.ap = 0  # End unit turn if boxed
                        if player.pos.distance_to(closest.pos) <= 4.0 and player.ap >= 2:
                            self.attack_unit(player, closest)
                    else:
                        break

            self.end_turn()

        return {
            "winner": self.winner or "draw",
            "turns_taken": self.turn,
            "game_over": self.game_over,
            "final_log": self.battle_log,
            "survivors": [
                {
                    "name": c.name,
                    "team": c.team,
                    "hp": f"{c.hp}/{c.max_hp}",
                    "shields": f"{c.shields}/{c.max_shields}"
                }
                for c in self.combatants if c.is_alive
            ]
        }


if __name__ == "__main__":
    game = TacticalGame()
    print("=== TACTICAL LEGENDS BATTLEFIELD MAP ===")
    print(game.render_map_ascii())
    print("\nRunning automated battle simulation...")
    result = game.simulate_automated_battle()
    print(f"\nResult: {result['winner'].upper()} won in {result['turns_taken']} turns!")
    print("\n--- Combat Log Highlights ---")
    for msg in result['final_log'][-8:]:
        print(msg)
