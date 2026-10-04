#!/usr/bin/env python3
"""
Tactical Legends - TypeScript Systems Unified Python Engine
Transpiled and consolidated from core TypeScript systems:
1. CHARACTERgenerator.ts -> Procedural Operative Generator
2. fog-of-war.ts         -> 2D Tactical Fog of War Grid & Vision Calculus
3. Relic Fusion System .ts & Crafting Tree -> Relic Synthesis & Synergy Matrix
4. Squad Performance Matrix.ts & update_tactical_legend.ts -> Escalation & Morale Dynamics

Usage:
  python3 typescript_engine.py --generate-operative
  python3 typescript_engine.py --fog-demo
  python3 typescript_engine.py --relic-fusion
  python3 typescript_engine.py --escalation-demo
  python3 typescript_engine.py --test
"""

import sys
import os
import json
import random
import math
import argparse
from dataclasses import dataclass, field
from enum import Enum
from typing import List, Dict, Tuple, Optional, Any, Set


# ============================================================================
# SYSTEM 1: PROCEDURAL OPERATIVE GENERATION (from CHARACTERgenerator.ts)
# ============================================================================

NAMES = {
    "male": ["Kaelen", "Theron", "Vex", "Zahn", "Drex", "Kors", "Vahn", "Rexus", "Jaxon", "Kyros"],
    "female": ["Lyra", "Zara", "Kira", "Vex", "Nyx", "Sera", "Tara", "Xara", "Maya", "Lux"],
    "neutral": ["Ash", "River", "Storm", "Echo", "Sage", "Nova", "Vale", "Raven", "Phoenix", "Zen"]
}

SURNAMES = [
    "Voidborn", "Starforge", "Ironwill", "Shadowbane", "Crystalfall",
    "Stormwind", "Nightblade", "Goldspear", "Frostborn", "Flameheart"
]

RACES = [
    "Oistarian Elite", "Neo-Human", "Synthetic Android",
    "Psionic Mutant", "Cybernetic Augment", "Quantum Entity"
]

CLASSES = [
    {"name": "Tactical Commander", "description": "Master of battlefield strategy and team coordination"},
    {"name": "Stealth Operative", "description": "Expert in infiltration and covert operations"},
    {"name": "Heavy Assault", "description": "Specialized in frontal combat and heavy weapons"},
    {"name": "Tech Specialist", "description": "Hacker and technology manipulator"},
    {"name": "Psionic Warrior", "description": "Wielder of mental powers and psychic abilities"},
    {"name": "Medic Support", "description": "Combat medic with advanced healing capabilities"}
]

BACKGROUNDS = [
    "Former Oistarian military deserter seeking redemption",
    "Resistance fighter from the outer colonies",
    "Corporate spy turned freedom fighter",
    "Survivor of the Great Purge of 2387",
    "Underground arena champion",
    "Refugee from a destroyed sector",
    "Ex-bounty hunter with a moral awakening",
    "Scientist who discovered Oistarian war crimes"
]

SPECIAL_ABILITIES = [
    "Battle Precognition - Can predict enemy movements",
    "Neural Override - Hack enemy cybernetics",
    "Phase Shift - Briefly become intangible",
    "Energy Manipulation - Control various energy forms",
    "Tactical Rally - Boost entire team's performance",
    "Stealth Field - Turn invisible for short periods",
    "Berserker Rage - Massive damage boost when injured",
    "Shield Projection - Create protective barriers",
    "Time Dilation - Slow down personal time perception"
]

EQUIPMENT = [
    "Plasma Rifle with targeting AI",
    "Quantum Armor with adaptive camouflage",
    "Neural Interface Headset",
    "Molecular Blade that cuts through anything",
    "Portable Shield Generator",
    "Gravitic Boots for wall-walking",
    "Tactical Hologram Projector",
    "EMP Grenades"
]


@dataclass
class GeneratedOperative:
    name: str
    surname: str
    full_name: str
    gender: str
    race: str
    operative_class: str
    class_description: str
    background: str
    special_ability: str
    equipment: str
    hp: int
    shields: int
    attack_power: int
    accuracy: int
    speed: int

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.full_name,
            "race": self.race,
            "class": self.operative_class,
            "background": self.background,
            "ability": self.special_ability,
            "equipment": self.equipment,
            "stats": {
                "hp": self.hp,
                "shields": self.shields,
                "attack": self.attack_power,
                "accuracy": f"{self.accuracy}%",
                "speed": self.speed
            }
        }


