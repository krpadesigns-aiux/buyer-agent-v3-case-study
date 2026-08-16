# Architecture Decision Records — Buyer Agent

> **Project:** Buyer Agent — Calibrated Autonomy for Household Grocery Shopping  
> **ADR baseline:** 2026-08-14  
> **Status:** Active
>
> These ADRs describe architectural decisions for the Buyer Agent system.
> Implementation status is recorded separately so that prototype behavior,
> separate backend work, and target architecture are never confused.

---

## Index

| ADR | Decision | Implementation status |
|---|---|---|
| [ADR-001](001-mobile-application-stack.md) | Mobile Application Stack | ✅ Replit V1 |
| [ADR-002](002-mobile-api-server.md) | Mobile API Server | ✅ Replit V1 |
| [ADR-003](003-bounded-agent-autonomy.md) | Bounded Agent Autonomy | 🔀 Split |
| [ADR-004](004-separate-ai-reasoning-from-authorization.md) | AI Reasoning vs Authorization | 🔀 Partial + separate backend |
| [ADR-005](005-buyer-aligned-optimization.md) | Buyer-Aligned Optimization | 🔀 Partial + separate backend |
| [ADR-006](006-commerce-adapter.md) | Commerce Adapter | 🧩 Separate backend |
| [ADR-007](007-canonical-product-identity.md) | Canonical Product Identity | 🧩 Separate backend / architecture |
| [ADR-008](008-controlled-woocommerce-merchant-environment.md) | WooCommerce Merchant Environment | 🧩 Separate merchant/backend layer |
| [ADR-009](009-household-context-and-decision-audit-store.md) | Household Context + Audit Store | 🔀 Split |
| [ADR-010](010-hybrid-product-and-catalog-strategy.md) | Hybrid Product Architecture | 🔀 Split |
| [ADR-011](011-product-image-enrichment.md) | Product Image Enrichment | ✅ Replit V1 |
| [ADR-012](012-authentication-deferred-for-v1.md) | Authentication Deferred | ✅ Replit V1 |

---

## Architecture Principles

These principles are derived from the ADR set.

### 1. The agent represents the buyer

Household intent takes precedence over merchant incentives.

### 2. Recommendation is not authorization

An AI recommendation does not grant permission to spend money.

### 3. Authorization is explicit

Purchase authority comes from household-defined policies and deterministic
rules.

### 4. AI reasoning cannot override authorization

Probabilistic reasoning may inform decisions but does not grant authority.

### 5. Merchant integrations are replaceable

Buyer Agent logic should not depend directly on FreshMart, ValueGrocer,
WooCommerce or any future retailer.

### 6. Commerce truth and enrichment are different

Merchant systems provide price and availability.

External sources may enrich product information.

### 7. Decisions are auditable

Consequential agent behavior should retain enough information to explain
what happened and why.

### 8. Prototype state is not architecture truth

A V1 implementation shortcut does not redefine the target system.

### 9. V2 integrates the layers

V2 should preserve the successful Replit experience while progressively
connecting it to the existing Buyer Agent backend architecture.

---

## V2 Boundary

The ADRs are architectural decision records.

They are NOT instructions for an AI coding agent to implement every
unimplemented ADR simultaneously.

When beginning V2:

1. Preserve the successful V1 user experience unless explicitly changing it.
2. Read these ADRs before making architectural changes.
3. Treat implementation-status sections as the current baseline.
4. Do not assume "Accepted" means "already implemented."
5. Integrate architecture incrementally.
6. Do not recreate backend capabilities that already exist separately
   without first inspecting those implementations.
7. Each implementation task should explicitly identify which ADRs it affects.
