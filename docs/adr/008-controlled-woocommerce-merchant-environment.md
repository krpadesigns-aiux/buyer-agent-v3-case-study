# ADR-008 — Controlled WooCommerce Merchant Environment

**Decision status:** Accepted  
**Implementation status:** SEPARATE BACKEND / MERCHANT ENVIRONMENT

## Context

Major retailer APIs can introduce:

- access restrictions
- partner requirements
- inconsistent capabilities
- external dependencies

The prototype nevertheless benefits from real commerce APIs rather than
purely static merchant mocks.

## Decision

Use FreshMart and ValueGrocer as controlled WooCommerce prototype merchants.

They provide a controlled environment for testing:

- products
- price differences
- availability
- substitutions
- merchant switching
- commerce API integration

The architecture must not be limited to these two merchants.

## Current Implementation

### Replit V1

FreshMart and ValueGrocer currently appear only as UI/demo merchant names.

No WooCommerce API client exists in the Replit repository.

### Separate commerce environment

FreshMart and ValueGrocer exist as separate WooCommerce merchant sites
and their APIs are used by the separately developed Buyer Agent backend.

### V2 integration gap

Connect Replit V2 through the Commerce Adapter rather than directly
embedding WooCommerce logic in the mobile application.

## Alternatives Considered

- Static merchant mocks
- Immediate production retailer integrations
- Custom commerce backend

## Rationale

WooCommerce provides controllable real commerce behavior while allowing
the broader architecture to remain retailer-independent.

## Consequences

FreshMart and ValueGrocer demonstrate the architecture but do not prove
production interoperability with every retailer.
