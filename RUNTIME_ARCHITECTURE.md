# Tactical Legends: Rise of OISTARIAN - Python Runtime
# Unified Single-Language Game Engine

## Quick Start

```bash
# Install dependencies (minimal - pure Python)
pip install -r requirements.txt

# Run interactive menu
python run.py

# Run specific commands
python run.py --briefing       # Show mission briefing with dialogue
python run.py --squad          # Show squad roster
python run.py --factions       # Show all factions
python run.py --relics         # Show relic catalog
python run.py --simulate       # Run battle simulation
python run.py --status         # Show engine status snapshot
```

## Architecture

```
core/
├── __init__.py              # Package exports
├── engine.py                # Master game engine & state
├── world.py                 # World data (factions, relics, missions)
├── combat.py                # Tactical combat system
├── ai.py                    # Behavior trees & pathfinding
├── squad.py                 # Squad roster & member management
├── narrative.py             # Story engine & dialogue trees
├── ui.py                    # Rich console UI panels
├── events.py                # Event bus (pub/sub)
├── data_loader.py           # JSON config/data loading
└── audio.py                 # Audio manager stub

data/
├── missions/index.json      # Mission definitions
├── abilities/index.json     # Ability catalog
└── equipment/index.json     # Equipment catalog

run.py                        # Unified runtime launcher
main.py                       # Legacy entrypoint (deprecated)
requirements.txt              # Python dependencies
README.md                      # This file
```

## Systems

### 1. Engine (`core/engine.py`)
- Global game state machine
- Mission progression
- Morale & intel tracking
- Story event logging
- State snapshots for UI/API

### 2. World (`core/world.py`)
- Faction definitions
- Relic catalog
- Mission database
- Story beats
- Bootstraps game world on startup

### 3. Combat (`core/combat.py`)
- Grid-based tactical battles
- Unit positioning & movement
- Attack resolution
- Cover mechanics
- Status effects

### 4. AI (`core/ai.py`)
- Behavior trees (Selector, Sequence, Action, Condition)
- A* pathfinding
- Enemy decision-making
- Difficulty scaling

### 5. Squad (`core/squad.py`)
- Squad roster management
- Member stats & progression
- Equipment & ability loadouts
- Squad-wide synergies

### 6. Narrative (`core/narrative.py`)
- Dialogue tree system
- Branching conversation paths
- Morale modifiers from choices
- Story state tracking

### 7. UI (`core/ui.py`)
- Rich console panels
- Mission briefing cards
- Faction dossiers
- Relic artifact cards
- Battle status display
- Story event logging

### 8. Events (`core/events.py`)
- Publish/subscribe event bus
- Game-wide event routing
- Listener registration

## Running the Game

### Interactive Mode (Default)
```bash
python run.py
```

Menu-driven interface to:
- View mission briefings
- Inspect squad roster
- Browse world factions
- Examine relic catalog
- Simulate battles
- Check engine status

### CLI Mode
Each command shows formatted output:

```bash
python run.py --briefing
```
Shows mission briefing card with:
- Sector & threat level
- Primary objective
- Recommended loadout
- Mission rewards
- Dialogue tree (deploy confirmation)

### API Server Mode (Optional)
```bash
python -m http.server 3000
```

Then access:
- `http://localhost:3000/api/health` - Engine status
- `http://localhost:3000/api/mission` - Active mission
- `http://localhost:3000/api/squad` - Squad roster
- `http://localhost:3000/api/battle` - Battle status

## Game Flow

1. **Boot** → Load world state (factions, relics, missions)
2. **Select Mission** → Choose operation from available missions
3. **Mission Briefing** → View objectives, rewards, dialogue
4. **Squad Preparation** → Review roster, equipment, abilities
5. **Combat** → Execute tactical battle (AI vs Player)
6. **Debrief** → Narrative resolution, rewards, story progression
7. **Campaign** → Unlock new missions, relics, factions

## Development

To add new content:

### New Mission
Edit `data/missions/index.json`:
```json
{
  "mission_custom": {
    "id": "mission_custom",
    "name": "Custom Operation",
    "sector": "Sector X-1",
    "objective": "Secure the objective",
    "threat_level": "High",
    "enemy_count": 8,
    "rewards": [...]
  }
}
```

### New Faction
Update `core/world.py` `WorldState.bootstrap()`:
```python
Faction(
    "New Faction",
    "ideology",
    "control region",
    threat_level,
    "description"
)
```

### New Dialogue Tree
```python
from core.narrative import DialogueTree, DialogueNode

tree = DialogueTree("my_dialogue")
node = DialogueNode("start", "Speaker", "Hello...")
node.add_choice("Response", "next_node_id")
tree.add_node(node)
```

## Requirements

```
Python 3.8+
```

No external dependencies - pure stdlib Python.

## License

Apache 2.0

## Status

✅ Python Unified Runtime v2.0
✅ Single-language architecture
✅ Rich console UI
✅ Narrative engine
✅ Combat system
✅ AI behavior trees
✅ Squad management
✅ World data model

🔄 Next: Web dashboard, mobile port, multiplayer
