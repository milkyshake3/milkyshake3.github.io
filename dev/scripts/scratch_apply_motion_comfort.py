import re

html_path = r"c:\Apps\personal site project\index.html"

with open(html_path, "r", encoding="utf-8") as f:
    html = f.read()

# -----------------------------------------------------------------------------
# 1. Add CSS for Motion Toggle & Canvas Scroll Transition
# -----------------------------------------------------------------------------
css_canvas_old = """    /* Full-screen Background Living Canvas */
    #hero-scene-canvas {
      position: fixed;
      top: 0;
      left: 0;
      width: 100vw;
      height: 100vh;
      pointer-events: none;
      z-index: 0;
    }"""

css_canvas_new = """    /* Full-screen Background Living Canvas with Scroll-Driven Fade */
    #hero-scene-canvas {
      position: fixed;
      top: 0;
      left: 0;
      width: 100vw;
      height: 100vh;
      pointer-events: none;
      z-index: 0;
      transition: opacity 0.35s ease-out;
    }

    /* Motion Accessibility Control Button in Top Navigation */
    .nav-motion-control {
      display: flex;
      align-items: center;
    }

    .btn-motion {
      background: rgba(15, 22, 77, 0.75);
      border: 1px solid var(--panel-border);
      color: var(--text-soft);
      font-family: var(--font-mono);
      font-size: 0.72rem;
      font-weight: 600;
      letter-spacing: 0.06em;
      padding: 0.35rem 0.75rem;
      border-radius: 3px;
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      gap: 0.45rem;
      transition: all 0.2s ease;
      user-select: none;
    }

    .btn-motion:hover {
      border-color: var(--text-white);
      color: var(--text-white);
      background: rgba(255, 255, 255, 0.15);
      box-shadow: 0 0 12px rgba(255, 255, 255, 0.2);
    }

    .btn-motion[data-mode="STATIC"] {
      border-color: var(--accent-warm);
      color: var(--accent-warm);
    }

    .btn-motion[data-mode="VIVID"] {
      border-color: var(--accent-cyan);
      color: var(--accent-cyan);
    }

    @media (max-width: 600px) {
      .btn-motion span#motion-label {
        font-size: 0.65rem;
      }
    }"""

assert css_canvas_old in html, "css_canvas_old not found in html"
html = html.replace(css_canvas_old, css_canvas_new)

# -----------------------------------------------------------------------------
# 2. Add Motion Control Button to Top Navigation Markup
# -----------------------------------------------------------------------------
nav_old = """      <nav aria-label="Main Navigation">
        <ul class="nav-links">
          <li><a href="#about">about</a></li>
          <li><a href="#projects">projects</a></li>
          <li><a href="#skills">skills</a></li>
          <li><a href="#hire">hire me</a></li>
        </ul>
      </nav>
    </div>
  </header>"""

nav_new = """      <nav aria-label="Main Navigation">
        <ul class="nav-links">
          <li><a href="#about">about</a></li>
          <li><a href="#projects">projects</a></li>
          <li><a href="#skills">skills</a></li>
          <li><a href="#hire">hire me</a></li>
        </ul>
      </nav>
      <div class="nav-motion-control">
        <button id="motion-toggle-btn" class="btn-motion" data-mode="CALM" title="Cycle motion: CALM / VIVID / STATIC" aria-label="Motion control mode">
          <span class="motion-icon">⚙</span>
          <span id="motion-label">MOTION: CALM</span>
        </button>
      </div>
    </div>
  </header>"""

assert nav_old in html, "nav_old not found in html"
html = html.replace(nav_old, nav_new)

# -----------------------------------------------------------------------------
# 3. Update Script Engine with Motion Modes, Scroll Dimming & Zero Camera Sway
# -----------------------------------------------------------------------------
script_start_marker = "      // -----------------------------------------------------------------------\n      // 3. HEAVENLY VOLUMETRIC \"POCKETS OF DUST\" CLOUD FIELD (M83 Outro Aesthetic)"
script_end_marker = "    // -------------------------------------------------------------------------\n    // 2. HIGH-DETAIL ROTATING WIREFRAME ASCII GLOBE (Top-Left Ambient Telemetry)"