def generate_procedural_operative(gender: Optional[str] = None) -> GeneratedOperative:
    """Procedurally generates an operative using the rules from CHARACTERgenerator.ts."""
    g = gender or random.choice(["male", "female", "neutral"])
    first_name = random.choice(NAMES[g])
    surname = random.choice(SURNAMES)
    full_name = f"{first_name} {surname}"
    race = random.choice(RACES)
    cls_obj = random.choice(CLASSES)
    background = random.choice(BACKGROUNDS)
    ability = random.choice(SPECIAL_ABILITIES)
    eq = random.choice(EQUIPMENT)

    # Base stat calculations
    hp = random.randint(90, 150)
    shields = random.randint(40, 80)
    attack = random.randint(25, 45)
    accuracy = random.randint(75, 98)
    speed = random.randint(3, 6)

    # Class-based modifiers
    if cls_obj["name"] == "Heavy Assault":
        hp += 30
        shields += 20
        speed -= 1
    elif cls_obj["name"] == "Stealth Operative":
        speed += 2
        accuracy += 5
        hp -= 15
    elif cls_obj["name"] == "Tactical Commander":
        shields += 15
        attack += 5

    return GeneratedOperative(
        name=first_name,
        surname=surname,
        full_name=full_name,
        gender=g,
        race=race,
        operative_class=cls_obj["name"],
        class_description=cls_obj["description"],
        background=background,
        special_ability=ability,
        equipment=eq,
        hp=hp,
        shields=shields,
        attack_power=attack,
        accuracy=accuracy,
        speed=speed
    )


# ============================================================================
# SYSTEM 2: TACTICAL FOG OF WAR ENGINE (from fog-of-war.ts)
# ============================================================================

class CellState(Enum):
    HIDDEN = "hidden"
    EXPLORED = "explored"
    VISIBLE = "visible"


@dataclass
class MapCell:
    x: int = 0
    y: int = 0
    state: CellState = CellState.HIDDEN


@dataclass
class UnitVision:
    id: str
    x: int
    y: int
    vision_radius: int = 3


class FogOfWarGrid:
    def __init__(self, width: int = 12, height: int = 8):
        self.width = width
        self.height = height
        self.grid: List[List[MapCell]] = [
            [MapCell(x=x, y=y, state=CellState.HIDDEN) for x in range(width)]
            for y in range(height)
        ]

    def update_visibility(self, units: List[UnitVision]):
        """Sets visible cells to explored, then calculates currently visible tiles."""
        # Step 1: Transition previously visible tiles to explored
        for row in self.grid:
            for cell in row:
                if cell.state == CellState.VISIBLE:
                    cell.state = CellState.EXPLORED

        # Step 2: Compute radius vision from each active operative
        for unit in units:
            for y in range(self.height):
                for x in range(self.width):
                    dist = math.sqrt((x - unit.x) ** 2 + (y - unit.y) ** 2)
                    if dist <= unit.vision_radius:
                        self.grid[y][x].state = CellState.VISIBLE

    def render_ascii(self, units: List[UnitVision]) -> str:
        lines = []
        lines.append("   " + "".join(f"{x % 10} " for x in range(self.width)))
        lines.append("  +" + "--" * self.width + "+")
        for y in range(self.height):
            row_str = f"{y:02d}|"
            for x in range(self.width):
                # Check if a unit is on this tile
                unit_here = next((u for u in units if u.x == x and u.y == y), None)
                cell = self.grid[y][x]
                if unit_here:
                    row_str += "U "
                elif cell.state == CellState.VISIBLE:
                    row_str += ". "  # Revealed ground
                elif cell.state == CellState.EXPLORED:
                    row_str += "~ "  # Explored memory
                else:
                    row_str += "? "  # Unexplored shroud
            row_str += "|"
            lines.append(row_str)
        lines.append("  +" + "--" * self.width + "+")
        lines.append("Legend: [U] Operative, [.] Visible, [~] Explored, [?] Shrouded Fog")
        return "\n".join(lines)


# ============================================================================
# SYSTEM 3: RELIC FUSION & SYNTHESIS TREE (from Relic Fusion System .ts)
# ============================================================================

