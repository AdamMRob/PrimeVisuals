HTML = r"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Laser Plane Visualiser</title>
  <script src="https://cdn.plot.ly/plotly-2.35.2.min.js"></script>
  <style>
    *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

    body {
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
      background: #ebebeb;
      color: #1a1a1a;
      min-height: 100vh;
    }

    header {
      background: #1d1d1f;
      color: #f0f0f0;
      padding: 20px 28px 18px;
      border-bottom: 2px solid #333;
    }
    header h1 { font-size: 17px; font-weight: 700; letter-spacing: 0.02em; font-family: monospace; }
    header p  { margin-top: 5px; font-size: 12px; color: #888; font-family: monospace; line-height: 1.5; }

    main { max-width: 1120px; margin: 0 auto; padding: 24px 24px 60px; }

    /* ── Section labels ── */
    .sect {
      font-size: 10px; font-weight: 700; letter-spacing: 0.1em;
      text-transform: uppercase; color: #777;
      margin-bottom: 10px; margin-top: 24px;
    }

    /* ── Drawing row ── */
    .draw-row { display: flex; gap: 36px; align-items: flex-start; flex-wrap: wrap; margin-bottom: 18px; }
    .grid-wrap { display: flex; flex-direction: column; gap: 6px; }
    .grid-label { font-size: 12px; font-weight: 700; color: #333; font-family: monospace; }
    .grid-sub   { font-size: 11px; color: #888; font-family: monospace; }
    svg.grid    { display: block; cursor: crosshair; border: 1px solid #aaa; background: #fff; }

    /* ── Controls ── */
    .controls { display: flex; gap: 10px; align-items: center; flex-wrap: wrap; margin-bottom: 14px; }

    select {
      font-size: 12px; padding: 7px 10px; border: 1px solid #bbb;
      border-radius: 5px; background: #fff; color: #1a1a1a;
      cursor: pointer; font-family: monospace;
    }
    select:focus { outline: 2px solid #0071e3; outline-offset: 1px; }

    button.primary {
      font-size: 12px; font-weight: 700; padding: 7px 22px;
      background: #1d1d1f; color: #fff; border: none; border-radius: 5px;
      cursor: pointer; font-family: monospace; letter-spacing: 0.04em;
      transition: background 0.12s;
    }
    button.primary:hover:not(:disabled) { background: #3a3a3c; }
    button.primary:disabled { background: #aaa; cursor: not-allowed; }

    button.secondary {
      font-size: 11px; font-weight: 600; padding: 6px 14px;
      background: #fff; color: #333; border: 1px solid #bbb; border-radius: 5px;
      cursor: pointer; font-family: monospace; transition: background 0.1s;
    }
    button.secondary:hover { background: #e4e4e4; }

    /* ── Error ── */
    .error-box {
      background: #fff3f3; border: 1px solid #f5a0a0; border-radius: 5px;
      color: #b00; font-size: 12px; font-family: monospace; line-height: 1.5;
      padding: 10px 14px; margin-bottom: 14px;
    }
    .hidden { display: none !important; }

    /* ── Output area ── */
    #output { margin-top: 32px; }
    .out-header {
      display: flex; align-items: center; gap: 14px; margin-bottom: 14px;
    }
    .out-header span { font-size: 10px; font-weight: 700; letter-spacing: 0.1em;
      text-transform: uppercase; color: #777; }

    .plot-box {
      background: #fff; border-radius: 7px;
      box-shadow: 0 1px 4px rgba(0,0,0,0.1); overflow: hidden;
      margin-bottom: 22px;
    }
    .plot-box-title {
      font-size: 10px; text-transform: uppercase; letter-spacing: 0.09em;
      color: #999; padding: 9px 14px; border-bottom: 1px solid #eee; font-weight: 700;
    }

    /* ── Grid size row ── */
    .size-row { display: flex; gap: 8px; align-items: center; margin-bottom: 12px; }
    .size-row input[type=number] {
      width: 64px; font-family: monospace; font-size: 12px;
      padding: 5px 8px; border: 1px solid #bbb; border-radius: 5px;
    }

    /* ── Mode tabs ── */
    .tab-row { display: flex; margin-bottom: 18px; }
    .tab {
      font-size: 12px; font-weight: 700; padding: 6px 22px;
      border: 1px solid #bbb; background: #fff; color: #555;
      cursor: pointer; font-family: monospace;
    }
    .tab:first-child { border-radius: 5px 0 0 5px; }
    .tab:last-child  { border-radius: 0 5px 5px 0; margin-left: -1px; }
    .tab.active      { background: #1d1d1f; color: #fff; border-color: #1d1d1f; }

    /* ── Upload panel ── */
    .upload-row { display: flex; gap: 36px; flex-wrap: wrap; margin-bottom: 16px; }
    .upload-col { display: flex; flex-direction: column; gap: 8px; }
    .preproc-row { display: flex; }
    .preproc-row .secondary             { border-radius: 0; margin-left: -1px; }
    .preproc-row .secondary:first-child { border-radius: 5px 0 0 5px; margin-left: 0; }
    .preproc-row .secondary:last-child  { border-radius: 0 5px 5px 0; }
    .preproc-row .secondary.active { background: #1d1d1f; color: #fff; border-color: #1d1d1f; }
    .density-row { display: flex; gap: 12px; align-items: center; margin-bottom: 14px; }
  </style>
</head>
<body>

<header>
  <h1>Laser Plane Visualiser</h1>
  <p>
    Three planes perpendicular to X: &nbsp;A at x=0 (target), &nbsp;B at x=80 (guide), &nbsp;C at x=160 (laser source). &nbsp;
    Lasers fire C → B → A. &nbsp;Grid maps to a ±10 × ±10 YZ space.
  </p>
</header>

<main>
  <!-- Grid size -->
  <div class="size-row">
    <span class="sect" style="margin:0">Grid size (N×N)</span>
    <input type="number" id="n-input" min="5" max="100" value="20"
           onchange="setN(+this.value)" onkeydown="if(event.key==='Enter')setN(+this.value)">
    <button class="secondary" onclick="setN(20)">20</button>
    <button class="secondary" onclick="setN(50)">50</button>
    <button class="secondary" onclick="setN(100)">100</button>
  </div>
  <div id="mode-note" class="hidden"
       style="font-size:11px;color:#b00;font-family:monospace;margin-bottom:10px;">
    Draw mode requires N ≤ 50 — switched to Upload.
  </div>

  <!-- Mode tabs -->
  <div class="tab-row">
    <button class="tab active" id="tab-draw"   onclick="setMode('draw')">Draw</button>
    <button class="tab"        id="tab-upload" onclick="setMode('upload')">Upload</button>
  </div>

  <!-- Draw panel -->
  <div id="draw-panel">
    <div class="sect">Draw patterns</div>
    <div class="draw-row">
      <div class="grid-wrap">
        <div class="grid-label">Plane A &nbsp;<span class="grid-sub">x = 0 &nbsp;(target image)</span></div>
        <svg id="grid-a" class="grid"></svg>
      </div>
      <div class="grid-wrap">
        <div class="grid-label">Plane B &nbsp;<span class="grid-sub">x = 80 &nbsp;(guide image)</span></div>
        <svg id="grid-b" class="grid"></svg>
      </div>
    </div>
  </div>

  <!-- Upload panel -->
  <div id="upload-panel" class="hidden">
    <div class="sect">Upload patterns</div>
    <div class="upload-row">
      <div class="upload-col">
        <div class="grid-label">Plane A &nbsp;<span class="grid-sub">x = 0 &nbsp;(target image)</span></div>
        <input type="file" accept="image/*" onchange="handleUpload(event,'A')">
        <div class="preproc-row">
          <button class="secondary active" id="pp-A-lum" onclick="setPreproc('A','luminance')">Luminance</button>
          <button class="secondary"        id="pp-A-edg" onclick="setPreproc('A','edges')">Edges</button>
        </div>
        <canvas id="preview-A"
          style="width:200px;height:200px;image-rendering:pixelated;border:1px solid #aaa;display:block;background:#f4f4f4"></canvas>
      </div>
      <div class="upload-col">
        <div class="grid-label">Plane B &nbsp;<span class="grid-sub">x = 80 &nbsp;(guide image)</span></div>
        <input type="file" accept="image/*" onchange="handleUpload(event,'B')">
        <div class="preproc-row">
          <button class="secondary active" id="pp-B-lum" onclick="setPreproc('B','luminance')">Luminance</button>
          <button class="secondary"        id="pp-B-edg" onclick="setPreproc('B','edges')">Edges</button>
        </div>
        <canvas id="preview-B"
          style="width:200px;height:200px;image-rendering:pixelated;border:1px solid #aaa;display:block;background:#f4f4f4"></canvas>
      </div>
    </div>
    <div class="density-row">
      <label class="grid-label">Density</label>
      <input type="range" id="density-slider" min="0" max="100" value="30"
             oninput="updateDensity(this.value)" style="width:220px">
      <span id="density-label" class="grid-sub">30%</span>
    </div>
  </div>

  <!-- Shared counter + controls -->
  <div class="grid-sub" id="counter" style="margin-bottom:10px">B: 0 / A: 0</div>
  <div class="controls">
    <select id="strategy">
      <option value="min">Minimise angle of incidence</option>
      <option value="max">Maximise angle of incidence</option>
      <option value="random">Random pairing</option>
    </select>
    <button class="primary" id="create-btn" onclick="create()" disabled>Create</button>
  </div>

  <div class="error-box hidden" id="error-box"></div>

  <div id="output" class="hidden">
    <div class="out-header">
      <span>Output</span>
      <span id="sample-label"
            style="font-size:10px;color:#888;font-family:monospace;font-weight:400;text-transform:none;letter-spacing:0"></span>
      <button class="secondary" id="toggle-btn" onclick="toggleBeams()">Hide Beams</button>
    </div>
    <div class="plot-box">
      <div class="plot-box-title">3D Laser Configuration</div>
      <div id="laser-3d"></div>
    </div>
    <div class="plot-box">
      <div class="plot-box-title">Cross-section at X &nbsp;— drag slider to scan</div>
      <div id="slider-view"></div>
    </div>
  </div>
</main>

<script>
// ── Constants ──────────────────────────────────────────────────────────────────
const MAX_N      = 100;   // hard grid cap
const MAX_DRAW_N = 50;    // draw mode cap — cells ≥ 8 px in ~400 px display
const MAX_3D     = 500;   // max laser traces rendered in the 3D view
const X_A        = 0;
const X_B        = 80;
const X_C        = 160;
const MAX_SWAPS  = 500;   // swap-repair limit before giving up

// ── Mutable grid config ────────────────────────────────────────────────────────
let N       = 20;
let CELL_PX = 20;
function computeCellPx(n) { return Math.max(3, Math.floor(400 / n)); }

// ── State ──────────────────────────────────────────────────────────────────────
let litA = new Set();   // "col,row" keys for lit cells on Plane A (draw mode)
let litB = new Set();
let beamsVisible    = true;
let laserBaseIdx    = 0;
let laserTraceCount = 0;
let appMode         = 'draw';

// Upload mode state
const upload = {
  A: { rawLum: null, sortedIndices: null, mode: 'luminance' },
  B: { rawLum: null, sortedIndices: null, mode: 'luminance' },
};
let densityPct = 30;

// ── Grid construction ──────────────────────────────────────────────────────────
function buildGrid(svgId, litSet) {
  const svg = document.getElementById(svgId);
  const NS  = 'http://www.w3.org/2000/svg';
  svg.setAttribute('width',  N * CELL_PX);
  svg.setAttribute('height', N * CELL_PX);

  for (let row = 0; row < N; row++) {
    for (let col = 0; col < N; col++) {
      const rect = document.createElementNS(NS, 'rect');
      rect.setAttribute('x',      col * CELL_PX);
      rect.setAttribute('y',      row * CELL_PX);
      rect.setAttribute('width',  CELL_PX - 1);
      rect.setAttribute('height', CELL_PX - 1);
      rect.setAttribute('fill',   '#ffffff');
      rect.dataset.col = col;
      rect.dataset.row = row;
      rect.addEventListener('click', () => toggleCell(litSet, col, row, rect));
      svg.appendChild(rect);
    }
  }
}

function toggleCell(litSet, col, row, rect) {
  const key = `${col},${row}`;
  if (litSet.has(key)) {
    litSet.delete(key);
    rect.setAttribute('fill', '#ffffff');
  } else {
    litSet.add(key);
    rect.setAttribute('fill', '#1a1a2e');
  }
  updateCounter();
}

function updateCounter() {
  if (appMode === 'draw') {
    const na = litA.size, nb = litB.size;
    document.getElementById('counter').textContent = `B: ${nb} / A: ${na}`;
    document.getElementById('create-btn').disabled = (na !== nb || na === 0);
  } else {
    const T     = Math.round(densityPct / 100 * N * N);
    const ready = upload.A.sortedIndices !== null && upload.B.sortedIndices !== null && T > 0;
    document.getElementById('counter').textContent =
      ready ? `${T} lit cells per plane ✓` : 'Upload both images to begin';
    document.getElementById('create-btn').disabled = !ready;
  }
}

// ── Grid size control ──────────────────────────────────────────────────────────
function setN(n) {
  N       = Math.max(5, Math.min(MAX_N, Math.round(n) || 20));
  CELL_PX = computeCellPx(N);
  document.getElementById('n-input').value = N;
  buildHmapAxes();

  // Reset draw state
  litA = new Set(); litB = new Set();
  ['grid-a', 'grid-b'].forEach(id => { document.getElementById(id).innerHTML = ''; });
  buildGrid('grid-a', litA);
  buildGrid('grid-b', litB);

  // Reset upload state
  upload.A.rawLum = upload.A.sortedIndices = null;
  upload.B.rawLum = upload.B.sortedIndices = null;
  ['preview-A', 'preview-B'].forEach(id => {
    const c = document.getElementById(id);
    if (c) { c.width = c.height = N; c.getContext('2d').clearRect(0, 0, N, N); }
  });

  if (N > MAX_DRAW_N && appMode === 'draw') {
    setMode('upload');
    document.getElementById('mode-note').classList.remove('hidden');
  } else {
    document.getElementById('mode-note').classList.add('hidden');
  }

  updateCounter();
  document.getElementById('output').classList.add('hidden');
}

// ── Mode switching ─────────────────────────────────────────────────────────────
function setMode(mode) {
  appMode = mode;
  document.getElementById('draw-panel').classList.toggle('hidden', mode !== 'draw');
  document.getElementById('upload-panel').classList.toggle('hidden', mode !== 'upload');
  document.getElementById('tab-draw').classList.toggle('active', mode === 'draw');
  document.getElementById('tab-upload').classList.toggle('active', mode === 'upload');
  updateCounter();
}

// ── Upload mode ────────────────────────────────────────────────────────────────
function applySobel(lum, n) {
  const mag = new Float32Array(n * n);
  for (let r = 1; r < n - 1; r++) {
    for (let c = 1; c < n - 1; c++) {
      const gx = -lum[(r-1)*n+(c-1)] - 2*lum[r*n+(c-1)] - lum[(r+1)*n+(c-1)]
                + lum[(r-1)*n+(c+1)] + 2*lum[r*n+(c+1)] + lum[(r+1)*n+(c+1)];
      const gy = -lum[(r-1)*n+(c-1)] - 2*lum[(r-1)*n+c] - lum[(r-1)*n+(c+1)]
                + lum[(r+1)*n+(c-1)] + 2*lum[(r+1)*n+c] + lum[(r+1)*n+(c+1)];
      mag[r*n+c] = Math.sqrt(gx*gx + gy*gy);
    }
  }
  return mag;
}

function recomputeRanked(which) {
  const { rawLum, mode } = upload[which];
  if (!rawLum) return;
  const vals = mode === 'edges' ? applySobel(rawLum, N) : rawLum;
  const idx  = Array.from({ length: N * N }, (_, i) => i);
  // Edges: highest gradient first (lit = strong edge).
  // Luminance: darkest pixel first (lit = dark).
  idx.sort(mode === 'edges'
    ? (a, b) => vals[b] - vals[a]
    : (a, b) => vals[a] - vals[b]);
  upload[which].sortedIndices = idx;
}

function updatePreview(which) {
  const { sortedIndices } = upload[which];
  if (!sortedIndices) return;
  const T      = Math.round(densityPct / 100 * N * N);
  const litSet = new Set(sortedIndices.slice(0, T));
  const canvas = document.getElementById(`preview-${which}`);
  canvas.width = canvas.height = N;
  const ctx    = canvas.getContext('2d');
  const imgData = ctx.createImageData(N, N);
  for (let i = 0; i < N * N; i++) {
    const v = litSet.has(i) ? 0 : 255;
    imgData.data[i*4] = imgData.data[i*4+1] = imgData.data[i*4+2] = v;
    imgData.data[i*4+3] = 255;
  }
  ctx.putImageData(imgData, 0, 0);
}

function handleUpload(event, which) {
  const file = event.target.files[0];
  if (!file) return;
  const img = new Image();
  img.onload = () => {
    const oc  = document.createElement('canvas');
    oc.width  = oc.height = N;
    const ctx = oc.getContext('2d');
    ctx.drawImage(img, 0, 0, N, N);
    const { data } = ctx.getImageData(0, 0, N, N);
    const lum = new Float32Array(N * N);
    for (let i = 0; i < N * N; i++)
      lum[i] = 0.299 * data[i*4] + 0.587 * data[i*4+1] + 0.114 * data[i*4+2];
    upload[which].rawLum = lum;
    recomputeRanked(which);
    updatePreview(which);
    updateCounter();
    URL.revokeObjectURL(img.src);
  };
  img.src = URL.createObjectURL(file);
}

function setPreproc(which, mode) {
  upload[which].mode = mode;
  const isEdge = mode === 'edges';
  document.getElementById(`pp-${which}-lum`).classList.toggle('active', !isEdge);
  document.getElementById(`pp-${which}-edg`).classList.toggle('active',  isEdge);
  recomputeRanked(which);
  updatePreview(which);
}

function updateDensity(pct) {
  densityPct = parseInt(pct);
  const T = Math.round(densityPct / 100 * N * N);
  document.getElementById('density-label').textContent = `${densityPct}% — ${T} cells`;
  updatePreview('A');
  updatePreview('B');
  updateCounter();
}

function getUploadPoints(which) {
  const { sortedIndices } = upload[which];
  if (!sortedIndices) return null;
  const T   = Math.round(densityPct / 100 * N * N);
  const pts = [];
  for (let k = 0; k < T; k++) {
    const idx = sortedIndices[k];
    pts.push(cellToYZ(idx % N, Math.floor(idx / N)));
  }
  return pts;
}

// ── Heatmap axis arrays (rebuilt whenever N changes) ──────────────────────────
let HMAP_X = [], HMAP_Y = [];
function buildHmapAxes() {
  HMAP_X = Array.from({ length: N }, (_, i) => cellToYZ(i, 0).y);
  HMAP_Y = Array.from({ length: N }, (_, i) => cellToYZ(0, i).z);
}

// ── Coordinate helpers ─────────────────────────────────────────────────────────
// Maps (col, row) to physical YZ in [-10, 10] × [-10, 10] for any N.
// Cell centres are evenly spaced with step = 20/N.
function cellToYZ(col, row) {
  const step = 20 / N;
  return { y: (col + 0.5) * step - 10, z: 10 - (row + 0.5) * step };
}

// Returns lit points in raster order (top→bottom, left→right within each row)
function getPoints(litSet) {
  const pts = [];
  for (let row = 0; row < N; row++)
    for (let col = 0; col < N; col++)
      if (litSet.has(`${col},${row}`))
        pts.push(cellToYZ(col, row));
  return pts;
}

// Back-project one step beyond B to find the laser source on Plane C.
// Since the three planes are equally spaced (80 units), C = B + (B − A) = 2B − A.
function computeC(a, b) {
  return { y: 2 * b.y - a.y, z: 2 * b.z - a.z };
}

// ── Pairing strategies ─────────────────────────────────────────────────────────
// Each function accepts aPoints and bPoints (raster-ordered) and returns
// an array of { a, b } pairs aligned with aPoints order.

function pairMinAngle(aPoints, bPoints) {
  // Sort both by diagonal (y+z), pair in the same order → minimises average displacement.
  const sa = [...aPoints].sort((a, b) => (a.y + a.z) - (b.y + b.z));
  const sb = [...bPoints].sort((a, b) => (a.y + a.z) - (b.y + b.z));
  return sa.map((a, i) => ({ a, b: sb[i] }));
}

function pairMaxAngle(aPoints, bPoints) {
  // Sort A ascending, B descending → maximises average displacement.
  const sa = [...aPoints].sort((a, b) => (a.y + a.z) - (b.y + b.z));
  const sb = [...bPoints].sort((a, b) => (b.y + b.z) - (a.y + a.z));
  return sa.map((a, i) => ({ a, b: sb[i] }));
}

function pairRandom(aPoints, bPoints) {
  // Fisher-Yates shuffle of B, then zip with A in raster order.
  const shuffled = [...bPoints];
  for (let i = shuffled.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [shuffled[i], shuffled[j]] = [shuffled[j], shuffled[i]];
  }
  return aPoints.map((a, i) => ({ a, b: shuffled[i] }));
}

// ── Collision detection & repair ───────────────────────────────────────────────

// O(n) hash-map collision detection: two C-origins collide within the 0.1×0.1 hitbox.
function cKey(c) {
  return `${Math.round(c.y / 0.1)},${Math.round(c.z / 0.1)}`;
}

function findFirstCollision(aArr, bArr) {
  const seen = new Map();
  for (let i = 0; i < aArr.length; i++) {
    const k = cKey(computeC(aArr[i], bArr[i]));
    if (seen.has(k)) return { found: true, i: seen.get(k), j: i };
    seen.set(k, i);
  }
  return { found: false };
}

// Iteratively swap B-assignments until all C-origin collisions are resolved,
// or MAX_SWAPS is exhausted.
function repairCollisions(aArr, initialBArr) {
  const bs = [...initialBArr];
  const n  = bs.length;

  for (let s = 0; s < MAX_SWAPS; s++) {
    const col = findFirstCollision(aArr, bs);
    if (!col.found) return { bs, success: true };

    // Swap bs[col.i] with a randomly chosen third laser (not col.j) to avoid
    // trivial two-way swap cycles. For n=2, the only option is col.j itself.
    let k;
    if (n === 2) {
      k = col.j;
    } else {
      do { k = Math.floor(Math.random() * n); } while (k === col.i || k === col.j);
    }
    [bs[col.i], bs[k]] = [bs[k], bs[col.i]];
  }
  return { bs, success: false };
}

// ── Frame precomputation ───────────────────────────────────────────────────────

// Linearly interpolate every laser at each integer X from 0 to 160.
// Returns 161 N×N grids where 1 = illuminated, 0 = dark.
function precomputeFrames(pairs) {
  const frames = [];
  for (let x = 0; x <= X_C; x++) {
    const t    = x / X_C;
    const grid = Array.from({ length: N }, () => new Array(N).fill(0));

    for (const { a, c } of pairs) {
      const y = a.y + (c.y - a.y) * t;
      const z = a.z + (c.z - a.z) * t;

      // Inverse of cellToYZ: map continuous YZ back to nearest grid cell.
      const col = Math.round((y + 10) * N / 20 - 0.5);
      const row = Math.round((10 - z) * N / 20 - 0.5);

      if (col >= 0 && col < N && row >= 0 && row < N)
        grid[row][col] = 1;
    }
    frames.push(grid);
  }
  return frames;
}

// ── 3D render ──────────────────────────────────────────────────────────────────
function render3D(pairs, aPoints, bPoints) {
  const traces = [];

  // Plane boundary rectangles (corners connected as closed polylines)
  [
    [X_A, 'Plane A (x=0)',   '#5588bb'],
    [X_B, 'Plane B (x=80)',  '#bb8855'],
    [X_C, 'Plane C (x=160)', '#55aa77'],
  ].forEach(([xv, name, color]) => {
    traces.push({
      type: 'scatter3d', mode: 'lines',
      x: [xv, xv,  xv,  xv, xv],
      y: [-10, 10,  10, -10, -10],
      z: [-10, -10, 10,  10, -10],
      line: { color, width: 2 },
      name, hoverinfo: 'skip',
    });
  });

  // Lit cell markers on Plane A
  traces.push({
    type: 'scatter3d', mode: 'markers',
    x: aPoints.map(() => X_A),
    y: aPoints.map(p => p.y),
    z: aPoints.map(p => p.z),
    marker: { size: 5, color: '#0071e3', symbol: 'square', opacity: 0.9 },
    name: 'A pixels',
    hovertemplate: 'A  y=%{y}  z=%{z}<extra></extra>',
  });

  // Lit cell markers on Plane B
  traces.push({
    type: 'scatter3d', mode: 'markers',
    x: bPoints.map(() => X_B),
    y: bPoints.map(p => p.y),
    z: bPoints.map(p => p.z),
    marker: { size: 5, color: '#bf5af2', symbol: 'square', opacity: 0.9 },
    name: 'B pixels',
    hovertemplate: 'B  y=%{y}  z=%{z}<extra></extra>',
  });

  // Sample laser traces for large pair counts so the 3D view stays responsive.
  let displayPairs = pairs;
  let sampledMsg   = '';
  if (pairs.length > MAX_3D) {
    const idx = Array.from({ length: pairs.length }, (_, i) => i);
    for (let i = idx.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      [idx[i], idx[j]] = [idx[j], idx[i]];
    }
    displayPairs = idx.slice(0, MAX_3D).map(i => pairs[i]);
    sampledMsg   = `3D showing ${MAX_3D} of ${pairs.length} beams (sampled)`;
  }
  document.getElementById('sample-label').textContent = sampledMsg;

  // First laser trace starts at this index (used by toggleBeams)
  laserBaseIdx    = traces.length;
  laserTraceCount = displayPairs.length;

  // One trace per laser, coloured by index across 280° of the HSL wheel
  displayPairs.forEach(({ a, b, c }, i) => {
    const hue = Math.round((i / displayPairs.length) * 280);
    traces.push({
      type: 'scatter3d', mode: 'lines',
      x: [X_C, X_B, X_A],
      y: [c.y,  b.y, a.y],
      z: [c.z,  b.z, a.z],
      line: { color: `hsl(${hue},75%,62%)`, width: 2 },
      name: `Laser ${i + 1}`,
      showlegend: false,
      hovertemplate:
        `Laser ${i + 1}<br>` +
        `C (${c.y.toFixed(1)}, ${c.z.toFixed(1)}) → ` +
        `B (${b.y.toFixed(1)}, ${b.z.toFixed(1)}) → ` +
        `A (${a.y.toFixed(1)}, ${a.z.toFixed(1)})<extra></extra>`,
    });
  });

  const layout = {
    scene: {
      xaxis: { title: 'X', color: '#aaa', gridcolor: '#282828', range: [-5, 165] },
      yaxis: { title: 'Y', color: '#aaa', gridcolor: '#282828', range: [-12, 12] },
      zaxis: { title: 'Z', color: '#aaa', gridcolor: '#282828', range: [-12, 12] },
      bgcolor: '#0a0a14',
      // Stretch X visually to reflect the 160:20 physical aspect ratio
      aspectmode: 'manual',
      aspectratio: { x: 4, y: 1, z: 1 },
      // Camera: from the C side (high +X), offset in −Y and +Z so all beams are visible
      camera: {
        eye:    { x: 1.9, y: -1.5, z: 0.75 },
        center: { x: 0.3, y: 0,    z: 0    },
        up:     { x: 0,   y: 0,    z: 1    },
      },
    },
    paper_bgcolor: '#0a0a14',
    font: { color: '#ccc', size: 11, family: 'monospace' },
    margin: { t: 10, b: 10, l: 0, r: 0 },
    height: 520,
    legend: {
      x: 0.01, y: 0.99, bgcolor: 'rgba(0,0,0,0.45)',
      font: { color: '#ccc', size: 10 },
    },
  };

  Plotly.react('laser-3d', traces, layout, { responsive: true });

  // Reset beam toggle state on every fresh Create
  beamsVisible = true;
  document.getElementById('toggle-btn').textContent = 'Hide Beams';
}

// ── Slider render ──────────────────────────────────────────────────────────────
function renderSlider(framesData) {
  const initialTrace = {
    type: 'heatmap',
    x: HMAP_X, y: HMAP_Y,   // Y and Z axis labels baked into the trace
    z: framesData[0],
    colorscale: [[0, '#f8f8f8'], [1, '#1a1a2e']],
    showscale: false,
    zmin: 0, zmax: 1,
    hovertemplate: 'y=%{x}  z=%{y}  lit=%{z}<extra></extra>',
  };

  const sliderSteps = framesData.map((_, i) => ({
    label: String(i),
    method: 'animate',
    args: [[`f${i}`], {
      mode: 'immediate',
      transition: { duration: 0 },
      frame: { duration: 0, redraw: true },
    }],
  }));

  const layout = {
    xaxis: { title: 'Y', zeroline: false, tickmode: 'auto', nticks: 11 },
    yaxis: { title: 'Z', zeroline: false, tickmode: 'auto', nticks: 11, scaleanchor: 'x' },
    margin: { t: 20, b: 90, l: 55, r: 20 },
    height: 520,
    paper_bgcolor: '#ffffff',
    plot_bgcolor:  '#f4f4f4',
    font: { family: 'monospace', size: 11 },
    sliders: [{
      active: 0,
      currentvalue: {
        prefix: 'x = ',
        visible: true,
        xanchor: 'center',
        font: { family: 'monospace', size: 13, color: '#333' },
      },
      pad: { t: 50, b: 10 },
      steps: sliderSteps,
    }],
  };

  // Each animation frame updates only z; x and y are inherited from the initial trace
  const animFrames = framesData.map((grid, i) => ({
    name: `f${i}`,
    data: [{ z: grid }],
  }));

  Plotly.purge('slider-view');
  Plotly.newPlot('slider-view', [initialTrace], layout, { responsive: true })
    .then(() => Plotly.addFrames('slider-view', animFrames));
}

// ── Beam toggle ────────────────────────────────────────────────────────────────
function toggleBeams() {
  beamsVisible = !beamsVisible;
  const idxs = Array.from({ length: laserTraceCount }, (_, i) => laserBaseIdx + i);
  Plotly.restyle('laser-3d', { visible: beamsVisible }, idxs);
  document.getElementById('toggle-btn').textContent =
    beamsVisible ? 'Hide Beams' : 'Show Beams';
}

// ── UI helpers ─────────────────────────────────────────────────────────────────
function showError(msg) {
  const box = document.getElementById('error-box');
  box.textContent = msg;
  box.classList.remove('hidden');
}
function clearError() {
  document.getElementById('error-box').classList.add('hidden');
}

// ── Main create action ─────────────────────────────────────────────────────────
function create() {
  clearError();

  let aPoints, bPoints;
  if (appMode === 'draw') {
    aPoints = getPoints(litA);
    bPoints = getPoints(litB);
  } else {
    aPoints = getUploadPoints('A');
    bPoints = getUploadPoints('B');
    if (!aPoints || !bPoints) { showError('Upload both images first.'); return; }
    if (aPoints.length === 0) { showError('Density is 0 — move the slider up.'); return; }
  }

  if (aPoints.length !== bPoints.length || aPoints.length === 0) {
    showError('Both grids must have the same number of lit cells.');
    return;
  }

  // Apply selected pairing strategy to get initial B-assignment for each A-point
  const stratKey = document.getElementById('strategy').value;
  let pairs;
  if      (stratKey === 'min') pairs = pairMinAngle(aPoints, bPoints);
  else if (stratKey === 'max') pairs = pairMaxAngle(aPoints, bPoints);
  else                         pairs = pairRandom(aPoints, bPoints);

  const aArr = pairs.map(p => p.a);
  const bArr = pairs.map(p => p.b);

  // Attempt to repair any Plane-C origin collisions by swapping B-assignments
  const { bs, success } = repairCollisions(aArr, bArr);
  if (!success) {
    showError(
      `No collision-free pairing found after ${MAX_SWAPS} swap attempts. ` +
      `Try a different strategy, or reduce the number of lit cells.`
    );
    return;
  }

  // Build final pairs with C-origins computed from the repaired B-assignments
  const finalPairs = aArr.map((a, i) => ({ a, b: bs[i], c: computeC(a, bs[i]) }));

  // Pre-compute all 161 cross-section frames before any rendering
  const frames = precomputeFrames(finalPairs);

  // Show output section first so Plotly can measure container dimensions
  document.getElementById('output').classList.remove('hidden');
  render3D(finalPairs, aPoints, bPoints);
  renderSlider(frames);
}

// ── Init ───────────────────────────────────────────────────────────────────────
buildHmapAxes();
buildGrid('grid-a', litA);
buildGrid('grid-b', litB);
updateCounter();
updateDensity(densityPct);
</script>
</body>
</html>
"""
