"""
Mission Manager - Mission structure, objectives, and campaign flow.

Handles:
- Mission loading and progression
- Objective tracking
- Branching narratives
- Mission completion and rewards
"""

from enum import Enum
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Callable
from pathlib import Path
import json


class ObjectiveType(Enum):
    """Mission objective types."""
    ELIMINATE_ENEMIES = "eliminate_enemies"
    PROTECT_UNIT = "protect_unit"
    REACH_LOCATION = "reach_location"
    RETRIEVE_ITEM = "retrieve_item"
    SURVIVE_WAVES = "survive_waves"
    STEALTH_ONLY = "stealth_only"


class MissionDifficulty(Enum):
    """Mission difficulty tiers."""
    EASY = 1
    NORMAL = 2
    HARD = 3
    NIGHTMARE = 4


@dataclass
class Objective:
    """Single mission objective."""
    id: str
    name: str
    objective_type: ObjectiveType
    description: str
    target_value: int = 0  # Enemy count, turns survived, etc.
    is_primary: bool = True
    is_complete: bool = False
    progress: int = 0
    
    def update_progress(self, amount: int = 1):
        """Increment progress toward objective."""
        self.progress = min(self.progress + amount, self.target_value)
        if self.progress >= self.target_value:
            self.is_complete = True


@dataclass
class Mission:
    """A playable mission."""
    id: str
    name: str
    description: str
    environment: str  # "desert", "urban", "jungle", etc.
    difficulty: MissionDifficulty
    faction: str  # Mission giver faction
    
    objectives: List[Objective] = field(default_factory=list)
    available_squad_slots: int = 4
    turn_limit: Optional[int] = None
    
    enemy_count: int = 0
    enemy_types: List[str] = field(default_factory=list)
    
    rewards_credits: int = 0
    rewards_xp: int = 0
    unlocks: List[str] = field(default_factory=list)
    
    branches: Dict[str, str] = field(default_factory=dict)  # Branching narrative paths
    
    is_complete: bool = False
    success: bool = False
    morale_impact: int = 0
    
    def get_primary_objectives(self) -> List[Objective]:
        """Get primary mission objectives."""
        return [o for o in self.objectives if o.is_primary]
    
    def get_optional_objectives(self) -> List[Objective]:
        """Get optional side objectives."""
        return [o for o in self.objectives if not o.is_primary]
    
    def check_completion(self) -> bool:
        """Check if primary objectives are complete."""
        primary = self.get_primary_objectives()
        return all(o.is_complete for o in primary)
    
    def to_dict(self) -> dict:
        """Serialize to dictionary."""
        return {
            "id": self.id,
            "name": self.name,
            "difficulty": self.difficulty.name,
            "environment": self.environment,
            "objectives": [
                {
                    "id": o.id,
                    "name": o.name,
                    "progress": o.progress,
                    "target": o.target_value,
                    "complete": o.is_complete,
                }
                for o in self.objectives
            ],
            "is_complete": self.is_complete,
            "success": self.success,
        }


class MissionManager:
    """Manages mission database and progression."""
    
    def __init__(self, data_loader):
        self.data_loader = data_loader
        self.missions: Dict[str, Mission] = {}
        self.current_mission: Optional[Mission] = None
        self.mission_history: List[str] = []
        
        self._load_missions()
    
    def _load_missions(self):
        """Load missions from data files."""
        missions_data = self.data_loader.load("data/missions/index.json")
        
        for mission_id, mission_data in missions_data.items():
            self.missions[mission_id] = self._parse_mission(mission_data)
        
        print(f"[MissionManager] Loaded {len(self.missions)} missions")
    
    def _parse_mission(self, data: dict) -> Mission:
        """Parse mission from JSON."""
        objectives = []
        for obj_data in data.get("objectives", []):
            obj = Objective(
                id=obj_data["id"],
                name=obj_data["name"],
                objective_type=ObjectiveType[obj_data["type"]],
                description=obj_data.get("description", ""),
                target_value=obj_data.get("target", 0),
                is_primary=obj_data.get("primary", True),
            )
            objectives.append(obj)
        
        mission = Mission(
            id=data["id"],
            name=data["name"],
            description=data.get("description", ""),
            environment=data.get("environment", "desert"),
            difficulty=MissionDifficulty[data.get("difficulty", "NORMAL")],
            faction=data.get("faction", "Unknown"),
            objectives=objectives,
            available_squad_slots=data.get("squad_slots", 4),
            turn_limit=data.get("turn_limit"),
            enemy_count=data.get("enemy_count", 0),
            enemy_types=data.get("enemy_types", []),
            rewards_credits=data.get("rewards", {}).get("credits", 0),
            rewards_xp=data.get("rewards", {}).get("xp", 0),
            unlocks=data.get("unlocks", []),
            branches=data.get("branches", {}),
            morale_impact=data.get("morale_impact", 0),
        )
        
        return mission
    
    def get_mission(self, mission_id: str) -> Optional[Mission]:
        """Get mission by ID."""
        return self.missions.get(mission_id)
    
    def start_mission(self, mission_id: str) -> bool:
        """Start a mission."""
        mission = self.get_mission(mission_id)
        if mission:
            self.current_mission = mission
            self.mission_history.append(mission_id)
            print(f"[MissionManager] Started mission: {mission.name}")
            return True
        return False
    
    def complete_mission(self, success: bool = True) -> dict:
        """Complete current mission."""
        if not self.current_mission:
            return {}
        
        mission = self.current_mission
        mission.is_complete = True
        mission.success = success
        
        rewards = {
            "credits": mission.rewards_credits if success else int(mission.rewards_credits * 0.5),
            "xp": mission.rewards_xp if success else int(mission.rewards_xp * 0.5),
            "unlocked": mission.unlocks if success else [],
        }
        
        print(f"[MissionManager] Mission complete: {mission.name} ({'SUCCESS' if success else 'FAILED'})")
        print(f"[MissionManager] Rewards: {rewards['credits']} credits, {rewards['xp']} XP")
        
        return rewards
    
    def get_available_missions(self) -> List[Mission]:
        """Get missions player can access."""
        return list(self.missions.values())
    
    def get_mission_briefing(self, mission_id: str) -> str:
        """Get formatted mission briefing."""
        mission = self.get_mission(mission_id)
        if not mission:
            return ""
        
        briefing = f"""
╔════════════════════════════════════════╗
║  MISSION BRIEFING: {mission.name:^26} ║
╠════════════════════════════════════════╣
║ Difficulty:    {mission.difficulty.name:^26} ║
║ Environment:   {mission.environment:^26} ║
║ Enemies:       {mission.enemy_count:^26} ║
╠════════════════════════════════════════╣
║ OBJECTIVES:                            ║
"""
        
        for obj in mission.get_primary_objectives():
            briefing += f"║ • {obj.name}\n"
        
        if mission.get_optional_objectives():
            briefing += "║\n║ OPTIONAL:\n"
            for obj in mission.get_optional_objectives():
                briefing += f"║ ◦ {obj.name}\n"
        
        briefing += """╠════════════════════════════════════════╣
║ REWARDS:                               ║"""
        briefing += f"║ Credits: {mission.rewards_credits:>28} ║\n"
        briefing += f"║ XP:      {mission.rewards_xp:>28} ║\n"
        briefing += "╚════════════════════════════════════════╝"
        
        return briefing
