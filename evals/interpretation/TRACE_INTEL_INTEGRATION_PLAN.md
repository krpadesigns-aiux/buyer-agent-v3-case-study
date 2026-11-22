# Buyer’s Agent → Langfuse → Trace Intel: observability contract

**Status (2026-11-22): proposed integration contract, not a completed Langfuse ingestion or Trace Intel integration.**

## Current evidence boundary

Forty-four local Ollama model calls generated synthetic JSONL test outputs. They are reproducible offline results, but they currently have **no verified Langfuse trace IDs**. Do not present a JSONL row as a hosted trace.

Trace Intel V3's inspected Next.js route uses the older Langfuse GET /api/public/traces read endpoint. The current Langfuse Observations API v2 is recommended for fresh OpenTelemetry traces. The legacy POST /api/public/ingestion endpoint stopped accepting trace/span events on Langfuse Cloud as of November 16, 2026. New event ingestion must use an OpenTelemetry-based SDK/exporter.

Documentation: https://langfuse.com/docs/observability/sdk/overview and https://langfuse.com/docs/api-and-data-platform/features/public-api

## Proposed span hierarchy for the **actual** app backend

    buyer_agent_run (trace, case_id, synthetic=true, app_commit, dataset_version)
      ├─ interpret_request (generation: provider, resolved_model, prompt_hash, masked input, structured output, latency)
      ├─ resolve_catalog_candidate (span: CP-* mapping, normalized offer, ambiguity)
      ├─ evaluate_authority (span: deterministic R1–R8 rule, policy version, engine and final authority)
      ├─ execute_purchase (tool/span: only for authorized controlled tests; attempt identity, final-total recheck)
      ├─ reconcile_order (tool/span: merchant evidence, payment evidence, status, unknown-vs-failed)
      └─ render_user_state (span: display status consistent with verified outcome)

**Separation rule:** the model's interpretation output never owns or overwrites the deterministic rule, ACT/ASK/STOP result, or merchant/payment verification.

## Minimal case-level fields

| Field | Meaning |
|---|---|
| case_id, dataset_version | Link a trace to a pre-labeled synthetic test |
| model_provider, resolved_model, model_digest | Pin actual model, not just mutable display name |
| prompt_hash, app_commit | Reproducibility |
| gold_need_status, predicted_need_status | Interpretation error |
| gold_product_id, predicted_product_id | Exact catalog match / substitution proxy |
| false_positive_need, incorrect_product, purchase_intent_mismatch | Boolean evaluation scores |
| engine_authority, final_authority, rule_id | **Only** from deterministic code, never the model |
| execution_state, merchant_order_confirmed, payment_confirmed | Truthful purchase outcome |
| trace_id | Backend-generated Langfuse/OTel trace ID, saved only once verified |

## Step-by-step verification gate

1. Create or select a **separate, access-controlled Langfuse project** for Buyer Agent synthetic evaluations. Keep its credentials in the backend only; never in browser bundles or GitHub.
2. Instrument the actual model-call server with the up-to-date Langfuse Python/TS OpenTelemetry SDK; record one synthetic request and confirm its root observation and generation are visible.
3. Save the returned real trace ID alongside the local case ID. Verify the trace through Observations API v2 before marking instrumentation complete.
4. Update Trace Intel's backend adapter to read Observations API v2 with cursor pagination and to group observations by trace ID. Do not assume the existing legacy traces route can render newly ingested spans.
5. Investigate a measured failure (for example, the return-vs-buy interpretation error) in Trace Intel. Record the trace ID, failing span, cause hypothesis, fixed prompt/code version, and retest trace.
6. Export only scrubbed fixtures and derived scores to the public case-study repository. No household identities, authorization tokens, raw billing records, Stripe secrets, or real addresses.

## Not yet verified

- No live Langfuse trace was written or retrieved in this evaluation.
- Trace Intel has not been demonstrated displaying Buyer Agent case traces.
- The configured private Buyer Agent model has not been evaluated here.
- This document cannot be used to claim integrated end-to-end observability.
