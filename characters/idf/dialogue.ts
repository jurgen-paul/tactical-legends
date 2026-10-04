/**
 * Tactical Legends - Dynamic Squad Dialogue Module
 */

import { getMoraleLevel, SquadMemberMorale } from './Morale';

export function getDynamicDialogue(member: SquadMemberMorale): string {
  const moraleLevel = getMoraleLevel(member.morale);
  switch (moraleLevel) {
    case "High":
      return `${member.name}: “We finish this together.”`;
    case "Neutral":
      return `${member.name}: “I’m holding it together. For now.”`;
    case "Low":
      return `${member.name}: “I’m not sure I can keep going.”`;
    case "Broken":
      return `${member.name}: “I’m done. Don’t count on me.”`;
    default:
      return `${member.name}: “Awaiting tactical orders.”`;
  }
}
