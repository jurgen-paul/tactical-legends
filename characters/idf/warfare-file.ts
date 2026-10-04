/**
 * Tactical Legends - Modern Warfare Engine Module
 * Weapon matrix, tactical ballistics, and combat configuration.
 */

export interface WeaponProfile {
  name: string;
  damage: number;
  fireRate: number;
  range: number;
  recoil: number;
  magSize: number;
}

export const WEAPON_ARSENAL: Record<string, WeaponProfile> = {
  assault_rifle: {
    name: "TAR-21 Pulse Carbine",
    damage: 32,
    fireRate: 650,
    range: 45,
    recoil: 1.8,
    magSize: 30
  },
  sniper_rifle: {
    name: "Barak .338 Overwatch",
    damage: 95,
    fireRate: 45,
    range: 120,
    recoil: 4.2,
    magSize: 10
  },
  smg: {
    name: "Micro Tavor 9mm",
    damage: 22,
    fireRate: 900,
    range: 25,
    recoil: 1.2,
    magSize: 32
  },
  shotgun: {
    name: "Kel-Tec Tactical Breach",
    damage: 80,
    fireRate: 120,
    range: 15,
    recoil: 3.5,
    magSize: 12
  }
};

export function getWeapon(weaponKey: string): WeaponProfile | undefined {
  return WEAPON_ARSENAL[weaponKey];
}
