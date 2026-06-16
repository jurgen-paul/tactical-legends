# Tactical Legends Roadmap

This roadmap outlines planned features, milestones, and priorities for Tactical Legends. Items are prioritized to help contributors focus effort on the highest-impact work.

## Release targets

- v0.5 — Improved tooling & documentation (current focus)
  - Add README gameplay video section and contributor instructions
  - Add ROADMAP and issue templates
  - Basic CI (build & lint)
- v1.0 — Core gameplay
  - Polished single-player campaign
  - Stable AI and core combat systems
  - Usability polish (UI, settings, accessibility)
- v1.1 — Content & polish
  - More maps and units
  - Visual/audio improvements
  - Bugfix and balance pass
- v2.0 — Multiplayer & advanced systems
  - Online multiplayer (lobby, matchmaking, sync)
  - Terrain effects & advanced pathfinding
  - Competitive balancing and leaderboards

## Prioritized work (short-term)

1. Documentation & onboarding (P1)
   - Add gameplay video and screenshots to README
   - CONTRIBUTING.md and contributor guide improvements
   - Add issue templates to standardize reports
2. CI / DX (P1)
   - Add GitHub Actions for build, lint, and tests
3. Core features (P0/P1)
   - Stabilize single-player loop
   - Break out multiplayer and terrain into tracked epics

## Epics and next steps

- Epic: Multiplayer
  - Design network architecture (authoritative server vs P2P)
  - Implement lobby & matchmaking UI
  - Implement state synchronization and rollback/desync detection

- Epic: Terrain & Map Systems
  - Map format and editor support for terrain types (forest, hills, rivers)
  - Pathfinding updates for terrain movement costs
  - Line-of-sight and combat modifiers per terrain

## How to propose changes to the roadmap

- Open an issue using the "Roadmap item" issue template (or label proposals with `roadmap`).
- For major roadmap proposals, add a short design summary, motivation, and suggested milestones.
- Maintainers will review and schedule items into releases.

## Notes

This is a living document — items will be reprioritized as development and community needs evolve.
