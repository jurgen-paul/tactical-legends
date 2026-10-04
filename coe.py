#!/usr/bin/env python3
"""
Cathedral of Echoes (COE) - Moral Consequence & Reactive Weapon Engine
Converted from COE.sc Scala script to full Python architecture.

Features:
- Dynamic Morality Evaluation & Trait Shifting (Empathetic, Cold, Detached)
- Ability Unlocks & Evolution (Chord of Mercy -> Harmony Surge, Pulse of Silence)
- Reactive Codex Generator (PlayerPath, RegretLog)
- Emotionally Reactive & Guilt-Fed Weapons (Griefshard, Mercybrand, Judicator's Coil, Echofang)
- Emotional Ammo (Guilt, Fear, Regret, Hope Echo Charges)
- Corrupted Grid Map Mutation & Shadow Echo NPC Haunting
"""

import sys
import json
from dataclasses import dataclass, field
from enum import Enum
from typing import List, Dict, Set, Optional, Any


class MoralityAlignment(Enum):
    COMPASSION = "Compassion"
    COLD = "Cold"
    JUSTICE = "Justice"
    BETRAYAL = "Betrayal"
    REDEMPTION = "Redemption"
    REGRET = "Regret"
    NEUTRAL = "Neutral"


@dataclass
class Trait:
    name: str
    duration: float = 60.0  # seconds until decay if not reinforced
    active: bool = True


@dataclass
class Ability:
    name: str
    description: str
    uses: int = 0
    evolved_into: Optional[str] = None


@dataclass
class ReactiveWeapon:
    name: str
    base_type: str
    alignment: MoralityAlignment
    tactical_ability: str
    guilt_consequence: str
    haunt_level: int = 0
    echo_charge_type: str = "Guilt"
    base_damage: int = 30

    def calculate_damage(self, player_morality: int, echo_intensity: int = 1) -> int:
        multiplier = 1.0
        if self.alignment == MoralityAlignment.COMPASSION and player_morality > 10:
            multiplier = 1.3
        elif self.alignment == MoralityAlignment.COLD and player_morality < -10:
            multiplier = 1.3
        elif self.alignment == MoralityAlignment.REGRET:
            # Damage scales directly with guilt/emotional intensity
            return self.base_damage + (echo_intensity * 12)
        return int(self.base_damage * multiplier)

    def trigger_firing_effect(self, player_morality: int) -> Dict[str, Any]:
        effect = {
            "weapon": self.name,
            "fired": True,
            "tactical_effect": self.tactical_ability,
            "consequence": self.guilt_consequence,
            "whisper": None
        }

        # Mirror-linked weapon behavior
        if self.name == "Judicator’s Coil" and player_morality < -10:
            effect["fired"] = False
            effect["consequence"] = "Judicator's Coil refuses to fire for a morally compromised operative."
        elif self.name == "Mercybrand" and player_morality < -10:
            effect["consequence"] = "Mercybrand backfires! Spared enemy spirits cause self-inflicted feedback."
        elif self.haunt_level >= 3:
            effect["whisper"] = f"A high Haunt Level triggers UI distortion and auditory hallucinations: '{self.guilt_consequence}'"

        return effect


@dataclass
class PlayerState:
    name: str = "Oistarian Recon"
    morality: int = 0
    actions: Set[str] = field(default_factory=set)
    dialogue: Set[str] = field(default_factory=set)
    traits: Dict[str, Trait] = field(default_factory=dict)
    abilities: Dict[str, Ability] = field(default_factory=dict)
    unlocked_codex: Dict[str, str] = field(default_factory=dict)
    inventory_weapons: List[ReactiveWeapon] = field(default_factory=list)
    equipped_weapon: Optional[ReactiveWeapon] = None


