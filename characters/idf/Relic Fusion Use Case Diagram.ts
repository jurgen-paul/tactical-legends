// PlantUML Architecture Diagram
export const DIAGRAM_NAME = 'Relic Fusion Use Case Diagram.ts';
export const PLANTUML_SOURCE = '@startuml\ntitle Tactical Legend: Relic Fusion Use Case Diagram\n\nactor Player\nactor GameEngine\n\nusecase "Initiate Relic Fusion" as UC1\nusecase "Apply Faction Modifier" as UC2\nusecase "Select Mutation Path" as UC3\nusecase "Generate Glyph" as UC4\nusecase "Compose Fusion Lore" as UC5\nusecase "Unlock Achievement" as UC6\nusecase "Update Relic Codex" as UC7\n\nPlayer --> UC1\nUC1 --> UC2\nUC1 --> UC3\nUC1 --> UC4\nUC1 --> UC5\nUC1 --> UC6\nUC1 --> UC7\n\nGameEngine --> UC2\nGameEngine --> UC3\nGameEngine --> UC4\nGameEngine --> UC5\nGameEngine --> UC6\nGameEngine --> UC7\n\n@enduml\n\n';
export default PLANTUML_SOURCE;
