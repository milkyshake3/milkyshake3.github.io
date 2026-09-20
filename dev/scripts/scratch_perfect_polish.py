import os
import re

html_path = r"c:\Apps\personal site project\index.html"

with open(html_path, "r", encoding="utf-8") as f:
    html = f.read()

# -----------------------------------------------------------------------------
# 1. NEW CSS STYLES: CRT Overlay, HUD Brackets, Hero Telemetry Panel
# -----------------------------------------------------------------------------
new_css = """    /* ==========================================================================
       AEROSPACE CRT RASTER & TELEMETRY HUD OVERLAY
       Tactile CRT scanlines, peripheral vignette, corner brackets,
       and real-time flight telemetry readout.
       ========================================================================== */

    .crt-overlay {
      position: fixed;
      top: 0;
      left: 0;
      width: 100vw;
      height: 100vh;
      pointer-events: none;
      z-index: 2;
      background: 
        repeating-linear-gradient(
          0deg,
          rgba(0, 0, 0, 0.07) 0px,
          rgba(0, 0, 0, 0.07) 1px,
          transparent 1px,
          transparent 3px
        ),
        radial-gradient(
          circle at center,
          transparent 52%,
          rgba(8, 12, 45, 0.30) 85%,
          rgba(5, 8, 30, 0.60) 100%
        );
      mix-blend-mode: multiply;
    }

    /* Tactical HUD Corner Brackets */
    .hud-bracket {
      position: absolute;
      width: 22px;
      height: 22px;
      border-color: rgba(255, 255, 255, 0.40);
      pointer-events: none;
      z-index: 12;
      transition: border-color 0.3s ease;
    }
    .hud-tl { top: 5rem; left: 1.25rem; border-top: 2px solid; border-left: 2px solid; }
    .hud-tr { top: 5rem; right: 1.25rem; border-top: 2px solid; border-right: 2px solid; }
    .hud-bl { bottom: 1.5rem; left: 1.25rem; border-bottom: 2px solid; border-left: 2px solid; }
    .hud-br { bottom: 1.5rem; right: 1.25rem; border-bottom: 2px solid; border-right: 2px solid; }

    /* Tactical Aerospace Telemetry Panel (Top-Right Hero HUD) */
    .hero-telemetry-panel {
      position: absolute;
      top: 5rem;
      right: 1.5rem;
      z-index: 10;
      user-select: none;
      pointer-events: none;
      font-family: var(--font-mono);
      font-size: 0.66rem;
      line-height: 1.6;
      color: var(--text-dim);
      background: rgba(15, 22, 77, 0.45);
      backdrop-filter: blur(8px);
      border: 1px solid var(--panel-border);
      border-radius: 3px;
      padding: 0.6rem 0.9rem;
      text-align: right;
      letter-spacing: 0.06em;
      box-shadow: 0 4px 20px rgba(0, 0, 0, 0.25);
    }

    .telemetry-row {
      display: flex;
      justify-content: space-between;
      gap: 1.2rem;
    }

    .tel-label {
      color: var(--text-dim);
      font-weight: 500;
    }

    .tel-val {
      color: var(--text-white);
      font-weight: 700;
    }

    .tel-val.green {
      color: var(--accent-green);
      text-shadow: 0 0 8px rgba(0, 255, 102, 0.6);
    }

    .tel-val.cyan {
      color: var(--accent-cyan);
      text-shadow: 0 0 8px rgba(56, 244, 255, 0.6);
    }

    @media (max-width: 820px) {
      .hero-telemetry-panel {
        display: none; /* Hide secondary telemetry panel on small screens to keep mobile clean */
      }
      .hud-tl, .hud-tr, .hud-bl, .hud-br {
        display: none;
      }
    }
"""

css_anchor = "    /* Top-Left Integrated Wireframe ASCII Globe */"
assert css_anchor in html, "css_anchor not found in html"
html = html.replace(css_anchor, new_css + "\n" + css_anchor)