class CathedralOfEchoes:
    def __init__(self, player: Optional[PlayerState] = None):
        self.player = player or PlayerState()
        self.logs: List[str] = []
        self._init_weapons()

    def _init_weapons(self):
        weapons = [
            ReactiveWeapon(
                name="Mercybrand",
                base_type="Assault Blade",
                alignment=MoralityAlignment.COMPASSION,
                tactical_ability="Heals allies on kill",
                guilt_consequence="Whispers of spared enemies haunt your frequency",
                echo_charge_type="Hope",
                base_damage=35
            ),
            ReactiveWeapon(
                name="Echofang",
                base_type="Silenced Carbine",
                alignment=MoralityAlignment.BETRAYAL,
                tactical_ability="Backstab deals double damage",
                guilt_consequence="Nearby NPCs flinch when you draw near",
                echo_charge_type="Fear",
                base_damage=40
            ),
            ReactiveWeapon(
                name="Judicator’s Coil",
                base_type="Energy Rifle",
                alignment=MoralityAlignment.JUSTICE,
                tactical_ability="Stuns enemies who have harmed innocents",
                guilt_consequence="Cannot harm neutral or surrendered targets",
                echo_charge_type="Hope",
                base_damage=45
            ),
            ReactiveWeapon(
                name="Pulse of Silence",
                base_type="Acoustic Disruptor",
                alignment=MoralityAlignment.COLD,
                tactical_ability="Silences enemy abilities and communication",
                guilt_consequence="Drains player empathy over extended usage",
                echo_charge_type="Guilt",
                base_damage=38
            ),
            ReactiveWeapon(
                name="Griefshard",
                base_type="Psychic Catalyst",
                alignment=MoralityAlignment.REGRET,
                tactical_ability="Damage scales with emotional echoes",
                guilt_consequence="Causes hallucinations of those you failed",
                echo_charge_type="Regret",
                base_damage=50
            ),
            ReactiveWeapon(
                name="Barrett M82 Judgment",
                base_type="Anti-Material Sniper",
                alignment=MoralityAlignment.JUSTICE,
                tactical_ability="Pierces multiple armored targets",
                guilt_consequence="Scope flashes spectral memories of distant victims",
                echo_charge_type="Fear",
                base_damage=90
            ),
            ReactiveWeapon(
                name="M4 Echo Variant",
                base_type="Burst Assault Rifle",
                alignment=MoralityAlignment.COMPASSION,
                tactical_ability="Burst fire synchronizes with operative heartbeat",
                guilt_consequence="Missed shots whisper names of fallen fireteam allies",
                echo_charge_type="Hope",
                base_damage=32
            )
        ]
        self.player.inventory_weapons = weapons
        self.player.equipped_weapon = weapons[0]

    def log(self, msg: str):
        self.logs.append(msg)

    def record_action(self, action: str):
        self.player.actions.add(action)
        self.log(f"Action logged: {action}")

    def record_dialogue(self, dialogue_choice: str):
        self.player.dialogue.add(dialogue_choice)
        self.log(f"Dialogue choice: {dialogue_choice}")

    def evaluate_morality(self):
        """Evaluate morality based on actions and speech."""
        delta = 0
        if "spared_enemy" in self.player.actions or "civilian_rescue" in self.player.actions:
            delta += 10
        if "compassion" in self.player.dialogue or "reassure" in self.player.dialogue:
            delta += 5

        if "executed_enemy" in self.player.actions or "abandon_allies" in self.player.actions:
            delta -= 10
        if "threat" in self.player.dialogue or "ruthless" in self.player.dialogue:
            delta -= 5

        self.player.morality += delta
        self.log(f"Morality evaluated: {self.player.morality:+d} (Net shift: {delta:+d})")

    def apply_trait_shift(self):
        """Add or remove traits according to current morality thresholds."""
        if self.player.morality >= 10:
            self.player.traits["Empathetic"] = Trait("Empathetic")
            if "Detached" in self.player.traits:
                del self.player.traits["Detached"]
            self.log("Trait Shift: Gained [Empathetic], purged [Detached].")
        elif self.player.morality <= -10:
            self.player.traits["Cold"] = Trait("Cold")
            if "Empathetic" in self.player.traits:
                del self.player.traits["Empathetic"]
            self.log("Trait Shift: Gained [Cold], purged [Empathetic].")

    def unlock_ability(self):
        """Unlock morality-tied tactical abilities."""
        if self.player.morality >= 10:
            self.player.abilities["Chord of Mercy"] = Ability(
                name="Chord of Mercy",
                description="Heals fireteam allies and calms agitated sentinels."
            )
            self.log("Unlocked Ability: Chord of Mercy (Compassion Path).")
        elif self.player.morality <= -10:
            self.player.abilities["Pulse of Silence"] = Ability(
                name="Pulse of Silence",
                description="Disables enemy communications and drains hostile resolve."
            )
            self.log("Unlocked Ability: Pulse of Silence (Ruthless Path).")
        else:
            self.log("No unique ability unlocked: Morality remains neutral.")

    def evolve_abilities(self):
        """Evolve abilities through frequent use."""
        if "Chord of Mercy" in self.player.abilities:
            ability = self.player.abilities["Chord of Mercy"]
            if ability.uses >= 5:
                del self.player.abilities["Chord of Mercy"]
                self.player.abilities["Harmony Surge"] = Ability(
                    name="Harmony Surge",
                    description="AoE heal + morale boost; grants temporary empathy aura."
                )
                self.log("Evolution: Chord of Mercy evolved into [Harmony Surge]!")

    def update_codex(self):
        """Update dynamic codex entries according to player journey."""
        if self.player.morality > 10:
            self.player.unlocked_codex["PlayerPath"] = (
                "You chose compassion. The world remembers your mercy, and the cathedral glyphs glow gold."
            )
        elif self.player.morality < -10:
            self.player.unlocked_codex["PlayerPath"] = (
                "You silenced the weak. The echoes of fear remain, vibrating through cold obsidian corridors."
            )
        else:
            self.player.unlocked_codex["PlayerPath"] = (
                "You walked the line. Neither condemned nor redeemed, an enigma in the archives."
            )

        if self.player.morality < -10:
            self.player.unlocked_codex["RegretLog"] = (
                "You silenced the innocent. The vault remembers every breath extinguished."
            )
        else:
            self.player.unlocked_codex["RegretLog"] = (
                "No active regrets found in memory logs. The path remains untarnished by guilt."
            )

    def complete_mission_echoes_of_judgment(self):
        """Complete the canonical mission 'Echoes of Judgment'."""
        self.log("\n--- EXECUTING MISSION: Echoes of Judgment ---")
        self.evaluate_morality()
        self.apply_trait_shift()
        self.unlock_ability()
        self.update_codex()
        self.log("Mission [Echoes of Judgment] successfully evaluated.\n")

    def simulate_shadow_echo_encounter(self) -> str:
        """NPC interaction logic converted from Scala npc 'ShadowEcho'."""
        if "executed_enemy" in self.player.actions or self.player.morality < -10:
            return "ShadowEcho (Haunt/Flicker): 'They begged. You walked away. Blood never forgets.'"
        elif self.player.morality > 10:
            return "ShadowEcho (Harmonic/Calm): 'You spared the fallen. The resonance is clear.'"
        return "ShadowEcho (Distant): 'We watch from between the frequencies.'"

    def simulate_grid_corruption(self) -> Dict[str, Any]:
        """Map mutation logic converted from Scala map 'CorruptedGrid'."""
        if self.player.morality < -10:
            return {
                "layout": "Chaotic & Mutated",
                "visibility_reduction": "50%",
                "labels": "Scrambled",
                "hazard_density": "High (Trauma Spikes)"
            }
        elif self.player.morality > 10:
            return {
                "layout": "Harmonized & Stabilized",
                "visibility_reduction": "0%",
                "hidden_paths_revealed": True,
                "hazard_density": "Low (Pacified)"
            }
        return {
            "layout": "Standard Grid",
            "visibility_reduction": "0%",
            "hazard_density": "Moderate"
        }

    def to_dict(self) -> Dict[str, Any]:
        return {
            "player": {
                "name": self.player.name,
                "morality": self.player.morality,
                "traits": list(self.player.traits.keys()),
                "abilities": [
                    {"name": a.name, "description": a.description, "uses": a.uses}
                    for a in self.player.abilities.values()
                ],
                "codex": self.player.unlocked_codex
            },
            "equipped_weapon": {
                "name": self.player.equipped_weapon.name,
                "alignment": self.player.equipped_weapon.alignment.value,
                "ability": self.player.equipped_weapon.tactical_ability,
                "consequence": self.player.equipped_weapon.guilt_consequence
            } if self.player.equipped_weapon else None,
            "grid_status": self.simulate_grid_corruption(),
            "npc_interaction": self.simulate_shadow_echo_encounter(),
            "logs": self.logs
        }


