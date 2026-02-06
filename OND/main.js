const TAU = Math.PI * 2;

const clamp01 = (v) => Math.min(1, Math.max(0, v));
const lerp = (a, b, t) => a + (b - a) * t;
const smooth = (current, target, dt, hz) => lerp(current, target, 1 - Math.exp(-dt * hz));
const mapRange = (v, in0, in1, out0, out1) => {
  const denom = in1 - in0;
  if (!Number.isFinite(v) || !Number.isFinite(denom) || denom === 0) return out0;
  return out0 + ((v - in0) / denom) * (out1 - out0);
};

function hsvToRgb(h, s, v) {
  const hh = ((h % 360) + 360) % 360;
  const c = v * s;
  const x = c * (1 - Math.abs(((hh / 60) % 2) - 1));
  const m = v - c;
  let r = 0,
    g = 0,
    b = 0;
  if (hh < 60) [r, g, b] = [c, x, 0];
  else if (hh < 120) [r, g, b] = [x, c, 0];
  else if (hh < 180) [r, g, b] = [0, c, x];
  else if (hh < 240) [r, g, b] = [0, x, c];
  else if (hh < 300) [r, g, b] = [x, 0, c];
  else [r, g, b] = [c, 0, x];
  return { r: (r + m) * 255, g: (g + m) * 255, b: (b + m) * 255 };
}

function fmtHz(hz) {
  if (!Number.isFinite(hz) || hz <= 0) return "—";
  if (hz < 1000) return `${Math.round(hz)} Hz`;
  return `${(hz / 1000).toFixed(2)} kHz`;
}

const NOTE_NAMES = ["C", "C♯", "D", "D♯", "E", "F", "F♯", "G", "G♯", "A", "A♯", "B"];
function hzToNote(hz) {
  if (!Number.isFinite(hz) || hz <= 0) return { note: "—", cents: 0 };
  const midi = 69 + 12 * Math.log2(hz / 440);
  if (!Number.isFinite(midi)) return { note: "—", cents: 0 };
  const rounded = Math.round(midi);
  const idx = ((rounded % 12) + 12) % 12;
  const octave = Math.floor(rounded / 12) - 1;
  const cents = Math.round((midi - rounded) * 100);
  return { note: `${NOTE_NAMES[idx]}${octave}`, cents };
}

function binFromHz(hz, sampleRate, fftSize) {
  return Math.max(0, Math.round((hz * fftSize) / sampleRate));
}

function bandAvg(freqBins, bin0, bin1) {
  const n = freqBins.length;
  const a = Math.max(0, Math.min(n - 1, bin0));
  const b = Math.max(0, Math.min(n - 1, bin1));
  const from = Math.min(a, b);
  const to = Math.max(a, b);
  const count = Math.max(1, to - from + 1);
  let sum = 0;
  for (let i = from; i <= to; i++) sum += freqBins[i];
  return sum / (count * 255);
}

async function createAudio(mode) {
  const AudioCtx = window.AudioContext || window.webkitAudioContext;
  if (!AudioCtx) throw new Error("AudioContext no soportado");
  const audioCtx = new AudioCtx();

  const analyser = audioCtx.createAnalyser();
  analyser.fftSize = 2048;
  analyser.smoothingTimeConstant = 0.78;

  const silent = audioCtx.createGain();
  silent.gain.value = 0;

  let stream = null;
  let nodes = [];

  if (mode === "mic") {
    if (!navigator.mediaDevices?.getUserMedia) throw new Error("getUserMedia no soportado");
    stream = await navigator.mediaDevices.getUserMedia({
      audio: {
        echoCancellation: true,
        noiseSuppression: true,
        autoGainControl: true,
      },
      video: false,
    });
    const src = audioCtx.createMediaStreamSource(stream);
    src.connect(analyser);
    analyser.connect(silent);
    silent.connect(audioCtx.destination);
    nodes = [src, analyser, silent];
  } else {
    const carrier = audioCtx.createOscillator();
    carrier.type = "sawtooth";
    carrier.frequency.value = 200;

    const lfo = audioCtx.createOscillator();
    lfo.type = "sine";
    lfo.frequency.value = 0.23;

    const lfoGain = audioCtx.createGain();
    lfoGain.gain.value = 180;
    lfo.connect(lfoGain);
    lfoGain.connect(carrier.frequency);

    const trem = audioCtx.createOscillator();
    trem.type = "sine";
    trem.frequency.value = 1.7;

    const tremGain = audioCtx.createGain();
    tremGain.gain.value = 0.38;
    trem.connect(tremGain);

    const amp = audioCtx.createGain();
    amp.gain.value = 0.22;
    tremGain.connect(amp.gain);

    carrier.connect(amp);
    amp.connect(analyser);
    analyser.connect(silent);
    silent.connect(audioCtx.destination);

    carrier.start();
    lfo.start();
    trem.start();
    nodes = [carrier, lfo, trem, lfoGain, tremGain, amp, analyser, silent];
  }

  const floatTime = typeof analyser.getFloatTimeDomainData === "function";
  const timeBins = floatTime ? new Float32Array(analyser.fftSize) : new Uint8Array(analyser.fftSize);
  const freqBins = new Uint8Array(analyser.frequencyBinCount);

  try {
    await audioCtx.resume();
  } catch {}

  return {
    mode,
    audioCtx,
    analyser,
    floatTime,
    timeBins,
    freqBins,
    get sampleRate() {
      return audioCtx.sampleRate;
    },
    stop() {
      try {
        for (const n of nodes) {
          if (typeof n.stop === "function") n.stop();
          if (typeof n.disconnect === "function") n.disconnect();
        }
      } catch {}
      try {
        if (stream) {
          for (const t of stream.getTracks()) t.stop();
        }
      } catch {}
      try {
        audioCtx.close();
      } catch {}
    },
  };
}

