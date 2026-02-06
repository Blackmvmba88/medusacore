#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import time
from pathlib import Path

try:
  import librosa
  import numpy as np
  from aiohttp import web
except Exception as exc:  # pragma: no cover
  raise SystemExit(
    "\n".join(
      [
        "Faltan dependencias para el servidor de pitch (librosa).",
        "Instala y vuelve a intentar:",
        "  python3 -m pip install -r requirements.txt",
        "",
        f"Detalle: {exc}",
      ],
    ),
  ) from exc

ROOT = Path(__file__).resolve().parent


async def index(_request: web.Request) -> web.StreamResponse:
  res = web.FileResponse(ROOT / "index.html")
  res.headers["Cache-Control"] = "no-store"
  return res


def safe_pitch_hz(hz: float, fmin: float, fmax: float) -> float:
  if not np.isfinite(hz):
    return 0.0
  if hz < fmin or hz > fmax:
    return 0.0
  return float(hz)


async def ws_pitch(request: web.Request) -> web.StreamResponse:
  ws = web.WebSocketResponse(heartbeat=20.0, max_msg_size=8 * 1024 * 1024)
  await ws.prepare(request)

  sr = 48000
  fmin = float(librosa.note_to_hz("A0"))
  fmax = float(librosa.note_to_hz("C8"))

  ring = np.zeros(0, dtype=np.float32)
  last_compute = 0.0

  async for msg in ws:
    if msg.type == web.WSMsgType.TEXT:
      try:
        payload = json.loads(msg.data)
      except Exception:
        continue

      if payload.get("type") == "hello":
        sr_in = payload.get("sr")
        if isinstance(sr_in, (int, float)) and 8000 <= sr_in <= 192000:
          sr = int(sr_in)
        ring = np.zeros(0, dtype=np.float32)
        await ws.send_json({"type": "hello", "ok": True, "sr": sr})
      continue

    if msg.type != web.WSMsgType.BINARY:
      continue

    frame = np.frombuffer(msg.data, dtype=np.float32)
    if frame.size == 0:
      continue

    # Keep a short sliding window (~250ms) for stable low notes.
    ring = np.concatenate((ring, frame))
    max_len = int(sr * 0.25)
    if ring.size > max_len:
      ring = ring[-max_len:]

    now = time.monotonic()
    if now - last_compute < 0.10:
      continue
    last_compute = now

    # Need at least ~50ms of audio.
    if ring.size < int(sr * 0.05):
      continue

    window_len = min(8192, ring.size)
    y = ring[-window_len:]
    rms = float(np.sqrt(np.mean(y * y)))

    # Hard gate on silence/noise.
    if rms < 0.01:
      await ws.send_json({"type": "pitch", "hz": 0.0, "note": "—", "rms": rms, "voiced": False})
      continue

    try:
      f0 = float(
        librosa.yin(
          y,
          fmin=fmin,
          fmax=fmax,
          sr=sr,
          frame_length=window_len,
          hop_length=window_len,
          center=False,
        )[0],
      )
    except Exception:
      f0 = 0.0

    f0 = safe_pitch_hz(f0, fmin, fmax)
    voiced = f0 > 0.0
    note = "—"
    if voiced:
      try:
        note = str(librosa.hz_to_note(f0, cents=False))
      except Exception:
        note = "—"
        voiced = False
        f0 = 0.0

    await ws.send_json({"type": "pitch", "hz": f0, "note": note, "rms": rms, "voiced": voiced})

  return ws


def parse_args() -> argparse.Namespace:
  p = argparse.ArgumentParser(description="OND pitch server (librosa) + static files")
  p.add_argument("--host", default="127.0.0.1")
  p.add_argument("--port", type=int, default=8081)
  return p.parse_args()


def main() -> None:
  args = parse_args()

  app = web.Application(client_max_size=8 * 1024 * 1024)
  app.router.add_get("/", index)
  app.router.add_get("/ws", ws_pitch)
  app.router.add_static("/", ROOT, show_index=False)

  web.run_app(app, host=args.host, port=args.port)


if __name__ == "__main__":
  main()
