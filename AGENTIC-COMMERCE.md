# Agentic Commerce — Buyer’s Agent V3

Buyer’s Agent is designed as more than an AI shopping interface. V3 connects to live merchant commerce APIs, compares offers across merchants, applies household authorization rules deterministically, and separates recommendation, purchase authority, and successful execution.

## Status at a glance

| Capability / protocol | Status | Buyer’s Agent use |
|---|---|---|
| WooCommerce Store API | **Implemented** | Live offer retrieval from FreshMart and ValueGrocer |
| WooCommerce REST API v3 | **Configured / tested** | Authenticated merchant commerce access |
| Multi-merchant Commerce Adapter | **Implemented** | Normalizes canonical product identity, availability and price |
| Deterministic authorization | **Implemented** | Household policy resolves purchase authority to ACT / ASK / STOP |
| Decision + execution contract | **Implemented** | Separates `AUTHORIZED`, `ORDERED`, and `FAILED` |
| UCP — Universal Commerce Protocol | **Evaluated / roadmap** | Future common interface across commerce discovery and checkout |
| AP2 — Agent Payments Protocol | **Evaluated / architecture mapping** | Future mandate / delegated-payment authorization layer |
| ACP — Agentic Commerce Protocol | **Evaluated / roadmap** | Future agent-to-merchant purchasing interoperability |
| MCP — Model Context Protocol | **Evaluated / roadmap** | Future standardized tool access to commerce services |
| A2A — Agent2Agent Protocol | **Evaluated / roadmap** | Future collaboration with merchant, payment or fulfillment agents |

> UCP, AP2, ACP, MCP and A2A are **not claimed as implemented** in V3. They are architecture references used to evaluate how the system could evolve toward interoperable agentic commerce.

## What is implemented

The current TypeScript commerce adapter calls the WooCommerce Store API for two independent test merchants:

- FreshMart
- ValueGrocer

It normalizes merchant-specific product records into a common offer model and compares purchasable offers using canonical `CP-*` product identity.

```text
FreshMart Store API ───┐
                       ├─→ Commerce Adapter ─→ Normalized Offers
ValueGrocer Store API ─┘
                                  ↓
                           Household Policy
                                  ↓
                         Decision Engine
                                  ↓
                         ACT / ASK / STOP
```

FreshMart and ValueGrocer are the current test merchants, not a fixed two-store product model. Additional merchant adapters can participate in the same normalized offer layer.

## Buyer-aligned commerce logic

Buyer’s Agent does not automatically optimize for cheapest price. Decision evidence may include:

- price
- availability / purchasability
- preferred merchant
- approved or prohibited merchants
- merchant-switching permission
- product familiarity
- substitution permission
- household price ceiling

Purchase authority is resolved by deterministic policy logic rather than by an LLM.

## Intent, authority and execution

```text
Household Intent
      ↓
PURCHASE / RECOMMEND / MONITOR
      ↓
Merchant + Household Evidence
      ↓
ACT / ASK / STOP      ← purchase authority
      ↓
AUTHORIZED / ORDERED / FAILED
      ↓
Explanation + Audit Log
```

`RECOMMEND` is deliberately separate from purchase authority. An advisory suggestion cannot silently become permission to transact.

## Mapping to emerging protocols

### UCP — Universal Commerce Protocol

UCP is designed as a common commerce language between agents, platforms and merchants across flows such as discovery and checkout.

Possible evolution:

```text
Current
Buyer’s Agent → custom Commerce Adapter → merchant APIs

Future
Buyer’s Agent → UCP-compatible commerce layer → many merchants
```

Reference: https://developers.google.com/pay/api/universal-commerce-protocol/overview

### AP2 — Agent Payments Protocol

AP2 focuses on verifiable delegated authorization for agent-driven payments.

Buyer’s Agent already explores the product behavior behind bounded authority through price ceilings, merchant permissions, substitution rules, autonomy levels, ASK escalation and audit logging. These are **not AP2 cryptographic mandates today**, but the policy model could later evolve into a mandate-based authorization layer.

```text
Household Policy
      ↓
Decision Contract
      ↓
AP2-style Mandate
      ↓
Payment
      ↓
Order + Audit Evidence
```

Reference: https://github.com/google-agentic-commerce/AP2

### ACP — Agentic Commerce Protocol

ACP provides a possible future agent-to-merchant commerce interface after Buyer’s Agent has already resolved household intent and authority.

```text
Buyer’s Agent
      ↓
Household Authorization
      ↓
ACP-compatible Merchant Interaction
      ↓
Checkout / Payment / Fulfillment
```

Reference: https://openai.com/index/buy-it-in-chatgpt/

### MCP — Model Context Protocol

A future Buyer’s Agent could expose or consume commerce tools such as catalog search, offer retrieval, policy lookup, purchase evaluation, order creation and order-state inspection through MCP.

V3 currently calls commerce APIs directly; it is **not an MCP implementation**.

Reference: https://modelcontextprotocol.io/

### A2A — Agent2Agent Protocol

A2A could support future collaboration between independent buyer, merchant, payment and fulfillment agents.

V3 is currently a single Buyer’s Agent system with merchant API integrations; it does **not** currently use A2A.

Reference: https://a2a-protocol.org/

## Current vs roadmap

### Implemented in V3

- WooCommerce commerce APIs
- multi-merchant offer retrieval
- canonical offer normalization
- merchant price comparison
- household-policy evidence
- deterministic ACT / ASK / STOP authorization
- recommendation vs purchase-authority separation
- authorization vs successful-order separation
- decision logging / auditability

### Evaluated / roadmap

- UCP integration
- AP2 cryptographic mandates
- ACP merchant checkout integration
- MCP commerce tools/server
- A2A orchestration
- production delegated-payment execution

## Product-design implication

The core agentic-commerce problem is not simply **“Can an AI agent buy something?”**

It is:

> **What authority did the household grant, what evidence did the agent use, when must it involve the user, and how can the resulting action be verified and explained?**

Buyer’s Agent treats those questions as first-class product behavior rather than implementation details.
