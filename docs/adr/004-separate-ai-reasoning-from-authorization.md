# ADR-004 — Separate AI Reasoning from Purchase Authorization

**Decision status:** Accepted  
**Implementation status:** PARTIALLY IMPLEMENTED IN REPLIT + BACKEND INTEGRATION PENDING

## Context

AI models can interpret intent, compare options and explain decisions.

However, probabilistic AI reasoning should not itself grant permission
to spend household money.

## Decision

Separate:

AI reasoning

from:

purchase authorization.

AI may assist with:

- intent interpretation
- recommendations
- comparison
- explanations
- contextual reasoning

Purchase authority is determined by explicit household policies and
deterministic rules.

AI reasoning must never override authorization.

## Current Implementation

### Replit V1

AI is used for intent parsing and explanation.

Replit verified that no AI call occurs directly in the approve/dismiss
purchase path.

However, the Replit repository does not contain the deterministic
authorization engine.

### Separate backend

Deterministic authorization logic exists in the separately developed
Buyer Agent backend.

### V2 integration gap

Connect Replit's experience layer to the authorization engine.

## Alternatives Considered

- LLM-only authorization
- AI confidence threshold determines purchase authority
- Human approval for every purchase

## Rationale

Deterministic authorization is more:

- predictable
- testable
- auditable
- controllable

for consequential financial actions.

## Consequences

Some actions that an AI model believes are reasonable may still require
ASK or an authorization stop.

This is intentional.
