# ADR-003 — Bounded Agent Autonomy

**Decision status:** Accepted  
**Implementation status:** SPLIT IMPLEMENTATION

## Context

The Buyer Agent should reduce repetitive household purchasing work without
giving an AI system unrestricted authority to spend money.

Different decisions require different levels of authority.

## Decision

Use a bounded action model:

### ACT

The system may execute an action when explicit household authorization
and relevant conditions permit it.

### ASK

The system must request user approval when a decision exceeds an
authorized boundary or contains meaningful uncertainty.

### RECOMMEND

The system may suggest a product, merchant, substitution or other action
without treating that recommendation as permission to purchase.

### AUTHORIZATION STOP

The system must not execute an action when the required authority is absent.

An authorization stop means:

> "The agent is not authorized to perform this action."

It does not mean:

> "The household should not buy this."

## Current Implementation

### Replit V1

The experience states exist in the UI:

- `bought`
- `needs-decision`
- `recommendation`
- `couldnt-purchase`

These states are currently driven primarily by seeded/demo data rather
than runtime policy evaluation.

### Separate backend

The Buyer Agent backend contains deterministic decision/authorization
logic developed separately from the Replit mobile prototype.

### V2 integration gap

Connect the mobile action states to runtime backend decisions rather than
seeded cards.

## Alternatives Considered

- Fully autonomous purchasing
- Human approval for every purchase
- LLM determines purchase authority
- One fixed autonomy level for every household action

## Rationale

Bounded autonomy provides useful delegation while preserving meaningful
human control.

## Consequences

- Some transactions require user intervention.
- Authorization boundaries must remain explicit.
- The UI must distinguish completed, proposed and unauthorized actions.
- Decisions should remain explainable and auditable.
