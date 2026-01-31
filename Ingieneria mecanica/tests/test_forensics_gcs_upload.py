from unittest.mock import MagicMock
from hydras.forensics import persist_forensics_entries
from hydras.gcs import upload_artifacts_to_gcs
from pathlib import Path


def test_upload_artifacts_to_gcs(tmp_path, monkeypatch):
    # create fake file via persist_forensics_entries
    entries = [{"name": "X", "_forensics_originals": {"a": "1"}}]
    results = persist_forensics_entries(entries, branch="b", artifacts_dir=tmp_path, batch=True)
    assert len(results) == 1
    # mock client
    mock_client = MagicMock()
    mock_bucket = MagicMock()
    mock_client.bucket.return_value = mock_bucket
    mock_blob = MagicMock()
    mock_bucket.blob.return_value = mock_blob
    uploaded = upload_artifacts_to_gcs(results, "test-bucket", mock_client, prefix="t")
    assert len(uploaded) == 1
    assert uploaded[0]["gcs_urls"]["raw"].startswith("gs://test-bucket/t/")
