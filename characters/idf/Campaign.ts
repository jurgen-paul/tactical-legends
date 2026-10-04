/**
 * Tactical Legends - Campaign Module
 * Defines campaign missions, triggers, environmental hazards, and enemies.
 */

export interface MissionObjective {
  id: string;
  description: string;
  completed: boolean;
  required: boolean;
}

export interface CampaignMission {
  id: string;
  title: string;
  environment: string;
  enemies: string[];
  objectives: MissionObjective[];
  triggers?: Record<string, string>;
}

export const CAMPAIGN_MISSIONS: CampaignMission[] = [
  {
    id: "m-01",
    title: "Sandstorm Infiltration // Sector CH-03",
    environment: "Desert Ruins / Atmospheric Interference",
    enemies: ["Dominion Enforcer", "Holo Hunter", "Mecha Sentry"],
    objectives: [
      { id: "obj-1", description: "Infiltrate Vault of Eden perimeter", completed: false, required: true },
      { id: "obj-2", description: "Retrieve Echo Core Relic", completed: false, required: true },
      { id: "obj-3", description: "Extract entire fireteam without casualties", completed: false, required: false }
    ],
    triggers: {
      "perimeter_breached": "Spawn 2x Holo Hunters",
      "core_accessed": "Activate Vault Defense Protocol"
    }
  },
  {
    id: "m-02",
    title: "Orbital Dawn Echo",
    environment: "Crashed Orbital Carrier / Low Gravity",
    enemies: ["Cybernetic Vanguard", "Dominion Elite"],
    objectives: [
      { id: "obj-4", description: "Siphon data logs from primary bridge", completed: false, required: true },
      { id: "obj-5", description: "Destroy reactor containment before overload", completed: false, required: true }
    ]
  }
];

export function getCampaignMission(id: string): CampaignMission | undefined {
  return CAMPAIGN_MISSIONS.find(m => m.id === id);
}

export function getAllMissions(): CampaignMission[] {
  return CAMPAIGN_MISSIONS;
}
