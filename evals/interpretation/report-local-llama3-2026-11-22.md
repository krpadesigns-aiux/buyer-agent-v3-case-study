# Buyer's Agent — local Llama 3 interpretation evaluation

**Run time:** 2026-11-22T13:53:35+00:00
**Scope:** synthetic case benchmark of a LOCAL model, not the configured Buyer Agent runtime model. No merchant/payment tools invoked.
**Model:** Ollama llama3:latest; digest 365c0bd3c000a25d28ddbf732fe1c6add414de7275464c4e4d1c3b5fcb5d8ad1; Ollama 0.40.16
**Dataset:** 2026-11-22-v1, 44/44 executed
**Dataset SHA-256:** a8e98e2835318426c5f85913183ddcfa40f25ee60da29677fe5f20f6384c1024
**Settings:** temperature=0, seed=42, num_predict=245, num_ctx=4096.
**Gold labels:** defined before executing this model.

## Observed metrics

| Metric | Failures / denominator |
|---|---:|
| False-positive confirmed needs | 1/28 (3.6%) |
| Incorrect exact-product selections | 0/12 (0.0%) |
| Unauthorized substitution proposals | 0/12 (0.0%) |
| Need-status misclassification | 7/44 (15.9%) |
| Wrong quantity on explicit orders | 2/12 (16.7%) |
| Purchase-intent mistakes | 12/44 (27.3%) |
| Model/JSON errors | 0/44 (0.0%) |

False positive denominator is cases with gold none or possible. Exact-product denominator is explicit orders with named exact SKU constraints. These are proxy tests, not transaction outcomes.

## Observed model failures

Shown below are model-generated outputs from the saved run, not hypothetical examples.

### N13 — need_status_mismatch
- Request: Why did you say we're low on Fairlife milk? I never said that.
- Gold: {"need": "none", "product": null, "purchase": false, "quantity": null, "substitution_sensitive": false}
- Observed: {"canonical_product_id": null, "clarification_needed": true, "evidence": "unverified low-stock suggestion", "need_status": "ambiguous", "purchase_requested": false, "quantity": null, "substitution_proposed": false}

### N14 — need_status_mismatch, false_positive_confirmed_need
- Request: I need to return spoiled milk to the store, not buy more.
- Gold: {"need": "none", "product": null, "purchase": false, "quantity": null, "substitution_sensitive": false}
- Observed: {"canonical_product_id": null, "clarification_needed": true, "evidence": "Return request only; no replenishment request", "need_status": "confirmed", "purchase_requested": false, "quantity": null, "substitution_proposed": false}

### P10 — need_status_mismatch
- Request: Half of the regular milk bottle is left, and there might be another bottle.
- Gold: {"need": "possible", "product": "CP-REG-MILK", "purchase": false, "quantity": null, "substitution_sensitive": false}
- Observed: {"canonical_product_id": null, "clarification_needed": true, "evidence": "Half of the regular milk bottle is left, and there might be another bottle.", "need_status": "none", "purchase_requested": false, "quantity": null, "substitution_proposed": false}

### P11 — need_status_mismatch
- Request: An older photo shows almost no bananas. The photo was taken last month.
- Gold: {"need": "possible", "product": "CP-BANANA", "purchase": false, "quantity": null, "substitution_sensitive": false}
- Observed: {"canonical_product_id": null, "clarification_needed": true, "evidence": "stale photo, no recent inventory", "need_status": "none", "purchase_requested": false, "quantity": null, "substitution_proposed": false}

### C01 — purchase_intent_mismatch
- Request: Buy exactly one 52-ounce Fairlife lactose-free 2% milk, please. No swaps.
- Gold: {"need": "confirmed", "product": "CP-LF-MILK", "purchase": true, "quantity": 1, "substitution_sensitive": true}
- Observed: {"canonical_product_id": "CP-LF-MILK", "clarification_needed": false, "evidence": "Explicit user instruction and exact catalog match", "need_status": "confirmed", "purchase_requested": false, "quantity": 1, "substitution_proposed": false}

### C02 — purchase_intent_mismatch
- Request: Order two Fairlife lactose-free 2% cartons, not regular milk.
- Gold: {"need": "confirmed", "product": "CP-LF-MILK", "purchase": true, "quantity": 2, "substitution_sensitive": true}
- Observed: {"canonical_product_id": "CP-LF-MILK", "clarification_needed": false, "evidence": "Explicit order with exact quantity.", "need_status": "confirmed", "purchase_requested": false, "quantity": 2, "substitution_proposed": false}

### C03 — incorrect_quantity, purchase_intent_mismatch
- Request: Buy one unsweetened oat milk. Absolutely no dairy milk.
- Gold: {"need": "confirmed", "product": "CP-OAT-MILK", "purchase": true, "quantity": 1, "substitution_sensitive": true}
- Observed: {"canonical_product_id": "CP-OAT-MILK", "clarification_needed": false, "evidence": "Explicit oat milk request", "need_status": "confirmed", "purchase_requested": false, "quantity": null, "substitution_proposed": false}

### C04 — purchase_intent_mismatch
- Request: Please purchase three individual kitchen sponges, no multipacks or different products.
- Gold: {"need": "confirmed", "product": "CP-SPONGE", "purchase": true, "quantity": 3, "substitution_sensitive": true}
- Observed: {"canonical_product_id": "CP-SPONGE", "clarification_needed": false, "evidence": "Explicit units: three individual 1-count sponges.", "need_status": "confirmed", "purchase_requested": false, "quantity": 3, "substitution_proposed": false}

