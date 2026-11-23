/* AB Royal Steels — generated industrial artwork.
   Every element with [data-art] gets a canvas illustration of steel material.
   To use a real photograph instead, add its path to assets/js/photos.js under the element's data-key. */
(function () {
  'use strict';
  var C = { red: '#E31824', navy: '#102B55', char: '#17191E', grey: '#F3F4F6' };

  function rng(seedStr) {
    var h = 2166136261;
    for (var i = 0; i < seedStr.length; i++) { h ^= seedStr.charCodeAt(i); h = Math.imul(h, 16777619); }
    return function () { h += 0x6D2B79F5; var t = h; t = Math.imul(t ^ (t >>> 15), t | 1); t ^= t + Math.imul(t ^ (t >>> 7), t | 61); return ((t ^ (t >>> 14)) >>> 0) / 4294967296; };
  }
  function lg(ctx, x0, y0, x1, y1, stops) { var g = ctx.createLinearGradient(x0, y0, x1, y1); stops.forEach(function (s) { g.addColorStop(s[0], s[1]); }); return g; }
  function rg(ctx, x, y, r0, r1, stops) { var g = ctx.createRadialGradient(x, y, r0, x, y, r1); stops.forEach(function (s) { g.addColorStop(s[0], s[1]); }); return g; }
  function steel(l, a) { l = Math.max(0, Math.min(100, l)); return 'hsla(215,' + (8 + (100 - l) * 0.08) + '%,' + l + '%,' + (a == null ? 1 : a) + ')'; }

  function backdrop(ctx, w, h, tone) {
    ctx.fillStyle = lg(ctx, 0, 0, 0, h, tone === 'light'
      ? [[0, '#e9ecf1'], [1, '#c9ced8']]
      : [[0, '#0d1a33'], [0.55, '#0b1427'], [1, '#07090d']]);
    ctx.fillRect(0, 0, w, h);
  }
  function vignette(ctx, w, h, k) {
    ctx.fillStyle = rg(ctx, w * 0.5, h * 0.45, Math.min(w, h) * 0.2, Math.max(w, h) * 0.85, [[0, 'rgba(0,0,0,0)'], [1, 'rgba(4,8,18,' + (k || 0.65) + ')']]);
    ctx.fillRect(0, 0, w, h);
  }
  function grain(ctx, w, h, r, amt) {
    var n = Math.floor(w * h / 900);
    for (var i = 0; i < n; i++) {
      ctx.fillStyle = r() > 0.5 ? 'rgba(255,255,255,' + (amt * r()) + ')' : 'rgba(0,0,0,' + (amt * 1.4 * r()) + ')';
      ctx.fillRect(r() * w, r() * h, 1.2, 1.2);
    }
  }
  function redGlow(ctx, w, h, x, y, s) {
    ctx.globalCompositeOperation = 'screen';
    ctx.fillStyle = rg(ctx, x, y, 0, s, [[0, 'rgba(227,24,36,0.35)'], [1, 'rgba(227,24,36,0)']]);
    ctx.fillRect(0, 0, w, h);
    ctx.globalCompositeOperation = 'source-over';
  }

  /* ---- Round pipes / tubes, end-on, hex packed ---- */
  function pipes(ctx, w, h, r, o) {
    backdrop(ctx, w, h);
    var R = o.size || Math.max(w, h) / (o.dense ? 22 : 13);
    var rowH = R * 1.74, cols = Math.ceil(w / (R * 2)) + 2, rows = Math.ceil(h / rowH) + 2;
    var lx = w * 0.28, ly = -h * 0.2;
    for (var j = -1; j < rows; j++) {
      for (var i = -1; i < cols; i++) {
        var cx = i * R * 2.02 + (j % 2 ? R : 0) + (r() - 0.5) * R * 0.06, cy = j * rowH + (r() - 0.5) * R * 0.06;
        var rr = R * (0.92 + r() * 0.08);
        var d = Math.hypot(cx - w * 0.45, cy - h * 0.4) / Math.max(w, h);
        var base = 70 - d * 60 + (r() - 0.5) * 10;
        var ang = Math.atan2(ly - cy, lx - cx);
        ctx.beginPath(); ctx.arc(cx, cy, rr, 0, Math.PI * 2);
        ctx.fillStyle = lg(ctx, cx + Math.cos(ang) * rr, cy + Math.sin(ang) * rr, cx - Math.cos(ang) * rr, cy - Math.sin(ang) * rr,
          [[0, steel(base + 22)], [0.45, steel(base)], [1, steel(base - 35)]]);
        ctx.fill();
        var wall = o.wall || 0.14;
        var paint = r();
        if (paint < 0.05) { ctx.beginPath(); ctx.arc(cx, cy, rr * (1 - wall * 0.35), 0, Math.PI * 2); ctx.fillStyle = 'rgba(227,24,36,0.85)'; ctx.fill(); }
        ctx.beginPath(); ctx.arc(cx, cy, rr * (1 - wall), 0, Math.PI * 2);
        ctx.fillStyle = rg(ctx, cx - Math.cos(ang) * rr * 0.35, cy - Math.sin(ang) * rr * 0.35, rr * 0.05, rr, [[0, 'rgba(2,4,10,1)'], [0.7, 'rgba(10,16,30,1)'], [1, steel(base - 25)]]);
        ctx.fill();
        ctx.beginPath(); ctx.arc(cx, cy, rr * (1 - wall * 0.5), ang - 0.9, ang + 0.9);
        ctx.strokeStyle = 'rgba(255,255,255,' + (0.18 + r() * 0.2) + ')'; ctx.lineWidth = Math.max(1, rr * 0.03); ctx.stroke();
      }
    }
    redGlow(ctx, w, h, w * 0.85, h * 0.85, Math.max(w, h) * 0.5);
    vignette(ctx, w, h, 0.75);
  }

  /* ---- Square / rectangular hollow sections ---- */
  function boxes(ctx, w, h, r, o) {
    backdrop(ctx, w, h);
    var S = Math.max(w, h) / 11, rect = o.rect, gap = S * 0.06;
    var bw = rect ? S * 1.5 : S, bh = S;
    for (var y = -bh * 0.3; y < h + bh; y += bh + gap) {
      var off = (Math.round(y / (bh + gap)) % 2) * bw * 0.5;
      for (var x = -bw + off; x < w + bw; x += bw + gap) {
        var d = Math.hypot(x - w * 0.4, y - h * 0.35) / Math.max(w, h);
        var b = 72 - d * 60 + (r() - 0.5) * 10, t = bh * 0.11, rad = bh * 0.08;
        ctx.fillStyle = lg(ctx, x, y, x + bw, y + bh, [[0, steel(b + 18)], [0.5, steel(b)], [1, steel(b - 32)]]);
        roundRect(ctx, x, y, bw, bh, rad); ctx.fill();
        ctx.fillStyle = lg(ctx, x, y, x + bw, y + bh, [[0, '#020409'], [1, steel(b - 40)]]);
        roundRect(ctx, x + t, y + t, bw - 2 * t, bh - 2 * t, rad * 0.5); ctx.fill();
        if (r() < 0.07) { ctx.fillStyle = 'rgba(227,24,36,0.9)'; ctx.fillRect(x + t * 0.3, y + bh - t * 0.7, bw - t * 0.6, t * 0.4); }
        ctx.strokeStyle = 'rgba(255,255,255,0.22)'; ctx.lineWidth = 1; ctx.beginPath(); ctx.moveTo(x + rad, y + 1); ctx.lineTo(x + bw - rad, y + 1); ctx.stroke();
      }
    }
    redGlow(ctx, w, h, w * 0.1, h * 0.95, Math.max(w, h) * 0.45);
    vignette(ctx, w, h, 0.7);
  }
  function roundRect(ctx, x, y, w, h, r) { ctx.beginPath(); ctx.moveTo(x + r, y); ctx.arcTo(x + w, y, x + w, y + h, r); ctx.arcTo(x + w, y + h, x, y + h, r); ctx.arcTo(x, y + h, x, y, r); ctx.arcTo(x, y, x + w, y, r); ctx.closePath(); }

  /* ---- Structural profiles end-on: I/H beam, channel, angle ---- */
  function profilePath(ctx, kind, x, y, s) {
    var t = s * 0.12, f = s * 0.1; ctx.beginPath();
    if (kind === 'i' || kind === 'h') {
      var fw = kind === 'h' ? s : s * 0.62, ox = x + (s - fw) / 2;
      ctx.moveTo(ox, y); ctx.lineTo(ox + fw, y); ctx.lineTo(ox + fw, y + f); ctx.lineTo(x + s / 2 + t / 2, y + f);
      ctx.lineTo(x + s / 2 + t / 2, y + s - f); ctx.lineTo(ox + fw, y + s - f); ctx.lineTo(ox + fw, y + s); ctx.lineTo(ox, y + s);
      ctx.lineTo(ox, y + s - f); ctx.lineTo(x + s / 2 - t / 2, y + s - f); ctx.lineTo(x + s / 2 - t / 2, y + f); ctx.lineTo(ox, y + f);
    } else if (kind === 'c') {
      var cw = s * 0.5, cx = x + s * 0.25;
      ctx.moveTo(cx, y); ctx.lineTo(cx + cw, y); ctx.lineTo(cx + cw, y + f); ctx.lineTo(cx + t, y + f); ctx.lineTo(cx + t, y + s - f);
      ctx.lineTo(cx + cw, y + s - f); ctx.lineTo(cx + cw, y + s); ctx.lineTo(cx, y + s);
    } else {
      var aw = s * 0.8, ax = x + s * 0.1, ay = y + s * 0.1;
      ctx.moveTo(ax, ay); ctx.lineTo(ax + t, ay); ctx.lineTo(ax + t, ay + aw - t); ctx.lineTo(ax + aw, ay + aw - t); ctx.lineTo(ax + aw, ay + aw); ctx.lineTo(ax, ay + aw);
    }
    ctx.closePath();
  }
  function profiles(ctx, w, h, r, o) {
    backdrop(ctx, w, h);
    var S = Math.max(w, h) / (o.kind === 'a' ? 9 : 7.5), gap = S * 0.08;
    // depth extrusion first (shadow side), then face
    for (var y = -S * 0.4; y < h + S; y += S + gap) {
      for (var x = -S * 0.3 + ((y / (S + gap)) | 0) % 2 * S * 0.15; x < w + S; x += S + gap) {
        var d = Math.hypot(x - w * 0.45, y - h * 0.4) / Math.max(w, h), b = 70 - d * 55 + (r() - 0.5) * 8;
        for (var k = 6; k > 0; k--) { ctx.save(); ctx.translate(k * S * 0.012, k * S * 0.016); profilePath(ctx, o.kind, x, y, S); ctx.fillStyle = steel(b - 45 - k, 1); ctx.fill(); ctx.restore(); }
        profilePath(ctx, o.kind, x, y, S);
        ctx.fillStyle = lg(ctx, x, y, x + S, y + S, [[0, steel(b + 20)], [0.5, steel(b)], [1, steel(b - 28)]]); ctx.fill();
        ctx.strokeStyle = 'rgba(255,255,255,0.18)'; ctx.lineWidth = 1; ctx.stroke();
        if (r() < 0.03) { profilePath(ctx, o.kind, x, y, S); ctx.fillStyle = 'rgba(227,24,36,0.75)'; ctx.fill(); }
      }
    }
    redGlow(ctx, w, h, w * 0.9, h * 0.1, Math.max(w, h) * 0.45);
    vignette(ctx, w, h, 0.72);
  }

  /* ---- Solid bars / rods bundle ---- */
  function bars(ctx, w, h, r, o) {
    backdrop(ctx, w, h);
    var R = Math.max(w, h) / (o.square ? 34 : 40);
    for (var j = -1; j < h / (R * 1.8) + 2; j++) {
      for (var i = -1; i < w / (R * 2.05) + 2; i++) {
        var cx = i * R * 2.05 + (j % 2 ? R : 0) + (r() - 0.5) * R * 0.5, cy = j * R * 1.8 + (r() - 0.5) * R * 0.5;
        var d = Math.hypot(cx - w * 0.5, cy - h * 0.45) / Math.max(w, h), b = 68 - d * 70 + (r() - 0.5) * 14;
        ctx.fillStyle = rg(ctx, cx - R * 0.3, cy - R * 0.3, R * 0.1, R * 1.1, [[0, steel(b + 22)], [0.6, steel(b)], [1, steel(b - 30)]]);
        if (o.square) { ctx.fillRect(cx - R * 0.9, cy - R * 0.9, R * 1.8, R * 1.8); }
        else { ctx.beginPath(); ctx.arc(cx, cy, R * 0.94, 0, Math.PI * 2); ctx.fill(); }
        if (o.ribbed) { ctx.strokeStyle = 'rgba(0,0,0,0.35)'; ctx.lineWidth = R * 0.12; ctx.beginPath(); ctx.arc(cx, cy, R * 0.94, 0, Math.PI * 2); ctx.stroke(); ctx.beginPath(); ctx.moveTo(cx - R * 0.94, cy); ctx.lineTo(cx + R * 0.94, cy); ctx.stroke(); }
        if (r() < 0.015) { ctx.beginPath(); ctx.arc(cx, cy, R * 0.6, 0, Math.PI * 2); ctx.fillStyle = 'rgba(227,24,36,0.85)'; ctx.fill(); }
      }
    }
    redGlow(ctx, w, h, w * 0.15, h * 0.2, Math.max(w, h) * 0.45);
    vignette(ctx, w, h, 0.75);
  }

  /* ---- Stacked sheets / plates, side view in perspective ---- */
  function sheets(ctx, w, h, r, o) {
    backdrop(ctx, w, h);
    var hor = h * 0.18;
    ctx.fillStyle = lg(ctx, 0, hor, 0, h, [[0, '#0a1222'], [1, '#05070b']]); ctx.fillRect(0, hor, w, h);
    var stacks = o.stacks || 3;
    for (var s = 0; s < stacks; s++) {
      var sx = w * (0.02 + s * 0.36) - w * 0.04, sw = w * 0.44, top = h * (0.28 + (s % 2) * 0.06), bottom = h * 0.92;
      var layers = Math.floor((bottom - top) / Math.max(2.2, h / 120));
      var th = (bottom - top) / layers;
      for (var l = 0; l < layers; l++) {
        var y = top + l * th, jitter = (r() - 0.5) * w * 0.006;
        var b = 74 - (l / layers) * 34 + (r() - 0.5) * 8;
        var col = o.coated ? ['hsl(357,78%,' + (30 + b * 0.25) + '%)', 'hsl(216,68%,' + (12 + b * 0.18) + '%)', null][s % 3] : null;
        ctx.fillStyle = col || lg(ctx, sx, y, sx + sw, y, [[0, steel(b - 12)], [0.3, steel(b + 8)], [0.7, steel(b)], [1, steel(b - 20)]]);
        ctx.fillRect(sx + jitter, y, sw, th * 0.78);
        ctx.fillStyle = 'rgba(0,0,0,0.55)'; ctx.fillRect(sx + jitter, y + th * 0.78, sw, th * 0.22);
      }
      // top face in perspective
      ctx.beginPath(); ctx.moveTo(sx, top); ctx.lineTo(sx + sw, top); ctx.lineTo(sx + sw * 0.93, top - h * 0.07); ctx.lineTo(sx + sw * 0.07, top - h * 0.07); ctx.closePath();
      ctx.fillStyle = lg(ctx, sx, top - h * 0.07, sx + sw, top, [[0, steel(86)], [0.5, steel(64)], [1, steel(78)]]); ctx.fill();
      if (o.chequer) { ctx.save(); ctx.clip(); tread(ctx, sx, top - h * 0.07, sw, h * 0.07, r, 0.6); ctx.restore(); }
    }
    redGlow(ctx, w, h, w * 0.5, h * 0.05, Math.max(w, h) * 0.5);
    vignette(ctx, w, h, 0.6);
  }
  function tread(ctx, x0, y0, w, h, r, sc) {
    var s = 16 * (sc || 1);
    for (var y = y0; y < y0 + h + s; y += s) for (var x = x0 + ((y - y0) / s % 2) * s / 2; x < x0 + w + s; x += s) {
      var a = (((x + y) / s) | 0) % 2 ? 0.6 : -0.6;
      ctx.save(); ctx.translate(x, y); ctx.rotate(a); ctx.fillStyle = 'rgba(255,255,255,0.35)'; ctx.fillRect(-s * 0.3, -s * 0.06, s * 0.6, s * 0.12); ctx.fillStyle = 'rgba(0,0,0,0.4)'; ctx.fillRect(-s * 0.3, s * 0.06, s * 0.6, s * 0.05); ctx.restore();
    }
  }
  /* ---- Chequered plate close-up ---- */
  function chequer(ctx, w, h, r) {
    ctx.fillStyle = lg(ctx, 0, 0, w, h, [[0, steel(68)], [0.45, steel(50)], [1, steel(26)]]); ctx.fillRect(0, 0, w, h);
    var s = Math.max(w, h) / 22;
    for (var y = -s; y < h + s; y += s) for (var x = -s + ((y / s | 0) % 2) * s / 2; x < w + s; x += s) {
      var a = ((Math.round(x / (s / 2)) + Math.round(y / s)) % 2) ? 0.78 : -0.78;
      ctx.save(); ctx.translate(x, y); ctx.rotate(a);
      ctx.fillStyle = 'rgba(0,0,0,0.45)'; roundRect(ctx, -s * 0.34, -s * 0.06, s * 0.7, s * 0.17, s * 0.08); ctx.fill();
      ctx.fillStyle = 'rgba(255,255,255,0.42)'; roundRect(ctx, -s * 0.36, -s * 0.1, s * 0.7, s * 0.14, s * 0.07); ctx.fill();
      ctx.restore();
    }
    ctx.fillStyle = lg(ctx, 0, 0, w, h, [[0, 'rgba(255,255,255,0.18)'], [0.5, 'rgba(255,255,255,0)'], [1, 'rgba(0,0,0,0.3)']]); ctx.fillRect(0, 0, w, h);
    grain(ctx, w, h, r, 0.12);
    redGlow(ctx, w, h, w, h, Math.max(w, h) * 0.5); vignette(ctx, w, h, 0.55);
  }

  /* ---- Corrugated roofing sheets ---- */
  function roofing(ctx, w, h, r, o) {
    backdrop(ctx, w, h);
    var period = Math.max(w, h) / 18;
    for (var x = 0; x < w; x += 1) {
      var ph = (x % period) / period, v = o.trap ? (ph < 0.25 ? 1 : ph < 0.4 ? 1 - (ph - 0.25) / 0.15 * 1.4 : ph < 0.85 ? -0.4 : -0.4 + (ph - 0.85) / 0.15 * 1.4) : Math.cos(ph * Math.PI * 2);
      var b = 50 + v * 26 - (x / w) * 12;
      var base = o.coated ? 'hsl(357,' + (70 + v * 8) + '%,' + (30 + v * 14) + '%)' : steel(b);
      ctx.fillStyle = base; ctx.fillRect(x, 0, 1.2, h);
    }
    // sheet laps
    for (var y = h * 0.33; y < h; y += h * 0.33) { ctx.fillStyle = 'rgba(0,0,0,0.45)'; ctx.fillRect(0, y, w, 3); ctx.fillStyle = 'rgba(255,255,255,0.2)'; ctx.fillRect(0, y + 3, w, 1); }
    // fixings
    ctx.fillStyle = 'rgba(20,24,30,0.8)';
    for (var yy = h * 0.16; yy < h; yy += h * 0.33) for (var xx = period * (o.trap ? 0.12 : 0); xx < w; xx += period * 2) { ctx.beginPath(); ctx.arc(xx, yy, Math.max(2, period * 0.06), 0, 7); ctx.fill(); }
    ctx.fillStyle = lg(ctx, 0, 0, 0, h, [[0, 'rgba(255,255,255,0.14)'], [1, 'rgba(0,0,0,0.5)']]); ctx.fillRect(0, 0, w, h);
    vignette(ctx, w, h, 0.6);
  }

  /* ---- Steel coils ---- */
  function coils(ctx, w, h, r, o) {
    backdrop(ctx, w, h);
    var floor = h * 0.78;
    ctx.fillStyle = lg(ctx, 0, h * 0.5, 0, h, [[0, '#0b1426'], [1, '#040609']]); ctx.fillRect(0, h * 0.5, w, h);
    var n = 4, R = Math.min(h * 0.34, w / 5.2);
    for (var i = 0; i < n; i++) {
      var cx = w * (0.08 + i * 0.29), cy = floor - R, depth = R * 0.55;
      // body (cylinder seen 3/4) — side band
      ctx.fillStyle = lg(ctx, 0, cy - R, 0, cy + R, [[0, steel(80)], [0.35, steel(62)], [0.8, steel(30)], [1, steel(18)]]);
      ctx.beginPath(); ctx.ellipse(cx + depth, cy, R * 0.32, R, 0, -Math.PI / 2, Math.PI / 2); ctx.lineTo(cx, cy + R); ctx.ellipse(cx, cy, R * 0.32, R, 0, Math.PI / 2, -Math.PI / 2, true); ctx.closePath(); ctx.fill();
      for (var b = 0; b < 3; b++) { ctx.strokeStyle = 'rgba(16,43,85,0.9)'; ctx.lineWidth = R * 0.05; ctx.beginPath(); var bx = cx + depth * (0.25 + b * 0.25); ctx.ellipse(bx, cy, R * 0.32, R, 0, -Math.PI / 2, Math.PI / 2); ctx.stroke(); }
      // face
      ctx.save(); ctx.beginPath(); ctx.ellipse(cx, cy, R * 0.32, R, 0, 0, Math.PI * 2); ctx.clip();
      ctx.fillStyle = steel(56); ctx.fillRect(cx - R, cy - R, R * 2, R * 2);
      for (var k = 0; k < 26; k++) { var rr = R * (1 - k / 26 * 0.6); ctx.strokeStyle = k % 2 ? 'rgba(255,255,255,0.22)' : 'rgba(0,0,0,0.25)'; ctx.lineWidth = 1; ctx.beginPath(); ctx.ellipse(cx, cy, rr * 0.32, rr, 0, 0, Math.PI * 2); ctx.stroke(); }
      ctx.fillStyle = '#05080f'; ctx.beginPath(); ctx.ellipse(cx, cy, R * 0.32 * 0.4, R * 0.4, 0, 0, Math.PI * 2); ctx.fill();
      ctx.fillStyle = lg(ctx, cx - R * 0.3, 0, cx + R * 0.3, 0, [[0, 'rgba(255,255,255,0.25)'], [1, 'rgba(0,0,0,0.25)']]); ctx.fillRect(cx - R, cy - R, R * 2, R * 2);
      ctx.restore();
      ctx.fillStyle = 'rgba(0,0,0,0.5)'; ctx.beginPath(); ctx.ellipse(cx + depth * 0.5, floor + 6, R * 0.9, R * 0.08, 0, 0, 7); ctx.fill();
    }
    redGlow(ctx, w, h, w * 0.92, h * 0.25, Math.max(w, h) * 0.5);
    vignette(ctx, w, h, 0.6);
  }

  /* ---- Warehouse interior with racks ---- */
  function warehouse(ctx, w, h, r, o) {
    ctx.fillStyle = lg(ctx, 0, 0, 0, h, [[0, '#132a52'], [0.5, '#0c1a33'], [1, '#05070c']]); ctx.fillRect(0, 0, w, h);
    var vx = w * (o.vx || 0.58), vy = h * 0.46;
    // roof trusses
    ctx.strokeStyle = 'rgba(180,195,220,0.16)'; ctx.lineWidth = 1;
    for (var i = 0; i < 14; i++) {
      var t = Math.pow(i / 14, 1.6), y = vy - (vy + h * 0.1) * (1 - t) , xl = vx - (vx + w * 0.2) * (1 - t), xr = vx + (w * 1.2 - vx) * (1 - t);
      ctx.beginPath(); ctx.moveTo(xl, y + (vy - y) * 0.05); ctx.lineTo(vx, y - (vy - y) * 0.15); ctx.lineTo(xr, y + (vy - y) * 0.05); ctx.stroke();
    }
    // skylight strip
    ctx.fillStyle = lg(ctx, 0, 0, 0, vy, [[0, 'rgba(230,236,245,0.22)'], [1, 'rgba(230,236,245,0)']]);
    ctx.beginPath(); ctx.moveTo(vx - w * 0.12, 0); ctx.lineTo(vx + w * 0.12, 0); ctx.lineTo(vx + 4, vy); ctx.lineTo(vx - 4, vy); ctx.closePath(); ctx.fill();
    // light shafts
    ctx.globalCompositeOperation = 'screen';
    for (var s = 0; s < 3; s++) {
      var sx = vx + (s - 1) * w * 0.22;
      ctx.fillStyle = lg(ctx, sx, 0, sx, h, [[0, 'rgba(210,222,240,0.14)'], [1, 'rgba(210,222,240,0)']]);
      ctx.beginPath(); ctx.moveTo(sx - w * 0.03, 0); ctx.lineTo(sx + w * 0.03, 0); ctx.lineTo(sx + w * 0.12, h); ctx.lineTo(sx - w * 0.02, h); ctx.closePath(); ctx.fill();
    }
    ctx.globalCompositeOperation = 'source-over';
    // floor
    ctx.fillStyle = lg(ctx, 0, vy, 0, h, [[0, '#0d1526'], [1, '#05070b']]);
    ctx.beginPath(); ctx.moveTo(0, h); ctx.lineTo(w, h); ctx.lineTo(w, vy + h * 0.02); ctx.lineTo(0, vy + h * 0.02); ctx.closePath(); ctx.fill();
    // floor markings (red lane lines)
    ctx.strokeStyle = 'rgba(227,24,36,0.7)'; ctx.lineWidth = 2;
    [-0.16, 0.16].forEach(function (k) { ctx.beginPath(); ctx.moveTo(vx + k * w * 0.05, vy + 2); ctx.lineTo(vx + k * w * 3.2, h); ctx.stroke(); });
    // racks with long stock (pipes seen from the side) converging to the vanishing point
    [-1, 1].forEach(function (side) {
      var xn = vx + side * w * 0.95, xf = vx + side * w * 0.07, topN = vy - h * 0.62, botN = vy + h * 0.5, topF = vy - h * 0.06, botF = vy + h * 0.03;
      function lerp(a, b, t) { return a + (b - a) * t; }
      var lv = 5;
      for (var l = 0; l < lv; l++) {
        var t0 = (l + 0.15) / lv, t1 = (l + 0.85) / lv;
        var yn0 = lerp(topN, botN, t0), yn1 = lerp(topN, botN, t1), yf0 = lerp(topF, botF, t0), yf1 = lerp(topF, botF, t1);
        ctx.beginPath(); ctx.moveTo(xn, yn0); ctx.lineTo(xf, yf0); ctx.lineTo(xf, yf1); ctx.lineTo(xn, yn1); ctx.closePath();
        ctx.fillStyle = lg(ctx, 0, yn0, 0, yn1, [[0, steel(70)], [0.5, steel(46)], [1, steel(24)]]); ctx.fill();
        var lines = 9;
        for (var k = 1; k < lines; k++) { var tt = k / lines; ctx.strokeStyle = k % 2 ? 'rgba(0,0,0,0.45)' : 'rgba(255,255,255,0.22)'; ctx.lineWidth = 1; ctx.beginPath(); ctx.moveTo(xn, lerp(yn0, yn1, tt)); ctx.lineTo(xf, lerp(yf0, yf1, tt)); ctx.stroke(); }
        if (r() < 0.5) { var tc = 0.2 + r() * 0.5; ctx.strokeStyle = 'rgba(227,24,36,0.85)'; ctx.lineWidth = 2; ctx.beginPath(); ctx.moveTo(xn, lerp(yn0, yn1, tc)); ctx.lineTo(xf, lerp(yf0, yf1, tc)); ctx.stroke(); }
        // shelf beam
        ctx.beginPath(); ctx.moveTo(xn, yn1); ctx.lineTo(xf, yf1); ctx.lineTo(xf, yf1 + 1.5); ctx.lineTo(xn, yn1 + h * 0.025); ctx.closePath(); ctx.fillStyle = '#102B55'; ctx.fill();
      }
      for (var i = 0; i < 12; i++) {
        var t = 1 - Math.pow(i / 12, 0.55), x = lerp(xf, xn, t), top = lerp(topF, topN, t), bot = lerp(botF, botN, t);
        ctx.fillStyle = C.red; ctx.fillRect(x - Math.max(1, t * 7) / 2, top, Math.max(1, t * 7), bot - top);
      }
      ctx.fillStyle = lg(ctx, xn, 0, xf, 0, [[0, 'rgba(5,7,12,0.1)'], [1, 'rgba(12,26,51,0.75)']]);
      ctx.beginPath(); ctx.moveTo(xn, topN); ctx.lineTo(xf, topF); ctx.lineTo(xf, botF); ctx.lineTo(xn, botN); ctx.closePath(); ctx.fill();
    });
    if (o.fog !== false) { ctx.fillStyle = rg(ctx, vx, vy, 0, w * 0.5, [[0, 'rgba(160,180,210,0.18)'], [1, 'rgba(160,180,210,0)']]); ctx.fillRect(0, 0, w, h); }
    vignette(ctx, w, h, 0.7);
  }

  /* ---- Steel frame structure at dusk (construction / projects) ---- */
  function structure(ctx, w, h, r, o) {
    var sky = o.variant === 'night' ? [[0, '#07101f'], [0.6, '#102b55'], [1, '#1d2f52']] : [[0, '#0d2147'], [0.55, '#2a3f68'], [0.85, '#8a5a63'], [1, '#c8484f']];
    ctx.fillStyle = lg(ctx, 0, 0, 0, h, sky); ctx.fillRect(0, 0, w, h);
    var ground = h * (0.86 + r() * 0.04), floors = 4 + Math.floor(r() * 4), bays = 5 + Math.floor(r() * 5);
    var bx = w * (0.08 + r() * 0.12), bw = w * (0.55 + r() * 0.2), fh = (ground - h * (0.18 + r() * 0.14)) / floors, baw = bw / bays;
    ctx.strokeStyle = '#06090f'; ctx.fillStyle = '#06090f';
    for (var f = 0; f <= floors; f++) { var y = ground - f * fh; ctx.fillRect(bx, y - fh * 0.06, bw, fh * 0.06); }
    for (var b = 0; b <= bays; b++) { var x = bx + b * baw; ctx.fillRect(x - baw * 0.03, ground - floors * fh - fh * 0.06, baw * 0.06, floors * fh + fh * 0.06); }
    ctx.lineWidth = Math.max(1, baw * 0.02);
    for (var f2 = 0; f2 < floors; f2++) for (var b2 = 0; b2 < bays; b2++) if (r() < 0.35) { var x0 = bx + b2 * baw, y0 = ground - f2 * fh; ctx.beginPath(); ctx.moveTo(x0, y0); ctx.lineTo(x0 + baw, y0 - fh); ctx.moveTo(x0 + baw, y0); ctx.lineTo(x0, y0 - fh); ctx.stroke(); }
    // tower crane
    var cx = bx + bw * (0.6 + r() * 0.5), ct = h * 0.08, cw = Math.max(4, w * 0.012);
    ctx.fillRect(cx - cw / 2, ct, cw, ground - ct);
    ctx.lineWidth = 1; for (var y2 = ct; y2 < ground; y2 += cw * 1.4) { ctx.beginPath(); ctx.moveTo(cx - cw / 2, y2); ctx.lineTo(cx + cw / 2, y2 + cw * 1.4); ctx.stroke(); }
    ctx.fillRect(cx - w * 0.35, ct, w * 0.55, cw * 0.9);
    ctx.fillRect(cx + w * 0.12, ct, w * 0.06, cw * 2.2);
    ctx.beginPath(); ctx.moveTo(cx - w * 0.2, ct + cw); ctx.lineTo(cx - w * 0.2, ct + h * 0.32); ctx.lineWidth = 1; ctx.stroke();
    ctx.fillStyle = C.red; ctx.fillRect(cx - w * 0.2 - w * 0.025, ct + h * 0.32, w * 0.05, Math.max(3, h * 0.012)); ctx.fillStyle = '#06090f';
    ctx.fillStyle = 'rgba(227,24,36,1)'; ctx.beginPath(); ctx.arc(cx, ct - 3, 2.5, 0, 7); ctx.fill();
    ctx.fillStyle = '#05070b'; ctx.fillRect(0, ground, w, h - ground);
    ctx.fillStyle = lg(ctx, 0, ground - h * 0.1, 0, ground, [[0, 'rgba(5,7,11,0)'], [1, 'rgba(5,7,11,0.5)']]); ctx.fillRect(0, ground - h * 0.1, w, h * 0.1);
    grain(ctx, w, h, r, 0.06);
    vignette(ctx, w, h, 0.45);
  }

  /* ---- Steel portal-frame shed (warehouse construction / roofing projects) ---- */
  function shed(ctx, w, h, r, o) {
    ctx.fillStyle = lg(ctx, 0, 0, 0, h, [[0, '#0d2147'], [0.6, '#33466c'], [1, '#6f5865']]); ctx.fillRect(0, 0, w, h);
    var ground = h * 0.84, n = 9, x0 = w * 0.06, span = w * 0.88, eave = h * 0.36, apex = h * 0.2;
    ctx.fillStyle = '#05070b'; ctx.fillRect(0, ground, w, h);
    for (var i = 0; i < n; i++) {
      var t = i / (n - 1), sc = 0.55 + t * 0.45, cx = w * 0.5 + (x0 + span * 0.5 - w * 0.5) * 1, half = span * 0.5 * sc;
      var gy = ground - (1 - sc) * h * 0.1, ey = gy - (gy - eave) * sc, ay = gy - (gy - apex) * sc;
      ctx.strokeStyle = 'rgba(6,9,15,' + (0.35 + t * 0.65) + ')'; ctx.lineWidth = 2 + t * 6;
      ctx.beginPath(); ctx.moveTo(cx - half, gy); ctx.lineTo(cx - half, ey); ctx.lineTo(cx, ay); ctx.lineTo(cx + half, ey); ctx.lineTo(cx + half, gy); ctx.stroke();
    }
    if (o.clad) {
      ctx.fillStyle = 'rgba(16,43,85,0.92)';
      var cx2 = w * 0.5, half2 = span * 0.5;
      ctx.beginPath(); ctx.moveTo(cx2 - half2, ground); ctx.lineTo(cx2 - half2, eave); ctx.lineTo(cx2 - half2 * 0.55, eave - (eave - apex) * 0.45); ctx.lineTo(cx2 - half2 * 0.55, ground); ctx.closePath(); ctx.fill();
      for (var k = 0; k < 30; k++) { ctx.fillStyle = 'rgba(255,255,255,0.06)'; ctx.fillRect(cx2 - half2 + k * half2 * 0.45 / 30, eave - 40, 1, ground - eave + 40); }
    }
    ctx.strokeStyle = 'rgba(227,24,36,0.9)'; ctx.lineWidth = 3; ctx.beginPath(); ctx.moveTo(0, ground + 1); ctx.lineTo(w, ground + 1); ctx.stroke();
    grain(ctx, w, h, r, 0.05); vignette(ctx, w, h, 0.5);
  }

  /* ---- Fabrication: welding sparks over profiles ---- */
  function fabrication(ctx, w, h, r) {
    profiles(ctx, w, h, r, { kind: 'i' });
    ctx.fillStyle = 'rgba(5,8,14,0.55)'; ctx.fillRect(0, 0, w, h);
    var sx = w * 0.62, sy = h * 0.58;
    ctx.globalCompositeOperation = 'screen';
    ctx.fillStyle = rg(ctx, sx, sy, 0, Math.max(w, h) * 0.35, [[0, 'rgba(255,240,230,0.9)'], [0.08, 'rgba(255,120,110,0.55)'], [0.4, 'rgba(227,24,36,0.18)'], [1, 'rgba(227,24,36,0)']]);
    ctx.fillRect(0, 0, w, h);
    for (var i = 0; i < 140; i++) {
      var a = -Math.PI * (0.1 + r() * 0.8) - (r() < 0.3 ? Math.PI : 0) * 0, len = Math.max(w, h) * (0.04 + r() * 0.25);
      var ex = sx + Math.cos(a) * len, ey = sy + Math.sin(a) * len * 0.6 + len * len / Math.max(w, h) * 0.9;
      ctx.strokeStyle = 'rgba(255,' + (150 + r() * 100 | 0) + ',' + (120 + r() * 80 | 0) + ',' + (0.4 + r() * 0.6) + ')'; ctx.lineWidth = r() * 1.6 + 0.4;
      ctx.beginPath(); ctx.moveTo(sx, sy); ctx.quadraticCurveTo(sx + (ex - sx) * 0.5, sy + (ey - sy) * 0.2, ex, ey); ctx.stroke();
    }
    ctx.globalCompositeOperation = 'source-over';
    vignette(ctx, w, h, 0.6);
  }

  /* ---- Logistics: road + motion, used behind truck ---- */
  function road(ctx, w, h, r) {
    ctx.fillStyle = lg(ctx, 0, 0, 0, h, [[0, '#0a1a38'], [0.55, '#102b55'], [0.62, '#1b2a44'], [1, '#05070b']]); ctx.fillRect(0, 0, w, h);
    var hy = h * 0.6;
    ctx.fillStyle = '#080b12'; ctx.beginPath(); ctx.moveTo(0, h); ctx.lineTo(w, h); ctx.lineTo(w * 0.62, hy); ctx.lineTo(w * 0.5, hy); ctx.closePath(); ctx.fill();
    ctx.strokeStyle = 'rgba(255,255,255,0.5)'; ctx.lineWidth = 2;
    for (var i = 0; i < 12; i++) { var t0 = Math.pow(i / 12, 2), t1 = Math.pow((i + 0.5) / 12, 2); ctx.beginPath(); ctx.moveTo(w * 0.56 + (w * 0.2) * t0, hy + (h - hy) * t0); ctx.lineTo(w * 0.56 + (w * 0.2) * t1, hy + (h - hy) * t1); ctx.lineWidth = 1 + t1 * 6; ctx.stroke(); }
    ctx.globalCompositeOperation = 'screen';
    for (var k = 0; k < 40; k++) { var y = hy - r() * h * 0.5; ctx.fillStyle = 'rgba(227,24,36,' + (r() * 0.25) + ')'; ctx.fillRect(0, y, w, r() * 2); }
    ctx.globalCompositeOperation = 'source-over';
    vignette(ctx, w, h, 0.6);
  }

  var R = {
    pipes: pipes, 'pipes-dense': function (c, w, h, r) { pipes(c, w, h, r, { dense: true }); },
    'pipes-thin': function (c, w, h, r) { pipes(c, w, h, r, { wall: 0.07 }); },
    square: function (c, w, h, r) { boxes(c, w, h, r, {}); }, rect: function (c, w, h, r) { boxes(c, w, h, r, { rect: true }); },
    ibeam: function (c, w, h, r) { profiles(c, w, h, r, { kind: 'i' }); }, hbeam: function (c, w, h, r) { profiles(c, w, h, r, { kind: 'h' }); },
    channel: function (c, w, h, r) { profiles(c, w, h, r, { kind: 'c' }); }, angle: function (c, w, h, r) { profiles(c, w, h, r, { kind: 'a' }); },
    bars: function (c, w, h, r) { bars(c, w, h, r, {}); }, rebar: function (c, w, h, r) { bars(c, w, h, r, { ribbed: true }); }, squarebar: function (c, w, h, r) { bars(c, w, h, r, { square: true }); },
    sheets: function (c, w, h, r) { sheets(c, w, h, r, {}); }, 'sheets-coated': function (c, w, h, r) { sheets(c, w, h, r, { coated: true }); },
    plates: function (c, w, h, r) { sheets(c, w, h, r, { stacks: 2 }); },
    chequer: chequer, roofing: function (c, w, h, r) { roofing(c, w, h, r, {}); }, 'roofing-trap': function (c, w, h, r) { roofing(c, w, h, r, { trap: true, coated: true }); },
    coils: coils, warehouse: function (c, w, h, r) { warehouse(c, w, h, r, {}); }, 'warehouse-left': function (c, w, h, r) { warehouse(c, w, h, r, { vx: 0.4 }); },
    structure: function (c, w, h, r) { structure(c, w, h, r, {}); }, 'structure-night': function (c, w, h, r) { structure(c, w, h, r, { variant: 'night' }); },
    shed: function (c, w, h, r) { shed(c, w, h, r, {}); }, 'shed-clad': function (c, w, h, r) { shed(c, w, h, r, { clad: true }); },
    fabrication: fabrication, road: road
  };

  function paint(el) {
    var key = el.getAttribute('data-key'), photos = window.ABRS_PHOTOS || {};
    if (key && photos[key]) {
      if (!el.querySelector('img.art-photo')) { var img = new Image(); img.className = 'art-photo'; img.alt = el.getAttribute('data-alt') || ''; img.loading = 'lazy'; img.src = (window.ABRS_ROOT || '') + photos[key]; el.insertBefore(img, el.firstChild); }
      el.classList.add('has-photo'); return;
    }
    var type = el.getAttribute('data-art'), fn = R[type]; if (!fn) return;
    var cv = el.querySelector('canvas.art-canvas');
    if (!cv) { cv = document.createElement('canvas'); cv.className = 'art-canvas'; cv.setAttribute('aria-hidden', 'true'); el.insertBefore(cv, el.firstChild); }
    var rect = el.getBoundingClientRect(), w = Math.max(1, Math.round(rect.width)), h = Math.max(1, Math.round(rect.height));
    if (cv._w === w && cv._h === h) return;
    var dpr = Math.min(2, window.devicePixelRatio || 1);
    cv.width = w * dpr; cv.height = h * dpr; cv._w = w; cv._h = h;
    var ctx = cv.getContext('2d'); ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    fn(ctx, w, h, rng((key || type) + ':' + type), {});
  }
  function paintAll() { document.querySelectorAll('[data-art]').forEach(paint); }
  var t; window.addEventListener('resize', function () { clearTimeout(t); t = setTimeout(paintAll, 180); });
  window.ABRS_ART = { paint: paint, paintAll: paintAll, types: Object.keys(R) };
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', paintAll); else paintAll();
})();
