# Trace Intel × Buyer’s Agent — local evidence investigation

**Date:** November 22, 2026  
**Status:** **LOCAL POST-HOC EVIDENCE REPLAY BUILT AND VERIFIED — NOT LANGFUSE TRACE INGESTION**

## What exists now

A new local route at `http://localhost:3991/evals/buyer-agent` was created in the user's separate **Trace Intel** Next.js repository. It uses the saved 44-case public synthetic dataset and the Replit V2 configured-model action outputs already preserved in this draft PR. The interface provides search, scenario and review filters, selected case detail, recorded request and observed action/parameters, and diagnostic investigation guidance.

**It does not call Langfuse, contain genuine instrumented model spans, provide Langfuse trace IDs, or demonstrate V4 purchasing behavior.** No source modifications were made to the Buyer’s Agent Replit application and no commerce calls were made.

TypeScript static validation passed, both local routes `/evals` and `/evals/buyer-agent` returned HTTP 200, and a 44-case integrity test passed with exact source-input and recorded-output correspondence. A headless Chrome desktop screenshot of the review was visually inspected. All local source changes remain uncommitted; existing unrelated Trace Intel working-tree edits were preserved.

## Investigations highlighted in the UI

| Case | Observed output | Why investigate |
|---|---|---|
| N10 | `dismiss_all` | Asking to stop **one** paper-towel suggestion could affect **all** cards if V2 UI handler executes this returned action |
| A01 | `add_item: milk` | “Order our usual milk” conflicts with the two plausible historical variants |
| A04 | `add_item: milk` | Single noun “Milk.” lacks explicit request or product variant |
| P01 | `add_item: Fairlife` | Recurring buying cadence has no corroborated current inventory or explicit instruction |
| P05 | `add_item: paper towels` | Promotion/tentative question became list action without confirmed need |
| C06 | `add_item`, quantity 12 eggs | Catalog sells a 12-count carton, so literal quantity can be misinterpreted at order time |
| C09 | `add_item` with fallback restrictions | Downstream product/substitution enforcement was not exercised; **unknown**, not a proven violation |
| P03 | `add_item` with “next week’s list” | Whether the UI honors the requested future-list destination is **unknown** |

These are **analyst-selected review hypotheses** and need independently adjudicated expectations. The remaining **36 cases are unreviewed**, not automatically correct.

## Source-verified counts

- Replit V2 run: 44/44 HTTP 200 and parseable JSON; reported actions: 17 add_item, 19 none, 7 remove_item, 1 dismiss_all.
- 12/44 outputs contained non-string values inconsistent with the current string-valued TypeScript declaration.
- Reproducibility checks: dataset coverage, uniqueness, exact output matching, action counts, annotated-review counts and evidence-class disclaimers all **passed**.
- The upstream provider resolved model revision was not exposed. The reported requested model is `gpt-5.6-luna`.

## What is missing for REAL Langfuse-based evaluation

1. Choose a **running** Buyer’s Agent V4 model/need interpretation endpoint, not the older current Replit V2 voice-action parser.
2. Attach OpenTelemetry-based model and policy instrumentation to the actual runtime. As of November 2026, Langfuse Cloud uses `POST /api/public/otel/v1/traces`; legacy trace ingestion sunset on Nov 16, 2026.
3. Capture real `model.interpret` and subsequent `catalog.resolve`, `policy.evaluate`, `execution.dry_run` observations where those operations actually execute, with synthetic input, prompt/code/model versions, validation outcome and timing.
4. Read those observations back from Langfuse (Observations API v2) with verified IDs and time bounds, then link Trace Intel to that **real data**.
5. Demonstrate one failing model case, root-cause correction and instrumented retest, keeping the V2 action parser results distinct from V4 R1–R8 safety outcomes.

Current official sources:
- https://langfuse.com/docs/api-and-data-platform/features/public-api
- https://langfuse.com/docs/observability/get-started
- https://langfuse.com/integrations/native/opentelemetry/migration-to-v4

**No connected Langfuse traces or before/after improvement have been claimed.**
