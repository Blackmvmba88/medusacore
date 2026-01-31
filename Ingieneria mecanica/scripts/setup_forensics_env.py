#!/usr/bin/env python3
"""
Create or update the `forensics` Environment and add a Required Reviewers deployment protection rule
using a GitHub App (installation token). Intended to be run from GitHub Actions or locally (if env vars set).

Env expected:
- GITHUB_APP_ID (app id, as integer)
- GITHUB_APP_PRIVATE_KEY (PEM contents)
- GITHUB_REPOSITORY (owner/repo)
- REVIEWERS (comma-separated usernames)
- REQUIRED_APPROVING_REVIEW_COUNT (int)

This script:
- Creates a JWT for the App
- Finds the installation id for the repo
- Creates an installation access token
- Creates the environment if missing
- Adds/updates a `required_reviewers` deployment protection rule

Note: the App must be installed on the repo and have 'metadata' and 'deployments' permissions.
"""

import os
import sys
import time
import json
import logging
from typing import List

import jwt
import requests

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

GITHUB_API = "https://api.github.com"


def get_env_var(name: str, required: bool = True) -> str:
    v = os.environ.get(name)
    if required and not v:
        logging.error("Missing required env var: %s", name)
        sys.exit(2)
    return v or ""


def create_jwt(app_id: str, private_key_pem: str) -> str:
    # Create a JWT for GitHub App authentication
    now = int(time.time())
    payload = {
        "iat": now - 60,
        "exp": now + (9 * 60),  # 9 minutes expiry
        "iss": int(app_id),
    }
    token = jwt.encode(payload, private_key_pem, algorithm="RS256")
    return token


def api_request(method: str, url: str, token: str = None, headers=None, **kwargs):
    headers = headers or {}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    headers.setdefault("Accept", "application/vnd.github+json")
    resp = requests.request(method, url, headers=headers, **kwargs)
    if not resp.ok:
        logging.error("API %s %s failed: %s\n%s", method, url, resp.status_code, resp.text)
        resp.raise_for_status()
    return resp.json()


def get_installation_id(jwt_token: str, owner: str, repo: str) -> int:
    url = f"{GITHUB_API}/repos/{owner}/{repo}/installation"
    resp = requests.get(url, headers={"Authorization": f"Bearer {jwt_token}", "Accept": "application/vnd.github+json"})
    if resp.status_code == 404:
        logging.error("App is not installed on repo %s/%s. Install the App and grant permissions.", owner, repo)
        sys.exit(3)
    if not resp.ok:
        logging.error("Error finding installation for repo: %s", resp.text)
        resp.raise_for_status()
    data = resp.json()
    return data["id"]


def create_installation_token(jwt_token: str, installation_id: int) -> str:
    url = f"{GITHUB_API}/app/installations/{installation_id}/access_tokens"
    resp = requests.post(url, headers={"Authorization": f"Bearer {jwt_token}", "Accept": "application/vnd.github+json"})
    if not resp.ok:
        logging.error("Failed to create installation access token: %s", resp.text)
        resp.raise_for_status()
    return resp.json()["token"]


def ensure_environment(owner: str, repo: str, env_name: str, token: str):
    url = f"{GITHUB_API}/repos/{owner}/{repo}/environments/{env_name}"
    resp = requests.put(url, headers={"Authorization": f"token {token}", "Accept": "application/vnd.github+json"}, json={})
    if not resp.ok:
        logging.error("Failed to create/update environment: %s", resp.text)
        resp.raise_for_status()
    logging.info("Environment ensured: %s", env_name)
    return resp.json()


def add_required_reviewers_rule(owner: str, repo: str, env_name: str, token: str, reviewers: List[str], required_approving_review_count: int):
    # Build payload similar to: {type: required_reviewers, reviewers: [{type: 'User', reviewer:{login: '...'}}, ...], required_approving_review_count: n}
    reviewers_payload = [{"type": "User", "reviewer": {"login": r}} for r in reviewers]
    payload = {
        "type": "required_reviewers",
        "dismiss_stale_reviews": False,
        "reviewers": reviewers_payload,
        "required_approving_review_count": int(required_approving_review_count),
        "wait_timer": 0,
    }
    url = f"{GITHUB_API}/repos/{owner}/{repo}/environments/{env_name}/deployment_protection_rules"
    resp = requests.post(url, headers={"Authorization": f"token {token}", "Accept": "application/vnd.github+json"}, json=payload)
    if resp.status_code == 422:
        # may happen if rule exists or app permissions missing. Log and raise.
        logging.error("Failed to create protection rule (422). Response: %s", resp.text)
        resp.raise_for_status()
    if not resp.ok:
        logging.error("Failed to create protection rule: %s", resp.text)
        resp.raise_for_status()
    logging.info("Protection rule created/updated for environment %s", env_name)
    return resp.json()


def main():
    app_id = get_env_var("GITHUB_APP_ID")
    private_key = get_env_var("GITHUB_APP_PRIVATE_KEY")
    repository = get_env_var("GITHUB_REPOSITORY")
    reviewers_raw = os.environ.get("REVIEWERS", "")
    required_count = os.environ.get("REQUIRED_APPROVING_REVIEW_COUNT", "1")

    owner, repo = repository.split("/")
    env_name = "forensics"

    reviewers = [r.strip() for r in reviewers_raw.split(",") if r.strip()]
    if not reviewers:
        logging.error("No reviewers specified (env REVIEWERS). Aborting.")
        sys.exit(4)

    logging.info("Creating JWT for app id %s", app_id)
    jwt_token = create_jwt(app_id, private_key)

    logging.info("Retrieving installation id for %s/%s", owner, repo)
    installation_id = get_installation_id(jwt_token, owner, repo)
    logging.info("Found installation id: %s", installation_id)

    logging.info("Creating installation access token")
    inst_token = create_installation_token(jwt_token, installation_id)

    logging.info("Ensuring environment exists: %s", env_name)
    ensure_environment(owner, repo, env_name, inst_token)

    logging.info("Adding required reviewers: %s", reviewers)
    add_required_reviewers_rule(owner, repo, env_name, inst_token, reviewers, required_count)

    logging.info("Done. Environment '%s' configured with required reviewers.", env_name)


if __name__ == "__main__":
    main()
