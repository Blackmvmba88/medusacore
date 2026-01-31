import boto3
from moto import mock_s3
from hydras.forensics import persist_forensics_entries
from hydras.cloud import upload_artifacts_to_s3
from pathlib import Path


@mock_s3
def test_upload_artifacts_to_s3(tmp_path):
    # create a fake bucket
    client = boto3.client("s3", region_name="us-east-1")
    client.create_bucket(Bucket="test-bucket")
    # prepare files by using persist_forensics_entries
    entries = [
        {
            "name": "X",
            "_forensics_originals": {"a": "1"},
        }
    ]
    results = persist_forensics_entries(
        entries, branch="b", artifacts_dir=tmp_path, batch=True
    )
    assert len(results) == 1
    uploaded = upload_artifacts_to_s3(results, "test-bucket", client, prefix="t")
    assert len(uploaded) == 1
    assert "s3://test-bucket/t/" in uploaded[0]["s3_urls"]["raw"]
