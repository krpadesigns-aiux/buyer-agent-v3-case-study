# ADR-010 — Hybrid Product and Catalog Strategy

**Decision status:** Accepted  
**Implementation status:** SPLIT / PARTIALLY IMPLEMENTED

## Context

Merchant systems and external product databases answer different questions.

Merchant systems are authoritative for commerce facts such as:

- price
- inventory
- merchant
- availability
- purchasability

External product sources may provide:

- images
- barcodes
- nutrition
- metadata

## Decision

Use a hybrid product architecture.

Merchant commerce sources provide commerce truth.

External product sources provide enrichment.

Conceptually:

```
Merchant APIs
   ↓
price / inventory / availability

External Product Sources
   ↓
images / metadata / enrichment

           ↓

Canonical / normalized product layer

           ↓

Buyer Agent
```

## Current Implementation

### Replit V1

Open Food Facts product-image enrichment is implemented.

Merchant commerce data is not connected in the Replit repository.

### Separate backend

WooCommerce merchant integration exists separately.

### V2 integration gap

Combine merchant commerce data and external enrichment through the
normalized product/commerce architecture.

## Alternatives Considered

- WooCommerce-only product data
- External catalog as commerce authority
- Manually maintain all product information
- Import the entire external catalog into WooCommerce

## Rationale

Commerce truth and product enrichment have different provenance and
freshness requirements.

Keeping them separate prevents external metadata from being mistaken for
live merchant information.

## Consequences

- Data provenance must remain explicit.
- Product matching is required.
- Enrichment cannot be treated as live merchant inventory or price.
