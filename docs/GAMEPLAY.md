# Tactical Legends — Gameplay Guide

Complete guide to game mechanics, combat system, unit customization, and campaign progression.

## Table of Contents

1. [Combat System](#combat-system)
2. [Unit Stats & Abilities](#unit-stats--abilities)
3. [Squad Customization](#squad-customization)
4. [Campaign Structure](#campaign-structure)
5. [Tactical Tips](#tactical-tips)
6. [Game Settings](#game-settings)

---

## Combat System

### Turn Management

Combat in Tactical Legends is **strictly turn-based**:

```
Player Turn Sequence:
├── Select a unit to activate
├── Choose an action:
│   ├── Move (costs movement points)
│   ├── Attack (costs action points)
│   ├── Use Ability (costs action points + optional resources)
│   └── Use Item (costs action points)
├── Confirm action
├── Animation plays
├── Results applied
└── Turn ends → Next unit's turn
```

### Action Points (AP)

- Each unit has a pool of **Action Points** per turn
- Different actions consume different amounts:
  - **Move**: 1 AP per tile (varies by terrain)
  - **Attack**: 1-2 AP depending on weapon
  - **Ability**: 2-3 AP depending on ability
  - **Item Use**: 1 AP

Example turn:
```
Unit starts with 2 AP
├── Move to new position (1 AP) → Remaining: 1 AP
├── Use Aimed Shot ability (1 AP) → Remaining: 0 AP
└── Turn ends (no actions left)
```

### Movement

- **Movement Speed**: Base stat determining tiles per turn
- **Terrain Cost**: Different terrain types cost different movement:
  - Plains: 1 movement point per tile
  - Forest: 2 movement points per tile
  - Rough: 2-3 movement points per tile
  - Water: Impassable (unless ability allows)

- **Cover Mechanics**:
  - Standing in cover reduces incoming damage
  - Partial cover: -20% damage
  - Full cover: -40% damage

### Attack Resolution

When attacking, the following occurs:

1. **Hit Chance Calculation**:
   ```
   Hit Chance = (Attacker Accuracy - Defender Evasion) + Range Modifier
   Range Modifier:
   - Close range (1-2 tiles): +20%
   - Medium range (3-5 tiles): 0%
   - Long range (6+ tiles): -20%
   ```

2. **Damage Calculation**:
   ```
   Base Damage = Weapon Damage + (Attacker Might - Armor)
   Final Damage = Base Damage × (1 + Critical Chance × Critical Multiplier)
   ```

3. **Armor & Mitigation**:
   - Each unit has an Armor stat
   - Armor reduces incoming damage by 1 per point (minimum 1 damage)
   - Cover stacks with armor

### Abilities

Units have special abilities that can:
- **Damage**: Deal area-of-effect or targeted damage
- **Heal**: Restore HP to self or allies
- **Control**: Move enemies or apply effects
- **Buff**: Increase stats temporarily
- **Debuff**: Decrease enemy stats or apply conditions

Example ability:
```
Suppressing Fire
├── Cost: 1 AP + 5 ammo
├── Range: 8 tiles
├── Effect: Deal damage to target and adjacent units
│   └── Targets hit suffer -20% accuracy next turn
├── Special: Can be used as reaction to enemy movement
```

### Conditions & Status Effects

Combat can inflict temporary conditions:

| Condition | Duration | Effect |
|-----------|----------|--------|
| Stunned | 1 turn | Can't act |
| Poisoned | 3 turns | Lose 1 HP per turn |
| Slowed | 2 turns | Movement halved |
| Bleeding | Until healed | Lose 1 HP per turn |
| Suppressed | 1 turn | Accuracy -20% |
| Marked | Until attack | Next attack from allies +30% damage |

---

## Unit Stats & Abilities

### Core Stats

Each unit has these primary stats:

| Stat | Range | Description |
|------|-------|-------------|
| **HP** | 5-20 | Health points; 0 = unit defeated |
| **Armor** | 0-10 | Damage reduction per hit |
| **Action Points (AP)** | 1-3 | Actions available per turn |
| **Movement** | 2-6 | Tiles you can move per turn |
| **Accuracy** | 30%-90% | Chance to hit with attacks |
| **Evasion** | 0%-40% | Reduces attacker hit chance |
| **Might** | 1-8 | Adds to physical damage |
| **Magic** | 1-8 | Adds to magical ability damage |
| **Willpower** | 1-8 | Resistance to mental/debuff abilities |
| **Speed** | 1-10 | Determines turn order |

### Unit Roles

**Frontline Warrior**
- High HP and Armor
- Medium Movement
- Good Might stat
- Abilities: Block, Counterattack, Taunt

**Marksman**
- Medium HP, Low Armor
- Medium Movement
- High Accuracy
- Abilities: Aimed Shot, Ricochet, Suppressing Fire

**Mage**
- Low HP and Armor
- Medium Movement
- High Magic stat
- Abilities: Fireball, Heal, Teleport

**Scout**
- Low HP, Low Armor
- High Movement
- High Evasion
- Abilities: Dash, Stealth, Reveal

**Support**
- Medium HP and Armor
- Low Movement
- Good Willpower
- Abilities: Heal, Buff, Revive

### Ability Types

#### Offensive Abilities

```
Fireball
├── Cost: 2 AP, 10 Mana
├── Range: 6 tiles
├── Area: 3x3 tile radius
├── Effect: Deal 5-8 damage to all units in area
└── Special: Ignite terrain for 2 turns
```

#### Defensive Abilities

```
Shield Bash
├── Cost: 1 AP
├── Range: Melee (adjacent)
├── Effect: Block next attack, push enemy back 2 tiles
└── Cooldown: 1 turn
```

#### Healing Abilities

```
Field Medic
├── Cost: 1 AP, 5 Mana
├── Range: 4 tiles
├── Effect: Restore 4-6 HP to target
├── Special: Also cures one condition
└── Cooldown: None
```

---

## Squad Customization

### Building Your Squad

A complete squad consists of **4-6 units** (mission dependent).

**Balanced squad example:**
```
Squad: OISTARIAN RECON
├── 1x Frontline Warrior (Tank)
├── 2x Marksman (Ranged damage)
├── 1x Mage (Area damage & Control)
└── 1x Support (Healing)
```

**Aggressive squad example:**
```
Squad: STRIKE FORCE
├── 2x Frontline Warrior (Tanks)
├── 2x Marksman (Ranged damage)
└── 1x Mage (Burst damage)
```

### Equipment System

#### Weapons

Each unit can equip:
- **Primary Weapon**: Rifle, Sword, Mace, Staff
- **Secondary Weapon/Item**: Pistol, Grenade, Shield

Weapon stats:
```json
{
  "name": "TL-Standard Rifle",
  "type": "Ranged",
  "damage": "3-5",
  "range": "4-8 tiles",
  "accuracy": "+10%",
  "weight": "Medium",
  "special": "Can suppress enemies"
}
```

#### Armor & Gear

- **Head Armor**: Helmet, Visor, Crown
- **Chest Armor**: Light, Medium, Heavy Vest
- **Legs**: Pants, Greaves, Exoskeleton
- **Accessory 1**: Amulet, Ring, Pendant
- **Accessory 2**: Backpack, Cloak, Badge

Armor provides:
- Armor stat increase
- Special resistances (fire, cold, magic)
- Passive bonuses (regeneration, damage reduction)

### Perks & Talents

Units unlock perks through leveling:

**Level 1 Perks:**
- Keen Eye: +10% accuracy
- Quick Reflexes: +1 movement speed
- Thick Skin: +2 armor

**Level 5 Perks:**
- Marksman: +20% critical damage
- Shield Mastery: +50% shield effectiveness
- Mana Efficiency: -20% ability cost

**Level 10 Perks:**
- Veteran Warrior: Attacks restore 1 HP
- Master Tactician: Gain +1 AP when moving
- Spell Amplification: Abilities do +30% damage

### Loadout Presets

Save multiple loadouts per unit:

```
Unit: Rifleman-01
├── Loadout 1: "Aggressor"
│   ├── Weapon: Assault Rifle
│   ├── Armor: Heavy Tactical Vest
│   └── Perks: Accuracy, Might
└── Loadout 2: "Scout"
    ├── Weapon: Sniper Rifle
    ├── Armor: Light Combat Suit
    └── Perks: Accuracy, Evasion
```

---

## Campaign Structure

### Campaign Progression

The campaign consists of **branching missions** across multiple chapters:

```
CAMPAIGN: RISE OF OISTARIAN

Chapter 1: Awakening
├── Mission 1.1: Prologue - Escape
├── Mission 1.2: Rally the Troops
└── Decision Point: Ally with Rebels or Militia?
    ├── Path A: Join the Rebels
    │   └── Chapter 2A: Shadow Operations
    └── Path B: Join the Militia
        └── Chapter 2B: Military Might

Chapter 3: The Vault of Eden
├── Mission 3.1: Investigate Ancient Site
├── Mission 3.2: Defend the Vault
└── Finale: Confront the Final Enemy
```

### Mission Types

**Story Missions**
- Mandatory campaign progression
- Unlock new units and abilities
- Advance the narrative

**Optional Missions**
- Side objectives for extra rewards
- Increased difficulty for challenge
- Unique unit/equipment unlocks

**Survival Missions**
- Wave-based enemies
- Endless enemies until defeat
- Leaderboard ranking

**Tactical Challenges**
- Specific objectives (protect area, eliminate target)
- Limited unit selections
- Puzzle-like gameplay

### Difficulty Levels

| Level | AI Behavior | Modifiers | Rewards |
|-------|-------------|-----------|---------|
| Easy | Hesitant, lower accuracy | -25% enemy damage | 1x base rewards |
| Normal | Balanced, typical tactics | No modifiers | 1x base rewards |
| Hard | Aggressive, flanking | +25% enemy damage | 1.5x rewards |
| Legendary | Perfect play, exploits | +50% enemy damage | 2x rewards |

### Mission Rewards

Upon completion, earn:
- **Gold**: Currency for equipment
- **Experience**: Levels up units
- **Loot**: New weapons/armor
- **Story Unlocks**: New chapters/units
- **Achievements**: Special recognition

---

## Tactical Tips

### Map Control

1. **High Ground**: Provides vision advantage
2. **Cover**: Use to protect from ranged attacks
3. **Flanking**: Attack enemies from multiple angles for bonus damage
4. **Chokepoints**: Funnel enemies into narrow areas

### Squad Positioning

```
Example formation against ranged enemies:

       Scout (mobile)
          |
Warrior - Support - Marksman
          |
       Warrior
          |
        Mage

Benefits:
- Warrior and Support form frontline
- Mage protected in center
- Marksman has clear line of sight
- Scout can flank/disrupt
```

### Resource Management

- **Action Points**: Don't waste - plan full turn ahead
- **Ability Cooldowns**: Track enemy cooldowns
- **Health**: Retreat to heal before unit dies
- **Mana/Ammo**: Budget for multiple turns

### AI Prediction

Common AI behaviors:
- Move to closest enemy
- Use high-damage ability if available
- Heal allies below 40% health
- Retreat if surrounded (on hard difficulty)

Use this to:
- Position units outside attack range
- Bait AI into traps
- Predict movement for ambushes

---

## Game Settings

### Difficulty

- **Combat Difficulty**: Enemy AI aggression
- **Encounter Scaling**: Adjust mission difficulty
- **Permadeath Mode**: Defeated units are gone forever
- **Iron Man Mode**: No manual saving, auto-save only

### Accessibility

- **Color Blind Mode**: Adjust palette for accessibility
- **Larger UI**: Increase interface scale
- **Text Size**: Adjust font size
- **Subtitle Speed**: Control dialogue pacing

### Graphics

- **Resolution**: Adjust game window size
- **Frame Rate**: Limit FPS for performance
- **Animation Speed**: Fast/Normal/Slow
- **Particle Effects**: On/Reduced/Off

### Audio

- **Master Volume**: 0-100%
- **Music Volume**: 0-100%
- **SFX Volume**: 0-100%
- **Voice Volume**: 0-100%

### Controls

- **Keyboard Bindings**: Customize key mappings
- **Mouse Sensitivity**: Adjust cursor speed
- **Controller Support**: Map gamepad buttons
- **Quick Action Keys**: Bind common actions

---

## Frequently Asked Questions

**Q: Can I change my squad mid-campaign?**
A: Yes, between missions you can swap units and equipment.

**Q: What happens if a unit dies?**
A: On normal difficulty, they're out for the current mission. On Permadeath, they're gone permanently.

**Q: How do I unlock new units?**
A: Complete missions, reach milestones, or unlock via achievements.

**Q: Can I retry a mission?**
A: Yes, any mission can be retried with your current squad.

**Q: What's the max unit level?**
A: Level 20, with new perks unlocking at each level.

**Q: Are there multiplayer battles?**
A: Campaign is single-player story. Check updates for future multiplayer.

---

**Last Updated**: September 2024
**Game Version**: 1.0.0
