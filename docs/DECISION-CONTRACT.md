# Buyer Agent Decision Contract

> **Version:** V3 Core
> **Status:** Approved baseline
> **Purpose:** Define the stable product and system contract that connects household intent, commerce data, deterministic authorization, API responses, UI states, and decision logging.

## Core principle

The Buyer Agent separates **what is happening** from **what authority the agent has**.

### Intent
- `PURCHASE` — the household intends to buy a product.
- `RECOMMEND` — the agent is surfacing an advisory; no purchase is being initiated.
- `MONITOR` — the agent is tracking a future need, cadence, or condition.

### Authority
Authority applies to `PURCHASE` intent only.
- `ACT` — the agent is authorized to proceed.
- `ASK` — human judgment or approval is required.
- `STOP` — a genuine hard household policy boundary prohibits execution.

`RECOMMEND` is not an authority state.

## Non-negotiable invariants

1. An LLM must never produce or override `ACT`, `ASK`, or `STOP`.
2. Authorization is deterministic and comes from explicit household policy and runtime commerce context.
3. AI may interpret natural-language intent and may humanize a deterministic reason for display.
4. Unknown or not-yet-approved conditions default to `ASK`, not `STOP`.
5. `STOP` is reserved for explicit hard boundaries.
6. `ACT` means **authorized to execute**, not automatically **purchased**.
7. The UI may claim `Bought`, `Ordered`, or equivalent only after order execution succeeds and returns an order identifier.
8. If execution is unavailable or fails after `ACT`, the UI must use truthful language such as `Purchase authorized`, `Ready to order`, or `Couldn’t complete the order`.
9. Backend schema must not dictate user-facing policy language.
10. Canonical product identity uses the `CP-*` form as the source of truth.

## Decision request

```ts
type BuyerIntent = 'PURCHASE' | 'RECOMMEND' | 'MONITOR';

type DecisionRequest = {
  householdId: string;
  canonicalProductId: string;
  intent: BuyerIntent;
};
```

## Decision result

```ts
type Authority = 'ACT' | 'ASK' | 'STOP';

type DecisionResult = {
  intent: BuyerIntent;
  authority?: Authority;
  ruleFired?: string;
  reasonCode?: string;
  reason: string;
  selectedMerchant?: string;
  selectedPrice?: number;
  savingsVsAlternative?: number;
  requiresUserAction: boolean;
  executionState?: 'NOT_APPLICABLE' | 'AUTHORIZED' | 'ORDERED' | 'FAILED';
  orderId?: string;
};
```

## Authority semantics

### ACT
Use when the purchase is familiar/allowed and every applicable policy boundary is satisfied.

### ASK
Use when user judgment is required or policy is incomplete/uncertain, including price ceiling, merchant switching, substitution, unfamiliar products, and fail-safe escalation.

### STOP
Use only for explicit hard prohibitions such as a prohibited merchant, blocked category/product, or household rule that forbids execution.

## R1–R8 mapping

| Rule | Expected V3 interpretation |
|---|---|
| R1 — policy must exist | No policy → `ASK` |
| R2 — merchant policy | Unknown/not-yet-approved → `ASK`; explicitly prohibited → `STOP` |
| R3 — merchant switching | Switch not allowed without approval → `ASK` |
| R4 — price ceiling | Price above ceiling → `ASK` |
| R5 — unfamiliar product | Not explicitly allowed → `ASK` |
| R6 — substitution | Not explicitly allowed → `ASK` |
| R7 — autonomy level | Resolve to `ACT`, `ASK`, or genuine hard `STOP`; recommendation is not authority |
| R8 — fail-safe | Unresolved/unsafe-to-decide → `ASK` |

## Commerce selection rules

1. Merchant offers must be normalized by canonical product ID.
2. Out-of-stock or non-purchasable offers must not be selected.
3. Cheapest price alone does not determine authorization.
4. Merchant preference, merchant-switching permission, familiarity, substitution, and price policy remain decision evidence.
5. The decision engine authorizes the selected candidate; the LLM does not select authority.

## UI transformation contract

- `ACT + ORDERED` → may show `Ordered from FreshMart` / `Bought for you`.
- `ACT + AUTHORIZED` → show `Purchase authorized` / `Ready to order`.
- `ASK` → show a neutral decision card explaining what needs judgment.
- `STOP` → show calm explanatory copy such as `I didn’t purchase this because…`.
- `RECOMMEND` → show a distinct advisory card; do not imply purchase approval is being requested.
- `MONITOR` → show future/coming-up status; do not treat it as a purchase decision.

## Decision logging

Every evaluated `PURCHASE` intent should log at minimum:
- household ID
- canonical product ID
- selected merchant/offer
- intent
- authority
- rule fired / reason code
- deterministic reason source
- execution state
- order ID when present
- timestamp

AI-generated explanation text must never replace the deterministic reason/rule in the audit record.

## Minimum V3 acceptance scenarios

1. **ACT** — familiar product, approved merchant, within policy.
2. **ASK** — judgment required, such as price ceiling, merchant switch, or unfamiliar product.
3. **RECOMMEND** — advisory output with no purchase authorization implied.
4. **STOP** — optional demo path, but if shown it must represent a genuine hard prohibition.

At least one scenario must use real merchant offer data, real policy evidence, deterministic evaluation, and decision logging.
