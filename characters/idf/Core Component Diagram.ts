// PlantUML Architecture Diagram
export const DIAGRAM_NAME = 'Core Component Diagram.ts';
export const PLANTUML_SOURCE = 'PlanTulm\n@startuml\ntitle Tactical Legend: Core Component Diagram\n\ncomponent "Fusion Engine" as Fusion\ncomponent "Synergy Calculator" as Synergy\ncomponent "Mutation Selector" as Mutation\ncomponent "Glyph Generator" as Glyphs\ncomponent "Achievement Tracker" as Achievements\ncomponent "Crafting Tree Manager" as Crafting\n\nFusion --> Synergy : calculateSynergy()\nFusion --> Mutation : selectMutationPath()\nFusion --> Glyphs : generateGlyph()\nFusion --> Achievements : checkAchievements()\nFusion --> Crafting : fetchRelicMetadata()\n\n@enduml\n\n';
export default PLANTUML_SOURCE;
