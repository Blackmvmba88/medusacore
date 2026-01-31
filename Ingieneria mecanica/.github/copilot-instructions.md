# GitHub Copilot Instructions for this repository ✅

Purpose
- Short summary: Add a concise (1–2 line) purpose of the project here.
- When to ask for help: list contact info, team Slack channel, or issue labels used for guidance.

Quick usage for AI agents
- Role: act like a code contributor and follow repository rules (code style, commit message format, PR template).
- When modifying code, run the full test-suite and include a failing test when proposing behavior changes.

What I (the human) will fill in
- **Architecture summary (REPLACE_ME):** one-paragraph description of the system, major components, service boundaries, and the "why" for chosen structure.
- **Top-level components:** list the key directories and their responsibilities (e.g., `api/`, `pkg/`, `cmd/`, `web/`, `infra/`).

Build / Test / Debug — please replace with exact commands
- Build (example): `make build` or `./gradlew build` or `npm run build` — **REPLACE with project command**
- Unit tests: `make test` or `npm test` — **REPLACE with project command**
- Integration tests: `make itest` or `pytest tests/integration` — **REPLACE with project command**
- Lint/Format: `make lint` or `npm run lint` — note required linters/formatters and configuration files (`.eslintrc`, `prettierrc`, etc.)
- Common debug flow: how to run locally, sample env vars to set, how to attach debugger, and where logs go.

Project-specific conventions (replace examples with real patterns)
- Commit message format: e.g., `type(scope): short description` (fill actual convention).
- Branching: e.g., `feature/*`, `fix/*`, `hotfix/*` (fill actual convention).
- Tests live in: `tests/` or `pkg/*/test` (list exact locations).
- Error handling: preferred patterns (returns vs exceptions) and where helper utilities are (e.g., `pkg/errors`).

Integration & external dependencies
- External services: list by name and purpose (DB, cache, 3rd-party APIs). Include how to mock or emulate locally (docker-compose, test fixtures).
- Secrets & config: where they live (Vault, `.env`, GitHub Secrets) and how to configure locally.
- CI: location of workflow files (e.g., `.github/workflows/ci.yml`) and what checks they run.

Important files to inspect
- README.md — high-level setup
- `Dockerfile` / `docker-compose.yml` — containerization
- `.github/workflows/*` — CI behavior
- `Makefile` / `package.json` / `build.gradle` — build and test commands
- `docs/` or `design/` — architecture decisions

Common pitfalls and special cases
- Long-running migrations — how to coordinate DB changes (separate migration PR + feature toggle pattern)
- Backwards-incompatible changes — who to notify and required approvals
- Performance-sensitive modules: list them here and any benchmarking commands

How to propose a change (AI agent guidance)
- Always run relevant tests locally and include logs or failing output in the PR description.
- When changing public APIs, add compatibility note and integration test.
- Keep PRs focused; for larger refactors, split into smaller steps and document the migration plan.

If updating an existing `.github/copilot-instructions.md`
- Preserve any human-written sections under **Maintainers** or **Project-Specific Notes**.
- Add only factual, discoverable content—do not add hypothetical or opinionated rules.

Example prompts for humans to add project detail (please fill these)
- "Fill 'Architecture summary' with a 2–3 sentence description linking to `docs/architecture.md` if present."
- "Add exact build and test commands (including flags) and a short sample of expected output for `make test` or `npm test`."

Questions for you
- Which build/test commands should I use for this repo?
- Where are the key integration points (DB, queues, third-party APIs)?

Please review this starter file, replace the REPLACE_ME placeholders with repository-specific examples, and tell me which parts are unclear so I can iterate. 🚀