# Decision Contract Verification — R1–R8

This document summarizes the verification work used to reconcile the earlier decision engine with the V3 Decision Contract.

## Verification summary

The earlier engine had solid deterministic foundations, but several output semantics needed to be normalized for V3.

| Rule | V3 result |
|---|---|
| R1 — policy must exist | Missing policy → `ASK` |
| R2 — merchant authorization | Unknown merchant → `ASK`; explicitly prohibited merchant → `STOP` |
| R3 — merchant switching | Unauthorized switch → `ASK` |
| R4 — price ceiling | Price above ceiling → `ASK` |
| R5 — unfamiliar product | Not explicitly allowed → `ASK` |
| R6 — substitution | Not explicitly allowed → `ASK` |
| R7 — autonomy level | `act` → `ACT`; advisory/prepare/ask → `ASK` |
| R8 — fail-safe | Unresolved authorization → `ASK` |

## Key semantic corrections

### ESCALATE → ASK
The earlier implementation used `ESCALATE` for some unresolved states. V3 removes that extra authority label. Unknown or unresolved conditions default to `ASK`.

### BLOCK → ASK or STOP
The earlier implementation sometimes used `BLOCK` for advisory-only autonomy. In V3, advisory-only authority is not a hard prohibition, so the purchase path resolves to `ASK`.

`STOP` is reserved only for explicit hard policy evidence such as a prohibited merchant or blocked category.

### RECOMMEND is not authority
`RECOMMEND` is a separate intent state. It must not be returned by the purchase-authorization engine as an authority result.

### ACT ≠ ORDERED
The decision engine may return `ACT`, meaning the action is authorized. The UI can only claim `ORDERED` or `Bought for you` after execution succeeds.

## Verification outcome

The V3 TypeScript engine applies the normalized contract:

- R1 → `ASK`
- R2 → `ASK` or explicit `STOP`
- R3–R6 preserve the deterministic household-policy checks
- R7 removes `BLOCK` and uses `ASK` for advisory-only authority
- R8 fails safely to `ASK`

This verification step was important because V3 treats the behavior spec as the source of truth and adapts implementation semantics explicitly rather than silently carrying forward incompatible prototype behavior.
