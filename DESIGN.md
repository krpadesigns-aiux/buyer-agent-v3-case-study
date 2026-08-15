# DESIGN.md — Buyer’s Agent V3

## Design intent

Buyer’s Agent should feel like a calm, competent household assistant: intelligent without excessive AI decoration, proactive without hiding consequential actions, and financially aware without becoming a finance dashboard.

The interface prioritizes **household decisions over system mechanics**.

## V3 design-system architecture

Buyer’s Agent uses three layers:

1. **Material Design 3** — semantic color roles, typography hierarchy, spacing, shape, interaction states, accessibility, touch targets.
2. **React Native Paper** — implementation layer for standard Material-compatible primitives.
3. **Buyer’s Agent components** — domain-specific components that communicate agent authority, merchant comparison, policies, and reasoning.

Representative custom components:

- `AgentActionCard`
- `DecisionStatus`
- `ProductSummary`
- `MerchantComparison`
- `ReasoningPanel`
- `PolicyIndicator`
- `AgentActionButtons`
- `AutonomyControl`
- `HouseholdStatus`

## Semantic state model

The core agent states are:

- `ACT`
- `ASK`
- `RECOMMEND`
- `AUTHORIZATION_STOP`

State meaning must be communicated through more than color alone. Use label, icon, copy, interaction structure, visual emphasis, and semantic color together.

### ACT
The agent acted within previously granted authority. Use past-tense or truthful execution language and expose “View why” and Undo where possible.

### ASK
Human judgment is required. Clearly state what changed, why the user is being asked, and what options are available.

### RECOMMEND
Advisory only. It should be visually quieter than ASK and must not imply that purchase approval is pending.

### AUTHORIZATION STOP
The agent was not permitted to execute because of a hard household boundary. This is **not a system error**.

## AgentActionCard

`AgentActionCard` is the primary UI representation of consequential agent activity.

Supported variants:

- ACT
- ASK
- RECOMMEND
- AUTHORIZATION_STOP

Possible anatomy:

1. DecisionStatus
2. ProductSummary
3. Headline
4. Context / reason
5. MerchantComparison
6. Savings or consequence
7. PolicyIndicator
8. Reasoning entry point
9. Primary / secondary action
10. Recovery action such as Undo

Cards should feel like household decisions, not alerts.

## Merchant comparison

MerchantComparison is used when differences between offers materially affect the decision. It may compare:

- merchant
- price
- savings
- availability
- preferred/familiar merchant
- substitution
- delivery timing

The design should answer: **“What changed, and why does it matter?”**

The cheapest option is not automatically the best option; buyer-aligned household context remains visible.

## Reasoning / “View why”

Reasoning is progressive disclosure. The default UI should communicate the decision clearly without requiring users to inspect detailed system logic.

“View why” may reveal:

- relevant household rule
- normal price or purchase pattern
- merchant comparison
- substitution history
- budget context
- observable confidence/context signals

Do not display raw chain-of-thought.

## Policy language

Translate system fields into household language.

Examples:

- `merchant_switching_allowed = true` → “You may switch stores when it saves money.”
- `max_item_price = 6` → “Buy automatically up to $6.”
- `substitutions_allowed = false` → “Ask before substituting.”

## Truthful execution language

A key V3 rule is that **authorization and execution are different states**.

- ACT + AUTHORIZED → “Purchase authorized” / “Ready to order”
- ACT + ORDERED → “Ordered from …” / “Bought for you”
- ASK → decision required
- STOP → calm explanation of the policy boundary
- RECOMMEND → advisory language only

The interface must never imply a purchase happened before backend execution confirms it.

## Product character

Preserve the warm consumer personality of the functional prototype while systematizing it with Material 3 foundations. Material 3 is the foundation, not the product identity.
