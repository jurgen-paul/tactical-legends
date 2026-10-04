/**
 * Tactical Legends - Tactical Character Pack Module
 */

export enum CharacterRarity {
  SILVER = "Silver",
  PLATINUM = "Platinum"
}

export enum Specialization {
  SNIPER = "Sniper",
  ASSAULT = "Assault",
  MEDIC = "Medic",
  ENGINEER = "Engineer",
  RECON = "Reconnaissance"
}

export interface TacticalCharacter {
  name: string;
  codename: string;
  specialization: Specialization;
  rarity: CharacterRarity;
  stats: {
    hp: number;
    attack: number;
    defense: number;
    accuracy: number;
  };
}

export const TACTICAL_CHARACTERS: TacticalCharacter[] = [
  {
    name: "David Goldstein",
    codename: "Phantom",
    specialization: Specialization.SNIPER,
    rarity: CharacterRarity.PLATINUM,
    stats: { hp: 95, attack: 45, defense: 14, accuracy: 96 }
  },
  {
    name: "Eli Cohen",
    codename: "Breaker",
    specialization: Specialization.ENGINEER,
    rarity: CharacterRarity.SILVER,
    stats: { hp: 130, attack: 28, defense: 26, accuracy: 82 }
  }
];

export function getCharacterByCodename(codename: string): TacticalCharacter | undefined {
  return TACTICAL_CHARACTERS.find(c => c.codename.toLowerCase() === codename.toLowerCase());
}
