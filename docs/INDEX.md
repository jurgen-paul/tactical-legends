# Documentation Index

Complete documentation for **Tactical Legends: Rise of OISTARIAN**

## Quick Links

| Document | Purpose | Audience |
|----------|---------|----------|
| [OVERVIEW.md](OVERVIEW.md) | Project overview, architecture, tech stack | Everyone |
| [INSTALLATION.md](INSTALLATION.md) | Setup & build instructions for all platforms | Developers |
| [GAMEPLAY.md](GAMEPLAY.md) | Game mechanics, combat system, strategies | Players, Game Designers |
| [ARCHITECTURE.md](ARCHITECTURE.md) | Technical design, code structure, patterns | Developers |
| [API.md](API.md) | Developer API reference | Developers |

---

## Documentation by Role

### 👤 Players

**Start Here:**
1. Read [GAMEPLAY.md](GAMEPLAY.md) for complete game mechanics
2. Learn [combat system](GAMEPLAY.md#combat-system) and [unit customization](GAMEPLAY.md#squad-customization)
3. Check [tactical tips](GAMEPLAY.md#tactical-tips) for strategy advice

**Key Sections:**
- Combat turn management and action points
- Unit roles and abilities
- Squad building strategies
- Campaign progression and story
- Game settings and accessibility

### 👨‍💻 Developers

**Getting Started:**
1. Install dependencies using [INSTALLATION.md](INSTALLATION.md)
2. Review [OVERVIEW.md](OVERVIEW.md) for project structure
3. Study [ARCHITECTURE.md](ARCHITECTURE.md) for technical design
4. Reference [API.md](API.md) for code interfaces

**Key Sections:**
- System architecture and layered design
- Game loop and event system
- Battle manager and AI system
- Build system and compilation
- Performance optimization techniques

### 🎮 Game Designers

**Essential Reading:**
1. [GAMEPLAY.md](GAMEPLAY.md) - Understand current mechanics
2. [ARCHITECTURE.md](ARCHITECTURE.md#game-systems) - Game systems overview
3. Design balance around existing unit stats and abilities

**Design Areas:**
- Unit stats and progression
- Ability costs and effectiveness
- Mission difficulty and scaling
- Campaign structure and pacing
- Difficulty levels and AI behavior

### 🔧 DevOps / Release Engineers

**Documentation:**
1. [INSTALLATION.md](INSTALLATION.md#build-system) - Build process
2. Review CI/CD workflow in `.github/workflows/`
3. Distribution notes in `store-assets/`

**Key Tasks:**
- Cross-platform builds (Linux, macOS, Windows)
- Testing and quality assurance
- Release automation and versioning
- Store listing preparation

---

## Documentation Structure

### Overview & Setup
```
Getting Started
├── OVERVIEW.md
│   ├── Project Overview
│   ├── System Architecture
│   ├── Core Gameplay Systems
│   ├── Technology Stack
│   └── Project Structure
├── INSTALLATION.md
│   ├── System Requirements
│   ├── Linux/Ubuntu Setup
│   ├── macOS Setup
│   ├── Windows Setup
│   ├── Troubleshooting
│   └── Development Setup
└── This File (INDEX.md)
```

### Game & Design
```
Gameplay & Design
├── GAMEPLAY.md
│   ├── Combat System
│   ├── Unit Stats & Abilities
│   ├── Squad Customization
│   ├── Campaign Structure
│   ├── Tactical Tips
│   └── Game Settings
└── Store Assets (in progress)
    └── Production & Preview Guidelines
```

### Technical Reference
```
Developer Reference
├── ARCHITECTURE.md
│   ├── Architecture Overview
│   ├── Core Engine
│   ├── Game Systems
│   ├── Data Layer
│   ├── AI System
│   ├── Build System
│   ├── Performance
│   └── Code Style
└── API.md (API reference)
    ├── Core Classes
    ├── Game Systems
    ├── Utilities
    └── Examples
```

---

## Key Concepts

### Turn-Based Combat

Combat flows through distinct phases:

```
Turn Start
  ├── Select Unit
  ├── Choose Action (Move/Attack/Ability)
  ├── Execute Action
  └── End Turn → Next Unit
```

**Resources:**
- Action Points (AP) - Limited per turn
- Abilities - Special actions with cooldowns
- Equipment - Weapons, armor, accessories

**References:** See [GAMEPLAY.md](GAMEPLAY.md#combat-system)

### Squad Management

Build balanced teams with:
- **Frontline Warriors** - High HP/Armor, melee combat
- **Marksmen** - Ranged damage dealers
- **Mages** - Area damage and crowd control
- **Support** - Healing and buffs
- **Scouts** - High mobility and evasion

**References:** See [GAMEPLAY.md](GAMEPLAY.md#unit-roles)

### Game Architecture

Layered system with clear separation:

```
UI Layer (Menus, HUD, Dialogue)
  ↓
Game Logic (Battle Manager, Campaign Manager)
  ↓
Engine Layer (Game Loop, Input, Events, Rendering)
  ↓
Platform Layer (SDL2, Audio, File I/O)
```

**References:** See [ARCHITECTURE.md](ARCHITECTURE.md#architecture-overview)

### AI System

Uses behavior trees for decision-making:

```
AI Makes Decisions
  ├── Evaluate Options (Attack, Move, Heal)
  ├── Select Best Action
  ├── Calculate Path (A* Pathfinding)
  └── Execute Action
```

Difficulty levels adjust:
- Accuracy and damage modifiers
- Aggression and decision-making
- Pathfinding and tactical awareness

**References:** See [ARCHITECTURE.md](ARCHITECTURE.md#ai-system)

---

## Common Tasks

### I want to...

**...build and run the game**
→ Follow [INSTALLATION.md](INSTALLATION.md) for your OS

**...understand how combat works**
→ Read [GAMEPLAY.md](GAMEPLAY.md#combat-system)

**...create custom units**
→ See [GAMEPLAY.md](GAMEPLAY.md#unit-stats--abilities) and modify `data/units.json`

**...add a new ability**
→ Reference [ARCHITECTURE.md](ARCHITECTURE.md#game-systems) and `src/systems/ability_system.cpp`

**...implement new AI behavior**
→ Review [ARCHITECTURE.md](ARCHITECTURE.md#ai-system) and `src/systems/ai/`

**...optimize performance**
→ Check [ARCHITECTURE.md](ARCHITECTURE.md#performance-considerations)

**...set up development environment**
→ Follow [INSTALLATION.md](INSTALLATION.md#development-setup)

**...prepare for release**
→ See production notes in `/docs/production-tactical-legend.md` and `/store-assets/`

---

## File Structure Reference

```
tactical-legends/
├── src/                          # Source code
│   ├── main.cpp
│   ├── engine/                   # Game engine
│   │   ├── game_loop.cpp
│   │   ├── input_system.cpp
│   │   ├── event_system.cpp
│   │   └── renderer.cpp
│   ├── systems/                  # Game systems
│   │   ├── battle_manager.cpp
│   │   ├── campaign_manager.cpp
│   │   ├── unit_manager.cpp
│   │   └── ai/                   # AI subsystem
│   │       ├── behavior_tree.cpp
│   │       ├── pathfinding.cpp
│   │       └── difficulty_scaler.cpp
│   ├── ui/                       # UI system
│   │   ├── menu.cpp
│   │   ├── hud.cpp
│   │   └── dialog.cpp
│   ├── audio/
│   │   └── audio_manager.cpp
│   ├── data/
│   │   ├── config.h
│   │   ├── units.json
│   │   ├── abilities.json
│   │   └── missions.json
│   └── utils/
│       ├── logger.cpp
│       └── math_utils.cpp
├── tests/                        # Unit tests
│   ├── test_battle_manager.cpp
│   ├── test_ai_system.cpp
│   └── test_pathfinding.cpp
├── docs/                         # Documentation
│   ├── OVERVIEW.md              # ← Start here
│   ├── INSTALLATION.md
│   ├── GAMEPLAY.md
│   ├── ARCHITECTURE.md
│   ├── API.md
│   └── INDEX.md                 # This file
├── store-assets/                # App store resources
│   ├── icon_512.png
│   ├── feature_graphic.png
│   ├── screenshots/
│   └── annotated/
├── CMakeLists.txt              # Build configuration
├── README.md                   # Project README
├── LICENSE                     # Apache 2.0 License
└── .github/
    └── workflows/              # CI/CD pipelines
        └── ci.yml
```

---

## Getting Help

### Common Questions

**Q: Where do I start as a new developer?**
A: Read [INSTALLATION.md](INSTALLATION.md) to set up your environment, then [OVERVIEW.md](OVERVIEW.md) to understand the project.

**Q: How do I add a new feature?**
A: Review [ARCHITECTURE.md](ARCHITECTURE.md) to understand system structure, then implement following the documented patterns.

**Q: What are the game's core mechanics?**
A: See [GAMEPLAY.md](GAMEPLAY.md) for complete gameplay rules and systems.

**Q: How is the AI implemented?**
A: See [ARCHITECTURE.md](ARCHITECTURE.md#ai-system) for detailed AI system design.

**Q: Can I contribute?**
A: Yes! Check [CONTRIBUTING.md](../CONTRIBUTING.md) for guidelines.

### Resources

- **GitHub Repository**: https://github.com/jurgen-paul/tactical-legends
- **Issue Tracker**: https://github.com/jurgen-paul/tactical-legends/issues
- **Discussions**: https://github.com/jurgen-paul/tactical-legends/discussions
- **Project Website**: https://jurgen-paul.github.io/tactical-legends/

### Report Issues

Found a bug or have a suggestion?

1. **Search existing issues** to avoid duplicates
2. **Create a new issue** with:
   - Clear title describing the problem
   - Steps to reproduce (for bugs)
   - Expected vs actual behavior
   - System information (OS, hardware)
   - Screenshots or logs if applicable

---

## Version History

| Version | Date | Notes |
|---------|------|-------|
| 1.0.0 | Sept 2024 | Initial release with core gameplay |
| 0.9.0 | Aug 2024 | Beta testing phase |
| 0.5.0 | July 2024 | Foundation and core systems |

---

## Glossary

| Term | Definition |
|------|-----------|
| **AP** | Action Points - limited resource per unit turn |
| **AI** | Artificial Intelligence - enemy behavior system |
| **HUD** | Heads-Up Display - on-screen game information |
| **UI** | User Interface - menus and interactive elements |
| **Tilemap** | Grid-based map for tactical positioning |
| **Ability** | Special action or power available to units |
| **Status Effect** | Temporary condition affecting unit stats |
| **Turn-Based** | Combat where units take turns sequentially |
| **Behavior Tree** | AI decision-making structure |
| **Pathfinding** | Algorithm for unit movement (A*) |

---

## Quick Reference

### Build Commands
```bash
# Configure
cmake -S. -B build -DCMAKE_BUILD_TYPE=Release

# Compile
cmake --build build -j$(nproc)

# Run
./build/tactical_legends

# Test
cd build && ctest --output-on-failure
```

### Key Files to Modify

| Task | File | Reference |
|------|------|-----------|
| Add unit | `data/units.json` | [GAMEPLAY.md](GAMEPLAY.md#unit-stats--abilities) |
| Add ability | `data/abilities.json` | [GAMEPLAY.md](GAMEPLAY.md#ability-types) |
| Adjust AI | `src/systems/ai/` | [ARCHITECTURE.md](ARCHITECTURE.md#ai-system) |
| Change balance | `src/systems/battle_manager.cpp` | [ARCHITECTURE.md](ARCHITECTURE.md#battle-manager) |
| Add mission | `data/missions.json` | [GAMEPLAY.md](GAMEPLAY.md#mission-types) |

---

## Next Steps

1. **New Players**: Read [GAMEPLAY.md](GAMEPLAY.md) to learn the game
2. **New Developers**: Follow [INSTALLATION.md](INSTALLATION.md) and read [OVERVIEW.md](OVERVIEW.md)
3. **Contributors**: Check [CONTRIBUTING.md](../CONTRIBUTING.md)
4. **Release Team**: Review production notes in `/store-assets/`

---

**Documentation Last Updated**: September 7, 2024
**Project Version**: 1.0.0
**License**: Apache 2.0
