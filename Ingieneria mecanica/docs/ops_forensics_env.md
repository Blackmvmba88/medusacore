# Operaciones: configurar Environment `forensics` automáticamente

Este documento guía la instalación y uso del GitHub App y del workflow que automatiza la creación de la Environment `forensics` y la regla de aprobadores.

Requisitos (admin repo):
- Permisos para crear GitHub Apps e instalar en el repositorio
- Añadir secrets del App en el repositorio

Pasos resumidos:

1. Crear GitHub App
   - Settings → Developer settings → GitHub Apps → New GitHub App
   - Name: e.g. `medusa-forensics-setup`
   - Homepage URL: repo URL
   - Webhook: opcional
   - Permissions: **Repository permissions** → set `Deployments` to `Read & write`; `Metadata` as `Read-only`.
   - Subscribe to events: none required for this automation.
   - Generate a private key (download the PEM file) and note the App ID.

2. Install the App into the repository
   - Install on `Blackmvmba88/medusacore` (or org level) and grant access.

3. Add secrets to the repository
   - Settings → Secrets → Actions → New repository secret
   - `GITHUB_APP_ID` → App ID (integer)
   - `GITHUB_APP_PRIVATE_KEY` → PEM contents (paste whole file)

4. Trigger the workflow
   - Go to the Actions tab → `Setup Forensics Environment` → `Run workflow`
   - Input: `reviewers` (comma-separated handles) and `required_approving_review_count` (default 1).
   - Optional: set `REVIEWERS` to a small test set and run with `--dry-run` locally to inspect payloads without changes.

5. Verificación
   - The workflow now includes a verification step that runs after setup and will fail the workflow if the protection rule does not match the requested configuration.
   - You can also run locally: `python scripts/setup_forensics_env.py --verify` to check current configuration.
   - Settings → Environments → `forensics` → Should list the protection rule with the required reviewers.

Notas:
- The workflow and script create the environment and add a `required_reviewers` protection rule via the App installation token.
- For full automation (CI creating the App), you need org-level admin tasks which are intentionally out-of-band.

FAQ
- Q: ¿Puedo añadir varios reviewers? A: Sí, separalos por comas en el input `reviewers`.
- Q: ¿Qué pasa si la App no está instalada? A: El paso para crear el token fallará y el workflow marcará error; instala la App y vuelve a ejecutar.
