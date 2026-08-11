# MedusaCore Core Contracts

## Status

Genesis / experimental. This specification defines what MedusaCore must prove before a candidate behavior can become stable behavior.

## Principle

AXIOM_ZERO remains a design principle. Runtime decisions are governed by explicit contracts:

1. **Observe** — capture a baseline and candidate measurement.
2. **Propose** — identify a candidate mutation, target, kind, and payload hash.
3. **Bound** — authorize the experiment only inside a declared runtime envelope.
4. **Measure** — collect objective metrics and invariant results.
5. **Evaluate** — return exactly one verdict: `ACCEPT`, `REJECT`, or `UNKNOWN`.
6. **Preserve evidence** — bind proposal, baseline, candidate, seed, and verdict into an evidence bundle.
7. **Promote** — allow promotion only for `ACCEPT` with required evidence.

`UNKNOWN` is a valid terminal result. Lack of evidence must never be converted into success.

## Immutable kernel and mutable organism

The **kernel** contains contracts and governance rules that define what may change and how changes are judged. It must not be mutated by the same candidate process it governs.

The **organism** contains parameters, strategies, workflows, and agents. These may be experimented with when the runtime envelope authorizes them.

This is a policy boundary, not an OS security boundary. Filesystem, process, network, CPU, and memory isolation require a separate sandbox implementation.

## Promotion invariant

A candidate can be promoted only when all of the following are true:

- its mutation kind is allowed;
- its target is outside the immutable kernel;
- its execution succeeds;
- every required invariant passes;
- the objective meets the declared minimum improvement;
- the verdict is `ACCEPT`;
- required evidence exists and is content-hashed.

Any failed condition yields `REJECT` or `UNKNOWN`; never implicit acceptance.
