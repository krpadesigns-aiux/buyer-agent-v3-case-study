// Decision Contract — TypeScript types

export type BuyerIntent = 'PURCHASE' | 'RECOMMEND' | 'MONITOR';
export type Authority = 'ACT' | 'ASK' | 'STOP';
export type ExecutionState = 'NOT_APPLICABLE' | 'AUTHORIZED' | 'ORDERED' | 'FAILED';

export interface MerchantOffer {
  merchantId: string;
  merchantName: string;
  canonicalProductId: string;
  merchantSku: string;
  name: string;
  price: number;
  currency: string;
  inStock: boolean;
  purchasable: boolean;
}

export interface AuthorizationPolicy {
  category: string;
  autonomyLevel: string;
  maxItemPrice?: number;
  substitutionsAllowed: boolean;
  unfamiliarProductsAllowed: boolean;
  merchantSwitchingAllowed: boolean;
  approvedMerchants: string[];
  prohibitedMerchants?: string[];
}

export interface DecisionCandidate {
  merchant: string;
  price: number;
}

export interface EngineResult {
  decision: Authority;
  rule: string;
  reason: string;
}

export interface DecisionRequest {
  householdId: string;
  canonicalProductId: string;
  intent: BuyerIntent;
}

export interface DecisionResult {
  intent: BuyerIntent;
  authority?: Authority;
  ruleFired?: string;
  reason: string;
  selectedMerchant?: string;
  selectedPrice?: number;
  savingsVsAlternative?: number;
  requiresUserAction: boolean;
  executionState?: ExecutionState;
  orderId?: string;
}
