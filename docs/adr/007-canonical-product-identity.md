# ADR-007 — Canonical Product Identity

**Decision status:** Accepted  
**Implementation status:** SEPARATE BACKEND / NOT IN REPLIT V1

## Context

Equivalent products can have different merchant-specific identifiers.

Example:

FreshMart: `FM-EGGS-001`

ValueGrocer: `VG-EGGS-001`

Canonical identity: `EGGS-001`

Cross-store comparison requires merchant-independent identity.

## Decision

Maintain canonical product identity while preserving merchant-specific
product identifiers.

## Current Implementation

### Replit V1

Products currently use free-text names/headlines.

There is no canonical product ID or merchant SKU mapping in the Replit
repository.

### Buyer Agent architecture/backend

Canonical product identity is part of the cross-merchant architecture.

### V2 integration gap

Expose normalized product identities to the mobile/application layer as
merchant integration is connected.

## Alternatives Considered

- Compare merchant SKUs directly
- Match only by product name
- Maintain completely independent merchant products

## Rationale

Canonical identity enables:

- cross-store comparison
- availability comparison
- merchant switching
- purchase-history matching
- familiarity detection

## Consequences

Product matching becomes an explicit system responsibility.

Scaling to uncontrolled retailer catalogs may require more sophisticated
entity matching.
