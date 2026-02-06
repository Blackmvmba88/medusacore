#!/usr/bin/env python3
"""Safe runner to perform a genesis dry-run (no git side-effects).

Usage:
    python scripts/genesis_run.py
"""

from core.genesis import run_genesis_dry_run, HermeticCore


def main():
    # Dry run: show first breath and initial principles
    out = run_genesis_dry_run()
    print("--- FIRST BREATH ---")
    print(out["first_breath"])
    print("--- INITIAL PRINCIPLES ---")
    for p in out["initial_principles"]:
        print("-", p)

    # Example mutation simulation
    core = HermeticCore()
    mutation = core.evolve_principle(
        principle_name="recursion",
        new_variant="recursion_ext: support meta-observation over ML updates",
        conditions="found when self-observation drift > threshold",
        evidence={"sample": True, "drift": 0.12},
    )
    print("\nSimulated mutation recorded:")
    print(mutation)


if __name__ == "__main__":
    main()