function extractFeatures(audio, out, dt) {
  if (audio.floatTime) audio.analyser.getFloatTimeDomainData(audio.timeBins);
  else audio.analyser.getByteTimeDomainData(audio.timeBins);
  audio.analyser.getByteFrequencyData(audio.freqBins);

  let sumSq = 0;
  for (let i = 0; i < audio.timeBins.length; i++) {
    const x = audio.floatTime ? audio.timeBins[i] : (audio.timeBins[i] - 128) / 128;
    sumSq += x * x;
  }
  const rms = Math.sqrt(sumSq / audio.timeBins.length);

  let total = 0;
  let weighted = 0;
  let maxV = -1;
  let maxI = 0;
  for (let i = 1; i < audio.freqBins.length; i++) {
    const v = audio.freqBins[i] / 255;
    total += v;
    weighted += v * i;
    if (v > maxV) {
      maxV = v;
      maxI = i;
    }
  }

  const centroidBin = total > 0 ? weighted / total : 0;
  const hasSignal = maxV > 0.02 || total > 0.6;
  const dominantHz = hasSignal ? (maxI * audio.sampleRate) / audio.analyser.fftSize : 0;
  const centroidHz = hasSignal ? (centroidBin * audio.sampleRate) / audio.analyser.fftSize : 0;

  const b0 = binFromHz(40, audio.sampleRate, audio.analyser.fftSize);
  const b1 = binFromHz(220, audio.sampleRate, audio.analyser.fftSize);
  const m0 = binFromHz(220, audio.sampleRate, audio.analyser.fftSize);
  const m1 = binFromHz(1900, audio.sampleRate, audio.analyser.fftSize);
  const t0 = binFromHz(1900, audio.sampleRate, audio.analyser.fftSize);
  const t1 = binFromHz(7600, audio.sampleRate, audio.analyser.fftSize);

  const bass = bandAvg(audio.freqBins, b0, b1);
  const mid = bandAvg(audio.freqBins, m0, m1);
  const treble = bandAvg(audio.freqBins, t0, t1);

  out.rms = rms;
  out.hasSignal = hasSignal;
  out.rmsSmooth = smooth(out.rmsSmooth, rms, dt, 10);
  out.dominantHz = smooth(out.dominantHz, dominantHz, dt, 8);
  out.centroidHz = smooth(out.centroidHz, centroidHz, dt, 6);
  out.bass = smooth(out.bass, bass, dt, 8);
  out.mid = smooth(out.mid, mid, dt, 8);
  out.treble = smooth(out.treble, treble, dt, 8);
}

