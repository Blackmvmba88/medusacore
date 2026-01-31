"""Optional cloud helpers for artifact upload (S3)."""

from __future__ import annotations
from pathlib import Path
from typing import Dict, Any


def upload_file_to_s3(
    path: str | Path, bucket: str, key: str, client
) -> Dict[str, Any]:
    """Upload a single file to S3 using provided boto3 client. Returns dict with s3 object info."""
    p = Path(path)
    with p.open("rb") as fh:
        client.put_object(Bucket=bucket, Key=key, Body=fh)
    url = f"s3://{bucket}/{key}"
    return {"bucket": bucket, "key": key, "url": url}


def upload_artifacts_to_s3(
    results: list, bucket: str, client, prefix: str = "forensics"
) -> list:
    """Upload raw+meta files referenced in results (each result has raw_path/meta_path).

    Returns the updated results list with added 's3_urls' entries for each artifact.
    """
    uploaded = []
    for meta in results:
        raw = Path(meta["raw_path"])
        metaf = Path(meta["meta_path"])
        key_raw = f"{prefix}/{raw.name}"
        key_meta = f"{prefix}/{metaf.name}"
        r1 = upload_file_to_s3(raw, bucket, key_raw, client)
        r2 = upload_file_to_s3(metaf, bucket, key_meta, client)
        meta_copy = dict(meta)
        meta_copy["s3_urls"] = {"raw": r1["url"], "meta": r2["url"]}
        uploaded.append(meta_copy)
    return uploaded
