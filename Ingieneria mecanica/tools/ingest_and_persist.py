"""Ingest markdown files from a directory and persist forensics artifacts.

Usage: python tools/ingest_and_persist.py --src tests/adversarial_corpus --branch mybranch --out tests/adversarial_artifacts --batch
"""

from __future__ import annotations
import argparse
from pathlib import Path
import json
from medusa.learners import parse_ingenierias_markdown
from hydras.forensics import persist_forensics_entries


def main():
    p = argparse.ArgumentParser(
        description="Ingest markdown files and persist forensics"
    )
    p.add_argument(
        "--src", required=True, help="Directory with .md files (or a single file)"
    )
    p.add_argument("--branch", required=True, help="Branch name/context")
    p.add_argument("--out", default=None, help="Artifacts output dir (optional)")
    p.add_argument(
        "--batch", action="store_true", help="Batch entries into a single artifact"
    )
    p.add_argument(
        "--s3-bucket", default=None, help="Optional S3 bucket to upload artifacts"
    )
    p.add_argument(
        "--retention-days",
        type=int,
        default=None,
        help="Retention days to include in metadata",
    )
    p.add_argument(
        "--approved-by", default=None, help="Approval identity to include in metadata"
    )
    args = p.parse_args()

    src = Path(args.src)
    files = []
    if src.is_file():
        files = [src]
    else:
        files = sorted(src.glob("**/*.md"))
    all_entries = []
    for f in files:
        txt = f.read_text(encoding="utf-8")
        parsed = parse_ingenierias_markdown(txt, redact=False, collect_forensics=True)
        # attach source
        for ent in parsed:
            ent["_source_file"] = str(f)
        all_entries.extend(parsed)

    results = persist_forensics_entries(
        all_entries,
        branch=args.branch,
        artifacts_dir=args.out,
        batch=args.batch,
        retention_days=args.retention_days,
        approved_by=args.approved_by,
    )
    print(f"Persisted {len(results)} artifacts")

    # optional upload to S3
    if args.s3_bucket:
        import os
        import boto3
        from hydras.cloud import upload_artifacts_to_s3

        endpoint = os.environ.get("AWS_S3_ENDPOINT")
        client = boto3.client("s3", endpoint_url=endpoint) if endpoint else boto3.client("s3")
        uploaded = upload_artifacts_to_s3(results, args.s3_bucket, client)
        print("Uploaded to S3:")
        for u in uploaded:
            print(json.dumps(u, ensure_ascii=False))

    # optional upload to GCS
    if args.gcs_bucket:
        from google.cloud import storage
        from hydras.gcs import upload_artifacts_to_gcs

        client = storage.Client()
        uploaded = upload_artifacts_to_gcs(results, args.gcs_bucket, client)
        print("Uploaded to GCS:")
        for u in uploaded:
            print(json.dumps(u, ensure_ascii=False))

    if not args.s3_bucket and not args.gcs_bucket:
        for r in results:
            print(json.dumps(r, ensure_ascii=False))


if __name__ == "__main__":
    main()
