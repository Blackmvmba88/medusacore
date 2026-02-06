# Forensics Capture & Retention Policy

This document describes how forensics artifacts are captured, stored and audited by the project.

## Overview
- Parser detects suspicious content and can optionally redact and collect originals (`_forensics_originals`).
- Use `tools/ingest_and_persist.py` to ingest markdown corpus and persist forensic artifacts.
- Artifacts are stored in `tests/adversarial_artifacts/` by default and contain:
  - `<artifact>.json` (raw payload)
  - `<artifact>.meta.json` (metadata: id, timestamp, branch, sha256, optionally retention/approval)

## Retention & Approval
- The CLI supports `--retention-days` and `--approved-by`. These values are embedded in artifact payloads for audit.
- CI integrates a `persist-forensics` job that runs in the GitHub Environment `forensics` which requires a human approval to run. This ensures manual review before PII is stored.

## Uploading to Cloud
- CLI supports `--s3-bucket` (S3) and `--gcs-bucket` (GCS). If provided, artifacts are uploaded after persistence.
- S3 uploads use the `hydras.cloud.upload_artifacts_to_s3` helper. GCS uploads use `hydras.gcs.upload_artifacts_to_gcs`.

## How to use
- Local dry-run: `python tools/ingest_and_persist.py --src tests/adversarial_corpus --branch feature/x --out /tmp/artifacts --batch`
- Upload to S3: `python tools/ingest_and_persist.py --src ... --branch ... --s3-bucket my-bucket --retention-days 90 --approved-by alice@example.com`

## Audit & Access
- Uploaded artifacts include `approved_by` and `retention_days` in metadata.
- Consider adding lifecycle/expiry policies on the object store to enforce retention.
