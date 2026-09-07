pip install pygame

cd tactical-legends
python tactical_legends_video_presentation.py

================================================================================
TACTICAL LEGENDS - RISE OF OISTARIAN
Video Presentation Generator
================================================================================
Hello World! Starting presentation...
================================================================================

  ████████╗ █████╗  ██████╗████████╗██╗ ██████╗ █████╗ ██╗     
  ╚══██╔══╝██╔══██╗██╔════╝╚══██╔══╝██║██╔════╝██╔══██╗██║     
     ██║   ███████║██║        ██║   ██║██║     ███████║██║     
     ██║   ██╔══██║██║        ██║   ██║██║     ██╔══██║██║     
     ██║   ██║  ██║╚██████╗   ██║   ██║╚██████╗██║  ██║███████╗
     ╚═╝   ╚═╝  ╚═╝ ╚═════╝   ╚═╝   ╚═╝ ╚═════╝╚═╝  ╚═╝╚══════╝
           LEGENDS - RISE OF OISTARIAN

Presentation Starting...
Press SPACE to skip scenes, ESC to exit
--------------------------------------------------------------------------------
Scene Changed: Opening - Black Screen
Scene Changed: Flash Cuts
Scene Changed: Combat Sequence
Scene Changed: Fast Montage
Scene Changed: Final Reveal
Scene Changed: Tagline
--------------------------------------------------------------------------------
Presentation Finished!
================================================================================


 Add audio support (background music/narration)?
✅ Create a CI/CD workflow to run this in GitHub Actions?
✅ Export the presentation to a video file (MP4)?
✅ Modify scene timings or effects?



// hello.ts
// Tactical Legends Character Management System v3.0
// Run: npm install chalk

import chalk from "chalk";

/**
 * Represents a Tactical Legends operative with combat specifications
 */
interface Character {
  codename: string;
  specialization: string;
  gear: string[];
  faction?: string;
  rank?: string;
  stats?: CharacterStats;
}

/**
 * Character combat and performance statistics
 */
interface CharacterStats {
  health: number;
  armor: number;
  speed: number;
  stealth: number;
  combatRating: number;
}

/**
 * Mission briefing structure
 */
interface MissionBriefing {
  character: Character;
  greeting: string;
  status: 'READY' | 'STANDBY' | 'DEPLOYED' | 'OFF-DUTY';
  timestamp: string;
}

// Utility: Draw a section header with color
function sectionHeader(title: string): void {
  console.log(chalk.bgBlue.white.bold(`\n╔════════════════════════════════════════════════╗`));
  console.log(chalk.bgBlue.white.bold(`║  ${title.padEnd(44)} ║`));
  console.log(chalk.bgBlue.white.bold(`╚════════════════════════════════════════════════╝\n`));
}

// Create a sample character with a full profile
const oistarian: Character = {
  codename: "OISTARIAN",
  specialization: "Emotional Recon Specialist",
  faction: "Oistarian Vanguard",
  rank: "Field Operative",
  gear: [
    "Whisper & Roar",
    "NeuroPulse Arm Module",
    "Quantum Comms Device",
    "Tactical HUD Visor"
  ],
  stats: {
    health: 150,
    armor: 75,
    speed: 12,
    stealth: 88,
    combatRating: 82
  }
};

/**
 * Generate a personalized greeting for the operative
 */
function greet(character: Character): string {
  const rankTitle = character.rank? `${character.rank} ` : '';
  return chalk. bold.blueBright(
`╔════════════════════════════════════════════════╗
║  TACTICAL LEGENDS - MISSION BRIEFING          ║
╚════════════════════════════════════════════════╝

Hello, ${chalk.yellow(rankTitle + character.codename)}!
Ready for your mission as a ${chalk.green(character.specialization)}?

Status: ${chalk.greenBright("OPERATIONAL")}
Clearance: ${chalk.cyanBright("GRANTED.")}`
  );
}

/**
 * Display the operative's equipment loadout
 */
function showGear(character: Character): void {
  sectionHeader(`EQUIPMENT LOADOUT: ${character.codename}`);
  character.gear.forEach((item, index) => {
    console.log(chalk.white(`  [${index + 1}] ${chalk.magenta(item)}`));
  });
  console.log(chalk.yellow(`\n  Total Items: ${character.gear.length}`));
}

/**
 * Display character statistics
 */
function showStats(character: Character): void {
  if (!character.stats) {
    console.log(chalk.red("\n[!] No stats available for this operative."));
    return;
  }

  sectionHeader("OPERATIVE STATISTICS");

  const { health, armor, speed, stealth, combatRating } = character.stats;

  console.log(`  Health:        ${chalk.green(`${health} HP`)}       ${chalk.green('█'.repeat(Math.floor(health / 10)))}`);
  console.log(`  Armor:         ${chalk.cyan(`${armor}%`)}         ${chalk.cyan('█'.repeat(Math.floor(armor / 10)))}`);
  console.log(`  Speed:         ${chalk.yellow(`${speed} m/s`)}      ${chalk.yellow('█'.repeat(speed))}`);
  console.log(`  Stealth:       ${chalk.magenta(`${stealth}%`)}        ${chalk.magenta('█'.repeat(Math.floor(stealth / 10)))}`);
  console.log(`  Combat Rating: ${chalk.redBright(`${combatRating}%`)}        ${chalk.redBright('█'.repeat(Math.floor(combatRating / 10)))}`);
}

/**
 * Generate complete mission briefing
 */
function generateMissionBriefing(character: Character): MissionBriefing {
  return {
    character,
    greeting: greet(character),
    status: 'READY',
    timestamp: new Date().toISOString()
  };
}

/**
 * Add equipment to character loadout
 */
function addGear(character: Character, item: string): void {
  character.gear.push(item);
  console.log(chalk.greenBright(`\n[+] Added "${item}" to ${character.codename}'s loadout.`));
}

/**
 * Display complete character profile
 */
function displayProfile(character: Character): void {
  sectionHeader("OPERATIVE DOSSIER");
  console.log(`  Codename:       ${chalk.yellow(character.codename)}`);
  console.log(`  Specialization: ${chalk.green(character.specialization)}`);
  if (character.faction) console.log(`  Faction:        ${chalk.cyan(character.faction)}`);
  if (character.rank) console.log(`  Rank:           ${chalk.blueBright(character.rank)}`);
  console.log(`  Equipment:      ${chalk.magenta(`${character.gear.length} items`)}`);
}

// ═══════════════════════════════════════════════════════
//  DEMO EXECUTION
// ═══════════════════════════════════════════════════════

console.log(chalk.bold("\n" + "=".repeat(50)));
console.log(chalk.bold.blueBright("  TACTICAL LEGENDS - CHARACTER SYSTEM v3.0"));
console.log(chalk.bold("=".repeat(50) + "\n"));

// Display greeting
console.log(greet(oistarian));

// Show complete profile
displayProfile(oistarian);

// Show equipment loadout
showGear(oistarian);

// Display stats
showStats(oistarian);

// Demo: Add new gear
addGear(oistarian, "EMP Grenade");

// Generate mission briefing
const briefing = generateMissionBriefing(oistarian);
sectionHeader("MISSION STATUS");
console.log(`  Status:    ${chalk.greenBright(briefing.status)}`);
console.log(`  Timestamp: ${chalk.cyan(briefing.timestamp)}`);

console.log(chalk.greenBright("\n[✓] All systems operational. Ready for deployment.\n"));