def run_demo():
    print("=======================================================")
    print("🔮 CATHEDRAL OF ECHOES (COE) PYTHON ENGINE")
    print("=======================================================\n")

    # Simulation 1: Compassion path
    coe_compassion = CathedralOfEchoes()
    coe_compassion.record_action("spared_enemy")
    coe_compassion.record_action("civilian_rescue")
    coe_compassion.record_dialogue("compassion")
    coe_compassion.complete_mission_echoes_of_judgment()

    print("[Path A: Compassion Outcome]")
    print(f"  • Morality: {coe_compassion.player.morality}")
    print(f"  • Traits: {list(coe_compassion.player.traits.keys())}")
    print(f"  • Abilities: {list(coe_compassion.player.abilities.keys())}")
    print(f"  • Codex: {coe_compassion.player.unlocked_codex.get('PlayerPath')}")
    print(f"  • NPC: {coe_compassion.simulate_shadow_echo_encounter()}")
    print(f"  • Grid: {coe_compassion.simulate_grid_corruption()['layout']}\n")

    # Simulation 2: Ruthless / Guilt path
    coe_ruthless = CathedralOfEchoes()
    coe_ruthless.record_action("executed_enemy")
    coe_ruthless.record_action("abandon_allies")
    coe_ruthless.record_dialogue("threat")
    coe_ruthless.complete_mission_echoes_of_judgment()

    print("[Path B: Ruthless / Guilt Outcome]")
    print(f"  • Morality: {coe_ruthless.player.morality}")
    print(f"  • Traits: {list(coe_ruthless.player.traits.keys())}")
    print(f"  • Abilities: {list(coe_ruthless.player.abilities.keys())}")
    print(f"  • Codex: {coe_ruthless.player.unlocked_codex.get('PlayerPath')}")
    print(f"  • NPC: {coe_ruthless.simulate_shadow_echo_encounter()}")
    print(f"  • Grid: {coe_ruthless.simulate_grid_corruption()['layout']}")

    print("\n[Weapon Testing: Griefshard & Judicator's Coil]")
    griefshard = next(w for w in coe_ruthless.player.inventory_weapons if w.name == "Griefshard")
    dmg = griefshard.calculate_damage(coe_ruthless.player.morality, echo_intensity=3)
    print(f"  • Griefshard Base DMG + Guilt Echo (Intensity 3): {dmg} DMG")
    print(f"  • Consequence: {griefshard.guilt_consequence}")


if __name__ == "__main__":
    if "--json" in sys.argv:
        engine = CathedralOfEchoes()
        engine.record_action("spared_enemy")
        engine.complete_mission_echoes_of_judgment()
        print(json.dumps(engine.to_dict(), indent=2))
    else:
        run_demo()