assert script_start_marker in html, "script_start_marker not found"
assert script_end_marker in html, "script_end_marker not found"

new_script_engine = """      // -----------------------------------------------------------------------
      // 3. MOTION ACCESSIBILITY & VESTIBULAR COMFORT CONTROLS
      //    Modes:
      //    - 'CALM'  (Default: Grounded camera, tranquil slow breathing, zero motion sickness)
      //    - 'VIVID' (Richer celestial god rays & starlight motes)
      //    - 'STATIC' (Frozen snapshot for vestibular disorders / migraine sensitivity)
      // -----------------------------------------------------------------------
      const MOTION_MODES = ['CALM', 'VIVID', 'STATIC'];
      const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
      let currentMotionMode = localStorage.getItem('noel_motion_mode') || (prefersReducedMotion ? 'STATIC' : 'CALM');

      const motionBtn = document.getElementById('motion-toggle-btn');
      const motionLabel = document.getElementById('motion-label');

      function updateMotionUI() {
        if (motionLabel) {
          motionLabel.textContent = `MOTION: ${currentMotionMode}`;
        }
        if (motionBtn) {
          motionBtn.setAttribute('data-mode', currentMotionMode);
        }
      }
      updateMotionUI();

      if (motionBtn) {
        motionBtn.addEventListener('click', () => {
          const nextIdx = (MOTION_MODES.indexOf(currentMotionMode) + 1) % MOTION_MODES.length;
          currentMotionMode = MOTION_MODES[nextIdx];
          localStorage.setItem('noel_motion_mode', currentMotionMode);
          updateMotionUI();
          if (currentMotionMode === 'STATIC') {
            requestAnimationFrame(render);
          }
        });
      }

      // Scroll-Driven Canvas Dimming (Fades canvas to 15% opacity when reading content)
      window.addEventListener('scroll', () => {
        const scrollY = window.scrollY;
        const heroH = window.innerHeight;
        const opacity = Math.max(0.15, Math.min(1.0, 1.0 - (scrollY / (heroH * 0.70)) * 0.85));
        canvas.style.opacity = opacity;
      }, { passive: true });

      // -----------------------------------------------------------------------
      // 3b. ANCHORED VOLUMETRIC "POCKETS OF DUST" CLOUD FIELD
      //     Immense, breathing atmospheric cloud deck with sunward silver/gold rim light.
      //     Zero conveyor-belt sliding; gentle organic billow undulation.
      // -----------------------------------------------------------------------
      const cloudCanvas = document.createElement('canvas');
      const cloudCtx = cloudCanvas.getContext('2d');

      const cloudPockets = [
        // Bottom-Right Grand Cloud Deck (immense sea of clouds behind eagle)
        { cx: 0.80, cy: 0.70, rx: 0.28, ry: 0.15, intensity: 0.94, phase: 0.0 },
        { cx: 0.64, cy: 0.76, rx: 0.22, ry: 0.12, intensity: 0.78, phase: 1.2 },
        { cx: 0.94, cy: 0.66, rx: 0.24, ry: 0.13, intensity: 0.85, phase: 2.4 },
        { cx: 0.72, cy: 0.63, rx: 0.18, ry: 0.09, intensity: 0.62, phase: 3.6 },
        { cx: 0.88, cy: 0.80, rx: 0.26, ry: 0.13, intensity: 0.80, phase: 4.8 },
        { cx: 0.54, cy: 0.82, rx: 0.18, ry: 0.10, intensity: 0.65, phase: 5.5 },
        { cx: 0.42, cy: 0.86, rx: 0.15, ry: 0.09, intensity: 0.55, phase: 1.8 },
        // Top-Left Stratospheric Wisps (bathed in high-altitude sunlight)
        { cx: 0.12, cy: 0.07, rx: 0.18, ry: 0.065, intensity: 0.68, phase: 0.8 },
        { cx: 0.22, cy: 0.05, rx: 0.13, ry: 0.048, intensity: 0.54, phase: 2.0 },
        { cx: 0.05, cy: 0.10, rx: 0.12, ry: 0.048, intensity: 0.46, phase: 3.2 },
        // Mid-Left Ethereal Cloud Bank
        { cx: 0.06, cy: 0.42, rx: 0.16, ry: 0.050, intensity: 0.48, phase: 4.0 },
        { cx: 0.16, cy: 0.40, rx: 0.11, ry: 0.042, intensity: 0.38, phase: 5.1 }
      ];

      let lastCloudUpdate = 0;
      function updateCloudField(now, w, h, isStatic) {
        if (!isStatic && (now - lastCloudUpdate < 32 && cloudCanvas.width > 0)) return;
        lastCloudUpdate = now;

        const cellPitch = 9.8;
        const gw = Math.max(20, Math.ceil(w / cellPitch));
        const gh = Math.max(20, Math.ceil(h / cellPitch));

        if (cloudCanvas.width !== gw || cloudCanvas.height !== gh) {
          cloudCanvas.width = gw;
          cloudCanvas.height = gh;
        }

        const imgData = cloudCtx.createImageData(gw, gh);
        const data = imgData.data;
        // In CALM mode, use slow tranquil breathing; in STATIC mode, freeze t
        const t = isStatic ? 0 : now * (currentMotionMode === 'VIVID' ? 0.00035 : 0.00018);

        for (let gy = 0; gy < gh; gy++) {
          const ny = gy / gh;
          for (let gx = 0; gx < gw; gx++) {
            const nx = gx / gw;
            let density = 0.0;

            for (let i = 0; i < cloudPockets.length; i++) {
              const p = cloudPockets[i];
              const pcx = p.cx + Math.sin(t + p.phase) * 0.008;
              const pcy = p.cy + Math.cos(t * 0.75 + p.phase) * 0.005;
              const prx = p.rx + Math.sin(t * 1.1 + p.phase) * 0.004;
              const pry = p.ry + Math.cos(t * 0.85 + p.phase) * 0.003;

              const dx = (nx - pcx) / prx;
              const dy = (ny - pcy) / pry;
              const d2 = dx * dx + dy * dy;
              if (d2 < 1.0) {
                density += p.intensity * Math.pow(1.0 - d2, 1.35);
              }
            }

            const idx = (gy * gw + gx) * 4;
            if (density > 0.02) {
              const jitter = Math.sin(gx * 12.9898 + gy * 78.233) * 0.08;
              const alpha = Math.max(0, Math.min(1.0, density + jitter));

              // Sunward rim lighting: top and right crests catch brilliant golden-white sunlight
              const isSunwardCrest = (ny < 0.70 && nx > 0.45) || (ny < 0.12);

              if (isSunwardCrest) {
                data[idx] = 255;
                data[idx + 1] = Math.round(252 - (1.0 - alpha) * 8);
                data[idx + 2] = Math.round(245 - (1.0 - alpha) * 12);
              } else if (ny > 0.75) {
                data[idx] = 255;
                data[idx + 1] = Math.round(232 - (1.0 - alpha) * 18);
                data[idx + 2] = Math.round(210 - (1.0 - alpha) * 25);
              } else {
                data[idx] = 248;
                data[idx + 1] = Math.round(242 - (1.0 - alpha) * 14);
                data[idx + 2] = Math.round(255 - (1.0 - alpha) * 8);
              }
              data[idx + 3] = Math.round(alpha * 225);
            } else {
              data[idx + 3] = 0;
            }
          }
        }
        cloudCtx.putImageData(imgData, 0, 0);
      }

      // Dynamic Crepuscular God Rays (Sunbeams streaming peacefully through stratosphere)
      function drawGodRays(now, w, h, mode) {
        const sunX = w * 0.84;
        const sunY = -h * 0.10;
        const numRays = mode === 'VIVID' ? 7 : 5;
        const rayAngles = [0.47, 0.53, 0.60, 0.67, 0.74, 0.80, 0.86];
        const rayWidths = [0.045, 0.075, 0.055, 0.085, 0.050, 0.065, 0.055];

        ctx.save();
        const rayLen = Math.max(w, h) * 1.45;
        const pulseRate = mode === 'VIVID' ? 0.0004 : 0.00015;
        const baseIntensity = mode === 'VIVID' ? 0.14 : 0.08;

        for (let i = 0; i < numRays; i++) {
          const rayPulse = mode === 'STATIC' ? baseIntensity : (Math.sin(now * pulseRate + i * 1.15) * 0.03 + baseIntensity);
          const angle = rayAngles[i] * Math.PI;
          const widthAngle = rayWidths[i] * Math.PI;

          const x1 = sunX + Math.cos(angle - widthAngle * 0.5) * rayLen;
          const y1 = sunY + Math.sin(angle - widthAngle * 0.5) * rayLen;
          const x2 = sunX + Math.cos(angle + widthAngle * 0.5) * rayLen;
          const y2 = sunY + Math.sin(angle + widthAngle * 0.5) * rayLen;

          const grad = ctx.createRadialGradient(sunX, sunY, 40, sunX, sunY, rayLen);
          grad.addColorStop(0, `rgba(255, 250, 235, ${rayPulse * 0.8})`);
          grad.addColorStop(0.5, `rgba(255, 246, 225, ${rayPulse * 0.35})`);
          grad.addColorStop(1, 'rgba(255, 255, 255, 0)');

          ctx.fillStyle = grad;
          ctx.beginPath();
          ctx.moveTo(sunX, sunY);
          ctx.lineTo(x1, y1);
          ctx.lineTo(x2, y2);
          ctx.closePath();
          ctx.fill();
        }
        ctx.restore();
      }

      // -----------------------------------------------------------------------
      // 3c. CELESTIAL FLOATING STARDUST (Tranquil, gentle floating motes)
      // -----------------------------------------------------------------------
      const DUST_COUNT = 32; // Reduced for serene visual comfort
      const stardustMotes = [];
      const moteColors = [
        'rgba(255, 248, 220, ',
        'rgba(255, 255, 255, ',
        'rgba(215, 242, 255, '
      ];

      for (let i = 0; i < DUST_COUNT; i++) {
        stardustMotes.push({
          x: Math.random() * width,
          y: Math.random() * height,
          sz: 2,
          vx: 0.04 + Math.random() * 0.08,
          vy: -(0.10 + Math.random() * 0.18),
          col: moteColors[Math.floor(Math.random() * moteColors.length)],
          baseAlpha: 0.16 + Math.random() * 0.32,
          twinkleSpeed: 0.0008 + Math.random() * 0.0012,
          phase: Math.random() * Math.PI * 2
        });
      }

      // -----------------------------------------------------------------------
      // 4. SENSOR TELEMETRY ACCENT DOTS & DOM READOUTS
      // -----------------------------------------------------------------------
      const floatingDots = [
        { x: 0.14, y: 0.32, color: '#ff4747', size: 5, phase: 0 },
        { x: 0.22, y: 0.74, color: '#00ff66', size: 5, phase: 1.5 },
        { x: 0.42, y: 0.15, color: '#ffffff', size: 4, phase: 3.0 },
        { x: 0.88, y: 0.18, color: '#ff4747', size: 5, phase: 4.2 },
        { x: 0.76, y: 0.72, color: '#00ff66', size: 4, phase: 2.1 },
        { x: 0.94, y: 0.45, color: '#ffffff', size: 4, phase: 5.5 }
      ];

      const eagleSensorDots = [
        { c: 17, r: 33, col: '#ff4747' },
        { c: 6, r: 29, col: '#00ff66' },
        { c: 4, r: 32, col: '#00ff66' },
        { c: 9, r: 34, col: '#00ff66' },
        { c: 7, r: 38, col: '#00ff66' }
      ];

      const telFlight = document.getElementById('tel-flight');
      const telAttitude = document.getElementById('tel-attitude');
      const telRange = document.getElementById('tel-range');
      const telBearing = document.getElementById('tel-bearing');

      // -----------------------------------------------------------------------
      // 5. HIGH-END CINEMATIC RENDER ENGINE (Ground-anchored, zero motion sickness)
      //    Rock-solid orthogonal dot matrix, 1:1 synchronized reticle kinematics.
      // -----------------------------------------------------------------------
      const loopDuration = 2000; // Exact 2.0s flapping cycle (24 frames @ 12 FPS)
      const frameDuration = loopDuration / 24; // 83.33ms per pose

      function render(now) {
        // In STATIC mode, if rendered once, we can skip continuous renders
        const isStatic = (currentMotionMode === 'STATIC');

        ctx.clearRect(0, 0, width, height);

        // 1. Responsive Proportions & Grounded Anchored Coordinates (Zero mouse sway!)
        const isMobile = width < 768;
        const isShortScreen = height < 800;

        const scale = isMobile
          ? (width / 720) * 0.92
          : Math.min(width / 980, height / 1050) * 0.92;

        const dotPitch = 9.8 * scale;
        const dotSize = Math.max(2.8, 5.8 * scale);

        const refCenterX = 350;
        const refCenterY = 580;

        // Grounded Center: Rock-solid, zero camera sway
        const baseCenterX = isMobile ? (width * 0.50) : (width * 0.58);
        const baseCenterY = isShortScreen ? (height * 0.36) : (height * 0.34);

        function toScreenX(rx) {
          return baseCenterX + (rx - refCenterX) * scale;
        }
        function toScreenY(ry) {
          return baseCenterY + (ry - refCenterY) * scale;
        }

        // 2. Heavenly Sky Gradient
        const skyGrad = ctx.createLinearGradient(0, 0, 0, height);
        skyGrad.addColorStop(0, '#101968');      // Celestial midnight zenith
        skyGrad.addColorStop(0.38, '#1e2f9e');   // Deep royal cobalt
        skyGrad.addColorStop(0.68, '#2e4fc8');   // Radiant luminous azure
        skyGrad.addColorStop(0.82, '#4870e8');   // Horizon twilight bloom
        skyGrad.addColorStop(1, '#0c1244');      // Void foundation
        ctx.fillStyle = skyGrad;
        ctx.fillRect(0, 0, width, height);

        // Subtle Analog Film Grain
        if (grainPattern) {
          ctx.fillStyle = grainPattern;
          ctx.fillRect(0, 0, width, height);
        }

        // 2b. Crepuscular God Rays
        drawGodRays(now, width, height, currentMotionMode);

        // 2c. Celestial Floating Stardust Motes
        ctx.save();
        for (const m of stardustMotes) {
          if (!isStatic) {
            m.x += m.vx;
            m.y += m.vy;

            if (m.y < -10) {
              m.y = height + 10;
              m.x = Math.random() * width;
            }
            if (m.x > width + 10) {
              m.x = -10;
            }
          }

          const twinkle = isStatic ? 0 : Math.sin(now * m.twinkleSpeed + m.phase);
          const alpha = Math.max(0.08, Math.min(0.65, m.baseAlpha + twinkle * 0.14));

          ctx.fillStyle = `${m.col}${alpha})`;
          ctx.fillRect(m.x, m.y, m.sz, m.sz);
        }
        ctx.restore();

        // 3. Anchored Volumetric "Pockets of Dust" Cloud Deck
        updateCloudField(now, width, height, isStatic);
        if (cloudCanvas.width > 0) {
          ctx.save();
          ctx.imageSmoothingEnabled = false;
          ctx.drawImage(cloudCanvas, 0, 0, width, height);
          ctx.imageSmoothingEnabled = true;
          ctx.restore();
        }

        // 4. Floating Sensor Accent Dots (Grounded in sky)
        ctx.save();
        for (const dot of floatingDots) {
          const dx = dot.x * width + (isStatic ? 0 : Math.sin(now * 0.0005 + dot.phase) * 5);
          const dy = dot.y * height + (isStatic ? 0 : Math.cos(now * 0.0005 + dot.phase) * 4);
          ctx.fillStyle = dot.color;
          ctx.shadowColor = dot.color;
          ctx.shadowBlur = 6;
          ctx.fillRect(dx, dy, dot.size, dot.size);
        }
        ctx.restore();

        // 5. Subpixel Cosine Hermite Interpolation of the 4 Reticle Lines
        const progress = isStatic ? 0.35 : ((now % loopDuration) / loopDuration);
        const rawIndex = progress * 24;
        const k0 = Math.floor(rawIndex) % 24;
        const k1 = (k0 + 1) % 24;
        const frac = rawIndex - Math.floor(rawIndex);
        const ease = 0.5 - 0.5 * Math.cos(frac * Math.PI);

        const curVLeft = RETICLE_KEYFRAMES[k0].vl + (RETICLE_KEYFRAMES[k1].vl - RETICLE_KEYFRAMES[k0].vl) * ease;
        const curVRight = RETICLE_KEYFRAMES[k0].vr + (RETICLE_KEYFRAMES[k1].vr - RETICLE_KEYFRAMES[k0].vr) * ease;
        const curHMid = RETICLE_KEYFRAMES[k0].hm + (RETICLE_KEYFRAMES[k1].hm - RETICLE_KEYFRAMES[k0].hm) * ease;
        const curHBot = RETICLE_KEYFRAMES[k0].hb + (RETICLE_KEYFRAMES[k1].hb - RETICLE_KEYFRAMES[k0].hb) * ease;

        const screenVLeft = toScreenX(curVLeft);
        const screenVRight = toScreenX(curVRight);
        const screenHMid = toScreenY(curHMid);
        const screenHBot = toScreenY(curHBot);

        // Update HUD Telemetry readouts
        if (telFlight) {
          const strokePhase = Math.sin(progress * Math.PI * 2);
          telFlight.textContent = strokePhase > 0 ? 'STROKE // DOWN' : 'STROKE // GLIDE';
          if (telAttitude) {
            telAttitude.textContent = '+0.0° / +0.0°';
          }
          if (telRange && telBearing) {
            telRange.textContent = '4.82 NM';
            telBearing.textContent = '042° TRUE';
          }
        }

        // 6. Ambient Architectural Grid (Clean, sleek CAD/telemetry lines)
        ctx.save();
        ctx.strokeStyle = 'rgba(255, 255, 255, 0.16)';
        ctx.lineWidth = 0.75;

        const hSpacing = 160 * scale;
        const vSpacing = 180 * scale;

        // Outer horizontal lines
        ctx.beginPath();
        for (let y = screenHMid - hSpacing; y > 0; y -= hSpacing) {
          ctx.moveTo(0, y);
          ctx.lineTo(width, y);
        }
        for (let y = screenHBot + hSpacing; y < height; y += hSpacing) {
          ctx.moveTo(0, y);
          ctx.lineTo(width, y);
        }

        // Outer vertical lines
        for (let x = screenVLeft - vSpacing; x > 0; x -= vSpacing) {
          ctx.moveTo(x, 0);
          ctx.lineTo(x, height);
        }
        for (let x = screenVRight + vSpacing; x < width; x += vSpacing) {
          ctx.moveTo(x, 0);
          ctx.lineTo(x, height);
        }
        ctx.stroke();

        // Sector meridian line
        const midSectorY = (screenHMid + screenHBot) / 2;
        ctx.strokeStyle = 'rgba(255, 255, 255, 0.12)';
        ctx.setLineDash([4, 8]);
        ctx.beginPath();
        ctx.moveTo(0, midSectorY);
        ctx.lineTo(width, midSectorY);
        ctx.stroke();
        ctx.setLineDash([]);

        // Architectural telemetry crosses & stamps
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

        // 7. Dynamic 4-Line Architectural Reticle
        ctx.save();
        ctx.strokeStyle = 'rgba(255, 255, 255, 0.72)';
        ctx.lineWidth = 1;
        ctx.shadowColor = 'rgba(255, 255, 255, 0.50)';
        ctx.shadowBlur = 4;

        ctx.beginPath();
        ctx.moveTo(0, screenHMid);
        ctx.lineTo(width, screenHMid);
        ctx.moveTo(0, screenHBot);
        ctx.lineTo(width, screenHBot);

        ctx.moveTo(screenVLeft, 0);
        ctx.lineTo(screenVLeft, height);
        ctx.moveTo(screenVRight, 0);
        ctx.lineTo(screenVRight, height);
        ctx.stroke();

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

        const dotSz = Math.max(3, 5.5 * scale);
        ctx.fillStyle = '#ffffff';
        ctx.shadowBlur = 6;
        ctx.fillRect(screenVLeft - dotSz / 2, screenHMid + 95 * scale, dotSz, dotSz);
        ctx.fillRect(screenVRight - dotSz / 2, screenHMid - 85 * scale, dotSz, dotSz);
        ctx.fillRect(screenVLeft + 250 * scale - dotSz / 2, screenHMid - dotSz / 2, dotSz, dotSz);
        ctx.restore();

        // 8. Authentic 24-Frame Eagle Dot Matrix
        if (typeof BIRD_FRAMES !== 'undefined' && BIRD_FRAMES && BIRD_FRAMES.length > 0) {
          const frameIndex = isStatic ? 0 : (Math.floor(now / frameDuration) % BIRD_FRAMES.length);
          const currentDots = BIRD_FRAMES[frameIndex];

          const reticleCenterX = (screenVLeft + screenVRight) / 2;
          const reticleCenterY = (screenHMid + screenHBot) / 2;

          const eagleAnchorX = reticleCenterX - 15 * dotPitch;
          const eagleAnchorY = reticleCenterY - 38 * dotPitch;

          ctx.save();
          for (let i = 0; i < currentDots.length; i++) {
            const d = currentDots[i];
            const c = d[0];
            const r = d[1];

            const px = eagleAnchorX + c * dotPitch;
            const py = eagleAnchorY + r * dotPitch;

            // Phosphor bloom halo
            ctx.fillStyle = 'rgba(215, 235, 255, 0.28)';
            ctx.fillRect(px - 0.75, py - 0.75, dotSize + 1.5, dotSize + 1.5);

            // High-luminance white core
            ctx.fillStyle = '#ffffff';
            ctx.fillRect(px, py, dotSize, dotSize);
          }

          // Embedded authentic sensor dots
          for (const sdot of eagleSensorDots) {
            const spx = eagleAnchorX + sdot.c * dotPitch;
            const spy = eagleAnchorY + sdot.r * dotPitch;
            ctx.fillStyle = sdot.col;
            ctx.shadowColor = sdot.col;
            ctx.shadowBlur = 8;
            ctx.fillRect(spx, spy, dotSize, dotSize);
          }
          ctx.restore();

          // 9. Vertical Motto ("grow wings and fly") Synchronized to (screenVRight, screenHMid)
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

        if (!isStatic) {
          requestAnimationFrame(render);
        }
      }

      requestAnimationFrame(render);
    })();\n\n"""

html = html[:html.find(script_start_marker)] + new_script_engine + html[html.find(script_end_marker):]

with open(html_path, "w", encoding="utf-8") as f:
    f.write(html)

print("SUCCESS: index.html updated with Motion Accessibility HUD, Scroll Dimming & Grounded Camera!")