# -----------------------------------------------------------------------------
# 2. HTML MARKUP: CRT Overlay & Hero HUD
# -----------------------------------------------------------------------------
old_canvas_tag = '<canvas id="hero-scene-canvas" aria-hidden="true"></canvas>'
new_canvas_tag = '<canvas id="hero-scene-canvas" aria-hidden="true"></canvas>\n  <div class="crt-overlay" aria-hidden="true"></div>'
assert old_canvas_tag in html, "old_canvas_tag not found in html"
html = html.replace(old_canvas_tag, new_canvas_tag)

old_hero_start = '<section id="hero" class="hero-container">'
new_hero_start = """<section id="hero" class="hero-container">

      <!-- Tactical HUD Viewport Brackets -->
      <div class="hud-bracket hud-tl" aria-hidden="true"></div>
      <div class="hud-bracket hud-tr" aria-hidden="true"></div>
      <div class="hud-bracket hud-bl" aria-hidden="true"></div>
      <div class="hud-bracket hud-br" aria-hidden="true"></div>

      <!-- Real-Time Aerospace Flight Telemetry Panel -->
      <div class="hero-telemetry-panel" id="hero-telemetry-panel" aria-hidden="true">
        <div class="telemetry-row"><span class="tel-label">SYSTEM</span><span class="tel-val green">● OPSEC // ARMED</span></div>
        <div class="telemetry-row"><span class="tel-label">FLIGHT</span><span class="tel-val cyan" id="tel-flight">LIFT +0.2G</span></div>
        <div class="telemetry-row"><span class="tel-label">ATTITUDE</span><span class="tel-val" id="tel-attitude">+0.4° / -1.2°</span></div>
        <div class="telemetry-row"><span class="tel-label">RANGE</span><span class="tel-val" id="tel-range">4.82 NM</span></div>
        <div class="telemetry-row"><span class="tel-label">BEARING</span><span class="tel-val" id="tel-bearing">042° TRUE</span></div>
        <div class="telemetry-row"><span class="tel-label">GRID PHASE</span><span class="tel-val" id="tel-phase">10.00 px</span></div>
      </div>"""
assert old_hero_start in html, "old_hero_start not found in html"
html = html.replace(old_hero_start, new_hero_start)

# -----------------------------------------------------------------------------
# 3. CANVAS ENGINE: Script Replacement
# -----------------------------------------------------------------------------
# Find script boundaries
start_script_str = "      // -----------------------------------------------------------------------\n      // 2. PROCEDURAL FILM GRAIN TEXTURE (Tactile analog depth for Cobalt sky)\n      // -----------------------------------------------------------------------"
end_script_str = "    // -------------------------------------------------------------------------\n    // 2. HIGH-DETAIL ROTATING WIREFRAME ASCII GLOBE (Top-Left Ambient Telemetry)\n    // -------------------------------------------------------------------------"

assert start_script_str in html, "start_script_str not found in html"
assert end_script_str in html, "end_script_str not found in html"

