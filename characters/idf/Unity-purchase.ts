/**
 * Tactical Legends - In-App Store & Purchase Module
 */

export interface StoreItem {
  id: string;
  name: string;
  priceUSD: number;
  tokens: number;
  itemType: "cosmetic" | "operative" | "relic";
}

export const STORE_ITEMS: StoreItem[] = [
  {
    id: "bundle_starter",
    name: "Oistarian Recruit Bundle",
    priceUSD: 4.99,
    tokens: 500,
    itemType: "operative"
  },
  {
    id: "bundle_veteran",
    name: "IDF Tactical Vanguard Pack",
    priceUSD: 14.99,
    tokens: 1800,
    itemType: "operative"
  }
];

export function purchaseItem(itemId: string): { success: boolean; message: string } {
  const item = STORE_ITEMS.find(i => i.id === itemId);
  if (!item) {
    return { success: false, message: "Item not found" };
  }
  return { success: true, message: `Purchased ${item.name} successfully!` };
}
