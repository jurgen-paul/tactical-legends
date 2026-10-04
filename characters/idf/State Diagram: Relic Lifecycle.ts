// PlantUML Architecture Diagram
export const DIAGRAM_NAME = 'State Diagram: Relic Lifecycle.ts';
export const PLANTUML_SOURCE = '@startuml\ntitle Tactical Legend: Relic Lifecycle State Diagram\n\n[*] --> Crafted: via Crafting Tree\nCrafted --> Infused: trait infusion\nInfused --> Factionalized: faction essence applied\nFactionalized --> Fused: combined with another relic\nFused --> Mutated: mutation path selected\nMutated --> Awakened: legendary synergy achieved\nAwakened --> Archived: stored in Relic Codex\nArchived --> [*]\n\n@enduml\n\n\n\n';
export default PLANTUML_SOURCE;
