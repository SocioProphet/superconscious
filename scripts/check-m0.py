#!/usr/bin/env python3
import argparse,json,sys
from datetime import datetime
from pathlib import Path
KEYS=("dataset","code","config","seed","base_model","checkpoint","eval_spec","compute_environment")
def t(x): return datetime.fromisoformat(x.replace("Z","+00:00"))
def band(x):
    if abs(x-1.0)<1e-9: return "fully_provenance_certified"
    if 0.625<=x<=0.875: return "partial_provenance"
    if 0.25<=x<=0.5: return "minimal_provenance"
    if 0.0<=x<=0.125: return "no_provenance_external_artifact"
    return "out_of_band"
def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("f")
    args=ap.parse_args()
    p=Path(args.f)
    d=json.loads(p.read_text())
    c=d.get("commitments",{})
    errs=[]
    if any(k not in c for k in KEYS): errs.append("missing key")
    idx=sum(1 for k in KEYS if c.get(k,{}).get("status")=="available")/8
    pc=d.get("provenance_completeness",{})
    if abs(float(pc.get("index",-1))-idx)>1e-9: errs.append("index")
    if pc.get("interpretation")!=band(idx): errs.append("band")
    tc=d.get("temporal_constraints",{})
    a,b,flag=tc.get("model_commitment_at"),tc.get("eval_spec_commitment_at"),tc.get("model_precedes_eval_spec")
    if a and b and flag is not (t(a)<t(b)): errs.append("time")
    if (not a or not b) and flag is not False: errs.append("nulltime")
    if errs:
        print(";".join(errs),file=sys.stderr); return 1
    print("OK",p); return 0
if __name__=="__main__": raise SystemExit(main())