function envelope(nx, t, features, envAmount) {
  const travel = 0.08 + 0.22 * envAmount + 0.12 * features.bass;
  const f1 = 1.2 + 1.8 * envAmount;
  const f2 = 0.7 + 1.2 * envAmount;
  const wob1 = Math.sin(TAU * (f1 * nx + t * travel) + 0.8);
  const wob2 = Math.sin(TAU * (f2 * nx - t * travel * 0.72) - 1.4);
  const wob3 = Math.sin(TAU * ((f1 * 0.45 + 0.08) * nx + t * travel * 0.44) + 2.1);

  const blend = 0.52 + 0.28 * wob1 + 0.16 * wob2 + 0.12 * wob3;
  const window = Math.sin(Math.PI * nx);
  const shaped = Math.pow(Math.max(0, blend), 1.35) * window * window;
  const pumped = shaped * (0.65 + 0.65 * features.bass);
  return pumped;
}

const scratch = {
  topY: new Float32Array(0),
  botY: new Float32Array(0),
  lineAmp: new Float32Array(0),
  x: new Float32Array(0),
  lastW: -1,
};

function ensureScratch(samples, w) {
  const prevXLen = scratch.x.length;
  if (scratch.topY.length !== samples) scratch.topY = new Float32Array(samples);
  if (scratch.botY.length !== samples) scratch.botY = new Float32Array(samples);
  if (scratch.lineAmp.length !== samples) scratch.lineAmp = new Float32Array(samples);
  if (scratch.x.length !== samples) scratch.x = new Float32Array(samples);

  if (scratch.lastW !== w || prevXLen !== samples) {
    const denom = Math.max(1, samples - 1);
    for (let j = 0; j < samples; j++) scratch.x[j] = (j / denom) * w;
    scratch.lastW = w;
  }
}

let reduceMotion = false;
const reduceMotionMq = window.matchMedia?.("(prefers-reduced-motion: reduce)");
if (reduceMotionMq) {
  const setReduceMotion = (e) => {
    reduceMotion = Boolean(e?.matches ?? reduceMotionMq.matches);
  };
  setReduceMotion(reduceMotionMq);
  reduceMotionMq.addEventListener?.("change", setReduceMotion);
  // Safari legacy
  reduceMotionMq.addListener?.(setReduceMotion);
}

function pathRoundRect(ctx, x, y, w, h, r) {
  const rr = Math.max(0, Math.min(r, w * 0.5, h * 0.5));
  ctx.beginPath();
  ctx.moveTo(x + rr, y);
  ctx.arcTo(x + w, y, x + w, y + h, rr);
  ctx.arcTo(x + w, y + h, x, y + h, rr);
  ctx.arcTo(x, y + h, x, y, rr);
  ctx.arcTo(x, y, x + w, y, rr);
  ctx.closePath();
}

