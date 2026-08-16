# ADR-012 — Authentication Deferred for V1

**Decision status:** Accepted  
**Implementation status:** VERIFIED IN REPLIT V1

## Context

V1 focuses on validating Buyer Agent interaction, autonomy and purchasing
concepts.

Authentication would add implementation complexity before the experience
and architecture are fully integrated.

## Decision

Do not require authentication in V1.

Authentication and household identity are required before broader
production deployment.

No authentication provider is selected by this ADR.

Provider selection should be made separately when implementation
requirements are known.

## Current Implementation

Replit verified that V1 has no authentication implementation.

## Alternatives Considered

- Authentication immediately
- Replit Auth
- Clerk
- Custom authentication
- Social authentication

## Rationale

Deferring authentication reduces prototype friction while core workflows
are evolving.

## Consequences

- V1 is not production-ready for persistent household identity.
- Multi-user household access is incomplete.
- Production access to household data requires authentication and
  authorization controls.