new_engine_code = """      // -----------------------------------------------------------------------
      // 2. PROCEDURAL FILM GRAIN TEXTURE (Tactile analog depth for Cobalt sky)
      // -----------------------------------------------------------------------
      const grainCanvas = document.createElement('canvas');
      grainCanvas.width = 256;
      grainCanvas.height = 256;
      const grainCtx = grainCanvas.getContext('2d');
      const grainData = grainCtx.createImageData(256, 256);
      for (let i = 0; i < grainData.data.length; i += 4) {
        const noise = (Math.random() - 0.5) * 32;
        grainData.data[i] = 255;
        grainData.data[i + 1] = 255;
        grainData.data[i + 2] = 255;
        grainData.data[i + 3] = Math.max(0, Math.min(255, 14 + noise));
      }
      grainCtx.putImageData(grainData, 0, 0);
      let grainPattern = ctx.createPattern(grainCanvas, 'repeat');

      // -----------------------------------------------------------------------
      // 3. MULTI-LAYERED VOLUMETRIC CLOUDS (Matching reference footage)
      //    High cirrus wisps, mid cumulus stratus, and low atmospheric bank
      // -----------------------------------------------------------------------
      const clouds = [
        // High Altitude Cirrus (faint, wide, slow)
        { x: width * 0.05, y: height * 0.12, speed: 0.08, scale: 1.4, opacity: 0.38, depth: 0.2, type: 'cirrus' },
        { x: width * 0.60, y: height * 0.08, speed: 0.06, scale: 1.2, opacity: 0.32, depth: 0.2, type: 'cirrus' },
        // Mid Altitude Cumulus (photographic billowing puffs with dual-tone lighting)
        { x: width * 0.10, y: height * 0.48, speed: 0.16, scale: 1.15, opacity: 0.70, depth: 0.5, type: 'cumulus' },
        { x: width * 0.75, y: height * 0.30, speed: 0.13, scale: 0.95, opacity: 0.60, depth: 0.5, type: 'cumulus' },
        // Low Altitude Atmospheric Bank (wraps under and behind lower reticle line)
        { x: width * 0.55, y: height * 0.76, speed: 0.22, scale: 1.45, opacity: 0.78, depth: 0.8, type: 'cumulus' },
        { x: -width * 0.25, y: height * 0.68, speed: 0.18, scale: 1.30, opacity: 0.65, depth: 0.8, type: 'cumulus' }
      ];

      function drawVolumetricCloud(cloud, pxOffset, pyOffset) {
        ctx.save();
        const cx = cloud.x + pxOffset;
        const cy = cloud.y + pyOffset;
        const scale = cloud.scale;
        const opacity = cloud.opacity;

        if (cloud.type === 'cirrus') {
          // Soft elongated horizontal wisps
          const wisps = [
            { dx: 0, dy: 0, rx: 140 * scale, ry: 20 * scale, a: 0.22 * opacity },
            { dx: -60 * scale, dy: 6 * scale, rx: 100 * scale, ry: 16 * scale, a: 0.18 * opacity },
            { dx: 70 * scale, dy: -4 * scale, rx: 110 * scale, ry: 18 * scale, a: 0.20 * opacity }
          ];
          for (const w of wisps) {
            const grad = ctx.createRadialGradient(cx + w.dx, cy + w.dy, 0, cx + w.dx, cy + w.dy, w.rx);
            grad.addColorStop(0, `rgba(255, 255, 255, ${w.a})`);
            grad.addColorStop(0.55, `rgba(230, 240, 255, ${w.a * 0.5})`);
            grad.addColorStop(1, 'rgba(255, 255, 255, 0)');
            ctx.fillStyle = grad;
            ctx.beginPath();
            ctx.ellipse(cx + w.dx, cy + w.dy, w.rx, w.ry, 0, 0, Math.PI * 2);
            ctx.fill();
          }
        } else {
          // Volumetric cumulus with illuminated tops and cobalt-tinted undersides
          const puffs = [
            { dx: 0, dy: -10 * scale, rx: 80 * scale, ry: 42 * scale, a: 0.38 * opacity, top: true },
            { dx: -55 * scale, dy: 5 * scale, rx: 65 * scale, ry: 35 * scale, a: 0.30 * opacity, top: true },
            { dx: 60 * scale, dy: 0 * scale, rx: 70 * scale, ry: 38 * scale, a: 0.32 * opacity, top: true },
            { dx: -105 * scale, dy: 18 * scale, rx: 50 * scale, ry: 28 * scale, a: 0.22 * opacity, top: false },
            { dx: 110 * scale, dy: 14 * scale, rx: 58 * scale, ry: 30 * scale, a: 0.25 * opacity, top: false },
            { dx: 0, dy: 18 * scale, rx: 95 * scale, ry: 42 * scale, a: 0.36 * opacity, top: false },
            { dx: -40 * scale, dy: 22 * scale, rx: 75 * scale, ry: 34 * scale, a: 0.28 * opacity, top: false },
            { dx: 45 * scale, dy: 20 * scale, rx: 80 * scale, ry: 36 * scale, a: 0.30 * opacity, top: false }
          ];

          for (const p of puffs) {
            const grad = ctx.createRadialGradient(cx + p.dx, cy + p.dy, 0, cx + p.dx, cy + p.dy, p.rx);
            if (p.top) {
              grad.addColorStop(0, `rgba(255, 255, 255, ${p.a})`);
              grad.addColorStop(0.55, `rgba(240, 246, 255, ${p.a * 0.65})`);
              grad.addColorStop(1, 'rgba(255, 255, 255, 0)');
            } else {
              grad.addColorStop(0, `rgba(225, 238, 255, ${p.a})`);
              grad.addColorStop(0.60, `rgba(180, 205, 255, ${p.a * 0.45})`);
              grad.addColorStop(1, 'rgba(180, 205, 255, 0)');
            }
            ctx.fillStyle = grad;
            ctx.beginPath();
            ctx.ellipse(cx + p.dx, cy + p.dy, p.rx, p.ry, 0, 0, Math.PI * 2);
            ctx.fill();
          }
        }
        ctx.restore();
      }

      // -----------------------------------------------------------------------
      // 4. INTERACTIVE MULTI-PLANE MOUSE PARALLAX & TELEMETRY TRACKER
      // -----------------------------------------------------------------------
      let mouseX = width * 0.5;
      let mouseY = height * 0.4;
      let targetMouseX = mouseX;
      let targetMouseY = mouseY;

      window.addEventListener('mousemove', (e) => {
        targetMouseX = e.clientX;
        targetMouseY = e.clientY;
      });

      window.addEventListener('mouseleave', () => {
        targetMouseX = width * 0.5;
        targetMouseY = height * 0.4;
      });

      // HUD Telemetry DOM elements
      const telFlight = document.getElementById('tel-flight');
      const telAttitude = document.getElementById('tel-attitude');
      const telRange = document.getElementById('tel-range');
      const telBearing = document.getElementById('tel-bearing');

      // -----------------------------------------------------------------------
      // 5. SENSOR TELEMETRY ACCENT DOTS (In sky matching reference footage)
      // -----------------------------------------------------------------------
      const floatingDots = [
        { x: 0.14, y: 0.32, color: '#ff4747', size: 5, speed: 0.08, phase: 0 },
        { x: 0.22, y: 0.74, color: '#00ff66', size: 5, speed: 0.05, phase: 1.5 },
        { x: 0.42, y: 0.15, color: '#ffffff', size: 4, speed: 0.04, phase: 3.0 },
        { x: 0.88, y: 0.18, color: '#ff4747', size: 5, speed: 0.06, phase: 4.2 },
        { x: 0.76, y: 0.72, color: '#00ff66', size: 4, speed: 0.05, phase: 2.1 },
        { x: 0.94, y: 0.45, color: '#ffffff', size: 4, speed: 0.07, phase: 5.5 }
      ];

      // Sensor dots embedded in eagle coordinates (frame-relative)
      // Centroids from reference.mp4: red at (17, 33), green at (6, 29), (4, 32), (9, 34), (7, 38)
      const eagleSensorDots = [
        { c: 17, r: 33, col: '#ff4747', glow: 'rgba(255, 71, 71, 0.8)' },
        { c: 6, r: 29, col: '#00ff66', glow: 'rgba(0, 255, 102, 0.8)' },
        { c: 4, r: 32, col: '#00ff66', glow: 'rgba(0, 255, 102, 0.8)' },
        { c: 9, r: 34, col: '#00ff66', glow: 'rgba(0, 255, 102, 0.8)' },
        { c: 7, r: 38, col: '#00ff66', glow: 'rgba(0, 255, 102, 0.8)' }
      ];

      // -----------------------------------------------------------------------
      // 6. ANIMATION & RENDER ENGINE (Aerodynamic Heave, Banking & Parallax)
      // -----------------------------------------------------------------------
      const loopDuration = 3000; // 3.0s per complete flight cycle (calm, majestic, unhurried)
      const frameDuration = loopDuration / 24; // 125ms per bird pose

      function render(now) {
        ctx.clearRect(0, 0, width, height);

        // Exponential mouse smoothing
        mouseX += (targetMouseX - mouseX) * 0.055;
        mouseY += (targetMouseY - mouseY) * 0.055;

        const normX = (mouseX / width) - 0.5;   // -0.5 to +0.5
        const normY = (mouseY / height) - 0.5;  // -0.5 to +0.5

        // Multi-plane Parallax Offsets
        const cloudParallaxX = normX * 16;
        const cloudParallaxY = normY * 10;
        const gridParallaxX  = normX * 26;
        const gridParallaxY  = normY * 18;
        const eagleParallaxX = normX * 46;
        const eagleParallaxY = normY * 32;

        // 1. Cobalt Sky Gradient
        const skyGrad = ctx.createLinearGradient(0, 0, 0, height);
        skyGrad.addColorStop(0, '#22329e');
        skyGrad.addColorStop(0.45, '#2b3ca8');
        skyGrad.addColorStop(0.85, '#192477');
        skyGrad.addColorStop(1, '#0f1752');
        ctx.fillStyle = skyGrad;
        ctx.fillRect(0, 0, width, height);

        // Subtle Film Grain Overlay
        if (grainPattern) {
          ctx.fillStyle = grainPattern;
          ctx.fillRect(0, 0, width, height);
        }

        // 2. Multi-Layered Volumetric Clouds
        for (const cloud of clouds) {
          cloud.x += cloud.speed;
          if (cloud.x - 220 * cloud.scale > width) {
            cloud.x = -240 * cloud.scale;
          }
          drawVolumetricCloud(cloud, cloudParallaxX * cloud.depth, cloudParallaxY * cloud.depth);
        }

        // 3. Responsive Proportions & Scaling
        const isMobile = width < 768;
        const isShortScreen = height < 800;

        const scale = isMobile
          ? (width / 720) * 0.92
          : Math.min(width / 980, height / 1050) * 0.92;

        const dotPitch = 9.8 * scale;
        const dotSize = Math.max(2.8, 5.8 * scale);

        const refCenterX = 350;
        const refCenterY = 580;

        const baseCenterX = isMobile ? (width * 0.50) : (width * 0.58);
        const baseCenterY = isShortScreen ? (height * 0.36) : (height * 0.34);

        function toScreenX(rx) {
          return baseCenterX + (rx - refCenterX) * scale;
        }
        function toScreenY(ry) {
          return baseCenterY + (ry - refCenterY) * scale;
        }

        // 4. Aerodynamic Kinematics: Flapping Lift (Heave), Sway, and Dynamic Banking
        const flightTime = now * 0.00030;
        const progress = (now % loopDuration) / loopDuration;
        const flapPhase = progress * Math.PI * 2;

        // Vertical Heave: downstroke produces lift, glide descends gently
        const flapHeave = -Math.sin(flapPhase) * 8.5 * scale;
        const flapLiftG = (-Math.sin(flapPhase) * 0.4).toFixed(2);

        const swayX = Math.sin(flightTime) * 12 * scale;
        const driftY = Math.cos(flightTime * 0.75) * 8 * scale;

        // Dynamic Bank Angle: coupled to sway velocity + mouse position
        const bankAngle = Math.cos(flightTime) * 0.024 + normX * 0.045;
        const pitchAngle = Math.sin(flightTime * 0.75) * 0.015 - normY * 0.035;

        // Update DOM Telemetry readouts in real time
        if (telFlight && (now % 6 < 1)) {
          telFlight.textContent = `LIFT ${flapLiftG >= 0 ? '+' : ''}${flapLiftG}G`;
          if (telAttitude) {
            const pitchDeg = (pitchAngle * 180 / Math.PI).toFixed(1);
            const bankDeg = (bankAngle * 180 / Math.PI).toFixed(1);
            telAttitude.textContent = `${pitchDeg >= 0 ? '+' : ''}${pitchDeg}° / ${bankDeg >= 0 ? '+' : ''}${bankDeg}°`;
          }
          if (telRange && telBearing) {
            const mouseDist = Math.hypot(normX, normY);
            const rng = (4.82 + mouseDist * 2.4).toFixed(2);
            let brg = Math.round((Math.atan2(normY, normX) * 180 / Math.PI + 90 + 360) % 360);
            telRange.textContent = `${rng} NM`;
            telBearing.textContent = `${String(brg).padStart(3, '0')}° TRUE`;
          }
        }

        // 5. Subpixel Cosine Hermite Interpolation of the 4 Reticle Lines
        const rawIndex = progress * 24;
        const k0 = Math.floor(rawIndex) % 24;
        const k1 = (k0 + 1) % 24;
        const frac = rawIndex - Math.floor(rawIndex);
        const ease = 0.5 - 0.5 * Math.cos(frac * Math.PI);

        const curVLeft = RETICLE_KEYFRAMES[k0].vl + (RETICLE_KEYFRAMES[k1].vl - RETICLE_KEYFRAMES[k0].vl) * ease;
        const curVRight = RETICLE_KEYFRAMES[k0].vr + (RETICLE_KEYFRAMES[k1].vr - RETICLE_KEYFRAMES[k0].vr) * ease;
        const curHMid = RETICLE_KEYFRAMES[k0].hm + (RETICLE_KEYFRAMES[k1].hm - RETICLE_KEYFRAMES[k0].hm) * ease;
        const curHBot = RETICLE_KEYFRAMES[k0].hb + (RETICLE_KEYFRAMES[k1].hb - RETICLE_KEYFRAMES[k0].hb) * ease;

        const screenVLeft = toScreenX(curVLeft) + swayX + eagleParallaxX;
        const screenVRight = toScreenX(curVRight) + swayX + eagleParallaxX;
        const screenHMid = toScreenY(curHMid) + driftY + flapHeave + eagleParallaxY;
        const screenHBot = toScreenY(curHBot) + driftY + flapHeave + eagleParallaxY;

        // 6. Ambient Architectural Grid (Fills canvas with sleek CAD/telemetry lines & parallax)
        ctx.save();
        ctx.strokeStyle = 'rgba(255, 255, 255, 0.16)';
        ctx.lineWidth = 0.75;

        const hSpacing = 160 * scale;
        const vSpacing = 180 * scale;

        // Outer horizontal lines (above and below the focal reticle)
        ctx.beginPath();
        for (let y = screenHMid - hSpacing; y > 0; y -= hSpacing) {
          ctx.moveTo(0, y);
          ctx.lineTo(width, y);
        }
        for (let y = screenHBot + hSpacing; y < height; y += hSpacing) {
          ctx.moveTo(0, y);
          ctx.lineTo(width, y);
        }

        // Outer vertical lines (left and right of the focal reticle)
        for (let x = screenVLeft - vSpacing; x > 0; x -= vSpacing) {
          ctx.moveTo(x, 0);
          ctx.lineTo(x, height);
        }
        for (let x = screenVRight + vSpacing; x < width; x += vSpacing) {
          ctx.moveTo(x, 0);
          ctx.lineTo(x, height);
        }
        ctx.stroke();

        // Subtle dashed flight sector meridian line between screenHMid and screenHBot
        const midSectorY = (screenHMid + screenHBot) / 2;
        ctx.strokeStyle = 'rgba(255, 255, 255, 0.12)';
        ctx.setLineDash([4, 8]);
        ctx.beginPath();
        ctx.moveTo(0, midSectorY);
        ctx.lineTo(width, midSectorY);
        ctx.stroke();
        ctx.setLineDash([]);

        // Subtle architectural telemetry stamps & intersection crosses
        ctx.fillStyle = 'rgba(255, 255, 255, 0.30)';
        ctx.font = `600 ${Math.max(8, Math.round(9.5 * scale))}px ui-monospace, monospace`;

        const ambientCrosses = [
          [screenVLeft - vSpacing, screenHMid, 'SEC // 01'],
          [screenVRight + vSpacing, screenHMid, 'SEC // 02'],
          [screenVLeft - vSpacing, screenHBot, 'ALT // 12.4K'],
          [screenVRight + vSpacing, screenHBot, 'GRID // 10.0'],
          [screenVLeft - 2 * vSpacing, screenHMid, 'TEL // ON'],
          [screenVRight + 2 * vSpacing, screenHMid, 'TRK // 0x4F'],
          [screenVLeft - vSpacing, screenHMid - hSpacing, '+'],
          [screenVRight + vSpacing, screenHMid - hSpacing, '+'],
          [screenVLeft - vSpacing, screenHBot + hSpacing, '+'],
          [screenVRight + vSpacing, screenHBot + hSpacing, '+']
        ];

        for (const [cx, cy, label] of ambientCrosses) {
          if (cx > 0 && cx < width && cy > 0 && cy < height) {
            ctx.beginPath();
            ctx.moveTo(cx - 3, cy);
            ctx.lineTo(cx + 3, cy);
            ctx.moveTo(cx, cy - 3);
            ctx.lineTo(cx, cy + 3);
            ctx.stroke();
            if (label && label !== '+') {
              ctx.fillText(label, cx + 6, cy - 6);
            }
          }
        }

        // Pitch Ladder HUD Ticks along screenVRight
        const ladderSpacing = 40 * scale;
        const ladderTicks = [
          { dy: -ladderSpacing * 2, deg: '+10°' },
          { dy: -ladderSpacing, deg: '+05°' },
          { dy: 0, deg: ' 00°' },
          { dy: ladderSpacing, deg: '-05°' },
          { dy: ladderSpacing * 2, deg: '-10°' }
        ];
        ctx.strokeStyle = 'rgba(255, 255, 255, 0.28)';
        ctx.fillStyle = 'rgba(255, 255, 255, 0.35)';
        ctx.lineWidth = 1;
        for (const tick of ladderTicks) {
          const ly = screenHMid + tick.dy;
          if (ly > 0 && ly < height) {
            ctx.beginPath();
            ctx.moveTo(screenVRight + 4 * scale, ly);
            ctx.lineTo(screenVRight + 12 * scale, ly);
            ctx.stroke();
            ctx.fillText(tick.deg, screenVRight + 16 * scale, ly + 3);
          }
        }
        ctx.restore();

        // 7. Dynamic 4-Line Architectural Reticle (Moving in lockstep with the eagle)
        ctx.save();
        ctx.strokeStyle = 'rgba(255, 255, 255, 0.72)';
        ctx.lineWidth = 1;
        ctx.shadowColor = 'rgba(255, 255, 255, 0.50)';
        ctx.shadowBlur = 4;

        // Two horizontal lines across full width
        ctx.beginPath();
        ctx.moveTo(0, screenHMid);
        ctx.lineTo(width, screenHMid);
        ctx.moveTo(0, screenHBot);
        ctx.lineTo(width, screenHBot);

        // Two vertical lines across full height
        ctx.moveTo(screenVLeft, 0);
        ctx.lineTo(screenVLeft, height);
        ctx.moveTo(screenVRight, 0);
        ctx.lineTo(screenVRight, height);
        ctx.stroke();

        // Architectural crosshair ticks (±5px) at the 4 intersections
        const tick = 5;
        const intersections = [
          [screenVLeft, screenHMid],
          [screenVLeft, screenHBot],
          [screenVRight, screenHMid],
          [screenVRight, screenHBot]
        ];
        ctx.strokeStyle = 'rgba(255, 255, 255, 0.95)';
        ctx.lineWidth = 1.5;
        ctx.beginPath();
        for (const [ix, iy] of intersections) {
          ctx.moveTo(ix - tick, iy);
          ctx.lineTo(ix + tick, iy);
          ctx.moveTo(ix, iy - tick);
          ctx.lineTo(ix, iy + tick);
        }
        ctx.stroke();

        // Embedded sensor square dots directly on lines (matching reference footage)
        const dotSz = Math.max(3, 5.5 * scale);
        ctx.fillStyle = '#ffffff';
        ctx.shadowBlur = 6;
        // Dot on v_left
        ctx.fillRect(screenVLeft - dotSz / 2, screenHMid + 95 * scale, dotSz, dotSz);
        // Dot on v_right
        ctx.fillRect(screenVRight - dotSz / 2, screenHMid - 85 * scale, dotSz, dotSz);
        // Dot on h_mid at eagle throat intersection
        ctx.fillRect(screenVLeft + 250 * scale - dotSz / 2, screenHMid - dotSz / 2, dotSz, dotSz);
        ctx.restore();

        // 8. Floating Sensor Accent Dots (Red, Green, White in sky)
        ctx.save();
        for (const dot of floatingDots) {
          const dx = (dot.x * width + Math.sin(now * 0.001 + dot.phase) * 15) + cloudParallaxX;
          const dy = (dot.y * height + Math.cos(now * 0.001 + dot.phase) * 10) + cloudParallaxY;
          ctx.fillStyle = dot.color;
          ctx.shadowColor = dot.color;
          ctx.shadowBlur = 8;
          ctx.fillRect(dx, dy, dot.size, dot.size);
        }
        ctx.restore();

        // 9. Authentic 24-Frame Eagle Dot Matrix (Phosphor Core + Radiant Optical Bloom)
        if (typeof BIRD_FRAMES !== 'undefined' && BIRD_FRAMES && BIRD_FRAMES.length > 0) {
          const frameIndex = Math.floor(now / frameDuration) % BIRD_FRAMES.length;
          const currentDots = BIRD_FRAMES[frameIndex];

          const reticleCenterX = (screenVLeft + screenVRight) / 2;
          const reticleCenterY = (screenHMid + screenHBot) / 2;

          const eagleAnchorX = reticleCenterX - 15 * dotPitch;
          const eagleAnchorY = reticleCenterY - 38 * dotPitch;

          ctx.save();
          ctx.translate(reticleCenterX, reticleCenterY);
          ctx.rotate(bankAngle);
          ctx.translate(-reticleCenterX, -reticleCenterY);

          // Render eagle dots with authentic phosphor optical bloom
          for (let i = 0; i < currentDots.length; i++) {
            const d = currentDots[i];
            const c = d[0];
            const r = d[1];

            const px = eagleAnchorX + c * dotPitch;
            const py = eagleAnchorY + r * dotPitch;

            // Soft radiant bloom halo
            ctx.fillStyle = 'rgba(215, 235, 255, 0.28)';
            ctx.fillRect(px - 1, py - 1, dotSize + 2, dotSize + 2);

            // High-luminance white core
            ctx.fillStyle = '#ffffff';
            ctx.fillRect(px, py, dotSize, dotSize);
          }

          // Embedded authentic sensor dots inside the eagle body
          for (const sdot of eagleSensorDots) {
            const spx = eagleAnchorX + sdot.c * dotPitch;
            const spy = eagleAnchorY + sdot.r * dotPitch;
            // Vibrant glow halo
            ctx.fillStyle = sdot.glow;
            ctx.fillRect(spx - 1.5, spy - 1.5, dotSize + 3, dotSize + 3);
            // Core
            ctx.fillStyle = sdot.col;
            ctx.fillRect(spx, spy, dotSize, dotSize);
          }

          ctx.restore();

          // 10. Vertical Motto ("grow wings and fly") Synchronized to (screenVRight, screenHMid)
          ctx.save();
          ctx.fillStyle = 'rgba(255, 255, 255, 0.95)';
          ctx.shadowColor = 'rgba(255, 255, 255, 0.8)';
          ctx.shadowBlur = 6;
          const fontSize = Math.max(13, Math.round(16.5 * scale));
          ctx.font = `italic 500 ${fontSize}px Georgia, "Times New Roman", serif`;

          const textX = screenVRight + Math.max(12, 16 * scale);
          const textMetrics = ctx.measureText('grow wings and fly');
          const textLen = textMetrics.width;
          const textY = screenHMid + textLen + 6 * scale;

          ctx.translate(textX, textY);
          ctx.rotate(-Math.PI / 2);
          ctx.fillText('grow wings and fly', 0, 0);
          ctx.restore();
        }

        requestAnimationFrame(render);
      }

      requestAnimationFrame(render);
    })();\n\n"""

# Perform replacement
before_engine = html[:html.find(start_script_str)]
after_engine = html[html.find(end_script_str):]
html = before_engine + new_engine_code + after_engine

with open(html_path, "w", encoding="utf-8") as f:
    f.write(html)

print("SUCCESS: index.html updated with CRT overlay, HUD telemetry, and enhanced eagle engine!")
