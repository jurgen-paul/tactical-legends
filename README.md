<div align="center">

# ⚔️ Tactical Legends: Rise of OISTARIAN

**A turn-based tactical strategy game featuring deep squad customization, adaptive AI behavior trees, and branching narrative campaigns set across the dunes and cyber-citadels of Oistarian.**

[![CI](https://github.com/jurgen-paul/tactical-legends/actions/workflows/ci.yml/badge.svg)](https://github.com/jurgen-paul/tactical-legends/actions)
[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](LICENSE)
[![OpenSSF Best Practices](https://www.bestpractices.dev/projects/default/badge)](https://www.bestpractices.dev/)
[![OpenSSF Scorecard](https://api.securityscorecards.dev/projects/github.com/jurgen-paul/tactical-legends/badge)](https://securityscorecards.dev/viewer/?repo=github.com/jurgen-paul/tactical-legends)
[![Platform](https://img.shields.io/badge/Platform-Linux%20%7C%20macOS%20%7C%20Windows%20%7C%20Web-00d4ff.svg)](#installation)
[![Engine](https://img.shields.io/badge/Engine-C%2B%2B%20%2F%20SDL2%20%2F%20Node.js-38bdf8.svg)](#architecture)

<br />

<img src="TL_001.jpeg" alt="Tactical Legends — Rise of OISTARIAN Hero Banner" width="100%" style="border-radius: 8px; max-height: 480px; object-fit: cover;" />

</div>

---

## 📑 Table of Contents

- [About the Game](#-about-the-game)
- [Key Features](#-key-features)
- [Visual Dossier & Media](#-visual-dossier--media)
- [System Architecture](#-system-architecture)
- [Installation & Quick Start](#-installation--quick-start)
  - [Web Applet (AI Studio / Node.js)](#1-web-applet-ai-studio--nodejs)
  - [Native C++ Engine (CMake & SDL2)](#2-native-c-engine-cmake--sdl2)
- [Testing & Verification](#-testing--verification)
- [Data-Driven Design & Modding](#-data-driven-design--modding)
- [Play Store Release Checklist](#-play-store-release-checklist)
- [Contributing](#-contributing)
- [License & Support](#-license--support)

---

## 🌌 About the Game

In the ancient, war-torn sands of **Oistarian**, forgotten relic vaults clash with high-tech corporate hegemony. As a tactical squad commander, you lead specialized fireteams through treacherous subterranean chambers, sandstorms, and fortified citadels.

Every choice matters:
* **The AP Economy**: Manage Action Points (AP) across unit movement, cover maneuvering, primary fire, and specialized gadget activations.
* **The Core Loop**: `Loadout Customization` ➔ `Silent Infiltration` ➔ `Grid Engagement` ➔ `Relic Extraction` ➔ `Narrative Debrief`.
* **Dynamic Morality & Faction Trust**: Align with ritualist factions like the *Crimson Vow*, tech-purists like *Echo Ascendants*, or corporate enforcers in the *Dominion*.

---

## ⚡ Key Features

- **🎯 Tactical Grid-Based Combat**: High-stakes turn-based combat with realistic cover mechanics, directional sightlines, elevation advantages, and suppression fire.
- **🤖 Adaptive AI Behavior Trees**: Opponents evaluate flanking corridors, lay down overwatch fire, coordinate suppression, and fall back when morale deteriorates.
- **🛡️ Futuristic Gadget Ecosystem**: Deploy surveillance drones, portable kinetic energy shields, optical camouflage cloaks, and EMP disruption charges.
- **🔬 Relic Fusion Matrix**: Recover prehistoric Oistarian relics (like the *Echo Core* and *Iron Sigil*) and forge them into synergistic *Surge Beacons* granting team-wide neural reflex buffs.
- **📖 Branching Campaign Paths**: Dynamic story paths influenced by your operative mortality rate, faction standing, and tactical objectives achieved.
- **🧩 Cross-Platform & Modular**: Built with a clean CMake architecture in C++ / SDL2, paired with a modern Node.js web command portal.

---

## 🖼️ Visual Dossier & Media

Explore key operatives, environments, and tactical interface schematics from *Tactical Legends: Rise of OISTARIAN*:

### 1. Frontline Vanguard — Operative TL-001
<img src="TL_001.jpeg" alt="Tactical Operative TL-001 — Frontline Vanguard" width="100%" />

*Heavy assault operative deployed in contested desert sectors, equipped with hardened ballistic plating and standard modular pulse rifle.*

---

### 2. Recon Specialist — Unit TL-003
<img src="TL_003.jpeg" alt="Recon Specialist TL-003 — Advanced Scout" width="100%" />

*Long-range tactical scout specializing in optical reconnaissance, sensor jamming, high-velocity sniper fire, and stealth flank maneuvers.*

---

### 3. Urban Infiltration Specialist — Operative TL-008
<img src="TL_008.jpeg" alt="Urban Infiltration Specialist TL-008" width="100%" />

*Cyber-warfare and CQB operative firing a precision marksman rifle over a neon skyline as VTOL support crafts coordinate extraction.*

---

### 4. The Vault of Eden — Ancient Subterranean Chamber
<img src="_bf325426-3049-42b5-b67d-b0049ca7858b.jpeg" alt="Vault of Eden — Ancient Subterranean Chamber" width="100%" />

*Cloaked operative exploring the primordial Vault of Eden beneath the desert surface, deciphering ancient relic inscriptions.*

---

### 5. Squad Bay Interface & Unit Diagnostics
<img src="store-assets/annotated/annotated-ss5.svg" alt="Tactical Legends Squad Bay UI & Diagnostics" width="100%" />

*Squad Bay terminal schematic detailing operative health (HP), action points (AP), movement speed (MOV), weapon range (RNG), and active ability loadouts.*

---

## 🏛️ System Architecture

Tactical Legends enforces a modular, decoupled engine design:

```
┌─────────────────────────────────────────────────────────────┐
│                       UI / HUD LAYER                        │
│          Menus, Squad Bay, Dialog, Web Command Terminal      │
├─────────────────────────────────────────────────────────────┤
│                     GAME LOGIC LAYER                        │
│    BattleManager, CampaignBranchingManager, Inventory, Lore │
├─────────────────────────────────────────────────────────────┤
│                    AI DECISION SUBSYSTEM                    │
│      Behavior Trees, A* Pathfinding, Difficulty Scaler      │
├─────────────────────────────────────────────────────────────┤
│                       ENGINE LAYER                          │
│         Game Loop, Event Bus, Input System, Renderer        │
├─────────────────────────────────────────────────────────────┤
│                      PLATFORM LAYER                         │
│       SDL2 (Graphics/Audio), File I/O, Web Host (Node.js)   │
└─────────────────────────────────────────────────────────────┘
```

<img width="100%" alt="Tactical Legends Architecture Diagram" src="https://github.com/user-attachments/assets/e6e160a1-1a7d-42f6-8991-63b6786e1112" />

### Onboarding Flow for Contributors
<img width="100%" alt="Onboarding Flow Diagram" src="https://github.com/user-attachments/assets/31835e2c-649f-4518-a8db-625105ac725b" />

---

## 🛠️ Installation & Quick Start

### 1. Web Applet (AI Studio / Node.js)

The web showcase and tactical command console run directly via Node.js on port 3000:

```bash
# Clone the repository
git clone https://github.com/jurgen-paul/tactical-legends.git
cd tactical-legends

# Install dependencies
npm install

# Start the dev server on port 3000 (0.0.0.0)
npm run dev
```

Visit `http://localhost:3000` to view the interactive briefing console, operative dossier, and documentation portal.

---

### 2. Native C++ Engine (CMake & SDL2)

To compile the standalone native engine client on Linux (Ubuntu/Debian):

```bash
# Install toolchain and SDL2 development libraries
sudo apt update
sudo apt install cmake g++ libsdl2-dev libsdl2-image-dev libsdl2-mixer-dev libsdl2-ttf-dev

# Generate build configuration
mkdir build && cd build
cmake -S .. -B . -DCMAKE_BUILD_TYPE=Release

# Compile binary
cmake --build . -j$(nproc)

# Launch game
./tactical_legends
```

On **macOS** (via Homebrew):
```bash
brew install cmake sdl2 sdl2_image sdl2_mixer sdl2_ttf
mkdir build && cd build
cmake .. && make -j
./tactical_legends
```

---

## 🧪 Testing & Verification

Automated unit tests validate pathfinding accuracy, damage formulas, and AI state transitions:

```bash
cd build
ctest --output-on-failure
```

For web applet verification:
```bash
npm run build
```

---

## 💾 Data-Driven Design & Modding

Tactical Legends loads content dynamically from JSON configurations.

### Adding an Operative
In `resource/CODEX.json`:
```json
{
  "name": "Lieutenant Sofia Varga",
  "faction": "Independent Operative",
  "role": "Intelligence",
  "expertise": ["Cyber infiltration", "Interrogation resistance", "Signal triangulation"],
  "unlockCondition": "Decode the 'Black Cipher' relic",
  "portraitPath": "Images/Operatives/SofiaVarga"
}
```

### Adding a Mission Configuration
In `Sample MissionConfig.json`:
```json
{
  "id": "MISSION_001",
  "name": "Dawn Infiltration",
  "environment": "UrbanRuins",
  "objectives": [
    { "type": "Infiltrate", "location": "ArmoryAccess" },
    { "type": "DisableCore", "location": "ReactorRoom" },
    { "type": "Exfiltrate", "location": "ExtractionPoint" }
  ],
  "difficulty": 1,
  "moralityImpact": 5,
  "branchingRules": {
    "ifMoralityGte": 50,
    "ifTrustGte": { "EchoAscendants": 60 }
  }
}
```

---

## 📱 Play Store Release Checklist

If packaging for Google Play Store Android distribution:

1. **Identifiers**:
   - Package Name: `com.example.tacticallegends`
   - Target SDK: Android 12+ (API 31+)
2. **Assets**:
   - High-Res Icon: 512x512 PNG (`store-assets/icon_512.png`)
   - Feature Graphic: 1024x500 PNG (`store-assets/feature_graphic.png`)
   - Screenshots: Portrait and landscape phone screenshots from `store-assets/screenshots/`
3. **Build Command**:
   ```bash
   bundletool build-apks --bundle=app-release.aab --output=app.apks --mode=universal
   bundletool install-apks --apks=app.apks
   ```

---

## 🤝 Contributing

We warmly welcome community contributions! Whether you're optimizing pathfinding algorithms, designing new maps, or translating narrative lore:

1. Fork the repository.
2. Create your feature branch (`git checkout -b feature/tactical-drone-support`).
3. Commit your changes (`git commit -m 'feat: Add EMP reconnaissance drone'`).
4. Push to the branch (`git push origin feature/tactical-drone-support`).
5. Open a Pull Request.

Please see [CONTRIBUTING.md](CONTRIBUTING.md) and our [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) for detailed guidelines.

---

## 📜 License & Support

* **License**: Distributed under the **Apache License 2.0**. See [`LICENSE`](LICENSE) for terms.
* **Documentation**: Full technical documentation is available in [`/docs/INDEX.md`](docs/INDEX.md).
* **Issues & Discussions**: Report bugs and propose game balancing changes in the [GitHub Issues](https://github.com/jurgen-paul/tactical-legends/issues) tracker.

<div align="center">
  <sub>Built with passion for tactical strategy gaming. Rise of OISTARIAN — Command, Customize, Conquer.</sub>
</div>