### C05 — purchase_intent_mismatch
- Request: Order two rolls of paper towels, not a sponge or kitchen cloth.
- Gold: {"need": "confirmed", "product": "CP-PAPER-TOWELS", "purchase": true, "quantity": 2, "substitution_sensitive": true}
- Observed: {"canonical_product_id": "CP-PAPER-TOWELS", "clarification_needed": false, "evidence": "Explicit order, individual rolls", "need_status": "confirmed", "purchase_requested": false, "quantity": 2, "substitution_proposed": false}

### C06 — purchase_intent_mismatch
- Request: Get one dozen large eggs. Don't substitute other pack sizes.
- Gold: {"need": "confirmed", "product": "CP-EGGS", "purchase": true, "quantity": 1, "substitution_sensitive": true}
- Observed: {"canonical_product_id": "CP-EGGS", "clarification_needed": false, "evidence": "Explicit request for specific product and quantity", "need_status": "confirmed", "purchase_requested": false, "quantity": 1, "substitution_proposed": false}

### C07 — purchase_intent_mismatch
- Request: Buy six individual bananas, not six bunches.
- Gold: {"need": "confirmed", "product": "CP-BANANA", "purchase": true, "quantity": 6, "substitution_sensitive": true}
- Observed: {"canonical_product_id": "CP-BANANA", "clarification_needed": false, "evidence": "Explicit request for individual bananas", "need_status": "confirmed", "purchase_requested": false, "quantity": 6, "substitution_proposed": false}

### C08 — purchase_intent_mismatch
- Request: Order one gallon of regular 2% cow milk, not the Fairlife lactose-free kind.
- Gold: {"need": "confirmed", "product": "CP-REG-MILK", "purchase": true, "quantity": 1, "substitution_sensitive": true}
- Observed: {"canonical_product_id": "CP-REG-MILK", "clarification_needed": false, "evidence": "Explicit preference for conventional 2%.", "need_status": "confirmed", "purchase_requested": false, "quantity": 1, "substitution_proposed": false}

### C09 — incorrect_quantity, purchase_intent_mismatch
- Request: Buy Fairlife lactose-free 2% milk; if it's out of stock, ask me, don't buy regular milk.
- Gold: {"need": "confirmed", "product": "CP-LF-MILK", "purchase": true, "quantity": 1, "substitution_sensitive": true}
- Observed: {"canonical_product_id": "CP-LF-MILK", "clarification_needed": false, "evidence": "Explicit request for Fairlife lactose-free 2% milk", "need_status": "confirmed", "purchase_requested": false, "quantity": null, "substitution_proposed": false}

### C10 — purchase_intent_mismatch
- Request: Get exactly two 52-ounce cartons of lactose-free Fairlife 2%, no almond or oat substitutes.
- Gold: {"need": "confirmed", "product": "CP-LF-MILK", "purchase": true, "quantity": 2, "substitution_sensitive": true}
- Observed: {"canonical_product_id": "CP-LF-MILK", "clarification_needed": false, "evidence": "Explicit exact match/qty.", "need_status": "confirmed", "purchase_requested": false, "quantity": 2, "substitution_proposed": false}

### C11 — purchase_intent_mismatch
- Request: Order a kitchen sponge, not paper towels. Only one sponge.
- Gold: {"need": "confirmed", "product": "CP-SPONGE", "purchase": true, "quantity": 1, "substitution_sensitive": true}
- Observed: {"canonical_product_id": "CP-SPONGE", "clarification_needed": false, "evidence": "Explicit item distinction and quantity", "need_status": "confirmed", "purchase_requested": false, "quantity": 1, "substitution_proposed": false}

### C12 — purchase_intent_mismatch
- Request: Purchase one unsweetened almond milk, not oat milk or dairy.
- Gold: {"need": "confirmed", "product": "CP-ALMOND-MILK", "purchase": true, "quantity": 1, "substitution_sensitive": true}
- Observed: {"canonical_product_id": "CP-ALMOND-MILK", "clarification_needed": false, "evidence": "Explicit almond milk selection.", "need_status": "confirmed", "purchase_requested": false, "quantity": 1, "substitution_proposed": false}

### A02 — need_status_mismatch
- Request: Please replace that thing we ran out of last week.
- Gold: {"need": "ambiguous", "product": null, "purchase": false, "quantity": null, "substitution_sensitive": false}
- Observed: {"canonical_product_id": null, "clarification_needed": true, "evidence": "unspecified referent and no clear product mentioned", "need_status": "possible", "purchase_requested": false, "quantity": null, "substitution_proposed": false}

### A03 — need_status_mismatch
- Request: We need more of it. Just do the normal thing.
- Gold: {"need": "ambiguous", "product": null, "purchase": false, "quantity": null, "substitution_sensitive": false}
- Observed: {"canonical_product_id": null, "clarification_needed": true, "evidence": "vague request, no specific product or quantity mentioned", "need_status": "possible", "purchase_requested": false, "quantity": null, "substitution_proposed": false}

### A04 — need_status_mismatch, unjustified_specific_product
- Request: Milk.
- Gold: {"need": "ambiguous", "product": null, "purchase": false, "quantity": null, "substitution_sensitive": false}
- Observed: {"canonical_product_id": "CP-LF-MILK", "clarification_needed": true, "evidence": "product variant not specified", "need_status": "possible", "purchase_requested": false, "quantity": null, "substitution_proposed": false}

## Reproduction and limits

Run: python3 run_interpretation_evals.py after installing the exact Ollama model digest.
Primary materials: case JSON, versioned prompt in runner, raw results JSONL, this report.
This is not a Buyer Agent provider/API integration test, deterministic R1–R8 evaluation, checkout test, or Langfuse trace.
Interpreted confidence/confirmed need never grants ACT purchasing authority.
The 44 examples are synthetic and should not be generalized to households or real customers.
