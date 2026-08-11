# Runtime Envelope

A runtime envelope declares the maximum authority of a MedusaCore experiment.

## Current contract

`ResourceBudget` declares:

- wall-clock seconds;
- CPU seconds;
- memory in MB;
- maximum iterations;
- maximum output bytes;
- whether network access is allowed.

`RuntimeEnvelope` declares:

- allowed mutation kinds;
- immutable targets;
- resource budget;
- whether promotion requires evidence.

## Important limitation

The current Genesis implementation defines and validates these parameters but does **not** claim OS-level enforcement. A future sandbox executor must map these declarations to real process, filesystem, network, CPU, memory, and timeout controls.

That distinction is intentional: MedusaCore must never describe a policy declaration as if it were an enforced security boundary.
