import os
import sys
import json
import types
from unittest import mock

import pytest

import scripts.setup_forensics_env as sfe


def test_verify_required_reviewers_success(monkeypatch):
    owner = "org"
    repo = "repo"
    env = "forensics"
    token = "token"
    reviewers = ["alice", "bob"]
    required_count = 1

    fake_rule = [
        {
            "type": "required_reviewers",
            "reviewers": [
                {"reviewer": {"login": "alice"}},
                {"reviewer": {"login": "bob"}},
            ],
            "required_approving_review_count": 1,
        }
    ]

    class Resp:
        ok = True

        def json(self):
            return fake_rule

    monkeypatch.setattr(sfe.requests, "get", lambda url, headers=None: Resp())

    assert (
        sfe.verify_required_reviewers(
            owner, repo, env, token, reviewers, required_count
        )
        is True
    )


def test_verify_required_reviewers_missing_reviewer(monkeypatch):
    owner = "org"
    repo = "repo"
    env = "forensics"
    token = "token"
    reviewers = ["alice", "bob", "carol"]
    required_count = 1

    fake_rule = [
        {
            "type": "required_reviewers",
            "reviewers": [
                {"reviewer": {"login": "alice"}},
                {"reviewer": {"login": "bob"}},
            ],
            "required_approving_review_count": 1,
        }
    ]

    class Resp:
        ok = True

        def json(self):
            return fake_rule

    monkeypatch.setattr(sfe.requests, "get", lambda url, headers=None: Resp())

    assert (
        sfe.verify_required_reviewers(
            owner, repo, env, token, reviewers, required_count
        )
        is False
    )


def test_dry_run_exits_without_api_calls(monkeypatch, capsys):
    # Ensure no requests are made
    def fail_request(*args, **kwargs):
        raise RuntimeError("requests should not be called in dry run")

    monkeypatch.setattr(
        sfe.requests,
        "get",
        lambda *a, **k: (_ for _ in ()).throw(RuntimeError("requests called")),
    )
    monkeypatch.setattr(
        sfe.requests,
        "post",
        lambda *a, **k: (_ for _ in ()).throw(RuntimeError("requests called")),
    )

    os.environ["GITHUB_APP_ID"] = "123"
    os.environ["GITHUB_APP_PRIVATE_KEY"] = (
        "-----BEGIN PRIVATE KEY-----\nMIIB...\n-----END PRIVATE KEY-----"
    )
    os.environ["GITHUB_REPOSITORY"] = "org/repo"
    os.environ["REVIEWERS"] = "alice,bob"
    os.environ["REQUIRED_APPROVING_REVIEW_COUNT"] = "1"

    # Run main with --dry-run
    test_args = ["setup_forensics_env.py", "--dry-run"]
    monkeypatch.setattr(sys, "argv", test_args)

    with pytest.raises(SystemExit) as exc:
        sfe.main()
    assert exc.value.code == 0


def test_add_required_reviewers_rule_payload(monkeypatch):
    owner = "org"
    repo = "repo"
    env = "forensics"
    token = "token"
    reviewers = ["alice", "bob"]
    required_count = 2

    captured = {}

    class Resp:
        ok = True

        def json(self):
            return {"id": 1}

    def fake_post(url, headers=None, json=None):
        captured["url"] = url
        captured["headers"] = headers
        captured["json"] = json
        return Resp()

    monkeypatch.setattr(sfe.requests, "post", fake_post)

    resp = sfe.add_required_reviewers_rule(
        owner, repo, env, token, reviewers, required_count
    )
    assert captured["url"].endswith(
        f"/repos/{owner}/{repo}/environments/{env}/deployment_protection_rules"
    )
    assert captured["json"]["type"] == "required_reviewers"
    assert captured["json"]["required_approving_review_count"] == required_count
    names = [r["reviewer"]["login"] for r in captured["json"]["reviewers"]]
    assert names == reviewers