function drawSignature(ctx, w, h, t, features, hueShift, pitch) {
  const label = "Elisa Thalia Castaño Maus · v2";
  const minDim = Math.max(1, Math.min(w, h));
  const size = Math.round(Math.max(12, Math.min(18, minDim * 0.032)));
  const subSize = Math.round(size * 0.78);
  const padX = Math.round(size * 0.7);
  const padY = Math.round(size * 0.55);
  const margin = Math.round(Math.max(12, minDim * 0.03));

  const fallbackHz = features.hasSignal ? features.dominantHz : 0;
  const hz = pitch?.voiced ? pitch.hz : fallbackHz;
  const note = pitch?.voiced ? pitch.note : hzToNote(hz).note;
  const sub = note && note !== "—" ? `${note} · ${fmtHz(hz)}` : "";

  ctx.save();
  const fontFamily = `"Space Grotesk", system-ui, -apple-system, Segoe UI, Roboto, sans-serif`;
  ctx.font = `600 ${size}px ${fontFamily}`;
  const m1 = ctx.measureText(label);
  const w1 = Math.ceil(m1.width);
  const h1 = Math.ceil((m1.actualBoundingBoxAscent || size) + (m1.actualBoundingBoxDescent || size * 0.24));

  let w2 = 0;
  let h2 = 0;
  let m2 = null;
  if (sub) {
    ctx.font = `600 ${subSize}px ${fontFamily}`;
    m2 = ctx.measureText(sub);
    w2 = Math.ceil(m2.width);
    h2 = Math.ceil(
      (m2.actualBoundingBoxAscent || subSize) + (m2.actualBoundingBoxDescent || subSize * 0.24),
    );
  }

  const gap = sub ? Math.round(size * 0.28) : 0;
  const textW = Math.max(w1, w2);
  const textH = h1 + gap + h2;

  const boxW = textW + padX * 2;
  const boxH = textH + padY * 2;
  const x = w - margin - boxW;
  const y = h - margin - boxH;

  const sig = clamp01(0.35 + 0.55 * features.rmsSmooth + 0.2 * features.treble);
  const boxA = 0.22 + 0.22 * sig;

  ctx.globalCompositeOperation = "source-over";
  ctx.globalAlpha = 1;
  pathRoundRect(ctx, x, y, boxW, boxH, Math.round(boxH * 0.38));
  ctx.fillStyle = `rgba(0, 0, 0, ${boxA.toFixed(3)})`;
  ctx.fill();
  ctx.strokeStyle = `rgba(255, 255, 255, ${(0.08 + 0.08 * sig).toFixed(3)})`;
  ctx.lineWidth = Math.max(1, Math.round(size * 0.08));
  ctx.stroke();

  const x0 = x + padX;
  const y0 = y + padY + (m1.actualBoundingBoxAscent || size);

  const drift = reduceMotion ? 0 : Math.sin(t * 0.85) * 0.5 + 0.5;
  const h0 = (200 + hueShift + drift * 80) % 360;
  const a = hsvToRgb(h0, 0.9, 0.98);
  const b = hsvToRgb((h0 + 120) % 360, 0.86, 0.98);
  const c = hsvToRgb((h0 + 220) % 360, 0.86, 0.98);
  const g = ctx.createLinearGradient(x0, y0, x0 + textW, y0);
  g.addColorStop(0, `rgb(${a.r.toFixed(0)},${a.g.toFixed(0)},${a.b.toFixed(0)})`);
  g.addColorStop(0.55, `rgb(${b.r.toFixed(0)},${b.g.toFixed(0)},${b.b.toFixed(0)})`);
  g.addColorStop(1, `rgb(${c.r.toFixed(0)},${c.g.toFixed(0)},${c.b.toFixed(0)})`);

  ctx.shadowColor = `rgba(40, 230, 255, ${(0.08 + 0.18 * sig).toFixed(3)})`;
  ctx.shadowBlur = Math.round(size * (0.35 + 0.65 * sig));
  ctx.fillStyle = g;
  ctx.globalAlpha = 0.55 + 0.38 * sig;
  ctx.font = `600 ${size}px ${fontFamily}`;
  ctx.fillText(label, x0, y0);

  if (sub) {
    ctx.shadowBlur = Math.round(subSize * (0.22 + 0.55 * sig));
    ctx.globalAlpha = 0.32 + 0.28 * sig;
    ctx.font = `600 ${subSize}px ${fontFamily}`;
    const y1 = y0 + (m1.actualBoundingBoxDescent || size * 0.24) + gap + (m2?.actualBoundingBoxAscent || subSize);
    ctx.fillStyle = `rgba(255, 255, 255, 0.92)`;
    ctx.fillText(sub, x0, y1);
  }

  ctx.restore();
}

const gfxCache = {
  vign: null,
  vignW: 0,
  vignH: 0,
};

function getVignette(ctx, w, h) {
  if (gfxCache.vign && gfxCache.vignW === w && gfxCache.vignH === h) return gfxCache.vign;
  const g = ctx.createRadialGradient(w * 0.5, h * 0.5, w * 0.12, w * 0.5, h * 0.5, w * 0.72);
  g.addColorStop(0, "rgba(0,0,0,0)");
  g.addColorStop(1, "rgba(0,0,0,0.35)");
  gfxCache.vign = g;
  gfxCache.vignW = w;
  gfxCache.vignH = h;
  return g;
}

