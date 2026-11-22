# Buyer’s Agent — Interpretation Model Evaluations

**Evidence status:** executed synthetic **local-model diagnostic baseline**, not a validated evaluation of the current private Buyer’s Agent runtime.

## What is included

- 44 prespecified synthetic scenarios in cases-2026-11-22.json: 16 explicit negative/no-need, 12 weak/possible-need, 12 exact purchase requests, and 4 ambiguous messages.
- A runnable Python evaluator in run_interpretation_evals.py that calls an Ollama model on localhost. No merchant, Stripe, Supabase, household data, or production endpoint is called.
- Raw observed outputs for all 44 requests in results-local-llama3-2026-11-22.jsonl, and a scored report with each failure in report-local-llama3-2026-11-22.md.
- Immutable evidence context: 2026-11-22-v1 dataset; SHA-256 a8e98e2835318426c5f85913183ddcfa40f25ee60da29677fe5f20f6384c1024; model llama3:latest; Ollama 0.40.16; model digest 365c0bd3c000a25d28ddbf732fe1c6add414de7275464c4e4d1c3b5fcb5d8ad1; temperature 0, seed 42.

## Measured, observed results — local Llama 3 only

| Metric | Observed |
|---|---:|
| False-positive confirmed need when gold was none/possible | **1/28 (3.6%)** |
| Incorrect exact product selection / substitution proxy | **0/12 (0%)** |
| Unauthorized substitution proposed | **0/12 (0%)** |
| Need-state mismatch | **7/44 (15.9%)** |
| Purchase-request intent mismatch | **12/44 (27.3%)** |
| Wrong quantity by original gold labels | **2/12 (16.7%)** |
| Parse or model call failures | **0/44** |

These are diagnostic slice results, not population accuracy or a production reliability guarantee. In particular, 0/12 mismatches does not establish substitution safety.

## Important observed failures

- **N14 — false-positive need:** the user asked to *return spoiled milk, not buy more*. The model output need_status=confirmed, but purchase_requested=false. This was a categorization error, not an actual purchase or policy bypass.
- **C01–C12 — missed explicit order intent:** the model correctly marked those as confirmed needs but returned purchase_requested=false for all 12. Even obvious 'Buy exactly one...' instructions were missed. This is a potentially critical handoff bug; deterministic authority was not invoked in this run.
- **C03 — omitted explicit quantity:** 'Buy one unsweetened oat milk' returned a null quantity.
- **A04 — premature product assumption:** the single word 'Milk.' resolved to a specific Fairlife SKU even though the variant was not given.

## Gold-label adjudication and benchmark limitations

- **C09 quantity is underspecified in the request.** The v1 dataset gold label assumes one carton, but the request does not specify a quantity. The raw v1 report counts this as a second quantity error. A more defensible explicitly-quantified rate is **1/11 (9.1%)**. This correction is disclosed rather than silently rewriting the original case labels or results.
- Some weak-signal gold labels are debatable (for example P10/P11). A future independent annotation pass should distinguish cautious deferral from substantive interpretation error.
- Several synthetic household-context descriptions are unusually explanatory. They may make these cases easier than real conversational inputs. A new neutral-context, independently held-out set is needed before using the scores as general model-quality evidence.
- This sample deliberately emphasizes known failure modes and is not a statistically representative measure of household requests.
- These 44 model calls evaluated a LOCAL Llama 3 model via Ollama. The private app's configured OpenAI-compatible model, prompt, deployed version, and end-to-end policy/tool bridge were **not** evaluated here.

## Reproduce

1. Install Ollama with the recorded model digest (the mutable llama3:latest tag may resolve differently in future).
2. Start Ollama on http://127.0.0.1:11434.
3. In this directory run: python3 run_interpretation_evals.py
4. Inspect the resulting JSONL and Markdown report; compare the model digest and dataset SHA-256 before comparing scores.

## Required next evidence

1. Pin and execute the **actual Buyer’s Agent configured model** against these cases, with a validated structured-output schema and exact prompt version.
2. Execute the **model → canonical catalog → deterministic R1–R8** dry-run bridge with no merchant side effects. Score wrongful ACT after the real policy layer, separately from interpretation mistakes.
3. Instrument the real backend with privacy-screened OpenTelemetry/Langfuse spans for interpretation, candidate resolution, policy, authorization, execution and reconciliation. Only the first interpretation step is measured here; do not present these JSONL records as hosted Langfuse traces.
4. Investigate 3–5 failures, make controlled changes and rerun this set plus an independent holdout. Publish both baseline and retest, not only improvement claims.

Langfuse has retired the old trace/span batch ingestion endpoint for Langfuse Cloud as of November 16, 2026. Use a current OpenTelemetry-based Langfuse SDK for **new** traces: https://langfuse.com/docs/observability/sdk/overview.

**Privacy boundary:** This curated evidence contains only fictional household fixtures. Keep the full private application, secrets, real household data, and merchant/payment credentials out of this repository.
