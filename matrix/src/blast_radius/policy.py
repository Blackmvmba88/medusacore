"""Policy loader and defaults for ethics engine."""
from typing import Dict, Any
import hashlib
import json
import os

DEFAULT_POLICY = {
    "block_threshold": 0.85,
    "review_threshold": 0.6,
    "review_count": 1,
    "penalty_scale": 1.0,
}


def load_policy(path: str = "policies/ethics_policy.yaml") -> Dict[str, Any]:
    """Load a simple YAML or JSON policy file and return (policy, policy_hash).

    Falls back to DEFAULT_POLICY when file not found or parsing fails.
    """
    try:
        import yaml
    except Exception:
        yaml = None

    if not os.path.exists(path):
        return DEFAULT_POLICY.copy(), None

    raw = open(path, "rb").read()
    policy_hash = hashlib.sha256(raw).hexdigest()

    try:
        text = raw.decode()
        if yaml:
            policy = yaml.safe_load(text)
        else:
            # Try JSON fallback
            policy = json.loads(text)
    except Exception:
        return DEFAULT_POLICY.copy(), policy_hash

    if not isinstance(policy, dict):
        return DEFAULT_POLICY.copy(), policy_hash

    # Fill defaults
    merged = DEFAULT_POLICY.copy()
    merged.update(policy)
    return merged, policy_hash