function draw(ctx, w, h, t, features, settings, pitch) {
  // Full redraw each frame (fast path): just paint over.

  const bg = ctx.createLinearGradient(0, 0, w, h);
  const hueShift = (t * (10 + 30 * settings.color) + features.treble * 90) % 360;
  const c0 = hsvToRgb(260 + hueShift, 0.55, 0.12);
  const c1 = hsvToRgb(190 + hueShift, 0.55, 0.11);
  const c2 = hsvToRgb(40 + hueShift, 0.55, 0.1);
  bg.addColorStop(0, `rgb(${c0.r.toFixed(0)},${c0.g.toFixed(0)},${c0.b.toFixed(0)})`);
  bg.addColorStop(0.55, `rgb(${c1.r.toFixed(0)},${c1.g.toFixed(0)},${c1.b.toFixed(0)})`);
  bg.addColorStop(1, `rgb(${c2.r.toFixed(0)},${c2.g.toFixed(0)},${c2.b.toFixed(0)})`);
  ctx.fillStyle = bg;
  ctx.fillRect(0, 0, w, h);

  const centerY = h * 0.52;
  const amp = Math.min(h * 0.9, (0.16 + 0.64 * settings.sensitivity * features.rmsSmooth) * h);
  const envAmount = settings.envelope;

  const samples = settings.samples;
  const denomSamples = Math.max(1, samples - 1);
  const invSamples = 1 / denomSamples;
  ensureScratch(samples, w);

  const envLift = 0.12 * h * (0.25 + settings.envelope) * (0.15 + features.mid);
  const fillScale = 0.35 + 0.85 * envAmount;
  for (let j = 0; j < samples; j++) {
    const nx = j * invSamples;
    const e = envelope(nx, t, features, envAmount);
    const fillAmp = (0.08 + 0.92 * e) * amp * fillScale;
    scratch.topY[j] = centerY - fillAmp - envLift;
    scratch.botY[j] = centerY + fillAmp + envLift;
    scratch.lineAmp[j] = (0.12 + 0.88 * e) * amp;
  }

  ctx.globalCompositeOperation = "screen";
  ctx.beginPath();
  ctx.moveTo(0, scratch.topY[0]);
  for (let j = 1; j < samples; j++) ctx.lineTo(scratch.x[j], scratch.topY[j]);
  for (let j = samples - 1; j >= 0; j--) ctx.lineTo(scratch.x[j], scratch.botY[j]);
  ctx.closePath();
  const glow = ctx.createRadialGradient(w * 0.5, centerY, 0, w * 0.5, centerY, w * 0.65);
  glow.addColorStop(0, `rgba(255, 211, 56, ${0.07 + 0.16 * features.bass})`);
  glow.addColorStop(0.55, `rgba(255, 59, 230, ${0.05 + 0.12 * settings.color})`);
  glow.addColorStop(1, `rgba(0, 0, 0, 0)`);
  ctx.fillStyle = glow;
  ctx.fill();

  const dotCount = Math.min(
    2600,
    Math.floor(560 + 1600 * (0.2 + settings.envelope) * (0.3 + features.bass)),
  );
  ctx.fillStyle = `rgba(255, 211, 56, ${0.06 + 0.12 * settings.envelope})`;
  ctx.beginPath();
  for (let i = 0; i < dotCount; i++) {
    const nx = (i * 0.61803398875 + t * 0.02) % 1;
    const j = Math.floor(nx * (samples - 1));
    const topY = scratch.topY[j];
    const span = scratch.botY[j] - topY;
    const ny = (i * 0.38196601125 + t * 0.03) % 1;
    const y = topY + ny * span;
    const x = nx * w;
    const r = 0.7 + 1.8 * (0.35 + features.treble);
    ctx.moveTo(x + r, y);
    ctx.arc(x, y, r, 0, TAU);
  }
  ctx.fill();

  const lineCount = settings.lines;
  const baseCycles = clamp01(mapRange(features.centroidHz, 120, 3200, 0, 1));
  const cycles = lerp(2.2, 22.0, Math.pow(baseCycles, 0.75)) * (0.8 + 0.4 * settings.sensitivity);
  const spreadCycles = lerp(0.25, 3.8, settings.spread) * (0.6 + 0.9 * features.treble);
  const phaseSpeed = (0.42 + 1.8 * settings.spread) * (0.35 + 0.9 * (features.treble + 0.25));
  const twist = lerp(1.2, 6.6, settings.spread);
  const bundleWidth = (0.012 + 0.09 * settings.spread) * h * (0.25 + 1.1 * features.rmsSmooth);

  ctx.globalAlpha = 1;
  ctx.lineCap = "round";
  ctx.lineJoin = "round";

  ctx.globalCompositeOperation = "lighter";

  const wobFreq = 0.25 + settings.envelope;
  const wobStep = TAU * wobFreq * invSamples;
  const wobSinStep = Math.sin(wobStep);
  const wobCosStep = Math.cos(wobStep);
  const wobBase = TAU * (t * 0.08);
  const wobScale = (0.12 + 0.22 * features.bass) * bundleWidth * 0.12;

  for (let i = 0; i < lineCount; i++) {
    const z = lineCount <= 1 ? 0.5 : i / (lineCount - 1);
    const depth = 1 - Math.abs(z - 0.5) * 2;
    const hue = (210 + hueShift + 140 * z + 30 * features.mid) % 360;
    const sat = 0.55 + 0.35 * settings.color + 0.15 * features.treble;
    const val = 0.72 + 0.22 * depth + 0.12 * settings.color;
    const col = hsvToRgb(hue, clamp01(sat), clamp01(val));
    const alpha = 0.025 + 0.11 * depth + 0.08 * features.rmsSmooth;
    ctx.strokeStyle = `rgba(${col.r.toFixed(0)},${col.g.toFixed(0)},${col.b.toFixed(0)},${alpha.toFixed(4)})`;
    ctx.lineWidth = 0.8 + 2.6 * depth + 1.6 * features.rmsSmooth;

    const f = cycles + (z - 0.5) * spreadCycles;
    const phase0 = (z - 0.5) * twist + t * phaseSpeed + features.dominantHz * 0.0007;
    const off = (z - 0.5) * bundleWidth;

    const phaseStep = TAU * f * invSamples;
    const sinStep = Math.sin(phaseStep);
    const cosStep = Math.cos(phaseStep);
    let sinA = Math.sin(phase0);
    let cosA = Math.cos(phase0);

    const wobPhase0 = wobBase + z * 3.1;
    let sinW = Math.sin(wobPhase0);
    let cosW = Math.cos(wobPhase0);

    ctx.beginPath();
    for (let j = 0; j < samples; j++) {
      const a = scratch.lineAmp[j];
      const y = centerY + off + sinW * wobScale + sinA * a;
      const x = scratch.x[j];
      if (j === 0) ctx.moveTo(x, y);
      else ctx.lineTo(x, y);

      // Advance oscillators (recurrence avoids per-point trig calls)
      const nextSinA = sinA * cosStep + cosA * sinStep;
      const nextCosA = cosA * cosStep - sinA * sinStep;
      sinA = nextSinA;
      cosA = nextCosA;

      const nextSinW = sinW * wobCosStep + cosW * wobSinStep;
      const nextCosW = cosW * wobCosStep - sinW * wobSinStep;
      sinW = nextSinW;
      cosW = nextCosW;
    }
    ctx.stroke();
  }

  ctx.globalCompositeOperation = "source-over";
  ctx.globalAlpha = 1;

  ctx.fillStyle = getVignette(ctx, w, h);
  ctx.fillRect(0, 0, w, h);

  drawSignature(ctx, w, h, t, features, hueShift, pitch);
}

