#!/usr/bin/env python3
import argparse,json,sys
from pathlib import Path


def load(path):
    return json.loads(Path(path).read_text())


def check_microbeat(doc):
    errs=[]
    actor_class=(doc.get("actor") or {}).get("actor_class")
    authority=doc.get("authority_layer")
    stele_state=(doc.get("stele_ref") or {}).get("stele_promotion_state")
    if actor_class in {"H","X"} and authority=="institutional_truth" and stele_state=="promoted_stele":
        if doc.get("consent_receipt_ref") is None:
            errs.append("missing consent receipt for human-or-hybrid institutional promotion")
        if doc.get("operator_visible_summary") is None:
            errs.append("missing operator visible summary for human-or-hybrid event")
    return errs


def check_cascade(doc):
    errs=[]
    authority=(doc.get("cascade_authority") or {}).get("authority_layer")
    affected=doc.get("affected_fragments",[])
    if any(f.get("previous_promotion_state")=="promoted_stele" for f in affected):
        if authority!="institutional_truth":
            errs.append("promoted fragments require institutional cascade authority")
    return errs


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("kind", choices=["microbeat","cascade"])
    ap.add_argument("file")
    a=ap.parse_args()
    doc=load(a.file)
    errs=check_microbeat(doc) if a.kind=="microbeat" else check_cascade(doc)
    if errs:
        print(";".join(errs), file=sys.stderr)
        return 1
    print("OK", a.file)
    return 0

if __name__=="__main__": raise SystemExit(main())
