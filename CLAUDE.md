# Buyer Agent — Claude Code Instructions

## Mission

Build V3 of the Buyer Agent as a working, portfolio-quality mobile prototype with calibrated autonomy for household grocery shopping.

V3 is **not a redesign of V2**. Preserve the V2 user-facing experience and visual identity unless a change is required for semantic correctness, real system behavior, accessibility, or a clearly documented V3 requirement.

The primary V3 change is that the prototype must behave like the Buyer Agent it already visually represents: real merchant comparison, real household policy evidence, deterministic authorization, grounded explanations, decision logging, and truthful execution state.

## Source-of-truth hierarchy

Before implementing V3, read these sources in order:

1. `docs/contracts/DECISION-CONTRACT.md` — canonical runtime semantics for V3.
2. `docs/audits/V2-TO-V3-AUDIT.md` — approved V2 assessment, V3 Core scope, and implementation sequence.
3. `DESIGN.md` — product experience and design intent.
4. `docs/adr/` — architectural decisions.
5. `docs/tradeoffs/TRADEOFFS.md` — documented tradeoffs and rationale.
6. Existing V2 application code — implementation baseline to preserve and upgrade.
7. Existing Python Commerce Adapter / decision engine and product catalog — behavioral and commerce references.

If implementation code conflicts with the Decision Contract, do not silently preserve the conflict. Surface it, explain it, and implement the approved V3 semantics.

## Product model

The Buyer Agent separates **intent** from **authority**.

Intent:
- `PURCHASE`
- `RECOMMEND`
- `MONITOR`

Purchase authority:
- `ACT`
- `ASK`
- `STOP`

`RECOMMEND` is not an authorization state.

An LLM must never grant, deny, or override purchase authority. `ACT`, `ASK`, and `STOP` come only from deterministic policy evaluation.

Unknown/not-yet-approved conditions should normally produce `ASK`. `STOP` is reserved for explicit hard household boundaries.

## V3 prototype requirement

V3 must remain recognizably the V2 product while replacing seeded/simulated core behavior with an integrated pipeline.

Preserve unless correctness requires change:
- navigation and tab structure
- Today screen hierarchy
- Shopping interactions
- Agent and Profile structure
- decision-card interaction patterns
- View Why / progressive disclosure
- strongest V2 visual identity and copy tone

Do not redesign screens merely because a new component library or backend is being introduced.

## V3 Core behavior

Build toward this pipeline:

```text
Household need / user intent
        ↓
Canonical product identity (CP-*)
        ↓
FreshMart + ValueGrocer offers via Commerce Adapter
        ↓
Normalize price / availability / merchant evidence
        ↓
Household policy + relevant preference/history evidence
        ↓
Deterministic authorization engine
        ↓
PURCHASE → ACT | ASK | STOP
RECOMMEND → advisory path
MONITOR → future/condition path
        ↓
Decision log
        ↓
Truthful mobile UI
        ↓
Controlled order execution for ACT where implemented
```

## Required V3 scenarios

V3 Core is not complete until the prototype demonstrates at least:

1. `PURCHASE + ACT` — familiar/allowed product within policy.
2. `PURCHASE + ASK` — user judgment required.
3. `RECOMMEND` — advisory suggestion that does not imply purchase authority.

A STOP scenario is useful but should only represent a genuine hard prohibition.

At least one scenario must be grounded end-to-end in real merchant data, policy evidence, deterministic evaluation, and decision logging.

## ACT and order truthfulness

Never equate authorization with successful purchase.

Valid progression:

```text
ACT
→ AUTHORIZED
→ attempt controlled WooCommerce order
→ ORDERED + orderId
```

Only `ORDERED` may drive UI claims such as `Bought for you` or `Ordered from FreshMart`.

If order execution is not implemented, use `Purchase authorized` or `Ready to order`.

If execution fails, show a truthful failure state without changing the original deterministic authorization decision.

Real payment is not required for V3 Core.

## Commerce and catalog

- Preserve the Commerce Adapter abstraction.
- Do not hardcode the architecture to FreshMart and ValueGrocer even though they are the controlled V3 merchants.
- Use canonical `CP-*` product identity for cross-merchant matching.
- Never select out-of-stock or non-purchasable offers.
- Cheapest offer alone does not determine authorization.
- Keep merchant preference, switching permission, price ceiling, familiarity, and substitution evidence available to the decision engine.

Do not build a large catalog platform or full equivalence engine for V3 Core unless required to make the approved scenarios work.

## Python vs TypeScript

Do not assume the existing Python Commerce Adapter and decision engine must be ported to TypeScript.

Before implementation, evaluate:

- keep Python behind a small service boundary, or
- port behavior into the existing Express/TypeScript server.

Choose based on deployment simplicity, testability, integration cost, and fidelity to existing R1–R8 behavior.

