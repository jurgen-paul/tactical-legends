# Software Architecture — Tactical Legends

Detailed technical architecture guide for developers working on Tactical Legends.

## Table of Contents

1. [Architecture Overview](#architecture-overview)
2. [Core Engine](#core-engine)
3. [Game Systems](#game-systems)
4. [Data Layer](#data-layer)
5. [AI System](#ai-system)
6. [Build System](#build-system)
7. [Performance Considerations](#performance-considerations)

---

## Architecture Overview

### Layered Architecture

Tactical Legends uses a **layered architecture** with clear separation of concerns:

```
┌─────────────────────────────────────────────────────────────┐
│                    Presentation Layer                        │
│  (UI, HUD, Menus, Dialogue, Visual Effects)                 │
└─────────────────────────────────────────────────────────────┘
                           ↑↓
┌─────────────────────────────────────────────────────────────┐
│                    Game Logic Layer                          │
│  (Battle Manager, Campaign Manager, Unit System)            │
└─────────────────────────────────────────────────────────────┘
                           ↑↓
┌─────────────────────────────────────────────────────────────┐
│                    Engine Layer                              │
│  (Game Loop, Input System, Event System, Renderer)          │
└─────────────────────────────────────────────────────────────┘
                           ↑↓
┌─────────────────────────────────────────────────────────────┐
│                    Platform Layer                            │
│  (SDL2, Audio, File I/O, Platform Abstractions)             │
└─────────────────────────────────────────────────────────────┘
```

### Design Patterns Used

- **Singleton**: Game instance, asset manager, audio manager
- **Observer**: Event system, input handling
- **Factory**: Unit creation, ability instantiation
- **Strategy**: AI tactics, ability execution
- **State Machine**: Unit states, battle states
- **Behavior Tree**: AI decision making

---

## Core Engine

### Game Loop

**File**: `src/engine/game_loop.cpp`

```cpp
class GameLoop {
    void run() {
        while (is_running) {
            float delta_time = clock.tick();
            
            // 1. Handle input
            input_system.process();
            
            // 2. Update game logic
            for (auto& system : game_systems) {
                system->update(delta_time);
            }
            
            // 3. Render frame
            renderer.begin_frame();
            for (auto& entity : scene.entities) {
                renderer.render(entity);
            }
            renderer.end_frame();
        }
    }
};
```

**Key Components:**
- **Delta Time**: Frames are time-independent (fixed or variable)
- **60 FPS Target**: ~16.67ms per frame
- **Vsync**: Optional frame limiting to monitor refresh rate

### Event System

**File**: `src/engine/event_system.cpp`

```cpp
class EventSystem {
    // Publish-subscribe pattern
    void subscribe(EventType type, Callback callback);
    void unsubscribe(EventType type, Callback callback);
    void emit(const Event& event);
};

// Usage
event_system.subscribe(EventType::UNIT_ATTACKED, [](const Event& e) {
    auto unit = e.get<Unit*>("attacker");
    auto damage = e.get<int>("damage");
    // Handle event
});
```

**Common Events:**
- `UNIT_MOVED`: Unit changed position
- `UNIT_ATTACKED`: Unit attacked another
- `ABILITY_USED`: Special ability activated
- `MISSION_COMPLETE`: Mission objectives met
- `BATTLE_END`: Combat phase ended

### Input System

**File**: `src/engine/input_system.cpp`

```cpp
class InputSystem {
    void process();
    
    bool is_key_pressed(KeyCode key);
    bool is_key_released(KeyCode key);
    vec2 get_mouse_position();
    bool is_mouse_clicked(MouseButton btn);
};

// Common inputs
enum class GameAction {
    SELECT_UNIT,
    MOVE,
    ATTACK,
    USE_ABILITY,
    END_TURN,
    OPEN_MENU,
    PAUSE
};
```

### Renderer

**File**: `src/engine/renderer.cpp`

Uses SDL2 for all graphics:

```cpp
class Renderer {
    void begin_frame();
    void render_sprite(const Sprite& sprite, vec2 position);
    void render_ui_element(const UIElement& element);
    void end_frame();
    
    // Drawing primitives
    void draw_rectangle(const Rect& rect, const Color& color);
    void draw_line(vec2 start, vec2 end, const Color& color);
    void draw_text(const std::string& text, vec2 pos, const Font& font);
};
```

**Rendering Pipeline:**
1. Clear screen
2. Render game world (layers: terrain, units, effects)
3. Render UI overlays
4. Present frame to display

---

## Game Systems

### Battle Manager

**File**: `src/systems/battle_manager.cpp`

Manages turn-based combat:

```cpp
class BattleManager {
    void start_battle(const Mission& mission);
    void process_turn();
    void end_turn();
    void resolve_action(const UnitAction& action);
    
    void calculate_hit(const Unit& attacker, const Unit& defender);
    void apply_damage(Unit& target, int damage);
    void apply_effect(Unit& target, const StatusEffect& effect);
    
    BattleState get_state() const;
    bool is_battle_over() const;
};
```

**State Machine:**
```
SETUP → PLAYER_TURN → AI_TURN → CHECK_END_CONDITION
  ↑                                        ↓
  └────────────────────────────────────────┘

END_CONDITION:
├── PLAYER_WIN: All enemies defeated
├── PLAYER_LOSE: All player units defeated
└── ABORT: Player retreats
```

### Unit System

**File**: `src/systems/unit_manager.cpp`

Manages unit state and actions:

```cpp
class Unit {
    // Core stats
    int hp, max_hp;
    int armor;
    int action_points, max_ap;
    int movement_speed;
    
    // Combat stats
    float accuracy;
    float evasion;
    int might;
    int magic;
    int willpower;
    int speed;
    
    // State
    vec2 position;
    std::vector<Ability> abilities;
    Equipment equipment;
    std::vector<StatusEffect> status_effects;
    
    // Methods
    void move_to(vec2 target);
    void perform_attack(Unit& target);
    void use_ability(const Ability& ability, vec2 target);
    void take_damage(int damage);
    void heal(int amount);
    void apply_status_effect(const StatusEffect& effect);
};
```

**Data Structure (JSON):**
```json
{
  "id": "unit_rifleman_01",
  "name": "Trooper-9BF9",
  "role": "Frontline",
  "level": 1,
  "experience": 0,
  "stats": {
    "hp": 10,
    "armor": 3,
    "actionPoints": 2,
    "movement": 4,
    "accuracy": 0.7,
    "evasion": 0.1,
    "might": 2,
    "magic": 1,
    "willpower": 2,
    "speed": 3
  },
  "equipment": {
    "weapon": "TL-Standard-Rifle",
    "armor": "Light-Tactical-Vest"
  },
  "abilities": ["Aimed-Shot", "Suppressing-Fire", "Take-Cover"],
  "perks": ["Marksman", "Steady-Aim"]
}
```

### Campaign Manager

**File**: `src/systems/campaign_manager.cpp`

Manages story progression:

```cpp
class CampaignManager {
    void load_campaign(const std::string& campaign_id);
    void start_mission(const std::string& mission_id);
    void complete_mission();
    void make_story_choice(const std::string& choice_id);
    
    const Mission& current_mission() const;
    bool is_campaign_complete() const;
    void save_progress();
    void load_progress();
};
```

**Campaign Structure:**
```
Campaign: Rise of OISTARIAN
├── Checkpoint: Chapter 1
│   ├── Mission: Prologue
│   ├── Mission: Rally the Troops
│   └── Choice Point: Join Rebels or Militia?
└── Checkpoint: Chapter 2
    ├── Mission: Based on Choice
    └── ...
```

---

## Data Layer

### Configuration Files

**Units Database** (`data/units.json`):
```json
{
  "units": [
    {
      "id": "unit_rifleman_01",
      "name": "Rifleman",
      "template": "frontline",
      "baseStats": { /* stats */ }
    }
  ]
}
```

**Abilities Database** (`data/abilities.json`):
```json
{
  "abilities": [
    {
      "id": "ability_aimed_shot",
      "name": "Aimed Shot",
      "cost": 1,
      "costType": "AP",
      "range": 8,
      "damage": "3-5",
      "effects": ["accuracy_bonus"]
    }
  ]
}
```

**Missions Database** (`data/missions.json`):
```json
{
  "missions": [
    {
      "id": "mission_prologue",
      "chapter": 1,
      "title": "Escape",
      "map": "map_prologue",
      "enemies": ["enemy_patrol_1", "enemy_patrol_2"],
      "objectives": ["survive_5_turns", "reach_exit"],
      "rewards": {
        "gold": 100,
        "experience": 50
      }
    }
  ]
}
```

### Asset Management

**File**: `src/engine/asset_manager.cpp`

```cpp
class AssetManager {
    static AssetManager& instance();
    
    // Loading
    Sprite load_sprite(const std::string& path);
    Texture load_texture(const std::string& path);
    Sound load_sound(const std::string& path);
    Font load_font(const std::string& path);
    
    // Caching
    void preload_assets(const std::vector<std::string>& paths);
    void unload_unused_assets();
    void clear_all();
};
```

**Asset Paths:**
```
assets/
├── sprites/
│   ├── units/
│   ├── terrain/
│   └── ui/
├── textures/
├── sounds/
│   ├── effects/
│   └── music/
├── fonts/
└── data/
    ├── units.json
    ├── abilities.json
    └── missions.json
```

### Save System

**File**: `src/engine/save_manager.cpp`

```cpp
struct SaveData {
    std::string player_name;
    int campaign_progress;
    int current_mission;
    std::vector<Unit> squad;
    std::map<std::string, int> inventory;
    long timestamp;
};

class SaveManager {
    void save_game(const std::string& slot, const SaveData& data);
    SaveData load_game(const std::string& slot);
    std::vector<SaveData> list_saves();
    void delete_save(const std::string& slot);
};
```

---

## AI System

### Behavior Tree

**File**: `src/systems/ai/behavior_tree.cpp`

```cpp
class BehaviorNode {
    virtual NodeState execute(AIAgent& agent) = 0;
};

class SelectorNode : public BehaviorNode {
    NodeState execute(AIAgent& agent) override {
        for (auto& child : children) {
            if (child->execute(agent) == NodeState::SUCCESS) {
                return NodeState::SUCCESS;
            }
        }
        return NodeState::FAILURE;
    }
};

class SequenceNode : public BehaviorNode {
    NodeState execute(AIAgent& agent) override {
        for (auto& child : children) {
            if (child->execute(agent) != NodeState::SUCCESS) {
                return NodeState::FAILURE;
            }
        }
        return NodeState::SUCCESS;
    }
};
```

**Example Behavior Tree:**
```
root (Selector)
├── IsHealthLow? (Condition)
│   └── FindNearestHealer (Action)
├── CanAttackEnemy? (Condition)
│   └── AttackEnemy (Action)
├── CanAdvance? (Condition)
│   └── MoveForward (Action)
└── Idle (Action)
```

### Pathfinding

**File**: `src/systems/ai/pathfinding.cpp`

Uses **A\* algorithm**:

```cpp
class Pathfinder {
    std::vector<vec2> find_path(vec2 start, vec2 goal, 
                                const Tilemap& tilemap);
private:
    float heuristic(vec2 a, vec2 b) const;
    std::vector<vec2> reconstruct_path(vec2 current);
};
```

**Heuristic**: Manhattan distance for tile-based movement
**Cost**: Terrain type and obstacles

### Difficulty Scaling

**File**: `src/systems/ai/difficulty_scaler.cpp`

```cpp
class DifficultyScaler {
    float accuracy_modifier;      // Easy: 0.6x, Hard: 1.4x
    float damage_modifier;         // Easy: 0.75x, Hard: 1.25x
    float aggression_level;        // Easy: 0.5, Hard: 1.0
    float decision_randomness;     // Easy: 0.8, Hard: 0.2
    
    void set_difficulty(DifficultyLevel level);
    UnitAction select_action(Unit& unit, const BattleState& state);
};
```

---

## Build System

### CMake Configuration

**File**: `CMakeLists.txt`

```cmake
cmake_minimum_required(VERSION 3.16)
project(tactical_legends)

# C++17 standard
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Find dependencies
find_package(SDL2 REQUIRED)
find_package(SDL2_image REQUIRED)
find_package(SDL2_mixer REQUIRED)
find_package(SDL2_ttf REQUIRED)

# Source files
file(GLOB_RECURSE SOURCES "src/*.cpp")

# Create executable
add_executable(tactical_legends ${SOURCES})

# Link libraries
target_link_libraries(tactical_legends 
    SDL2::SDL2 
    SDL2::SDL2_image 
    SDL2::SDL2_mixer 
    SDL2::SDL2_ttf
)

# Tests
enable_testing()
add_subdirectory(tests)
```

### Compiler Flags

```cmake
# Release build (optimized)
set(CMAKE_CXX_FLAGS_RELEASE "-O3 -DNDEBUG")

# Debug build (with symbols)
set(CMAKE_CXX_FLAGS_DEBUG "-g -O0 -DDEBUG")

# Warnings
add_compile_options(-Wall -Wextra -Wpedantic)

# Platform-specific
if(MSVC)
    add_compile_options(/W4)
endif()
```

---

## Performance Considerations

### Memory Management

- **Object Pools**: Pre-allocate units, abilities, effects
- **Smart Pointers**: Use `std::unique_ptr` and `std::shared_ptr`
- **Asset Caching**: Load once, reference many times
- **Garbage Collection**: Cleanup unused entities per frame

### Rendering Optimization

- **Sprite Batching**: Group render calls by texture
- **Viewport Culling**: Only render visible entities
- **Texture Atlas**: Combine small images into single texture
- **Mipmap Levels**: Use appropriate texture resolution

### AI Optimization

- **Pathfinding Cache**: Cache paths between frames
- **Decision Throttling**: Recalculate AI decisions every N frames
- **Spatial Partitioning**: Divide map into grids for queries
- **Ability Filtering**: Pre-filter valid abilities before evaluation

### Profiling

```cpp
class PerformanceProfiler {
    void start(const std::string& tag);
    void end(const std::string& tag);
    void report() const;  // Print timing data
};

// Usage
{
    ScopedProfile prof("AI_DECISION_MAKING");
    // Code to profile
}  // Automatically ends and logs
```

---

## Code Style Guidelines

### Naming Conventions

```cpp
// Classes: PascalCase
class BattleManager { };

// Functions/Methods: snake_case
void process_input() { }

// Constants: UPPER_SNAKE_CASE
const int MAX_UNITS = 6;

// Variables: snake_case
int unit_count = 0;

// Private members: m_prefix
class Unit {
private:
    int m_hp;
    std::string m_name;
};
```

### Header Guards

```cpp
#ifndef TACTICAL_LEGENDS_BATTLE_MANAGER_H_
#define TACTICAL_LEGENDS_BATTLE_MANAGER_H_

// Content

#endif  // TACTICAL_LEGENDS_BATTLE_MANAGER_H_
```

### Documentation

```cpp
/// Processes a single turn in battle.
/// 
/// @param unit The unit taking the turn
/// @return true if turn was valid, false otherwise
bool process_turn(Unit& unit);

/// Calculates damage with modifiers.
///
/// Formula: base_damage * (1 - armor_reduction) * crit_multiplier
int calculate_damage(int base_damage, int armor, 
                     float crit_chance) const;
```

---

## Dependency Graph

```
main.cpp
├── GameLoop
│   ├── InputSystem
│   ├── EventSystem
│   ├── Renderer
│   │   ├── SDL2
│   │   └── AssetManager
│   └── BattleManager
│       ├── UnitManager
│       ├── AISystem
│       └── EventSystem
├── CampaignManager
│   └── SaveManager
└── AudioManager
    └── SDL2_mixer
```

---

**Last Updated**: September 2024
**Architecture Version**: 1.0