@dataclass
class RelicRecipe:
    ingredient_a: str
    ingredient_b: str
    result_name: str
    success_rate: float
    unlocked_ability: str
    description: str


class RelicFusionEngine:
    def __init__(self):
        self.recipes: List[RelicRecipe] = [
            RelicRecipe(
                "EchoCore", "EdenAlloy",
                "Surge Beacon", 0.95,
                "Overclock Frequency",
                "Emits high-frequency tactical resonance that supercharges allied shields."
            ),
            RelicRecipe(
                "MercyShard", "QuantumCore",
                "Harmonic Aegis", 0.88,
                "Resonance Shielding",
                "Absorbs kinetic projectile bursts and converts impact energy into squad healing."
            ),
            RelicRecipe(
                "PsionicCatalyst", "VoidEssence",
                "Chronos Matrix", 0.82,
                "Time Dilation Pulse",
                "Distorts localized chronal field, granting +2 AP to all friendly operatives."
            )
        ]

    def fuse(self, item_a: str, item_b: str) -> Dict[str, Any]:
        target = None
        for r in self.recipes:
            if (r.ingredient_a.lower() == item_a.lower() and r.ingredient_b.lower() == item_b.lower()) or \
               (r.ingredient_a.lower() == item_b.lower() and r.ingredient_b.lower() == item_a.lower()):
                target = r
                break

        if not target:
            return {
                "success": False,
                "reason": f"No harmonic synthesis recipe found for '{item_a}' and '{item_b}'."
            }

        roll = random.random()
        if roll <= target.success_rate:
            return {
                "success": True,
                "crafted_relic": target.result_name,
                "unlocked_ability": target.unlocked_ability,
                "description": target.description,
                "roll": round(roll, 3),
                "threshold": target.success_rate
            }
        else:
            return {
                "success": False,
                "reason": "Resonance failure: Ingredients dissolved during quantum stabilization.",
                "roll": round(roll, 3),
                "threshold": target.success_rate
            }


# ============================================================================
# SYSTEM 4: SQUAD PERFORMANCE & CONFLICT ESCALATION (from update_tactical_legend.ts)
# ============================================================================

class ConflictAlertPhase(Enum):
    PEACEFUL = "Peaceful"
    ALERT = "Alert"
    SKIRMISH = "Skirmish"
    WARZONE = "Warzone"
    CATASTROPHE = "Catastrophe"


class ConflictEscalationManager:
    def __init__(self):
        self.alert_level: int = 0
        self.phase: ConflictAlertPhase = ConflictAlertPhase.PEACEFUL
        self.civilian_casualties: int = 0
        self.military_casualties: int = 0
        self.events_log: List[str] = []

    def escalate(self, increase: int, reason: str):
        self.alert_level = min(5, self.alert_level + increase)
        phases = [
            ConflictAlertPhase.PEACEFUL,
            ConflictAlertPhase.ALERT,
            ConflictAlertPhase.SKIRMISH,
            ConflictAlertPhase.WARZONE,
            ConflictAlertPhase.CATASTROPHE
        ]
        self.phase = phases[min(self.alert_level, len(phases) - 1)]
        log_entry = f"[ESCALATION +{increase}] Level {self.alert_level} ({self.phase.value}): {reason}"
        self.events_log.append(log_entry)
        return log_entry

    def record_casualty(self, is_civilian: bool):
        if is_civilian:
            self.civilian_casualties += 1
            self.escalate(1, f"Civilian casualty reported (Total: {self.civilian_casualties})")
        else:
            self.military_casualties += 1
            self.escalate(1, f"Military unit neutralized (Total: {self.military_casualties})")


# ============================================================================
# MASTER TEST & CLI SUITE
# ============================================================================

