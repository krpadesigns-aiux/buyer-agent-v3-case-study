# ADR-005 — Buyer-Aligned Optimization

**Decision status:** Accepted  
**Implementation status:** PARTIALLY IMPLEMENTED

## Context

The cheapest available product is not necessarily the best choice for
a household.

Relevant household signals include:

- preferred merchant
- brand preference
- product familiarity
- price ceilings
- substitution preferences
- merchant-switching permission
- household budget
- category-specific policies

## Decision

Optimize within household intent and authorization.

Do not optimize solely for lowest price.

## Current Implementation

### Replit V1

The policy vocabulary and corresponding UX examples exist.

Examples include:

- preferred stores
- grocery budget
- snack cap
- substitution rules
- price-increase ceiling
- organic preference

The current cards are primarily static examples rather than outputs of
a runtime optimization engine.

### Separate backend

Buyer-aligned rules and merchant comparison logic have been developed
outside the Replit mobile repository.

### V2 integration gap

Connect live policy evaluation and commerce comparison to the mobile UI.

## Alternatives Considered

- Always select cheapest
- Always select preferred merchant
- Optimize solely for convenience
- Merchant-sponsored ranking

## Rationale

The Buyer Agent represents the buyer.

Merchant incentives and absolute lowest price must not override household
intent.

## Consequences

The chosen product may occasionally cost more than the cheapest available
alternative.

The agent should be able to explain why.
