# MedusaCore 🌌

**Status:** WIP / Genesis  
**Primary languages:** Python, HTML, Shell  
**Current goal:** turn AXIOM_ZERO from a design philosophy into a bounded, measurable and auditable experimentation system.

## What MedusaCore is

MedusaCore is an experimental framework for observing a system, proposing bounded changes, measuring the result and preserving the evidence required to decide whether a change should survive.

Its conceptual genesis is **AXIOM_ZERO**:

> OBSERVA, ACTÚA, MIDE LA DIFERENCIA, AJUSTA EL MODELO

That sentence is a design principle, not a claim of autonomous intelligence. The executable core now separates philosophy from runtime contracts.

## Architecture

```text
MedusaCore
├── conceptual genesis
│   ├── PrimordialSeed / AXIOM_ZERO
│   └── HermeticCore principles
│
├── immutable governance kernel
│   ├── contracts.py
│   ├── governance.py
│   ├── evaluator.py
│   └── evidence.py
│
├── mutable organism
│   ├── parameters
│   ├── strategies
│   ├── workflows
│   └── agents
│
└── validation
    ├── unit tests
    ├── contract tests
    ├── adversarial tests
    └── reproducibility evidence
```

The governing rule is simple:

> A principle does not become runtime behavior until it can be expressed as a state, contract, metric, invariant, test or evidence record.

## Bounded experimentation lifecycle

```text
OBSERVE
   ↓
PROPOSE
   ↓
BOUND
   ↓
EXECUTE
   ↓
MEASURE
   ↓
EVALUATE
   ↓
ACCEPT / REJECT / UNKNOWN
   ↓
PRESERVE EVIDENCE
   ↓
PROMOTE (only when policy permits)
```

`UNKNOWN` is a valid outcome. Missing evidence is never treated as success.

## Runtime envelope

`ResourceBudget` declares the limits an experiment is expected to obey:

- wall-clock time;
- CPU time;
- memory;
- maximum iterations;
- maximum output size;
- network permission.

`RuntimeEnvelope` declares:

- which mutation kinds may be experimented with;
- which targets belong to the immutable kernel;
- the resource budget;
- whether evidence is mandatory for promotion.

### Important limitation

The current Genesis implementation **defines and validates these policies but does not yet provide OS-level sandbox enforcement**. Filesystem, process, network, CPU and memory isolation are the next execution-layer milestone. MedusaCore intentionally does not describe a policy declaration as if it were an enforced security boundary.

See [`spec/RUNTIME_ENVELOPE.md`](spec/RUNTIME_ENVELOPE.md).

## Formal decision model

A candidate is represented by a `MutationProposal`. Baseline and candidate executions produce `Measurement` records. An `Evaluator` compares one explicit objective while required invariants act as guardrails.

The evaluator returns exactly one verdict:

- `ACCEPT` — the objective satisfies the declared improvement and all invariants pass;
- `REJECT` — execution failed, an invariant failed or the objective did not improve enough;
- `UNKNOWN` — the evidence is insufficient or an invariant cannot be evaluated reliably.

Promotion is a separate governance decision. `MutationGate` requires an accepted evaluation and, by default, a content-hashed `EvidenceBundle`.

See [`spec/CORE_CONTRACTS.md`](spec/CORE_CONTRACTS.md).

## Example

```python
from core import (
    Evaluator,
    EvidenceBundle,
    InvariantResult,
    Measurement,
    MutationGate,
    MutationProposal,
    ObjectiveSpec,
    RuntimeEnvelope,
    stable_hash,
)

proposal = MutationProposal(
    candidate_id="router-v2",
    target="strategies/router.py",
    kind="strategy",
    payload_hash=stable_hash({"algorithm": "v2"}),
)

envelope = RuntimeEnvelope()
gate = MutationGate()

experiment = gate.authorize_experiment(proposal, envelope)
assert experiment.allowed

baseline = Measurement(
    operation="route",
    duration_seconds=0.15,
    success=True,
    metrics={"score": 0.72},
)

candidate = Measurement(
    operation="route",
    duration_seconds=0.14,
    success=True,
    metrics={"score": 0.81},
)


def safety(measurement: Measurement) -> InvariantResult:
    return InvariantResult("safety", passed=measurement.success)


evaluation = Evaluator().evaluate(
    baseline,
    candidate,
    ObjectiveSpec("score", direction="maximize", min_improvement=0.05),
    invariants=[safety],
)

bundle = EvidenceBundle.create(
    proposal=proposal,
    baseline=baseline,
    candidate=candidate,
    evaluation=evaluation,
    seed=42,
)

promotion = gate.authorize_promotion(
    evaluation,
    evidence_hash=bundle.evidence_hash(),
    envelope=envelope,
)
```

## Existing Genesis components

### PrimordialSeed / AXIOM_ZERO

`core/seed.py` initializes the conceptual seed and derives the initial HermeticCore principles.

### HermeticCore

HermeticCore preserves principle variants and an evolution log. The principles remain hypotheses and design vocabulary until connected to measurable runtime contracts.

### PerformanceMonitor / Optimizer

`core/optimizer.py` records operation duration and success rate, identifies simple bottlenecks and adjusts selected parameters. This is currently a deterministic heuristic optimizer, not a general self-learning system.

## Tests

```bash
pip install -r requirements.txt
pytest -v
```

The bounded-core contract suite is in:

```bash
pytest tests/test_rigorous_core.py -v
```

## Roadmap

### Genesis — contracts

- [x] AXIOM_ZERO / PrimordialSeed
- [x] HermeticCore principle evolution
- [x] Performance measurement primitives
- [x] Runtime envelope contract
- [x] Immutable-kernel mutation gate
- [x] `ACCEPT / REJECT / UNKNOWN` evaluation
- [x] Content-hashed evidence bundle
- [x] Promotion gate requiring evidence

### Execution boundary

- [ ] OS-level sandbox executor
- [ ] enforce wall/CPU/memory/output budgets
- [ ] explicit network deny/allow enforcement
- [ ] isolated filesystem workspace
- [ ] deterministic seed propagation
- [ ] automatic rollback of rejected candidates

### Evidence and reproducibility

- [ ] persist evidence bundles in a canonical schema
- [ ] artifact hashing/signatures
- [ ] environment capture: OS, interpreter and dependencies
- [ ] exact replay command for each experiment
- [ ] CI verification that replayed outputs match evidence

### Validation

- [ ] property-based invariants
- [ ] Red Team adversarial suite
- [ ] Blue Team safety/validation suite
- [ ] Forensics audit trail
- [ ] promotion policy requiring human sign-off for kernel changes

## Repository workflow

The active Genesis line is `wip/genesis`. New bounded-experimentation work should branch from that line until the architecture is ready to promote into a stable branch.

```bash
git checkout wip/genesis
git checkout -b feature/my-experiment
pytest
```

## License

This project is under active development. Consult the author for licensing terms.

---

MedusaCore is deliberately ambitious, but every new capability must state whether it is **conceptual**, **declared by policy**, **measured**, or **actually enforced**. That distinction is part of the architecture.
