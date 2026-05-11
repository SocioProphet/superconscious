#!/usr/bin/env python3
"""Resolve and write the M1 source-lock manifest.

This script records the public model / SAE artifacts used by the
Implementability Steering Pilot. It intentionally does not download full model
weights or SAE parameter files. It resolves Hugging Face repository metadata,
checks that the selected SAE path is present, and writes a JSON manifest that
subsequent M1 scripts can require.
"""

from __future__ import annotations

import argparse
import dataclasses
import datetime as dt
import json
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any

HF_API_ROOT = "https://huggingface.co/api/models"


@dataclasses.dataclass(frozen=True)
class SourceLockConfig:
    model_repo: str = "google/gemma-2-9b-it"
    sae_repo: str = "google/gemma-scope-9b-it-res"
    model_revision: str = "main"
    sae_revision: str = "main"
    layer: int = 20
    width: str = "131k"
    average_l0: str = "81"
    dtype: str = "bfloat16"
    position_classes: tuple[str, ...] = (
        "end_of_prompt",
        "beginning_of_completion",
        "mid_completion",
    )

    @property
    def sae_path(self) -> str:
        return f"layer_{self.layer}/width_{self.width}/average_l0_{self.average_l0}/params.npz"


def fetch_model_metadata(repo_id: str, revision: str) -> dict[str, Any]:
    encoded_repo = urllib.parse.quote(repo_id, safe="")
    encoded_revision = urllib.parse.quote(revision, safe="")
    url = f"{HF_API_ROOT}/{encoded_repo}/revision/{encoded_revision}"
    request = urllib.request.Request(
        url,
        headers={
            "Accept": "application/json",
            "User-Agent": "superconscious-m1-source-lock/0.1",
        },
    )
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"Hugging Face API error for {repo_id}@{revision}: {exc.code} {body}") from exc
    except urllib.error.URLError as exc:
        raise RuntimeError(f"Unable to reach Hugging Face API for {repo_id}@{revision}: {exc}") from exc


def sibling_paths(metadata: dict[str, Any]) -> set[str]:
    siblings = metadata.get("siblings", [])
    paths: set[str] = set()
    for item in siblings:
        if isinstance(item, dict) and isinstance(item.get("rfilename"), str):
            paths.add(item["rfilename"])
    return paths


def slim_metadata(metadata: dict[str, Any], *, selected_paths: set[str] | None = None) -> dict[str, Any]:
    siblings = metadata.get("siblings", [])
    selected: list[dict[str, Any]] = []
    if selected_paths is not None:
        for item in siblings:
            if isinstance(item, dict) and item.get("rfilename") in selected_paths:
                selected.append(item)

    return {
        "id": metadata.get("id"),
        "sha": metadata.get("sha"),
        "lastModified": metadata.get("lastModified"),
        "private": metadata.get("private"),
        "gated": metadata.get("gated"),
        "disabled": metadata.get("disabled"),
        "downloads": metadata.get("downloads"),
        "likes": metadata.get("likes"),
        "library_name": metadata.get("library_name"),
        "tags": metadata.get("tags", []),
        "cardData": metadata.get("cardData", {}),
        "selected_siblings": selected,
    }


def build_manifest(config: SourceLockConfig) -> dict[str, Any]:
    model_meta = fetch_model_metadata(config.model_repo, config.model_revision)
    sae_meta = fetch_model_metadata(config.sae_repo, config.sae_revision)

    paths = sibling_paths(sae_meta)
    if config.sae_path not in paths:
        similar = sorted(p for p in paths if f"layer_{config.layer}/width_{config.width}/" in p)[:20]
        raise RuntimeError(
            "Selected SAE path not found: "
            f"{config.sae_path}\nAvailable similar paths: {json.dumps(similar, indent=2)}"
        )

    now = dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat()
    return {
        "schema_version": "m1-source-lock.v0.1",
        "created_at_utc": now,
        "pilot": "implementability-steering-pilot",
        "stage": "M1-source-lock",
        "model": {
            "repo": config.model_repo,
            "requested_revision": config.model_revision,
            "resolved_sha": model_meta.get("sha"),
            "dtype": config.dtype,
            "metadata": slim_metadata(model_meta),
        },
        "tokenizer": {
            "source_repo": config.model_repo,
            "requested_revision": config.model_revision,
            "resolved_sha": model_meta.get("sha"),
            "chat_template_policy": "use tokenizer chat template from resolved model revision; record any override separately",
        },
        "sae": {
            "repo": config.sae_repo,
            "requested_revision": config.sae_revision,
            "resolved_sha": sae_meta.get("sha"),
            "family": "Gemma Scope residual-stream SAE",
            "layer": config.layer,
            "width": config.width,
            "average_l0": config.average_l0,
            "path": config.sae_path,
            "metadata": slim_metadata(sae_meta, selected_paths={config.sae_path}),
        },
        "experiment_defaults": {
            "position_classes": list(config.position_classes),
            "intervention_site": "assistant-turn token positions for behavioral sweep; position-conditioned activations for implementability phase",
            "metrics_for_m2_m3": ["layernorm_euclidean", "cosine", "readout_weighted"],
            "natural_distribution": {
                "pretraining_style_text": 0.50,
                "instruction_chat_format": 0.30,
                "task_near_no_pressure_prompts": 0.20,
            },
        },
        "m1_non_goals": [
            "no full model download by this script",
            "no SAE parameter download by this script",
            "no implementability distance claims at M1",
            "no proprietary Anthropic dependency",
        ],
    }


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--model-repo", default=SourceLockConfig.model_repo)
    parser.add_argument("--sae-repo", default=SourceLockConfig.sae_repo)
    parser.add_argument("--model-revision", default=SourceLockConfig.model_revision)
    parser.add_argument("--sae-revision", default=SourceLockConfig.sae_revision)
    parser.add_argument("--layer", type=int, default=SourceLockConfig.layer)
    parser.add_argument("--width", default=SourceLockConfig.width)
    parser.add_argument("--average-l0", default=SourceLockConfig.average_l0)
    parser.add_argument("--dtype", default=SourceLockConfig.dtype)
    parser.add_argument("--write", type=Path, default=Path("outputs/m1/source-lock.json"))
    parser.add_argument("--print", action="store_true", help="Also print the manifest to stdout.")
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    config = SourceLockConfig(
        model_repo=args.model_repo,
        sae_repo=args.sae_repo,
        model_revision=args.model_revision,
        sae_revision=args.sae_revision,
        layer=args.layer,
        width=args.width,
        average_l0=args.average_l0,
        dtype=args.dtype,
    )

    manifest = build_manifest(config)
    args.write.parent.mkdir(parents=True, exist_ok=True)
    args.write.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if args.print:
        print(json.dumps(manifest, indent=2, sort_keys=True))
    else:
        print(args.write)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
