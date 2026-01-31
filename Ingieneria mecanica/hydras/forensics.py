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
    entries: list, branch: str, artifacts_dir: str | Path | None = None
) -> list:
    """Persist each entry's `_forensics_originals` via ForensicsHydra.capture.

    For each entry in `entries` that contains `_forensics_originals`, this helper
    creates a ForensicsHydra (with `artifacts_dir` if given) and captures a
    JSON artifact with context. Returns a list of metadata dicts from captures.
    """
    results = []
    hydra = (
        ForensicsHydra(artifacts_dir) if artifacts_dir is not None else ForensicsHydra()
    )
    for entry in entries:
        originals = entry.get("_forensics_originals")
        if not originals:
            continue
        payload = {
            "entry_name": entry.get("name"),
            "originals": originals,
            "parser": "medusa.learners",
        }
        meta = hydra.capture(branch=branch, logs=payload)
        results.append(meta)
    return results