The Decision Contract is the architectural boundary. The language is an implementation choice.

Document the choice and rationale before making a large port.

## R1–R8 verification

Before relying on the engine in the V3 UI, verify the existing rules against `docs/contracts/DECISION-CONTRACT.md`.

Important semantics:
- no policy → ASK
- unknown/not-yet-approved merchant → ASK
- explicitly prohibited merchant → STOP
- price ceiling violation → ASK
- unfamiliar product without allowance → ASK
- substitution without allowance → ASK
- merchant switch requiring approval → ASK
- unresolved fail-safe condition → ASK

Do not preserve old `BLOCK`, `ESCALATE`, or `RECOMMEND` mappings if they conflict with the V3 contract. Adapt them explicitly and test the mapping.

## Supabase scope

Use Supabase only where necessary for V3 Core decision behavior:

- household bootstrap
- authorization policies
- relevant preferences
- purchase history only where needed for familiarity
- decision log

Do not spend V3 Core effort wiring profile decoration, dashboard metrics, forecasting charts, or unrelated prototype data unless needed by an approved scenario.

The database schema is not the UX.

Translate policy fields into household language. Example:

- `merchant_switching_allowed` → `You may switch stores when it saves money.`
- `max_item_price` → `Buy automatically up to $X.`
- `substitutions_allowed = false` → `Ask before substituting.`

## AI role

AI may:
- interpret natural-language shopping input
- normalize/understand user intent where appropriate
- humanize deterministic reason text
- support explanations and recommendations

AI may not:
- produce ACT/ASK/STOP
- override household authorization policy
- claim a purchase occurred
- invent merchant price, availability, policy evidence, savings, or order status

Ground View Why explanations in actual rule, policy, merchant, and offer evidence.

## Design-system work in V3

V3 should establish design-system foundations without turning the project into a redesign or migration exercise.

Include where useful:
- React Native Paper for appropriate reusable primitives
- Material 3 theme/token foundations
- Storybook coverage for core reusable Buyer Agent components

Prioritize components such as:
- DecisionCard
- StatusChip
- TrustStrip
- ReasoningChain / View Why elements
- other genuinely reused decision-system components

Do **not** perform a full-screen Material 3 redesign merely to use Paper.

Full component migration, exhaustive Storybook coverage, deep design-system polish, and broad M3 cleanup remain V3.1 work.

## Explicitly deferred from V3 Core

Unless required to make an approved V3 scenario function, defer:

- full Material 3 migration
- exhaustive Storybook rollout
- authentication
- provider migration solely to change LLM vendors
- voice-provider migration
- full replenishment forecasting
- full substitution/equivalence engine
- real payment
- production checkout
- broad legacy/experimental API documentation
- speculative infrastructure refactors

## API scope

Document the V3 Core decision and order-execution contracts.

Do not pause V3 Core to document every legacy or experimental route. Full API coverage is V3.1.

## Working method

For each meaningful implementation step:

1. Read the relevant source-of-truth files first.
2. State what is being changed and why.
3. Preserve V2 UX unless the contract requires a visible correction.
4. Prefer the smallest vertical slice that proves real behavior.
5. Test deterministic rules independently of AI.
6. Validate UI claims against actual backend/execution state.
7. Do not silently broaden scope.
8. Do not rewrite unrelated files.
9. Show changed files and test results before committing.
10. Never push or merge unless explicitly instructed.

## Recommended implementation order

1. Validate/finalize typed implementation of the Decision Contract.
2. Verify R1–R8 against it.
3. Resolve canonical `CP-*` identity through the commerce path.
4. Decide Python-service vs TypeScript-port architecture and document rationale.
5. Build minimal server-side decision pipeline.
6. Connect one real product scenario to the existing V2 UI.
7. Add ACT, ASK, and RECOMMEND demo paths.
8. Attempt controlled WooCommerce test-order execution for ACT.
9. Correct semantic UI language and household-policy UX where necessary.
10. Add/strengthen Paper/M3 foundations and Storybook for core reusable components without redesigning V2.

## Definition of done for V3 Core

V3 Core is done when a reviewer can use the recognizable Buyer Agent prototype and see that the key decisions are backed by real system behavior rather than seeded storytelling.

The prototype should be able to demonstrate:

- real merchant comparison
- canonical product matching
- real household policy evidence
- deterministic purchase authority
- distinct ACT / ASK / RECOMMEND behavior
- truthful STOP behavior where applicable
- grounded View Why explanation
- decision logging
- truthful ACT/order state
- preserved V2 product experience
- initial reusable design-system foundations for the decision experience

The goal is not maximum infrastructure or maximum component coverage. The goal is a coherent, defensible, working Buyer Agent prototype whose UI, policy model, commerce evidence, authorization behavior, and execution claims agree with each other.