const ui = {
  canvas: document.getElementById("viz"),
  hint: document.getElementById("hint"),
  startBtn: document.getElementById("startBtn"),
  stopBtn: document.getElementById("stopBtn"),
  sourceSelect: document.getElementById("sourceSelect"),
  lines: document.getElementById("lines"),
  sensitivity: document.getElementById("sensitivity"),
  spread: document.getElementById("spread"),
  envelope: document.getElementById("envelope"),
  color: document.getElementById("color"),
  rmsValue: document.getElementById("rmsValue"),
  hzValue: document.getElementById("hzValue"),
  bandsValue: document.getElementById("bandsValue"),
};

const ctx = ui.canvas.getContext("2d", { alpha: true, desynchronized: true });
if (!ctx) {
  ui.hint.style.display = "block";
  ui.hint.textContent = "Canvas 2D no está disponible en este navegador.";
  ui.startBtn.disabled = true;
  ui.stopBtn.disabled = true;
  throw new Error("Canvas 2D not available");
}

const state = {
  running: false,
  audio: null,
  dpr: 1,
  needsResize: true,
  pitch: {
    ws: null,
    connected: false,
    voiced: false,
    hz: 0,
    note: "—",
    lastSend: 0,
    sendBuf: new Float32Array(0),
  },
  features: {
    rms: 0,
    rmsSmooth: 0,
    hasSignal: false,
    dominantHz: 0,
    centroidHz: 0,
    bass: 0,
    mid: 0,
    treble: 0,
  },
  lastNow: performance.now(),
  lastUiNow: 0,
  settings: {
    lines: 120,
    sensitivity: 1.2,
    spread: 0.9,
    envelope: 1.2,
    color: 1.2,
    samples: 900,
  },
};

function resize() {
  const dpr = Math.max(1, Math.min(2.5, window.devicePixelRatio || 1));
  state.dpr = dpr;
  const rect = ui.canvas.getBoundingClientRect();
  const w = Math.max(1, Math.floor(rect.width * dpr));
  const h = Math.max(1, Math.floor(rect.height * dpr));
  if (ui.canvas.width !== w || ui.canvas.height !== h) {
    ui.canvas.width = w;
    ui.canvas.height = h;
  }
}

