# Changelog

All notable changes to **Tactical Legends: Rise of OISTARIAN** are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- AI difficulty scaling system with randomness adjustments
- New documentation suite (OVERVIEW.md, INSTALLATION.md, GAMEPLAY.md, ARCHITECTURE.md)
- Development workflow guidelines (WORKFLOW.md)
- Project website with landing page (docs/index.html)
- Support for custom unit loadout presets
- Perks and talent system for unit progression

### Changed
- Improved pathfinding performance on large maps
- Enhanced UI responsiveness for better player experience
- Refactored battle state management for cleaner code

### Fixed
- [#123] Turn order reset after unit defeat
- [#125] AI units stuck on impassable terrain
- [#127] Ability cooldown not resetting on new mission

### Deprecated
- Old configuration format (migrate to JSON by v1.1.0)

### Security
- Updated SDL2 to patch security vulnerability in image loading

---

## [1.0.0] - 2024-09-07

### Added (First Stable Release)

#### Core Gameplay
- ✅ Turn-based tactical combat system with action points
- ✅ Squad customization with 20+ hero units
- ✅ 5 unit roles: Warrior, Marksman, Mage, Scout, Support
- ✅ Deep equipment system (weapons, armor, accessories)
- ✅ Ability system with 40+ unique abilities
- ✅ Status effects and conditions (Stunned, Poisoned, Slowed, etc.)
- ✅ Cover mechanics and terrain advantages
- ✅ Line-of-sight and fog of war

#### Campaign & Story
- ✅ 10+ story missions across 3 chapters
- ✅ Branching narrative with multiple story paths
- ✅ 3 difficulty levels (Easy, Normal, Hard)
- ✅ Mission rewards and progression system
- ✅ Character dialogue and story sequences

#### AI System
- ✅ Behavior tree-based decision making
- ✅ A* pathfinding algorithm
- ✅ Adaptive difficulty scaling
- ✅ Combat and tactical analysis
- ✅ Difficulty modifiers for accuracy and damage

#### Graphics & UI
- ✅ SDL2-powered rendering engine
- ✅ Main menu with game options
- ✅ In-game HUD with unit information
- ✅ Tactical map display with fog of war
- ✅ Ability hotbar and quick actions
- ✅ Mission briefing screens
- ✅ Victory/defeat screens

#### Audio
- ✅ Background music system
- ✅ Sound effects for combat and abilities
- ✅ UI feedback sounds
- ✅ Audio volume control in settings
- ✅ Music and SFX toggle

#### Cross-Platform Support
- ✅ Windows (10+) via Visual Studio
- ✅ macOS (10.14+) via Homebrew
- ✅ Linux (Ubuntu 18.04+, Fedora, Arch)
- ✅ CMake build system
- ✅ Consistent gameplay across platforms

#### Testing & Quality Assurance
- ✅ Unit tests for core systems
- ✅ Integration tests for battle scenarios
- ✅ CI/CD pipeline with GitHub Actions
- ✅ Automated build verification
- ✅ Test coverage reporting

#### Development & Documentation
- ✅ Complete project documentation
- ✅ Installation guides for all platforms
- ✅ Gameplay mechanics documentation
- ✅ Technical architecture reference
- ✅ Developer API documentation
- ✅ Contributing guidelines
- ✅ Code of Conduct

#### Project Infrastructure
- ✅ Public GitHub repository
- ✅ Issue tracking system
- ✅ Discussion forum
- ✅ GitHub Pages project website
- ✅ Store assets preparation
- ✅ Release automation

### Technical Details

#### Technology Stack
- **Language**: C++ (C++17)
- **Graphics**: SDL2, SDL2_image
- **Audio**: SDL2_mixer, SDL2_ttf
- **Build System**: CMake 3.16+
- **Testing**: CTest, Google Test
- **CI/CD**: GitHub Actions
- **Documentation**: Markdown

#### Performance Metrics
- Target: 60 FPS on standard hardware
- Memory footprint: ~150MB baseline
- Load time: <5 seconds on SSD
- Pathfinding: <10ms per request
- AI decisions: <50ms per unit

#### System Requirements
- **Minimum**: Intel i5, 4GB RAM, 2GB storage
- **Recommended**: Intel i7, 8GB RAM, 2GB SSD storage
- **Display**: 1920×1080 or higher

---

## [0.9.0] - 2024-08-15

### Added (Beta Release)
- Battle system with turn management
- Core unit types and basic abilities
- Campaign mission framework
- AI opponent with basic tactics
- Main menu and game UI
- Sound effects and music
- Settings menu with game options
- Save/load game functionality
- Cross-platform building with CMake

### Changed
- Refactored game loop for better performance
- Improved input handling system
- Enhanced UI responsiveness

### Fixed
- [#98] Audio crash on Linux systems
- [#102] UI scaling issues on high-DPI displays
- [#105] Memory leak in sprite management

---

## [0.5.0] - 2024-07-01

### Added (Alpha Release - Foundation)
- Core game engine with SDL2
- Event system and input handling
- Basic tilemap rendering
- Unit spawning and movement
- Damage calculation system
- Basic AI pathfinding (A*)
- Asset management system
- Game state management
- Configuration loading from JSON

### Changed
- Switched from OpenGL to SDL2 for better cross-platform compatibility
- Refactored rendering pipeline for modularity

### Fixed
- [#45] Game crash on unit creation
- [#52] Memory leaks in event system

---

## [0.1.0] - 2024-06-01

### Added (Initial Commit - Project Setup)
- Project initialization with CMake
- Basic file structure
- SDL2 dependency setup
- GitHub repository creation
- README and documentation template
- CI/CD pipeline setup
- License (Apache 2.0)
- .gitignore configuration
- Initial empty game framework

---

## Roadmap

### v1.1.0 (Planned - Q4 2024)
- [ ] Multiplayer skirmish mode
- [ ] Unit leveling and permanent progression
- [ ] Additional 10+ mission campaign
- [ ] New unit roles and abilities
- [ ] Advanced map editor
- [ ] Performance optimization pass
- [ ] Accessibility improvements
- [ ] Community content support

### v1.2.0 (Planned - Q1 2025)
- [ ] Expanded story campaign (20+ missions)
- [ ] Customizable difficulty modifiers
- [ ] Leaderboard and achievements
- [ ] Battle replays and analysis tools
- [ ] User-generated content support
- [ ] Platform-specific optimizations

### v2.0.0 (Planned - Q2 2025)
- [ ] Cooperative multiplayer mode
- [ ] Competitive ranked battles
- [ ] Cross-platform play
- [ ] Enhanced graphics engine
- [ ] Full character customization
- [ ] Story DLC episodes
- [ ] Modding support
- [ ] Mobile port

---

## Version Details by Component

### Game Systems

| System | v0.1 | v0.5 | v0.9 | v1.0 | Status |
|--------|------|------|------|------|--------|
| Game Loop | ✓ | ✓ | ✓ | ✓ | Stable |
| Input System | ✓ | ✓ | ✓ | ✓ | Stable |
| Event System | | ✓ | ✓ | ✓ | Stable |
| Rendering | | ✓ | ✓ | ✓ | Stable |
| Audio | | | ✓ | ✓ | Stable |
| Battle Manager | | | ✓ | ✓ | Stable |
| AI System | | ✓ | ✓ | ✓ | Stable |
| Campaign | | | ✓ | ✓ | Stable |
| UI | | | ✓ | ✓ | Stable |
| Save/Load | | | ✓ | ✓ | Stable |

### Features

| Feature | v0.1 | v0.5 | v0.9 | v1.0 | Status |
|---------|------|------|------|------|--------|
| Turn-based Combat | | | ✓ | ✓ | Stable |
| Squad Customization | | | ✓ | ✓ | Stable |
| Unit Abilities | | | ✓ | ✓ | Stable |
| Equipment System | | | ✓ | ✓ | Stable |
| Story Campaign | | | ✓ | ✓ | Stable |
| Adaptive AI | | | ✓ | ✓ | Stable |
| Difficulty Scaling | | | | ✓ | Stable |
| Multiplayer | | | | | Planned |
| Leaderboards | | | | | Planned |
| Modding Support | | | | | Planned |

---

## Breaking Changes

### v1.0.0
No breaking changes - first stable release.

### Future Versions
Breaking changes will be documented clearly before release in pre-release notes.

---

## How to Report Issues

Found a bug or have a suggestion? Please:

1. **Check existing issues** first at https://github.com/jurgen-paul/tactical-legends/issues
2. **Create a new issue** with:
   - Clear title and description
   - Steps to reproduce (for bugs)
   - Expected vs actual behavior
   - System info (OS, version, hardware)
   - Screenshots/logs if applicable

3. **Security issues**: Report privately to project maintainers, do not create public issues

---

## How to Contribute

See [CONTRIBUTING.md](../CONTRIBUTING.md) for guidelines on:
- Fork and branch strategy
- Commit message conventions
- Pull request process
- Code review guidelines
- Testing requirements

---

## Version Maintenance

### Support Timeline

| Version | Released | Support Until | Status |
|---------|----------|---------------|--------|
| 1.0.x | Sept 2024 | Sept 2025 | **Active** |
| 0.9.x | Aug 2024 | Sept 2024 | Maintenance |
| 0.5.x | July 2024 | Aug 2024 | End of Life |
| 0.1.x | June 2024 | July 2024 | End of Life |

### Upgrade Paths

- **0.5.x → 0.9.x**: Automatic, no data migration needed
- **0.9.x → 1.0.0**: Save files are compatible
- **1.0.x → 1.1.x**: Full backward compatibility planned

---

## Licensing

All changes are licensed under **Apache License 2.0**.
See [LICENSE](../LICENSE) for full text.

---

## Contributors

### v1.0.0 Contributors

- **Joachim Paul Westerveld** (@jurgen-paul) - Project Lead, Core Development
- Community reviewers and testers

### Acknowledgments

- SDL2 team for excellent cross-platform graphics library
- Open source community for tools and libraries
- Beta testers for valuable feedback

---

## Links

- **GitHub Repository**: https://github.com/jurgen-paul/tactical-legends
- **Issues & Bugs**: https://github.com/jurgen-paul/tactical-legends/issues
- **Discussions**: https://github.com/jurgen-paul/tactical-legends/discussions
- **Project Website**: https://jurgen-paul.github.io/tactical-legends/
- **Documentation**: https://github.com/jurgen-paul/tactical-legends/tree/main/docs

---

**Last Updated**: September 7, 2024
**Current Version**: 1.0.0 (Stable)
**Next Release**: 1.1.0 (Estimated Q4 2024)

[Unreleased]: https://github.com/jurgen-paul/tactical-legends/compare/v1.0.0...develop
[1.0.0]: https://github.com/jurgen-paul/tactical-legends/releases/tag/v1.0.0
[0.9.0]: https://github.com/jurgen-paul/tactical-legends/releases/tag/v0.9.0
[0.5.0]: https://github.com/jurgen-paul/tactical-legends/releases/tag/v0.5.0
[0.1.0]: https://github.com/jurgen-paul/tactical-legends/releases/tag/v0.1.0
