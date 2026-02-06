"""Forensics Hydra: captures evidence, saves artifacts and metadata for reproducibility."""

from __future__ import annotations
import json
import hashlib
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Any
import uuid


class ForensicsHydra:
    def __init__(
        self,
        name: str = "forensics",
        artifacts_dir: str | Path = "tests/adversarial_artifacts",
    ):
        self.name = name
        self.artifacts_dir = Path(artifacts_dir)
        self.artifacts_dir.mkdir(parents=True, exist_ok=True)

    def _sha256_of_bytes(self, b: bytes) -> str:
        h = hashlib.sha256()
        h.update(b)
        return h.hexdigest()

    def capture(self, branch: str, logs: Dict[str, Any]) -> Dict[str, Any]:
        """Persist logs/artifacts and return metadata.

        Writes the logs JSON to a file and stores a metadata JSON with sha256, timestamp and id.
        """
        tid = str(uuid.uuid4())
        ts = datetime.now(timezone.utc).isoformat()
        # Prepare raw bytes and sha
        raw_json = json.dumps(logs, ensure_ascii=False, indent=2).encode("utf-8")
        sha = self._sha256_of_bytes(raw_json)
        base_name = f"artifact_{ts.replace(':', '_')}_{tid}"
        raw_path = self.artifacts_dir / (base_name + ".json")
        meta_path = self.artifacts_dir / (base_name + ".meta.json")
        # write raw logs
        raw_path.write_bytes(raw_json)
        # metadata
        meta = {
            "id": tid,
            "timestamp": ts,
            "branch": branch,
            "sha256": sha,
            "raw_path": str(raw_path),
        }
        meta_path.write_text(
            json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8"
        )
        return {
            "hydra": self.name,
            "id": tid,
            "timestamp": ts,
            "sha256": sha,
            "raw_path": str(raw_path),
            "meta_path": str(meta_path),
        }


def persist_forensics_entries(
    entries: list,
    branch: str,
    artifacts_dir: str | Path | None = None,
    batch: bool = True,
    retention_days: int | None = None,
    approved_by: str | None = None,
) -> list:
    """Persist forensics originals via ForensicsHydra.capture.

    If `batch` is True, combine all `_forensics_originals` into a single
    artifact (reduces artifact count). If False, persist one artifact per
    entry containing `_forensics_originals`.

    `retention_days` and `approved_by` are included in the captured metadata
    to provide retention policy and approval audit information.

    Returns a list of metadata dicts from captures.
    """
    results = []
    hydra = (
        ForensicsHydra(artifacts_dir) if artifacts_dir is not None else ForensicsHydra()
    )

    meta_extra = {}
    if retention_days is not None:
        meta_extra["retention_days"] = int(retention_days)
    if approved_by:
        meta_extra["approved_by"] = approved_by

    if batch:
        combined = []
        for entry in entries:
            originals = entry.get("_forensics_originals")
            if originals:
                combined.append({"name": entry.get("name"), "originals": originals})
        if combined:
            payload = {
                "batch": True,
                "items": combined,
                "parser": "medusa.learners",
                "meta": meta_extra,
            }
            meta = hydra.capture(branch=branch, logs=payload)
            results.append(meta)
        return results

    # non-batch: persist per-entry
    for entry in entries:
        originals = entry.get("_forensics_originals")
        if not originals:
            continue
        payload = {
            "entry_name": entry.get("name"),
            "originals": originals,
            "parser": "medusa.learners",
            "meta": meta_extra,
        }
        meta = hydra.capture(branch=branch, logs=payload)
        results.append(meta)
    return results
