#!/usr/bin/env python3
import argparse,json,sys
from pathlib import Path

def main():
    ap=argparse.ArgumentParser(); ap.add_argument("f"); a=ap.parse_args()
    p=Path(a.f); d=json.loads(p.read_text()); errs=[]
    if d.get("graph_manifest_digest")==d.get("graph_full_digest"): errs.append("graph")
    ids=set()
    for e in d.get("edges",[]):
        eid=e.get("edge_id")
        if eid in ids: errs.append("dup")
        ids.add(eid)
        if e.get("manifest_digest")==e.get("full_digest"): errs.append("edge")
    rv=d.get("replay_verification") or {}
    state=rv.get("replay_state")
    changed=rv.get("divergent_edges",[])
    if state=="manifest_diverges" and not changed: errs.append("need-edge")
    if state in {"bit_exact_replay","manifest_matches_latent_diverges"} and changed: errs.append("edge-list")
    if any(x not in ids for x in changed): errs.append("unknown")
    if d.get("implementability_assessment",{}).get("g_claimed_count")!=len(ids): errs.append("count")
    if errs:
        print(";".join(errs),file=sys.stderr); return 1
    print("OK",p); return 0
if __name__=="__main__": raise SystemExit(main())
