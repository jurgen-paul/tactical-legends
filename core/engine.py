from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Dict, Any

from core.world import WorldState


@dataclass
class TacticalEngine:
    world: WorldState = field(default_factory=lambda: WorldState().bootstrap())
    current_mission_index: int = 0
    turn: int = 1
    morale: int = 78
    intel: int = 0
    story_log: List[str] = field(default_factory=list)

    def __post_init__(self):
        self.world = self.world.bootstrap()
        self.story_log = [
            "Command uplink stable.",
            "Relic pulse detected in the Dune Rift.",
            "Squad readiness at 78%.",
        ]

    def next_mission(self):
        if self.current_mission_index + 1 < len(self.world.missions):
            self.current_mission_index += 1
        else:
            self.current_mission_index = 0
        self.turn = 1
        self.story_log.append(f"Mission focus shifted to {self.world.missions[self.current_mission_index].name}.")
        return self.world.missions[self.current_mission_index]

    def run_battle_summary(self) -> Dict[str, Any]:
        mission = self.world.missions[self.current_mission_index]
        return {
            "mission": mission.name,
            "sector": mission.sector,
            "threat_level": mission.threat_level,
            "turn": self.turn,
            "morale": self.morale,
            "intel": self.intel,
            "rewards": mission.rewards,
            "story_beat": self.world.random_event().title,
        }

    def update_story(self, text: str):
        self.story_log.append(text)

    def status_snapshot(self) -> Dict[str, Any]:
        mission = self.world.missions[self.current_mission_index]
        return {
            "mission": mission.name,
            "objective": mission.objective,
            "sector": mission.sector,
            "threat": mission.threat_level,
            "morale": self.morale,
            "intel": self.intel,
            "plot": self.story_log[-2:],
        }
