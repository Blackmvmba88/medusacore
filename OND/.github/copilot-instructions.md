# GitHub Copilot instructions for OND

Purpose: short, actionable guidance to help AI coding agents be immediately productive in this repo (visual/audio prototype).

## Quick start ✅
- Install deps and run the pitch server (recommended):
  ```bash
  python3 -m pip install -r requirements.txt
  python3 server.py --port 8081
  # open http://127.0.0.1:8081 and press "Iniciar"
  ```
- Static-only (no librosa pitch):
  ```bash
  python3 -m http.server 8080
  # open http://localhost:8080 and press "Iniciar"
  ```
- Python deps: see `requirements.txt` (notably `librosa`, `aiohttp`, `numpy`).

## Big picture (why + components) 💡
- This repo is a compact visual/audio prototype that maps live audio → features → generative Canvas 2D visualization.
- Major components:
  - `server.py`: small aiohttp app exposing static files and a WebSocket `/ws` for server-side pitch detection using `librosa`.
  - `index.html` + `main.js`: client-side app (ES module) that uses WebAudio `AnalyserNode` to extract features and render to a 2D `<canvas>` (`#viz`).
- Design note: pitch detection is optional (demo oscillator when no mic) and the server is only contacted from `localhost` for security by default.

## WebSocket contract (critical - keep in sync) 🔧
- Client -> server:
  - On open the client sends a JSON hello: `{"type":"hello","sr": <sampleRate>}` (sampleRate is an integer).
  - Then the client periodically sends binary Float32Array frames of time-domain samples to `/ws`.
- Server -> client:
  - Hello reply: `{"type":"hello","ok":true,"sr":<sr>}`
  - Pitch messages: `{"type":"pitch","hz":<float>,"note":"<string or —>","rms":<float>,"voiced":<bool>}`
- Implementation details:
  - `server.py` uses `librosa.yin` and gates on `rms < 0.01` (sends `hz: 0.0` and `note: "—"` for silence)
  - The server clamps invalid/out-of-range frequencies (see `safe_pitch_hz`).
- Rule for changes: if you change the WS message shape, update both `server.py` and parsing in `main.js::connectPitch` and add an explicit example in this file.

## Important client patterns & performance notes ⚡
- `main.js` is performance-sensitive and uses:
  - Typed arrays (Float32Array / Uint8Array) and preallocated buffers (`ensureScratch`)—prefer maintaining these patterns when editing.
  - Oscillator recurrence to avoid per-sample trig calls (see the recurrence in the draw loop that advances sin/cos without Math.sin per sample).
  - Render budget: `state.settings.samples` is computed from canvas width and a per-line budget; avoid naive increases without checking cost.
- Audio analysis uses `AnalyserNode` with `fftSize=2048` and `smoothingTimeConstant=0.78`—algorithms (band ranges, bin mapping) depend on these choices (see `extractFeatures`).

## Developer workflows & debugging 🐞
- Local manual testing is primary: run the server, open `http://127.0.0.1:8081`, press **Iniciar**, inspect the canvas, and verify `RMS` / `Nota` values.
- Mic permissions require secure context (HTTPS) or `localhost`. If you want pitch over the network, change the `connectPitch` guard in `main.js` (it only connects when host is `localhost/127.0.0.1`).
- Server errors on missing deps fail fast with a helpful message; run `pip install -r requirements.txt` if `server.py` aborts.

## Conventions & code style (repo-specific) 📐
- UI text and comments are in Spanish—prefer Spanish for UI/UX strings to preserve consistency.
- Keep visual fidelity: small visual changes should be documented with before/after screenshots in the PR description.
- No test suite is present—start with manual integration tests. If you add tests, document how to run them here.

## Files to inspect for most tasks 🔎
- `README.md` — product overview + run instructions
- `server.py` — WebSocket server, pitch detection, `/ws` contract
- `main.js` — audio capture, feature extraction, rendering (most logic lives here)
- `index.html`, `style.css` — small static UI and layout

## PR checklist for AI agents ✅
- Preserve typed array usage and pre-allocation where applicable.
- Keep the WS message contract backwards-compatible or update both client and server and add short examples in this file.
- Run manual QA: start server, open UI, test both `demo` and `mic` modes, verify the canvas renders and `Nota` updates.
- For performance changes, include measurements (explain perceived fps/memory and why the change is safe).

---
If anything above is unclear or you want more examples (e.g., exact binary frame format or a small unit test scaffold), tell me which part to expand and I will iterate. 🎯
