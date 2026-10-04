#!/usr/bin/env python3
"""
Tactical Legends - Squad Member Architecture
Defines elite squad operatives, gear loadouts, combat stats, and emotional states.
"""

from dataclasses import dataclass, field, asdict
from enum import Enum
from typing import List, Dict, Optional, Any
import json


class OperativeClass(Enum):
    CYBER_ENGINEER = "Cyber Engineer"
    SCOUT = "Holo Scout"
    VANGUARD = "Vault Vanguard"
    WARRIOR = "Dominion Warrior"
    TACTICIAN = "Echo Tactician"
    MEDIC = "Bio-Nano Medic"


class EmotionalState(Enum):
    RESOLUTE = "Resolute"
    FOCUSED = "Focused"
    HYPER_AWARE = "Hyper-Aware"
    ANGRY = "Angry"
    OVERCLOCKED = "Overclocked"
    STEALTH = "Stealth"


@dataclass
class GearItem:
    id: str
    name: str
    slot: str  # "weapon", "shield", "implant", "relic"
    stat_modifiers: Dict[str, int] = field(default_factory=dict)
    special_perk: Optional[str] = None


@dataclass
class SquadMember:
    id: str
    name: str
    class_type: OperativeClass
    health: int = 100
    max_health: int = 100
    shields: int = 50
    max_shields: int = 50
    action_points: int = 4
    movement_range: int = 5
    attack_power: int = 25
    defense: int = 15
    gear: Dict[str, GearItem] = field(default_factory=dict)
    traits: List[str] = field(default_factory=list)
    emotional_state: EmotionalState = EmotionalState.RESOLUTE
    status_effects: List[str] = field(default_factory=list)

    def is_alive(self) -> bool:
        return self.health > 0

    def take_damage(self, amount: int) -> int:
        """Apply damage first to shields, then to health."""
        effective_defense = self.defense
        for item in self.gear.values():
            effective_defense += item.stat_modifiers.get("defense", 0)

        mitigated = max(1, amount - (effective_defense // 3))
        if self.shields > 0:
            if self.shields >= mitigated:
                self.shields -= mitigated
                return mitigated
            else:
                remaining = mitigated - self.shields
                self.shields = 0
                self.health = max(0, self.health - remaining)
                return mitigated
        else:
            self.health = max(0, self.health - mitigated)
            return mitigated

    def heal(self, amount: int) -> int:
        before = self.health
        self.health = min(self.max_health, self.health + amount)
        return self.health - before

    def equip_gear(self, item: GearItem):
        self.gear[item.slot] = item

    def get_summary(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "class": self.class_type.value,
            "hp": f"{self.health}/{self.max_health}",
            "shields": f"{self.shields}/{self.max_shields}",
            "ap": self.action_points,
            "emotion": self.emotional_state.value,
            "gear": {slot: item.name for slot, item in self.gear.items()},
            "traits": self.traits
        }


class Squad:
    """Manages an active fireteam for tactical operations."""
    def __init__(self, name: str = "Alpha Strike Team"):
        self.name = name
        self.members: List[SquadMember] = []

    def add_member(self, member: SquadMember):
        if len(self.members) < 6:
            self.members.append(member)
        else:
            raise ValueError("Squad capacity reached (max 6 operatives)")

    def remove_member(self, member_id: str) -> bool:
        initial_len = len(self.members)
        self.members = [m for m in self.members if m.id != member_id]
        return len(self.members) < initial_len

    def get_operative(self, member_id: str) -> Optional[SquadMember]:
        for m in self.members:
            if m.id == member_id:
                return m
        return None

    def get_squad_summary(self) -> List[Dict[str, Any]]:
        return [m.get_summary() for m in self.members]

    def to_json(self) -> str:
        data = {
            "squad_name": self.name,
            "active_count": len(self.members),
            "roster": self.get_squad_summary()
        }
        return json.dumps(data, indent=2)


def get_default_squad() -> Squad:
    """Creates the canonical Tactical Legends squad (Oistarian, Zoe, Jax, Val)."""
    squad = Squad("Oistarian Strike Recon")

    oistarian = SquadMember(
        id="op-01",
        name="OISTARIAN",
        class_type=OperativeClass.CYBER_ENGINEER,
        health=140,
        max_health=140,
        shields=75,
        max_shields=75,
        attack_power=35,
        defense=22,
        traits=["Relentless Myth", "Overclock Mastery", "Eden Resonance"],
        emotional_state=EmotionalState.OVERCLOCKED
    )
    oistarian.equip_gear(GearItem(
        id="gear-01",
        name="NeuroPulse Kinetic Arm",
        slot="weapon",
        stat_modifiers={"attack": 18, "ap": 1},
        special_perk="Armor Piercing Arc"
    ))
    oistarian.equip_gear(GearItem(
        id="gear-02",
        name="Eden Shard Regulator",
        slot="relic",
        stat_modifiers={"shields": 25, "defense": 5}
    ))
    squad.add_member(oistarian)

    zoe = SquadMember(
        id="op-02",
        name="Zoe",
        class_type=OperativeClass.SCOUT,
        health=95,
        max_health=95,
        shields=40,
        max_shields=40,
        movement_range=7,
        attack_power=28,
        traits=["Holo Decoy", "Digital Glitch", "Data Siphon"],
        emotional_state=EmotionalState.HYPER_AWARE
    )
    zoe.equip_gear(GearItem(
        id="gear-03",
        name="Silenced Flux Carbine",
        slot="weapon",
        stat_modifiers={"attack": 14}
    ))
    squad.add_member(zoe)

    jax = SquadMember(
        id="op-03",
        name="Commander Jax",
        class_type=OperativeClass.VANGUARD,
        health=160,
        max_health=160,
        shields=90,
        max_shields=90,
        defense=30,
        traits=["Bulwark Stance", "Suppression Fire"],
        emotional_state=EmotionalState.RESOLUTE
    )
    jax.equip_gear(GearItem(
        id="gear-04",
        name="Heavy Aegis Barrier",
        slot="shield",
        stat_modifiers={"shields": 40, "defense": 10}
    ))
    squad.add_member(jax)

    val = SquadMember(
        id="op-04",
        name="Doctor Val",
        class_type=OperativeClass.MEDIC,
        health=85,
        max_health=85,
        shields=50,
        max_shields=50,
        traits=["Field Nanites", "Stim Booster"],
        emotional_state=EmotionalState.FOCUSED
    )
    squad.add_member(val)

    return squad


if __name__ == "__main__":
    squad = get_default_squad()
    print(f"--- Squad {squad.name} Initialized ---")
    print(squad.to_json())
