# Buyer’s Agent — V3 Spec-Driven Case Study

**Calibrated autonomy for household grocery shopping**

Buyer’s Agent is an agentic-commerce concept that explores how AI can reduce routine household shopping effort without removing user control. The product uses household preferences, purchase history, merchant availability, price limits, substitution rules, and authorization policies to determine when the system may act, when it must ask, and when a hard policy boundary stops execution.

V3 evolves the project from a functional prototype into a **spec-driven, auditable agent system**. It introduces an explicit decision contract, architecture decisions, deterministic authorization logic, clearer separation between AI reasoning and execution, merchant comparison, truthful execution states, and a reusable product design system.

## Explore the project

- **Working prototype:** https://buyer-agent-five.vercel.app/
- **Storybook / components:** https://6a80c992b7513c70c15c1cfd-ekhbujeujx.chromatic.com/
- **Product evolution — V0 → V4:** https://www.figma.com/design/mG0JTDjA5yWNqYqDaLccK0
- **AI Use Case Canvas:** https://www.figma.com/board/U4CCYRRJHLw1FIAuanZOPM

## V3 system model

```text
Household intent
      ↓
Household context + purchase history + policies
      ↓
Merchant offers + availability + price comparison
      ↓
Deterministic authorization engine
      ↓
ACT / ASK / STOP
      ↓
Execution state: AUTHORIZED / ORDERED / FAILED
      ↓
User-facing explanation + audit log
```

`RECOMMEND` is intentionally modeled separately from purchase authority. A recommendation does not silently become permission to purchase.

## Core V3 principles

1. **AI does not grant purchase authority.** ACT / ASK / STOP are deterministic outcomes derived from household policy and runtime commerce context.
2. **Unknown conditions fail safely to ASK.** STOP is reserved for genuine hard household prohibitions.
3. **ACT does not mean “purchased.”** The UI may claim an order only after execution succeeds.
4. **Buyer alignment comes before cheapest-price optimization.** Price, merchant preference, familiarity, substitutions, and household rules all remain decision evidence.
5. **Reasoning is explainable without exposing chain-of-thought.** The interface explains observable factors, rules, and outcomes.
6. **Consequential decisions are auditable.** The deterministic reason, rule, evidence, execution state, and outcome are logged.

## What is included here

This is a **curated public showcase** of the V3 work rather than the private production repository.

- `DESIGN.md` — product and design-system specification
- `docs/DECISION-CONTRACT.md` — behavioral contract for intent, authority, execution, and UI semantics
- `docs/DECISION-CONTRACT-VERIFICATION.md` — R1–R8 verification used to reconcile the earlier engine with V3
- `docs/ARCHITECTURE-DECISIONS.md` — selected architectural decisions and tradeoffs
- `docs/V2-TO-V3.md` — concise evolution from functional prototype to spec-driven implementation
- `src/decisionEngine.ts` — selected deterministic decision-engine implementation
- `src/types.ts` — V3 decision-contract types

## Decision model

### Intent

- `PURCHASE` — household intends to buy
- `RECOMMEND` — advisory only; no purchase authority
- `MONITOR` — track a future replenishment need or condition

### Authority for PURCHASE

- `ACT` — authorized to proceed
- `ASK` — human judgment or approval required
- `STOP` — explicit hard household policy prohibits execution

### Execution

- `AUTHORIZED` — permission exists, but order has not yet completed
- `ORDERED` — execution succeeded and an order identifier exists
- `FAILED` — execution was attempted but did not complete

## Representative scenarios

- Familiar staple, approved merchant, within ceiling → **ACT / AUTHORIZED**
- Price above household ceiling → **ASK**
- Merchant switch not permitted → **ASK**
- Unfamiliar product without explicit allowance → **ASK**
- Advisory suggestion → **RECOMMEND**, without purchase authority
- Explicitly prohibited merchant or category → **STOP**

## Why V3 matters

The key shift in V3 is not visual polish. It is the move from a promising prototype to a system whose behavior can be **specified, verified, implemented, explained, and audited**. The goal is to make agent autonomy legible to both users and the product team: what the agent knows, what it is allowed to do, what requires human judgment, and what happened after a decision.

---

**Private implementation details, credentials, environment configuration, internal agent memory, and infrastructure-sensitive files are intentionally excluded from this public repository.**