function syncSettings() {
  const to02 = (el) => Math.min(2, Math.max(0, (Number(el.value) / 100) || 0));
  state.settings.lines = Math.min(220, Math.max(40, Math.round(Number(ui.lines.value) || 120)));
  state.settings.sensitivity = to02(ui.sensitivity);
  state.settings.spread = to02(ui.spread);
  state.settings.envelope = to02(ui.envelope);
  state.settings.color = to02(ui.color);
  const cssW = ui.canvas.width / Math.max(1, state.dpr);
  const base = Math.floor(cssW * 0.95);
  const budget = Math.floor(130000 / Math.max(40, state.settings.lines));
  state.settings.samples = Math.max(420, Math.min(1400, Math.min(base, budget)));
}

function disconnectPitch() {
  const ws = state.pitch.ws;
  state.pitch.ws = null;
  state.pitch.connected = false;
  state.pitch.voiced = false;
  state.pitch.hz = 0;
  state.pitch.note = "—";
  if (!ws) return;
  try {
    ws.close();
  } catch {}
}

function connectPitch(audio) {
  disconnectPitch();
  if (!audio) return;
  if (!("WebSocket" in window)) return;
  if (!(location.hostname === "localhost" || location.hostname === "127.0.0.1")) return;

  const proto = location.protocol === "https:" ? "wss" : "ws";
  const url = `${proto}://${location.host}/ws`;
  let ws = null;
  try {
    ws = new WebSocket(url);
    ws.binaryType = "arraybuffer";
  } catch {
    return;
  }

  state.pitch.ws = ws;

  ws.addEventListener(
    "open",
    () => {
      if (state.pitch.ws !== ws) return;
      state.pitch.connected = true;
      try {
        ws.send(JSON.stringify({ type: "hello", sr: audio.sampleRate }));
      } catch {}
    },
    { passive: true },
  );

  ws.addEventListener(
    "message",
    (ev) => {
      if (state.pitch.ws !== ws) return;
      if (typeof ev.data !== "string") return;
      let msg = null;
      try {
        msg = JSON.parse(ev.data);
      } catch {
        return;
      }
      if (!msg || msg.type !== "pitch") return;
      const hz = Number(msg.hz) || 0;
      state.pitch.hz = hz;
      state.pitch.note =
        typeof msg.note === "string" ? msg.note.split("#").join("♯") : "—";
      state.pitch.voiced = Boolean(msg.voiced && hz > 0);
    },
    { passive: true },
  );

  const onDead = () => {
    if (state.pitch.ws === ws) state.pitch.ws = null;
    state.pitch.connected = false;
    state.pitch.voiced = false;
  };
  ws.addEventListener("close", onDead, { passive: true });
  ws.addEventListener("error", onDead, { passive: true });
}

function ensurePitchSendBuf(n) {
  if (state.pitch.sendBuf.length !== n) state.pitch.sendBuf = new Float32Array(n);
}

function maybeSendPitch(audio, now) {
  const ws = state.pitch.ws;
  if (!ws || ws.readyState !== WebSocket.OPEN) return;
  if (now - state.pitch.lastSend < 100) return;
  state.pitch.lastSend = now;

  const bins = audio.timeBins;
  const n = bins.length;
  ensurePitchSendBuf(n);
  const buf = state.pitch.sendBuf;
  if (audio.floatTime) {
    buf.set(bins);
  } else {
    for (let i = 0; i < n; i++) buf[i] = (bins[i] - 128) / 128;
  }

  try {
    ws.send(buf);
  } catch {}
}

async function start() {
  if (state.running) return;

  syncSettings();
  const mode = ui.sourceSelect.value === "mic" ? "mic" : "demo";
  ui.startBtn.disabled = true;
  ui.stopBtn.disabled = true;
  ui.hint.style.display = "none";

  if (
    mode === "mic" &&
    !(
      window.isSecureContext ||
      location.hostname === "localhost" ||
      location.hostname === "127.0.0.1"
    )
  ) {
    ui.hint.style.display = "block";
    ui.hint.innerHTML =
      "El micrófono requiere <b>https</b> o <b>localhost</b>. Cambia a <b>Demo</b> o sirve en local.";
    ui.startBtn.disabled = false;
    ui.stopBtn.disabled = true;
    return;
  }

  try {
    state.audio = await createAudio(mode);
  } catch (err) {
    console.error(err);
    ui.hint.style.display = "block";
    ui.hint.innerHTML =
      mode === "mic"
        ? `No se pudo activar el micrófono. Revisa permisos o prueba <b>Demo</b>.`
        : `No se pudo iniciar audio en Demo.`;
    ui.startBtn.disabled = false;
    ui.stopBtn.disabled = true;
    return;
  }

  connectPitch(state.audio);
  state.running = true;
  state.lastNow = performance.now();
  ui.stopBtn.disabled = false;
  requestAnimationFrame(tick);
}

