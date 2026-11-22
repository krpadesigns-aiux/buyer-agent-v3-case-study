# Buyer’s Agent → Langfuse → Trace Intel: observability contract

**Status (2026-11-22): Langfuse OTLP transport and Observations API v2 readback verified with one synthetic connectivity SPAN; actual Buyer Agent model/policy tracing remains unverified.**

## Current evidence boundary

Forty-four local Ollama model calls generated synthetic JSONL test outputs. They are reproducible offline results, but they currently have **no verified Langfuse trace IDs**. Do not present a JSONL row as a hosted trace.

Trace Intel V3's pre-existing trace-list route uses the retired Langfuse GET /api/public/traces endpoint; in this evaluation a **new local read-only route** was implemented for a verified traceId using Observations API v2, while the legacy list view still needs migration. The current Langfuse Observations API v2 is recommended for fresh OpenTelemetry traces. The legacy POST /api/public/ingestion endpoint stopped accepting trace/span events on Langfuse Cloud as of November 16, 2026. New event ingestion must use an OpenTelemetry-based SDK/exporter.

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

## Verified telemetry transport (not model tracing)

- **Langfuse Cloud US** accepted one synthetic-only OTLP span with HTTP 200 on `POST /api/public/otel/v1/traces`, header `x-langfuse-ingestion-version: 4`.
- **Observations API v2 readback verified the same real cloud observation**: trace `1507dab2977fbb06291e66bf5d7f01a4`, observation `7af7eb3284b5cb75`, named `buyer_agent.synthetic_otel_connectivity_check`, type `SPAN`. No model was called, and no user data, merchant or payment interaction occurred.
- Local Trace Intel `/evals/buyer-agent` now links to this API-verified **transport-only** observation, separately from the 44 saved Replit V2 model actions. Local `GET /api/langfuse/health` migrated to Observations API v2. The temporary probe POST route was removed afterward.
- **This is not evidence that actual model or purchasing steps have been instrumented.**

## Not yet verified

- Actual **V2 or V4 model generation** span in Langfuse, including latency, prompt/schema version and requested/resolved model identity.
- Trace Intel has not been demonstrated displaying Buyer Agent case traces.
- The configured private Buyer Agent model has not been evaluated here.
- This document cannot be used to claim integrated end-to-end observability.
