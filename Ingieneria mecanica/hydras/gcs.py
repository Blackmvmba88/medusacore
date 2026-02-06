"""GCS helpers for artifact upload (optional)."""
from __future__ import annotations
from typing import Dict, Any
from pathlib import Path


def upload_file_to_gcs(path: str | Path, bucket: str, key: str, client) -> Dict[str, Any]:
    p = Path(path)
    bucket_obj = client.bucket(bucket)
    blob = bucket_obj.blob(key)
    blob.upload_from_filename(str(p))
    url = f"gs://{bucket}/{key}"
    return {"bucket": bucket, "key": key, "url": url}


def upload_artifacts_to_gcs(results: list, bucket: str, client, prefix: str = "forensics") -> list:
    uploaded = []
    for meta in results:
        raw = Path(meta["raw_path"])
        metaf = Path(meta["meta_path"])
        key_raw = f"{prefix}/{raw.name}"
        key_meta = f"{prefix}/{metaf.name}"
        r1 = upload_file_to_gcs(raw, bucket, key_raw, client)
        r2 = upload_file_to_gcs(metaf, bucket, key_meta, client)
        meta_copy = dict(meta)
        meta_copy["gcs_urls"] = {"raw": r1["url"], "meta": r2["url"]}
        uploaded.append(meta_copy)
    return uploaded
