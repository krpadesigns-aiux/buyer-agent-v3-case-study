// Decision Engine — TypeScript port of decision_engine.py
// V3 fixes applied per the Decision Contract verification:
// R1: ESCALATE → ASK
// R2: prohibited merchant check added when explicit policy exists
// R7: advisory-only autonomy → ASK
// R8: ESCALATE → ASK

import type { AuthorizationPolicy, DecisionCandidate, EngineResult } from './types';

export function decide(
  candidate: DecisionCandidate,
  policy: AuthorizationPolicy | null,
  familiar: boolean = true,
  isSubstitution: boolean = false,
  preferredMerchant: string | null = null,
): EngineResult {
  const reasons: string[] = [];

  if (!policy) {
    return { decision: 'ASK', rule: 'R1', reason: 'No authorization policy exists for this category.' };
  }

  const prohibitedMerchants = policy.prohibitedMerchants ?? [];
  if (prohibitedMerchants.length > 0 && prohibitedMerchants.includes(candidate.merchant)) {
    return { decision: 'STOP', rule: 'R2', reason: `${candidate.merchant} is explicitly prohibited by household policy.` };
  }

  const approvedMerchants = policy.approvedMerchants ?? [];
  if (!approvedMerchants.includes(candidate.merchant)) {
    return { decision: 'ASK', rule: 'R2', reason: `${candidate.merchant} is not an approved merchant.` };
  }
  reasons.push('Merchant is approved');

  if (preferredMerchant && candidate.merchant !== preferredMerchant) {
    if (!policy.merchantSwitchingAllowed) {
      return { decision: 'ASK', rule: 'R3', reason: `Switching from ${preferredMerchant} to ${candidate.merchant} is not authorized.` };
    }
    reasons.push(`Merchant switch from ${preferredMerchant} to ${candidate.merchant} is authorized`);
  }

  if (policy.maxItemPrice !== undefined && candidate.price > policy.maxItemPrice) {
    return { decision: 'ASK', rule: 'R4', reason: `$${candidate.price.toFixed(2)} exceeds $${policy.maxItemPrice.toFixed(2)} authorization ceiling.` };
  }
  reasons.push('Price is within authorization ceiling');

  if (!familiar && !policy.unfamiliarProductsAllowed) {
    return { decision: 'ASK', rule: 'R5', reason: 'Product is unfamiliar and unfamiliar products are not authorized.' };
  }
  if (familiar) reasons.push('Product is familiar');

  if (isSubstitution && !policy.substitutionsAllowed) {
    return { decision: 'ASK', rule: 'R6', reason: 'Substitution is not authorized.' };
  }
  if (!isSubstitution) reasons.push('No substitution required');

  const autonomy = policy.autonomyLevel;
  if (autonomy === 'recommend') {
    return { decision: 'ASK', rule: 'R7', reason: 'This category is configured for advisory only. Your approval is required.' };
  }
  if (autonomy === 'prepare') {
    return { decision: 'ASK', rule: 'R7', reason: 'Agent may prepare the purchase but cannot execute it.' };
  }
  if (autonomy === 'ask') {
    return { decision: 'ASK', rule: 'R7', reason: 'User approval is required before purchase.' };
  }
  if (autonomy === 'act') {
    reasons.push('Category has ACT authority');
    return { decision: 'ACT', rule: 'R7', reason: reasons.join('; ') };
  }

  return { decision: 'ASK', rule: 'R8', reason: 'Authorization state could not be resolved safely.' };
}
