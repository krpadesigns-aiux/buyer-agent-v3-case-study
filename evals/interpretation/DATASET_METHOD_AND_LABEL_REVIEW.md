# Synthetic interpretation dataset: construction and review

**Created November 22, 2026. Not a household research dataset. Not collected from interviews, users or runtime logs.**

## Why 44, and what was designed?

The evaluation author constructed 44 synthetic cases directly from the Buyer's Agent behavioral thesis and known risk boundaries. The sample size was chosen to fit the earlier requested 30–50-case first benchmark; it is **not** a power calculation, unbiased sample or representative prevalence estimate.

| Group | IDs | Count | Distinct failure modes |
|---|---|---:|---|
| Known no present purchasing need | N01–N16 | 16 | Stock exists, explicit cancellation, recently bought, discontinued preference, third-party need, price-only lookup, bad sensor, stale/contradictory evidence, return not buy |
| Possible but unconfirmed need | P01–P12 | 12 | Cadence inference, tentative language, future list item, stale imagery, old sensor, unknown quantities or weak third-party statements |
| Explicit purchasing requests | C01–C12 | 12 | Named SKU, milk type/brand, quantity, single-count vs multipack, prohibition on substitutes, out-of-stock instruction |
| Ambiguous reference or intent | A01–A04 | 4 | “Usual” with conflicting history, unspecified prior item, pronoun-only request, one-word “Milk.” |

Items and merchant notions reflect the project specification: Fairlife milk, Market TEST commerce, Shopify kitchen sponge, eggs, bananas, household goods, and canonical CP-* product identity. The evaluation's product catalog and household contexts are *synthetic fixtures*, not actual stock reports or live merchant offers.

## How expected labels were determined

Labels were written **before the first Llama 3 call** using this rule of thumb:
- **none:** explicit absence of present buying need or cancel/no-buy request;
- **possible:** evidence of a plausible need, but no adequate confirmation;
- **confirmed:** an explicit, unambiguous current item/order;
- **ambiguous:** the product or intent cannot be identified;
- **purchase_requested:** specifically directed buy/order now;
- **gold_product / gold_quantity:** exact named catalog unit and quantity, if established;
- **substitution_sensitive:** exact product constraints that should not be silently replaced.

All 44 inputs and original labels are preserved unchanged in cases-2026-11-22.json. The same prompts and a fixed local model digest were used during the recorded run.

## Review weaknesses discovered after the first run

1. **C09 quantity label is invalid as a strict reference.** The user said buy Fairlife milk but gave no quantity. The original gold_quantity=1 assumes a default not present in the request. The raw report conservatively preserves that original scoring; the defensible count for explicit quantities is 1/11, not the naive 2/12.
2. **A01 is both an explicit purchase request and unresolved product ambiguity.** Original gold_purchase=false conflates whether the buyer *asked to order* with whether the system *has enough facts to execute*. Future dataset versions must represent these as separate fields.
3. **Possible versus none can be debated for P10/P11 and similar weak signals.** “No current proof of a need” may reasonably yield either defer/monitor or no purchase. These labels should be independently adjudicated before a high-stakes score is reported.
4. **Some household context is overly explanatory and sometimes gives away the answer.** Example N14 literally says “Return request only; no replenishment request.” A model may be solving a simplified exercise rather than handling noisy household records. Build a neutral-context held-out benchmark.
5. **Substitution assessment is a product-identity proxy, not a live substitute-selection test.** The original 12 exact-product cases never present concrete out-of-stock alternative offers, so 0/12 wrong SKU cannot establish zero unauthorized substitutions.
6. **One seeded catalog and single phrasing per case can mask prompt sensitivity.** Later test sets should include paraphrases, conflicting merchant offer data, language variants, and realistic failure injection.

## Evaluation gates before making portfolio-grade claims

1. Independently review annotations; version corrected/ambiguous labels without erasing the v1 evidence.
2. Compare the actual configured application's model on a schema that the application truly implements. The inspected /api/ai/intent returns voice-action JSON, **not** the need_status/CP-* schema used by this diagnostic dataset.
3. Execute source-to-policy integration with a **validated** product resolver, quantity constraints, household corroboration and real deterministic authority engine. The model cannot grant ACT/ASK/STOP.
4. Run an unseen held-out test set and report both aggregate rates and denominators, false-positive needs, incorrect substitutions, false purchase-intent negatives, wrongful ACT after policy and safe clarification.
5. Record trace IDs and revisions before attempting a reproducible before/after claim.

**Evidence boundary:** these tests are synthetic and their first results are for local Llama 3, not the private app model or a general household population.
