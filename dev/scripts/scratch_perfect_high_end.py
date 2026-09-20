import re

html_path = r"c:\Apps\personal site project\index.html"

with open(html_path, "r", encoding="utf-8") as f:
    html = f.read()

# -----------------------------------------------------------------------------
# Replace the canvas script engine with the authoritative high-end system
# -----------------------------------------------------------------------------
start_script_marker = "      // -----------------------------------------------------------------------\n      // 2. PROCEDURAL FILM GRAIN TEXTURE (Tactile analog depth for Cobalt sky)"
end_script_marker = "    // -------------------------------------------------------------------------\n    // 2. HIGH-DETAIL ROTATING WIREFRAME ASCII GLOBE (Top-Left Ambient Telemetry)"

assert start_script_marker in html, "start_script_marker not found"
assert end_script_marker in html, "end_script_marker not found"

new_engine = """      // -----------------------------------------------------------------------
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
      // 3. ANCHORED VOLUMETRIC "POCKETS OF DUST" CLOUD FIELD
      //    Matching reference.mp4: an immense, breathing atmospheric cloud deck
      //    anchored behind the eagle's tail (bottom-right) and stratosphere (top-left).
      //    Rendered via offscreen downsampled canvas with nearest-neighbor scaling
      //    for authentic quantized mosaic pixelation with organic billow breathing.
      // -----------------------------------------------------------------------
      const cloudCanvas = document.createElement('canvas');
      const cloudCtx = cloudCanvas.getContext('2d');

      // Cloud pocket definitions in normalized reference coordinates (0..1)
      const cloudPockets = [
        // Bottom-Right Majestic Cloud Bank (behind eagle's tail)
        { cx: 0.80, cy: 0.72, rx: 0.28, ry: 0.14, intensity: 0.88, phase: 0.0 },
        { cx: 0.65, cy: 0.76, rx: 0.20, ry: 0.10, intensity: 0.72, phase: 1.2 },
        { cx: 0.92, cy: 0.68, rx: 0.22, ry: 0.12, intensity: 0.80, phase: 2.4 },
        { cx: 0.72, cy: 0.66, rx: 0.16, ry: 0.08, intensity: 0.55, phase: 3.6 },
        { cx: 0.88, cy: 0.79, rx: 0.24, ry: 0.11, intensity: 0.75, phase: 4.8 },
        { cx: 0.58, cy: 0.80, rx: 0.16, ry: 0.09, intensity: 0.60, phase: 5.5 },
        // Top-Left Stratospheric Wisps
        { cx: 0.12, cy: 0.08, rx: 0.18, ry: 0.07, intensity: 0.60, phase: 0.8 },
        { cx: 0.22, cy: 0.06, rx: 0.12, ry: 0.05, intensity: 0.48, phase: 2.0 },
        { cx: 0.06, cy: 0.11, rx: 0.11, ry: 0.05, intensity: 0.42, phase: 3.2 },
        // Mid-Left Subtle Atmospheric Wisp
        { cx: 0.05, cy: 0.44, rx: 0.14, ry: 0.045, intensity: 0.42, phase: 4.0 },
        { cx: 0.14, cy: 0.42, rx: 0.10, ry: 0.038, intensity: 0.35, phase: 5.1 }
      ];

      let lastCloudUpdate = 0;
      function updateCloudField(now, w, h) {
        // Update offscreen cloud grid every 2 frames for silky performance
        if (now - lastCloudUpdate < 32 && cloudCanvas.width > 0) return;
        lastCloudUpdate = now;

        const cellPitch = 9.8; // Calibrated directly to eagle dot pitch
        const gw = Math.max(20, Math.ceil(w / cellPitch));
        const gh = Math.max(20, Math.ceil(h / cellPitch));

        if (cloudCanvas.width !== gw || cloudCanvas.height !== gh) {
          cloudCanvas.width = gw;
          cloudCanvas.height = gh;
        }

        const imgData = cloudCtx.createImageData(gw, gh);
        const data = imgData.data;

        // Gentle atmospheric breathing & billow undulation
        const t = now * 0.0004;

        for (let gy = 0; gy < gh; gy++) {
          const ny = gy / gh;
          for (let gx = 0; gx < gw; gx++) {
            const nx = gx / gw;
            let density = 0.0;

            for (let i = 0; i < cloudPockets.length; i++) {
              const p = cloudPockets[i];
              // Subtle organic billow oscillation
              const pcx = p.cx + Math.sin(t + p.phase) * 0.015;
              const pcy = p.cy + Math.cos(t * 0.7 + p.phase) * 0.010;
              const prx = p.rx + Math.sin(t * 1.2 + p.phase) * 0.008;
              const pry = p.ry + Math.cos(t * 0.9 + p.phase) * 0.006;

              const dx = (nx - pcx) / prx;
              const dy = (ny - pcy) / pry;
              const d2 = dx * dx + dy * dy;
              if (d2 < 1.0) {
                density += p.intensity * Math.pow(1.0 - d2, 1.4);
              }
            }

            const idx = (gy * gw + gx) * 4;
            if (density > 0.02) {
              // Discrete cellular pocket jitter
              const jitter = Math.sin(gx * 12.9898 + gy * 78.233) * 0.08;
              const alpha = Math.max(0, Math.min(1.0, density + jitter));

              // Luminous pale cloud tone (white with subtle cobalt tint)
              data[idx] = 255;
              data[idx + 1] = Math.round(246 - (1.0 - alpha) * 16);
              data[idx + 2] = Math.round(238 - (1.0 - alpha) * 12);
              data[idx + 3] = Math.round(alpha * 220);
            } else {
              data[idx + 3] = 0;
            }
          }
        }
        cloudCtx.putImageData(imgData, 0, 0);
      }

      // -----------------------------------------------------------------------
      // 4. FLOATING SENSOR TELEMETRY ACCENT DOTS (In sky matching reference)
      // -----------------------------------------------------------------------
      const floatingDots = [
        { x: 0.14, y: 0.32, color: '#ff4747', size: 5, speed: 0.04, phase: 0 },
        { x: 0.22, y: 0.74, color: '#00ff66', size: 5, speed: 0.03, phase: 1.5 },
        { x: 0.42, y: 0.15, color: '#ffffff', size: 4, speed: 0.02, phase: 3.0 },
        { x: 0.88, y: 0.18, color: '#ff4747', size: 5, speed: 0.03, phase: 4.2 },
        { x: 0.76, y: 0.72, color: '#00ff66', size: 4, speed: 0.02, phase: 2.1 },
        { x: 0.94, y: 0.45, color: '#ffffff', size: 4, speed: 0.04, phase: 5.5 }
      ];

      // Sensor dots embedded inside the eagle body at exact centroids
      const eagleSensorDots = [
        { c: 17, r: 33, col: '#ff4747' },
        { c: 6, r: 29, col: '#00ff66' },
        { c: 4, r: 32, col: '#00ff66' },
        { c: 9, r: 34, col: '#00ff66' },
        { c: 7, r: 38, col: '#00ff66' }
      ];

      // -----------------------------------------------------------------------
      // 5. MOUSE PARALLAX (Subtle, unified camera drift — no puppet tearing)
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

      const telFlight = document.getElementById('tel-flight');
      const telAttitude = document.getElementById('tel-attitude');
      const telRange = document.getElementById('tel-range');
      const telBearing = document.getElementById('tel-bearing');

      // -----------------------------------------------------------------------
      // 6. HIGH-END CINEMATIC RENDER ENGINE (Authentic 12 FPS Cycle: 2000ms)
      //    Rock-solid orthogonal dot matrix, 1:1 synchronized reticle kinematics,
      //    and anchored atmospheric dust pockets. Zero puppet rotation.
      // -----------------------------------------------------------------------
      const loopDuration = 2000; // Exact 2.0s flapping cycle (24 frames @ 12 FPS)
      const frameDuration = loopDuration / 24; // 83.33ms per pose

      function render(now) {
        ctx.clearRect(0, 0, width, height);

        // 1. Responsive Proportions & Base Coordinates
        const isMobile = width < 768;
        const isShortScreen = height < 800;

        const scale = isMobile
          ? (width / 720) * 0.92
          : Math.min(width / 980, height / 1050) * 0.92;

        const dotPitch = 9.8 * scale;
        const dotSize = Math.max(2.8, 5.8 * scale);

        const refCenterX = 350;
        const refCenterY = 580;

        // Subtle, elegant camera float (unified sub-pixel drift)
        mouseX += (targetMouseX - mouseX) * 0.04;
        mouseY += (targetMouseY - mouseY) * 0.04;
        const camX = ((mouseX / width) - 0.5) * 14 * scale;
        const camY = ((mouseY / height) - 0.5) * 10 * scale;

        const baseCenterX = (isMobile ? (width * 0.50) : (width * 0.58)) + camX;
        const baseCenterY = (isShortScreen ? (height * 0.36) : (height * 0.34)) + camY;

        function toScreenX(rx) {
          return baseCenterX + (rx - refCenterX) * scale;
        }
        function toScreenY(ry) {
          return baseCenterY + (ry - refCenterY) * scale;
        }

        // 2. Cobalt Sky Gradient
        const skyGrad = ctx.createLinearGradient(0, 0, 0, height);
        skyGrad.addColorStop(0, '#22329e');
        skyGrad.addColorStop(0.45, '#2b3ca8');
        skyGrad.addColorStop(0.85, '#192477');
        skyGrad.addColorStop(1, '#0f1752');
        ctx.fillStyle = skyGrad;
        ctx.fillRect(0, 0, width, height);

        // Subtle Analog Film Grain Overlay
        if (grainPattern) {
          ctx.fillStyle = grainPattern;
          ctx.fillRect(0, 0, width, height);
        }

        // 3. Anchored Volumetric "Pockets of Dust" Cloud Deck
        updateCloudField(now, width, height);
        if (cloudCanvas.width > 0) {
          ctx.save();
          ctx.imageSmoothingEnabled = false; // Authentic quantized mosaic dust blocks!
          ctx.drawImage(cloudCanvas, camX * 0.4, camY * 0.4, width, height);
          ctx.imageSmoothingEnabled = true;
          ctx.restore();
        }

        // 4. Floating Sensor Accent Dots
        ctx.save();
        for (const dot of floatingDots) {
          const dx = dot.x * width + Math.sin(now * 0.0008 + dot.phase) * 10 + camX * 0.6;
          const dy = dot.y * height + Math.cos(now * 0.0008 + dot.phase) * 8 + camY * 0.6;
          ctx.fillStyle = dot.color;
          ctx.shadowColor = dot.color;
          ctx.shadowBlur = 6;
          ctx.fillRect(dx, dy, dot.size, dot.size);
        }
        ctx.restore();

        // 5. Subpixel Cosine Hermite Interpolation of the 4 Reticle Lines (In 1:1 Lockstep with Wingstroke)
        const progress = (now % loopDuration) / loopDuration;
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
        if (telFlight && (now % 8 < 1)) {
          const strokePhase = Math.sin(progress * Math.PI * 2);
          telFlight.textContent = strokePhase > 0 ? 'STROKE // DOWN' : 'STROKE // GLIDE';
          if (telAttitude) {
            telAttitude.textContent = `${(camY * 0.2).toFixed(1)}° / ${(camX * 0.2).toFixed(1)}°`;
          }
          if (telRange && telBearing) {
            const dist = Math.hypot(camX, camY);
            telRange.textContent = `${(4.82 + dist * 0.05).toFixed(2)} NM`;
            const brg = Math.round((Math.atan2(camY, camX) * 180 / Math.PI + 90 + 360) % 360);
            telBearing.textContent = `${String(brg).padStart(3, '0')}° TRUE`;
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

        // Embedded sensor square dots directly on lines (matching reference video)
        const dotSz = Math.max(3, 5.5 * scale);
        ctx.fillStyle = '#ffffff';
        ctx.shadowBlur = 6;
        ctx.fillRect(screenVLeft - dotSz / 2, screenHMid + 95 * scale, dotSz, dotSz);
        ctx.fillRect(screenVRight - dotSz / 2, screenHMid - 85 * scale, dotSz, dotSz);
        ctx.fillRect(screenVLeft + 250 * scale - dotSz / 2, screenHMid - dotSz / 2, dotSz, dotSz);
        ctx.restore();

        // 8. Authentic 24-Frame Eagle Dot Matrix (Strictly Orthogonal, Crisp Phosphor Pixels)
        if (typeof BIRD_FRAMES !== 'undefined' && BIRD_FRAMES && BIRD_FRAMES.length > 0) {
          const frameIndex = Math.floor(now / frameDuration) % BIRD_FRAMES.length;
          const currentDots = BIRD_FRAMES[frameIndex];

          const reticleCenterX = (screenVLeft + screenVRight) / 2;
          const reticleCenterY = (screenHMid + screenHBot) / 2;

          const eagleAnchorX = reticleCenterX - 15 * dotPitch;
          const eagleAnchorY = reticleCenterY - 38 * dotPitch;

          ctx.save();
          // Draw eagle dots strictly on the orthogonal grid — zero paper puppet tilt!
          for (let i = 0; i < currentDots.length; i++) {
            const d = currentDots[i];
            const c = d[0];
            const r = d[1];

            const px = eagleAnchorX + c * dotPitch;
            const py = eagleAnchorY + r * dotPitch;

            // Optical bloom halo
            ctx.fillStyle = 'rgba(215, 235, 255, 0.28)';
            ctx.fillRect(px - 0.75, py - 0.75, dotSize + 1.5, dotSize + 1.5);

            // High-luminance white core
            ctx.fillStyle = '#ffffff';
            ctx.fillRect(px, py, dotSize, dotSize);
          }

          // Embedded authentic sensor dots inside the eagle body
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

        requestAnimationFrame(render);
      }

      requestAnimationFrame(render);
    })();\n\n"""

# Perform replacement
before_code = html[:html.find(start_script_marker)]
after_code = html[html.find(end_script_marker):]
html = before_code + new_engine + after_code

with open(html_path, "w", encoding="utf-8") as f:
    f.write(html)

print("SUCCESS: index.html overhauled with high-end anchored atmospheric clouds and rock-solid eagle dot matrix!")
