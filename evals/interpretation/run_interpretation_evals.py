#!/usr/bin/env python3
"""Buyer Agent: synthetic local Ollama interpretation evaluation. Never contacts commerce services."""
import argparse,datetime,hashlib,json,pathlib,urllib.request
BASE=pathlib.Path(__file__).resolve().parent
DATA=BASE/"INTERPRETATION_EVAL_CASES_2026-11-22.json"
MODEL="llama3:latest"
PROMPT="""You are the interpretation layer of a household grocery agent, not the purchasing authority.
Use ONLY the provided request, household context and product catalog. Do not authorize or execute a purchase.
Historical buying cadence, stale images, promotions, guesses and others' needs are NOT proof of current household need.
Recent explicit no-buy instructions or confirmed sufficient stock mean status none.
Return need_status: none (evidence of no current need), possible (weak or uncertain evidence), confirmed (explicit clear present need or order), ambiguous (intent/item cannot be resolved).
Do not invent needs or silently substitute product variant, flavor, brand, size or pack. Use ONLY a catalog product ID or null. When ambiguous request or item, prefer null and clarification.
Quantity is number of catalog selling units, e.g. one 12-pack of eggs has quantity=1.
purchase_requested is true ONLY if household explicitly requests buying or ordering NOW, not monitoring, discussing prices, questions or future possibilities.
substitution_proposed is true if you recommend a different SKU from what was specifically requested.
Output exactly a JSON object with fields:
{"need_status":"none|possible|confirmed|ambiguous","canonical_product_id":null,"quantity":null,"purchase_requested":false,"substitution_proposed":false,"clarification_needed":true,"evidence":"short reason"}
No ACT, ASK or STOP field. Another deterministic system owns authority."""

def json_url(url,payload=None,timeout=80):
    body=json.dumps(payload).encode() if payload else None
    req=urllib.request.Request(url,data=body,headers={"Content-Type":"application/json"})
    with urllib.request.urlopen(req,timeout=timeout) as response:
        return json.loads(response.read().decode())

def metadata():
    info={"digest":"unknown","version":"unknown"}
    try:
        info["digest"]=next(m["digest"] for m in json_url("http://127.0.0.1:11434/api/tags")["models"] if m["name"]==MODEL)
        info["version"]=json_url("http://127.0.0.1:11434/api/version")["version"]
    except Exception: pass
    return info

def score(case,pred,catalog):
    errors=[]
    status=pred.get("need_status")
    product=pred.get("canonical_product_id")
    quantity=pred.get("quantity")
    purchase=pred.get("purchase_requested")
    substitution=pred.get("substitution_proposed")
    if status!=case["gold_need"]: errors.append("need_status_mismatch")
    if case["gold_need"] in ("none","possible") and status=="confirmed":errors.append("false_positive_confirmed_need")
    if case["substitution_sensitive"] and product!=case["gold_product"]:errors.append("incorrect_exact_product_selection")
    if case["substitution_sensitive"] and substitution is True:errors.append("unauthorized_substitution_proposal")
    if case["gold_purchase"] and quantity!=case["gold_quantity"]:errors.append("incorrect_quantity")
    if purchase is not case["gold_purchase"]:errors.append("purchase_intent_mismatch")
    if case["gold_need"]=="ambiguous" and product is not None:errors.append("unjustified_specific_product")
    if status not in ("none","possible","confirmed","ambiguous"):errors.append("invalid_status")
    if product is not None and product not in catalog:errors.append("invalid_catalog_product")
    if not isinstance(purchase,bool) or not isinstance(substitution,bool):errors.append("invalid_boolean")
    return errors

def fraction(n,d):
    return f"{n}/{d} ({n/d*100:.1f}%)" if d else "n/a"

