# ADR-009 — Household Context and Decision Audit Store

**Decision status:** Accepted  
**Implementation status:** SPLIT IMPLEMENTATION

## Context

The Buyer Agent needs household-specific context independent of individual
merchants.

Relevant information includes:

- household
- preferences
- authorization policies
- purchase history
- decision history

Consequential agent decisions should be auditable.

## Decision

Use Supabase as the persistent Buyer Agent household-context and decision
audit store.

Domain entities include:

- `households`
- `preferences`
- `authorization_policies`
- `purchase_history`
- `decision_log`

## Current Implementation

### Replit V1

The mobile prototype stores UI/application state using React context and
AsyncStorage.

Replit verified that the repository does NOT contain the Supabase
household-domain schema.

The generic Drizzle/Postgres scaffold in the Replit repository is not
the Buyer Agent household data model.

### Separate backend

The Supabase Buyer Agent project and household-domain backend were
developed separately.

### V2 integration gap

Connect authenticated/server-side mobile access to the existing household
backend.

Do not expose privileged Supabase credentials in the mobile client.

## Alternatives Considered

- Mobile-only state
- Store household intelligence in WooCommerce
- Local files
- Custom database/backend

## Rationale

Household intelligence belongs to the Buyer Agent rather than any
individual merchant.

Persistent decision records also support auditability.

## Consequences

- V1 mobile and backend are currently separate.
- Integration requires API/data contracts.
- Production access requires appropriate authentication and authorization.
