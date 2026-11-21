# AI-native development evidence — Buyer’s Agent

**Evidence status:** Curated public showcase. This is not the full application repository and does not establish production adoption or completed model-interpretation evaluations.

## The development approach

1. **Specify behavior.** The [Decision Contract](DECISION-CONTRACT.md) defines intent, deterministic ACT / ASK / STOP authority, and truthful execution claims. The model may interpret needs; the model must not grant purchase authority.
2. **Constrain AI-assisted implementation.** [CLAUDE.md](../CLAUDE.md), [DESIGN.md](../DESIGN.md), and [architecture decisions](adr/) document the intended behavior, UX constraints, and technical trade-offs. These files are evidence of explicit development instructions; they do not by themselves prove how frequently an AI coding agent was used.
3. **Implement representative policy logic.** [decisionEngine.ts](../src/decisionEngine.ts) shows the R1–R8 authorization checks. This public repository does not yet include a runnable test harness or complete model/commerce integration.
4. **Verify deterministic behavior.** [Decision Contract Verification](DECISION-CONTRACT-VERIFICATION.md) records semantic corrections including unresolved states → ASK, explicit prohibitions → STOP, and ACT ≠ ORDERED. A reported larger private test suite is not independently reproducible here.
5. **Evaluate model interpretation (in progress).** The intended evaluation will test item identification, invented needs, uncertain requests, confidence calibration, and interpretation errors that could reach ACT. **No model evaluation results are published here yet.**
6. **Review outcomes truthfully.** The [agentic commerce documentation](../AGENTIC-COMMERCE.md) distinguishes implemented integrations from protocol explorations. Test-environment commerce execution is not a claim of real-money checkout, delivery, or customer adoption.

## What AI did / what I decided / what was verified

| Dimension | Evidence |
| --- | --- |
| AI's role in the product | Interpret a possible household need and propose candidate information; authorization must remain outside the model |
| Human design decision | Separate intent, deterministic authority, execution and verified outcome; distinguish ASK from a hard STOP |
| AI-assisted development governance | Explicit coding-agent instructions, specifications, design system guidance, and architecture decisions |
| Publicly inspectable implementation | Representative TypeScript decision engine, types, contract, and ADRs |
| Publicly inspectable verification | R1–R8 semantics and documented corrections |
| Not yet independently reproducible | Reported full deterministic test count, model interpretation evaluation, full application workflow and observed before/after results |

## Next reproducibility milestones

- [ ] Publish a sanitized TypeScript test runner and representative R1–R8 acceptance cases.
- [ ] Publish 30–50 labeled interpretation cases with expected item, uncertainty and policy outcome.
- [ ] Run model interpretation against the actual application pipeline, with redacted traces.
- [ ] Record baseline scores, failure taxonomy, changes and held-out rerun results.
- [ ] Publish safe, representative excerpts of actual model integration and workflow traces.
- [ ] Link precise supporting evidence from the portfolio case study.

**Publication boundary:** Never add secrets, real household data, private payment information, confidential employer material, or unreviewed private Git history to this repository.
