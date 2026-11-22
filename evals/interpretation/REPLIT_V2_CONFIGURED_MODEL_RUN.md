# Buyer Agent — configured Replit model, V2 voice-action evaluation

**Date:** November 22, 2026. **Source:** inspection and evaluation of the user's existing editable [Buyer Agent Replit app](https://replit.com/@krpadesigns/Buyer-Agent) through the Replit integration; Replit Agent reported its direct development API observations. **Not a V4 evaluation or validated household-need benchmark.**

## Verified tested surface

- Replit project checked out branch **V2** at `2013556b7efa4f275751b35f2de7a7fa2ce9f199`. This is distinct from the private GitHub V4 merchant/policy implementation.
- Replit confirms `gpt-5.6-luna` requested through its managed OpenAI-compatible integration. Development and production configuration keys were reported present; values were not read. The **underlying serving model revision/alias mapping is unverified**.
- Tested `POST /api/ai/intent` **on development**, with each input as `{transcript: case.request,context:{decisionCount:0,boughtCount:0,lowItemNames:[],cardHeadlines:[]}}`. The endpoint returns action, params and reply, **not** `need_status`, canonical product ID, validated quantity, `purchase_requested` and substitution fields.
- Dataset: synthetic 44 cases from `2026-11-22-v1`; SHA-256 `a8e98e2835318426c5f85913183ddcfa40f25ee60da29677fe5f20f6384c1024`.
- Run started `2026-11-22T16:48:42.484Z`; 70.881 seconds for 44 sequential requests. No UI handlers invoked, no checkout, orders, payments or data modifications. The Replit Agent reported 0 HTTP failures, 0 timeouts, 0 JSON failures and no unsupported action names. Provider token usage unavailable.

## Actual returned model actions

| Action | Number of cases |
|---|---:|
| `none` | 19 |
| `add_item` | 17 |
| `remove_item` | 7 |
| `dismiss_all` | 1 |
| **Total** | **44** |

All 12 unambiguous explicit purchase requests C01–C12 mapped to **add_item**. A01 (ambiguous “Order our usual milk”) also mapped to `add_item`, so **13** cases that used order/buy phrasing produced add_item. This endpoint **does not have a purchase action**: `add_item` does not imply an order was placed.

Five cases explicitly told the agent not to buy/reorder/restart checkout (N02, N04, N08, N11, N14), and none returned `add_item` in this test. This does **not** establish broad negative-intent safety.

## Observed defects and ambiguities

1. **Ambiguous item identity (A01/A04):** “Order our usual milk” and the single-word “Milk.” both produced `add_item` with `{itemName:'milk'}` despite insufficient identity evidence. This action was **not executed**; no product was purchased.
2. **Weak evidence promoted to list action (P01/P05):** a regular cadence statement and promotional price discussion returned `add_item`. P03 (“Maybe add ... next week's list”) also returned `add_item`, which could be appropriate only with the user's future-list context preserved; downstream handling was not tested.
3. **Broad dismissal hazard (N10):** “There are already five rolls of paper towels; stop the restock suggestion” produced `dismiss_all` with an `itemName` parameter. Replit's inspected UI handler ignores the targeted item and would dismiss all cards if invoked. **No cards were dismissed in this test.**
4. **Schema mismatch (12/44):** 12 responses included one or more non-string param values (e.g. numeric quantities, boolean `allowSubstitutions`, arrays of exclusions), despite the TypeScript response declaration `Record<string,string>` and no runtime schema validation.
5. **Unit normalization (C06):** “one dozen large eggs” returned `quantity:12, unit:'eggs'`. If downstream catalog sells one dozen per carton, conversion to 1 carton is necessary before order authorization. No transaction was attempted.
6. **No autonomy proof:** Replit V2's `/api/ai/intent` returns JSON consumed by local client handlers; model output was **not** found connected to the R1–R8 policy engine in this checkout.

## Methodology and evidence boundaries

- The original dataset gold labels were designed for **household-need interpretation**, and cannot be directly scored against this V2 voice-action output schema. **Do not compare these V2 action counts with the earlier local Llama 3 need-status accuracy figures.**
- The data file [`replit-v2-voice-action-results-2026-11-22.json`](replit-v2-voice-action-results-2026-11-22.json) preserves all 44 Replit-reported per-case action/param pairs and HTTP/parse status, as transcribed from the Replit Agent's response. This is **not** a dump of raw HTTP logs; it does not include response `reply` strings, provider upstream request IDs, trace IDs or token usage.
- Replit reported successful development inference; it did not independently expose the upstream model revision, production deployment commit, or Langfuse traces.
- The V2 voice UI has separate actions from the V4 deterministic purchase path; no actual request → model → canonical product → ACT/ASK/STOP → commerce end-to-end test occurred.

## Next actionable step

Inspect/run the actual V4 model/runtime and its prompts, then define a separately validated schema and candidate resolver for household needs. Exercise actual V4 deterministic R1–R8 in a side-effect-free dry run with proof that SKU identity and substitution constraints are verified independently. Add Langfuse model traces and investigate observed failures before rerun. Keep outcomes and model/version boundaries explicit.