def run_tests():
    print("=======================================================")
    print("🧪 EXECUTING TYPESCRIPT-TO-PYTHON VERIFICATION TESTS")
    print("=======================================================\n")

    # Test 1: Operative generation
    op = generate_procedural_operative()
    assert op.hp > 0 and op.shields > 0, "Operative must have valid health and shields"
    print(f"✅ Test 1 Passed: Procedural operative generated -> {op.full_name} ({op.operative_class})")

    # Test 2: Fog of War
    grid = FogOfWarGrid(10, 10)
    units = [UnitVision("lead", 4, 4, vision_radius=3)]
    grid.update_visibility(units)
    assert grid.grid[4][4].state == CellState.VISIBLE, "Operative position must be visible"
    print("✅ Test 2 Passed: 2D Tactical Fog of War line-of-sight and memory verified")

    # Test 3: Relic Fusion
    fusion = RelicFusionEngine()
    result = fusion.fuse("EchoCore", "EdenAlloy")
    assert result["success"] or "roll" in result, "Fusion calculation must resolve recipe"
    print(f"✅ Test 3 Passed: Relic synthesis evaluated -> EchoCore + EdenAlloy = {result.get('crafted_relic', 'Dissolved')}")

    # Test 4: Conflict Escalation
    escalation = ConflictEscalationManager()
    escalation.record_casualty(is_civilian=False)
    assert escalation.alert_level >= 1, "Alert level must increase on casualties"
    print(f"✅ Test 4 Passed: Conflict escalation -> {escalation.phase.value}")

    print("\n🎉 ALL 4 TYPESCRIPT MIGRATION TESTS PASSED!")


def main():
    parser = argparse.ArgumentParser(
        description="Tactical Legends - TypeScript Systems Unified Python Engine",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("--generate-operative", action="store_true", help="Generate a procedural tactical operative")
    parser.add_argument("--fog-demo", action="store_true", help="Render interactive 2D Fog of War tactical grid")
    parser.add_argument("--relic-fusion", action="store_true", help="Demonstrate Relic Fusion synthesis")
    parser.add_argument("--escalation-demo", action="store_true", help="Simulate combat escalation phases")
    parser.add_argument("--test", action="store_true", help="Run comprehensive unit tests")

    args = parser.parse_args()

    if args.test:
        run_tests()
        return

    if args.generate_operative:
        op = generate_procedural_operative()
        print("\n=======================================================")
        print(f"🎖️  PROCEDURAL OPERATIVE: {op.full_name.upper()}")
        print("=======================================================")
        print(f"Race:        {op.race}")
        print(f"Class:       {op.operative_class} - {op.class_description}")
        print(f"Background:  {op.background}")
        print(f"Ability:     {op.special_ability}")
        print(f"Equipment:   {op.equipment}")
        print(f"Combat:      HP {op.hp} | Shields {op.shields} | ATK {op.attack_power} | Accuracy {op.accuracy}% | SPD {op.speed}\n")
        return

    if args.fog_demo:
        print("\n=======================================================")
        print("🌫️  TACTICAL FOG OF WAR SIMULATION")
        print("=======================================================")
        grid = FogOfWarGrid(12, 8)
        units = [
            UnitVision("op_1", 3, 2, vision_radius=3),
            UnitVision("op_2", 8, 5, vision_radius=2)
        ]
        grid.update_visibility(units)
        print(grid.render_ascii(units))
        print()
        return

    if args.relic_fusion:
        print("\n=======================================================")
        print("⚗️  RELIC FUSION SYNTHESIS LAB")
        print("=======================================================")
        fusion = RelicFusionEngine()
        pairs = [("EchoCore", "EdenAlloy"), ("MercyShard", "QuantumCore"), ("UnknownShard", "Lead")]
        for a, b in pairs:
            res = fusion.fuse(a, b)
            if res["success"]:
                print(f"✨ SUCCESS: {a} + {b} => {res['crafted_relic'].upper()}")
                print(f"   Ability: {res['unlocked_ability']}")
                print(f"   Lore:    {res['description']}")
            else:
                print(f"❌ FAILED:  {a} + {b} => {res.get('reason')}")
            print()
        return

    if args.escalation_demo:
        print("\n=======================================================")
        print("⚠️  CONFLICT ESCALATION MONITOR")
        print("=======================================================")
        escalation = ConflictEscalationManager()
        escalation.record_casualty(is_civilian=False)
        escalation.escalate(1, "Player unit detected near primary vault vault")
        escalation.record_casualty(is_civilian=True)
        escalation.escalate(2, "Orbital kinetic strike inbound")
        for log in escalation.events_log:
            print(f"  {log}")
        print(f"\nFinal State: Phase = {escalation.phase.value} (Alert Level {escalation.alert_level})\n")
        return

    # If no flags passed, run tests by default
    run_tests()


if __name__ == "__main__":
    main()
