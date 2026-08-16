# ADR-011 — Product Image Enrichment

**Decision status:** Accepted  
**Implementation status:** VERIFIED IN REPLIT V1

## Context

Product thumbnails improve scanning and recognition across Buyer Agent
cards and household lists.

The prototype needs a low-friction external image source.

## Decision

Use Open Food Facts for product-image enrichment through the API server.

Provide category emoji fallback when no usable image is returned.

## Current Implementation

Replit verified:

- `GET /api/ai/product-image?q=`
- Open Food Facts proxy
- product-image utility
- in-memory cache
- search-term extraction
- category emoji fallback
- thumbnails in cards and shopping UI

## Alternatives Considered

- Manual image management
- Direct client requests
- Paid image/catalog service
- No product imagery

## Rationale

Open Food Facts provides useful grocery enrichment without requiring a
commercial API relationship for the prototype.

## Consequences

- Product coverage is inconsistent.
- Search results may not represent the exact merchant item.
- Images are enrichment, not merchant commerce truth.
