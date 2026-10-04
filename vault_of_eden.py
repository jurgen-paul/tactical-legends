#!/usr/bin/env python3
"""
Vault of Eden - Symphonic Tactical Combat & Dynamic Encounter Engine
Converted from 'Vault of Eden.sc' Scala script into a full Python simulation.

Features:
- 3 Boss Phases:
  1. Harmonic Sentinels: Beat-synchronized rhythm combat & Echo Dash
  2. Legacy Pulse Shift: Historical choices unlock 'Chord of Mercy'
  3. Echo Leviathan: Morality Dissonance boss evolution & Echo Accord protocol
- Dynamic Trait-Based Dialogue Trees (Varis, Syntax, Nyri)
- Symphonic Gear Sync & Relic Resonance Mechanics
"""

import sys
import json
import time
from dataclasses import dataclass, field
from enum import Enum
from typing import List, Dict, Optional, Any


class BossPhase(Enum):
    PHASE_1_SENTINELS = "Phase I: Resonant Guardians Awaken"
    PHASE_2_LEGACY = "Phase II: Legacy Pulse Shift"
    PHASE_3_LEVIATHAN = "Phase III: Echo Leviathan — Moral Dissonance"
    COMPLETED = "Encounter Concluded"


@dataclass
class DialogueLine:
    speaker: str
    text: str
    trait_trigger: Optional[str] = None


@dataclass
class VaultSquadMember:
    name: str
    role: str
    trait: str  # "Protective", "Ruthless", "Empathetic"
    morale: int = 70
    hp: int = 100
    gear_synced: bool = True


