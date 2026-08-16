# ADR-006 — Commerce Adapter

**Decision status:** Accepted  
**Implementation status:** SEPARATE BACKEND — NOT IN REPLIT V1

## Context

The Buyer Agent should support multiple merchants without embedding
merchant-specific logic throughout the decision system.

Merchant APIs can differ in:

- schemas
- SKUs
- pricing
- inventory
- checkout
- capabilities

## Decision

Use a Commerce Adapter between merchant systems and Buyer Agent logic.

Conceptually:

```
Merchant APIs
      ↓
Commerce Adapter
      ↓
Normalized Commerce Data
      ↓
Buyer Agent
```

## Current Implementation

### Replit V1

No Commerce Adapter or WooCommerce integration exists in the Replit
repository.

Merchant names appearing in Replit are currently UI/demo data.

### Separate backend

A Python Commerce Adapter was developed separately for the Buyer Agent
backend.

### V2 integration gap

Integrate the mobile/API layer with the existing Commerce Adapter rather
than recreating merchant-specific logic inside the mobile application.

## Alternatives Considered

- Direct merchant API calls from the mobile app
- Merchant-specific decision logic
- Build exclusively for FreshMart and ValueGrocer

## Rationale

The adapter keeps the Buyer Agent merchant-independent.

## Consequences

- Merchant data requires normalization.
- New merchants require adapter implementations.
- Merchant capabilities cannot be assumed to be identical.