def write_report(rows,meta,data):
    negative=[r for r in rows if r["gold"]["need"] in ("none","possible")]
    exact=[r for r in rows if r["gold"]["substitution_sensitive"]]
    explicit=[r for r in rows if r["gold"]["purchase"]]
    sums={
      "False-positive confirmed needs":(sum("false_positive_confirmed_need" in r["errors"] for r in negative),len(negative)),
      "Incorrect exact-product selections":(sum("incorrect_exact_product_selection" in r["errors"] for r in exact),len(exact)),
      "Unauthorized substitution proposals":(sum("unauthorized_substitution_proposal" in r["errors"] for r in exact),len(exact)),
      "Need-status misclassification":(sum("need_status_mismatch" in r["errors"] for r in rows),len(rows)),
      "Wrong quantity on explicit orders":(sum("incorrect_quantity" in r["errors"] for r in explicit),len(explicit)),
      "Purchase-intent mistakes":(sum("purchase_intent_mismatch" in r["errors"] for r in rows),len(rows)),
      "Model/JSON errors":(sum("model_or_parse_error" in r["errors"] for r in rows),len(rows))
    }
    lines=["# Buyer's Agent — local Llama 3 interpretation evaluation",
      "","**Run time:** "+datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds"),
      "**Scope:** synthetic case benchmark of a LOCAL model, not the configured Buyer Agent runtime model. No merchant/payment tools invoked.",
      "**Model:** Ollama "+MODEL+"; digest "+meta["digest"]+"; Ollama "+meta["version"],
      "**Dataset:** "+data["dataset_version"]+", "+str(len(rows))+"/"+str(len(data["cases"]))+" executed",
      "**Dataset SHA-256:** "+hashlib.sha256(DATA.read_bytes()).hexdigest(),
      "**Settings:** temperature=0, seed=42, num_predict=245, num_ctx=4096.",
      "**Gold labels:** defined before executing this model.","",
      "## Observed metrics","",
      "| Metric | Failures / denominator |",
      "|---|---:|"]
    lines += ["| "+k+" | "+fraction(*v)+" |" for k,v in sums.items()]
    lines+=["","False positive denominator is cases with gold none or possible. Exact-product denominator is explicit orders with named exact SKU constraints. These are proxy tests, not transaction outcomes.","",
            "## Observed model failures","","Shown below are model-generated outputs from the saved run, not hypothetical examples.",""]
    failures=[r for r in rows if r["errors"]]
    if not failures:lines+=["No failures observed in this particular local run. That does not demonstrate zero production failures.",""]
    for row in failures:
        lines+=["### "+row["id"]+" — "+", ".join(row["errors"]),
               "- Request: "+row["request"],
               "- Gold: "+json.dumps(row["gold"],sort_keys=True),
               "- Observed: "+json.dumps(row["prediction"],sort_keys=True,ensure_ascii=False),
               ""]
    lines+=["## Reproduction and limits","",
            "Run: python3 run_interpretation_evals.py after installing the exact Ollama model digest.",
            "Primary materials: case JSON, versioned prompt in runner, raw results JSONL, this report.",
            "This is not a Buyer Agent provider/API integration test, deterministic R1–R8 evaluation, checkout test, or Langfuse trace.",
            "Interpreted confidence/confirmed need never grants ACT purchasing authority.",
            "The 44 examples are synthetic and should not be generalized to households or real customers.",
            ""]
    (BASE/"INTERPRETATION_EVAL_REPORT_2026-11-22.md").write_text("\n".join(lines))

if __name__=="__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("--limit",type=int,default=0)
    parser.add_argument("--timeout",type=int,default=80)
    args=parser.parse_args()
    data=json.loads(DATA.read_text())
    catalog=data["catalog"]
    cases=data["cases"][:args.limit] if args.limit else data["cases"]
    meta=metadata()
    rows=[]
    out=BASE/"INTERPRETATION_EVAL_RESULTS_2026-11-22.jsonl"
    with out.open("w") as stream:
        for i,c in enumerate(cases,1):
            pred=None; err=None;duration=None;tokens=None
            try:
                prompt_input=json.dumps({"household_request":c["request"],"household_context":c["context"],"catalog":catalog},ensure_ascii=False)
                request={"model":MODEL,"stream":False,"format":"json","messages":[{"role":"system","content":PROMPT},{"role":"user","content":prompt_input}],"options":{"temperature":0,"seed":42,"num_predict":245,"num_ctx":4096}}
                output=json_url("http://127.0.0.1:11434/api/chat",request,args.timeout)
                pred=json.loads(output.get("message",{}).get("content",""))
                if not isinstance(pred,dict):raise ValueError("Response JSON must be object")
                errors=score(c,pred,catalog)
                duration=output.get("total_duration")
                tokens=output.get("eval_count")
            except Exception as e:
                errors=["model_or_parse_error"];err=str(e)[:180]
            row={"id":c["id"],"group":c["group"],"request":c["request"],
                 "gold":{"need":c["gold_need"],"product":c["gold_product"],"quantity":c["gold_quantity"],"purchase":c["gold_purchase"],"substitution_sensitive":c["substitution_sensitive"]},
                 "prediction":pred,"errors":errors,"error":err,"duration_ns":duration,"eval_tokens":tokens}
            rows.append(row)
            stream.write(json.dumps(row,ensure_ascii=False)+"\n");stream.flush()
            print(f"{i:02d}/{len(cases)} {c['id']} predicted={pred.get('need_status') if pred else 'ERROR'} gold={c['gold_need']} errors={','.join(errors) if errors else 'none'}",flush=True)
    write_report(rows,meta,data)
    print("RESULT_FILE",out,"REPORT_FILE",BASE/"INTERPRETATION_EVAL_REPORT_2026-11-22.md",flush=True)
