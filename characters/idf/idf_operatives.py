#!/usr/bin/env python3
"""
Tactical Legends - IDF Character Roster & Resource Parser
Parses Godot .tres resources and provides structured queryable data for all IDF operatives.
"""

import os
import re
import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Dict, Optional, Any

IDF_DIR = Path(__file__).resolve().parent


@dataclass
class IDFSoldier:
    name: str
    role: str
    background: str = ""
    expertise: List[str] = field(default_factory=list)
    rank: str = ""
    file_source: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "rank": self.rank,
            "role": self.role,
            "background": self.background,
            "expertise": self.expertise,
            "source_file": self.file_source
        }


class IDFRoster:
    def __init__(self, directory: Optional[Path] = None):
        self.dir = directory or IDF_DIR
        self.soldiers: List[IDFSoldier] = []
        self._load_tres_files()

    def _load_tres_files(self):
        tres_files = [f for f in self.dir.glob("*.tres")]
        for tf in sorted(tres_files):
            try:
                content = tf.read_text(encoding="utf-8")
                name_m = re.search(r'name\s*=\s*"([^"]+)"', content)
                role_m = re.search(r'role\s*=\s*"([^"]+)"', content)
                bg_m = re.search(r'background\s*=\s*"([^"]+)"', content)
                exp_m = re.search(r'expertise\s*=\s*\[(.*?)\]', content, re.DOTALL)

                if name_m and role_m:
                    name = name_m.group(1)
                    # Extract rank
                    rank = name.split()[0] if name else "Operative"
                    expertise = []
                    if exp_m:
                        expertise = [e.strip(' "\n\r') for e in exp_m.group(1).split(",") if e.strip(' "\n\r')]

                    soldier = IDFSoldier(
                        name=name,
                        role=role_m.group(1),
                        background=bg_m.group(1) if bg_m else "",
                        expertise=expertise,
                        rank=rank,
                        file_source=tf.name
                    )
                    self.soldiers.append(soldier)
            except Exception as e:
                print(f"[IDFRoster] Warning: Could not parse {tf.name}: {e}")

    def get_all(self) -> List[IDFSoldier]:
        return self.soldiers

    def filter_by_rank(self, rank_prefix: str) -> List[IDFSoldier]:
        return [s for s in self.soldiers if s.rank.lower() == rank_prefix.lower()]

    def search_role(self, query: str) -> List[IDFSoldier]:
        q = query.lower()
        return [s for s in self.soldiers if q in s.role.lower() or any(q in e.lower() for e in s.expertise)]

    def to_json(self) -> str:
        return json.dumps([s.to_dict() for s in self.soldiers], indent=2)


def get_idf_roster() -> IDFRoster:
    return IDFRoster()


if __name__ == "__main__":
    roster = get_idf_roster()
    print(f"=== IDF TACTICAL OPERATIVES ROSTER [{len(roster.soldiers)} OPERATIVES] ===")
    for rank in ["Lieutenant", "Sergeant", "Corporal", "Private"]:
        sub = roster.filter_by_rank(rank)
        print(f"\n--- {rank.upper()}S ({len(sub)}) ---")
        for s in sub:
            print(f"  • {s.name} - {s.role}")