function stop(reason) {
  if (!state.running) return;
  state.running = false;
  ui.startBtn.disabled = false;
  ui.stopBtn.disabled = true;
  ui.hint.style.display = "block";
  ui.hint.innerHTML =
    reason ?? `Pulsa <b>Iniciar</b> para volver a animar.`;
  disconnectPitch();
  try {
    state.audio?.stop();
  } finally {
    state.audio = null;
  }
}

function tick(now) {
  if (!state.running) return;

  if (state.needsResize) {
    resize();
    state.needsResize = false;
  }
  syncSettings();

  const dt = Math.min(0.05, Math.max(0, (now - state.lastNow) / 1000));
  state.lastNow = now;

  if (state.audio) extractFeatures(state.audio, state.features, dt);
  if (state.audio) maybeSendPitch(state.audio, now);
  const w = ui.canvas.width;
  const h = ui.canvas.height;

  draw(ctx, w, h, now / 1000, state.features, state.settings, state.pitch);

  if (now - state.lastUiNow > 120) {
    state.lastUiNow = now;
    ui.rmsValue.textContent = state.features.rmsSmooth.toFixed(3);
    if (state.pitch.voiced && state.pitch.note !== "—") {
      ui.hzValue.textContent = `${state.pitch.note} · ${fmtHz(state.pitch.hz)}`;
    } else if (state.features.hasSignal && state.features.dominantHz > 0) {
      const approx = hzToNote(state.features.dominantHz).note;
      ui.hzValue.textContent = `${approx} · ${fmtHz(state.features.dominantHz)}`;
    } else {
      ui.hzValue.textContent = "—";
    }
    ui.bandsValue.textContent = `${state.features.bass.toFixed(2)} · ${state.features.mid.toFixed(2)} · ${state.features.treble.toFixed(2)}`;
  }

  requestAnimationFrame(tick);
}

let resizeRaf = 0;
function scheduleResize() {
  state.needsResize = true;
  if (state.running) return;
  if (resizeRaf) return;
  resizeRaf = requestAnimationFrame((now) => {
    resizeRaf = 0;
    if (!state.needsResize) return;
    resize();
    syncSettings();
    draw(ctx, ui.canvas.width, ui.canvas.height, now / 1000, state.features, state.settings, state.pitch);
    state.needsResize = false;
  });
}

let previewRaf = 0;
function schedulePreview() {
  if (state.running) return;
  if (previewRaf) return;
  previewRaf = requestAnimationFrame((now) => {
    previewRaf = 0;
    draw(ctx, ui.canvas.width, ui.canvas.height, now / 1000, state.features, state.settings, state.pitch);
  });
}

window.addEventListener("resize", scheduleResize, { passive: true });
if (window.ResizeObserver) {
  const ro = new ResizeObserver(() => scheduleResize());
  ro.observe(ui.canvas);
}
for (const el of [ui.lines, ui.sensitivity, ui.spread, ui.envelope, ui.color]) {
  el.addEventListener(
    "input",
    () => {
      syncSettings();
      schedulePreview();
    },
    { passive: true },
  );
}
ui.sourceSelect.addEventListener(
  "change",
  () => {
    if (state.running) {
      stop("Cambiando fuente…");
      start();
    }
  },
  { passive: true },
);
ui.startBtn.addEventListener("click", () => start(), { passive: true });
ui.stopBtn.addEventListener("click", () => stop(), { passive: true });

document.addEventListener(
  "visibilitychange",
  () => {
    if (document.visibilityState === "hidden" && state.running) {
      stop("Pausado: pestaña oculta (micrófono liberado).");
    }
  },
  { passive: true },
);

window.addEventListener(
  "pagehide",
  () => {
    if (state.running) stop("Pausado.");
  },
  { passive: true },
);

resize();
state.needsResize = false;
syncSettings();
draw(ctx, ui.canvas.width, ui.canvas.height, performance.now() / 1000, state.features, state.settings, state.pitch);