class VaultOfEdenEncounter:
    def __init__(self, morality_score: int = 65, prior_civilian_rescue: bool = True):
        self.morality_score = morality_score
        self.prior_civilian_rescue = prior_civilian_rescue
        self.stability: int = 100
        self.current_phase: BossPhase = BossPhase.PHASE_1_SENTINELS
        self.boss_hp: int = 300
        self.boss_max_hp: int = 300
        self.echo_accord_activated: bool = False
        self.unlocked_relics: List[str] = []
        self.combat_logs: List[str] = []
        self.squad: List[VaultSquadMember] = [
            VaultSquadMember("Captain Varis", "Squad Leader", "Protective"),
            VaultSquadMember("Ronin Syntax", "Vanguard Breacher", "Ruthless"),
            VaultSquadMember("Tech Seer Nyri", "Relic Specialist", "Empathetic")
        ]

    def log(self, message: str):
        self.combat_logs.append(message)

    def phase_1_beat_sync_combat(self, on_beat: bool = True) -> Dict[str, Any]:
        """Phase I: Resonant Guardians Awaken (Harmonic Sentinels x4)."""
        self.log(f"Entering {self.current_phase.value}")
        self.log("HUD: Morality Score >= +60 — Harmonic Conduit Unlocked.")

        if on_beat:
            self.boss_hp -= 100
            self.log(">> Squad executes 'Echo Dash' on rhythm beat! Sentinels damaged (-100 HP).")
            self.log(">> Stability maintained: 100/100.")
        else:
            self.stability = max(0, self.stability - 12)
            self.boss_hp -= 50
            self.log(">> Sync Mismatch Detected! Stability dropped (-12). Squad afflicted with Confusion.")

        self.current_phase = BossPhase.PHASE_2_LEGACY
        return {
            "phase": "Phase 1 Complete",
            "boss_hp": f"{self.boss_hp}/{self.boss_max_hp}",
            "stability": self.stability
        }

    def phase_2_legacy_pulse_shift(self) -> Dict[str, Any]:
        """Phase II: Vault reacts based on prior war council legacy decisions."""
        self.log(f"\nTriggering {self.current_phase.value}")
        if self.prior_civilian_rescue:
            self.unlocked_relics.append("Chord of Mercy")
            self.boss_hp -= 60
            self.log("VAULT SYSTEM: >> 'Legacy Thread: Compassion Protocol Verified.'")
            self.log(">> Relic Unlocked: 'Chord of Mercy' (Empathetic squad trait boosts damage).")
            # Boost empathetic member
            for m in self.squad:
                if m.trait == "Empathetic":
                    m.morale += 20
        else:
            self.log("VAULT SYSTEM: >> 'Legacy Thread: Pragmatic Sacrifice Verified.'")
            self.unlocked_relics.append("Pulse of Silence")

        self.log("ENEMY SHIFT: Harmonic Sentinels fuse into Echo Leviathan!")
        self.current_phase = BossPhase.PHASE_3_LEVIATHAN
        return {
            "phase": "Phase 2 Complete",
            "relics_unlocked": self.unlocked_relics,
            "boss_hp": f"{self.boss_hp}/{self.boss_max_hp}"
        }

    def phase_3_echo_leviathan(self, activate_echo_accord: bool = True) -> Dict[str, Any]:
        """Phase III: Moral Dissonance boss fight & Echo Accord choice."""
        self.log(f"\nTriggering {self.current_phase.value}")

        if self.morality_score > 0:
            self.log("• Positive Morality: Boss attacks sync with music, telegraphable and rhythmic.")
        else:
            self.log("• Negative Morality: Boss becomes erratic; unpredictable chaos pulses disrupt squad.")

        self.echo_accord_activated = activate_echo_accord
        if activate_echo_accord:
            self.boss_hp = 0
            self.current_phase = BossPhase.COMPLETED
            self.log("PLAYER CHOICE: >> 'Activate Echo Accord Protocol: YES'")
            self.log(">> Squad harmonizes psychic frequency — Echo Leviathan is peacefully destabilized!")
            self.log("🏆 VAULT BREACH SUCCESSFUL: The Heart of Eden awakens in full resonance.")
        else:
            self.log("PLAYER CHOICE: >> 'Activate Echo Accord Protocol: NO'")
            self.log(">> Squad fractures! Trait clash risk activates.")
            for m in self.squad:
                if m.trait == "Ruthless":
                    self.log(f"⚠️ {m.name} rejects sentimental leadership and goes rogue as hostile NPC!")
                    m.morale = 0
            self.boss_hp = 0
            self.current_phase = BossPhase.COMPLETED
            self.log("💀 VAULT COLLAPSE: Core extracted through brutal force with internal casualties.")

        return {
            "phase": "Phase 3 Complete",
            "boss_defeated": True,
            "echo_accord": self.echo_accord_activated,
            "relics": self.unlocked_relics
        }

    def get_trait_dialogue(self) -> List[DialogueLine]:
        """Generate dialogue branches based on squad composition and traits."""
        return [
            DialogueLine("Captain Varis (Protective)", "This vault remembers loss. Stay tight—we go in together.", "Protective"),
            DialogueLine("Ronin Syntax (Ruthless)", "You sound sentimental. Sentiment dies first.", "Ruthless"),
            DialogueLine("Tech Seer Nyri (Empathetic)", "They hear us. We move in music, or we die in silence.", "Empathetic"),
            DialogueLine("Vault System", "Echo protocol detected: Prior civilian sacrifice embedded in neural lattice.", "System"),
            DialogueLine("Ronin Syntax", "So we’re praised for weakness?", "Ruthless"),
            DialogueLine("Captain Varis", "No. For remembering who we fight for.", "Protective")
        ]

    def run_full_simulation(self) -> Dict[str, Any]:
        """Executes the full 3-phase Vault encounter."""
        self.log("=== INITIATING VAULT OF EDEN EXPEDITION ===")
        self.phase_1_beat_sync_combat(on_beat=True)
        self.phase_2_legacy_pulse_shift()
        self.phase_3_echo_leviathan(activate_echo_accord=True)
        return {
            "status": "Victory",
            "morality_score": self.morality_score,
            "final_stability": self.stability,
            "relics_secured": self.unlocked_relics,
            "encounter_log": self.combat_logs,
            "dialogue": [
                {"speaker": d.speaker, "text": d.text}
                for d in self.get_trait_dialogue()
            ]
        }


def main():
    encounter = VaultOfEdenEncounter(morality_score=75, prior_civilian_rescue=True)
    if "--json" in sys.argv:
        print(json.dumps(encounter.run_full_simulation(), indent=2))
        return

    print("=======================================================")
    print("🏛️  VAULT OF EDEN: SYMPHONIC TACTICAL ENCOUNTER")
    print("=======================================================\n")

    res = encounter.run_full_simulation()
    print("Encounter Sequence:")
    for log in res["encounter_log"]:
        print(f"  {log}")

    print("\nDramatic Dialogue Seeds:")
    for d in res["dialogue"]:
        print(f"  💬 {d['speaker']}: \"{d['text']}\"")

    print(f"\nRelics Secured: {', '.join(res['relics_secured'])}")
    print(f"Final Stability: {res['final_stability']}% | Outcome: {res['status']}")


if __name__ == "__main__":
    main()
