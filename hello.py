//pip install pygame

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
// Tactical Legends Character Management System

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
 * @param character - The character to greet
 * @returns Formatted greeting message
 */
function greet(character: Character): string {
  const rankTitle = character.rank? `${character.rank} ` : '';
  return `╔════════════════════════════════════════════════╗
║  TACTICAL LEGENDS - MISSION BRIEFING          ║
╚════════════════════════════════════════════════╝

Hello, ${rankTitle}${character.codename}!
Ready for your mission as a ${character.specialization}?

Status: OPERATIONAL
Clearance: GRANTED.
}

/**
 * Display the operative's equipment loadout
 * @param character - The character whose gear to display
 */
function showGear(character: Character): void {
  console.log(`\n╔════════════════════════════════════════════════╗`);
  console.log(`║  EQUIPMENT LOADOUT: ${character.codename.padEnd(24)} ║`);
  console.log(`╚════════════════════════════════════════════════╝\n`);
  
  character.gear.forEach((item, index) => {
    console.log(`  [${index + 1}] ${item}`);
  });
  
  console.log(`\n  Total Items: ${character.gear.length}`);
}

/**
 * Display character statistics
 * @param character - The character whose stats to display
 */
function showStats(character: Character): void {
  if (!character.stats) {
    console.log("\n[!] No stats available for this operative.");
    return;
  }

  console.log(`\n╔════════════════════════════════════════════════╗`);
  console.log(`║  OPERATIVE STATISTICS                          ║`);
  console.log(`╚════════════════════════════════════════════════╝\n`);
  
  const { health, armor, speed, stealth, combatRating } = character.stats;
  
  console.log(`  Health:        ${health} HP       ${'█'.repeat(Math.floor(health / 10))}`);
  console.log(`  Armor:         ${armor}%         ${'█'.repeat(Math.floor(armor / 10))}`);
  console.log(`  Speed:         ${speed} m/s      ${'█'.repeat(speed)}`);
  console.log(`  Stealth:       ${stealth}%        ${'█'.repeat(Math.floor(stealth / 10))}`);
  console.log(`  Combat Rating: ${combatRating}%        ${'█'.repeat(Math.floor(combatRating / 10))}`);
}

/**
 * Generate complete mission briefing
 * @param character - The character for the briefing
 * @returns Mission briefing object
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
 * @param character - The character to equip
 * @param item - The equipment item to add
 */
function addGear(character: Character, item: string): void {
  character.gear.push(item);
  console.log(`\n[+] Added "${item}" to ${character.codename}'s loadout.`);
}

/**
 * Display complete character profile
 * @param character - The character to display
 */
function displayProfile(character: Character): void {
  console.log(`\n╔════════════════════════════════════════════════╗`);
  console.log(`║  OPERATIVE DOSSIER                             ║`);
  console.log(`╚════════════════════════════════════════════════╝\n`);
  console.log(`  Codename:       ${character.codename}`);
  console.log(`  Specialization: ${character.specialization}`);
  if (character.faction) console.log(`  Faction:        ${character.faction}`);
  if (character.rank) console.log(`  Rank:           ${character.rank}`);
  console.log(`  Equipment:      ${character.gear.length} items`);
}

// ═══════════════════════════════════════════════════════
//  DEMO EXECUTION
// ═══════════════════════════════════════════════════════

console.log("\n" + "=".repeat(50));
console.log("  TACTICAL LEGENDS - CHARACTER SYSTEM v1.0");
console.log("=".repeat(50) + "\n");

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
console.log(`\n╔════════════════════════════════════════════════╗`);
console.log(`║  MISSION STATUS: ${briefing.status.padEnd(32)} ║`);
console.log(`║  Timestamp: ${briefing.timestamp.padEnd(35)} ║`);
console.log(`╚════════════════════════════════════════════════╝\n`);

console.log("\n[✓] All systems operational. Ready for deployment.\n");
// transmission-log.ts
// Tactical-Legend: The Rise of the Oistarian
// Run: npm install chalk

import chalk from "chalk";

// Transmission data (simplified from your JSON)
const transmission = {
  transmissionID: "TL-RISE-HELLO-0001",
  origin: "Vault Beacon Node 7",
  timestamp: "2525-08-25T16:44:00Z",
  sender: {
    callSign: "Echo-27",
    faction: "Oistarian Vanguard",
    rank: "Field Commander."
  },
  message: {
    content: "Hello world! Tactical-Legend awakens. The Rise of the Oistarian begins.",
    status: "TRANSMITTED",
    priority: "HIGH."
  },
  routing: {
    targetSector: "Eden-Prime",
    relayNodes: ["Grid-Alpha", "Vault-Spire", "IDF Command"]
  }
};

// Utility: draw section headers
function sectionHeader(title: string): void {
  console.log(chalk.bgBlue.white.bold(`\n╔════════════════════════════════════════════════╗`));
  console.log(chalk.bgBlue.white.bold(`║  ${title.padEnd(44)} ║`));
  console.log(chalk.bgBlue.white.bold(`╚════════════════════════════════════════════════╝\n`));
}

// Styled console output
console.clear();
console.log(chalk.greenBright("=".repeat(60)));
console.log(chalk.greenBright.bold("   TACTICAL-LEGEND: THE RISE OF THE OISTARIAN"));
console.log(chalk.greenBright("=".repeat(60)));

// Transmission ID
sectionHeader("TRANSMISSION HEADER");
console.log(`  ID: ${chalk.yellow(transmission.transmissionID)}`);
console.log(`  Origin: ${chalk.cyan(transmission.origin)}`);
console.log(`  Timestamp: ${chalk.magenta(transmission.timestamp)}`);

// Sender
sectionHeader("SENDER PROFILE");
console.log(`  CallSign: ${chalk.yellow(transmission.sender.callSign)}`);
console.log(`  Faction:  ${chalk.green(transmission.sender.faction)}`);
console.log(`  Rank:     ${chalk.blueBright(transmission.sender.rank)}`);

// Message
sectionHeader("MESSAGE PAYLOAD");
console.log(chalk.whiteBright(`  Content: ${chalk.bold(transmission.message.content)}`));
console.log(`  Status:  ${chalk.greenBright(transmission.message.status)}`);
console.log(`  Priority:${chalk.redBright(transmission.message.priority)}`);

// Routing
sectionHeader("ROUTING DATA");
console.log(`  Target Sector: ${chalk.cyanBright(transmission.routing.targetSector)}`);
console.log(`  Relay Nodes:`);
transmission.routing.relayNodes.forEach((node, i) => {
  console.log(`    [${i + 1}] ${chalk.magenta(node)}`);
});

// Footer
console.log(chalk.greenBright("\n[✓] Transmission complete. All systems operational.\n"));
