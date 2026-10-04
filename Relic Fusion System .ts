/**
 * Tactical Legends - Relic Fusion System Engine
 */

export interface RelicComponent {
  id: string;
  name: string;
  category: "core" | "alloy" | "catalyst";
  resonanceTier: number;
}

export interface FusionRecipe {
  id: string;
  ingredients: string[];
  resultName: string;
  successRate: number;
  unlockedAbility: string;
}

export const FUSION_RECIPES: FusionRecipe[] = [
  {
    id: "recipe_surge_beacon",
    ingredients: ["EchoCore", "EdenAlloy"],
    resultName: "Surge Beacon",
    successRate: 0.95,
    unlockedAbility: "Overclock Frequency"
  },
  {
    id: "recipe_harmonic_aegis",
    ingredients: ["MercyShard", "QuantumCore"],
    resultName: "Harmonic Aegis",
    successRate: 0.88,
    unlockedAbility: "Resonance Shielding"
  }
];

export function fuseRelics(itemA: string, itemB: string): { success: boolean; result?: string; ability?: string } {
  const recipe = FUSION_RECIPES.find(r => 
    (r.ingredients[0] === itemA && r.ingredients[1] === itemB) ||
    (r.ingredients[0] === itemB && r.ingredients[1] === itemA)
  );

  if (!recipe) {
    return { success: false };
  }

  return {
    success: true,
    result: recipe.resultName,
    ability: recipe.unlockedAbility
  };
}
