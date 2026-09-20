import re

html_path = r"c:\Apps\personal site project\index.html"

with open(html_path, "r", encoding="utf-8") as f:
    html = f.read()

# -----------------------------------------------------------------------------
# 1. Update Cloud Field with Sunward Rim Lighting and Atmospheric Dispersion
# -----------------------------------------------------------------------------
old_cloud_section_start = "      // -----------------------------------------------------------------------\n      // 3. ANCHORED VOLUMETRIC \"POCKETS OF DUST\" CLOUD FIELD"
old_cloud_section_end = "      // -----------------------------------------------------------------------\n      // 4. FLOATING SENSOR TELEMETRY ACCENT DOTS (In sky matching reference)"

assert old_cloud_section_start in html, "old_cloud_section_start not found"
assert old_cloud_section_end in html, "old_cloud_section_end not found"

new_cloud_section = """      // -----------------------------------------------------------------------
      // 3. HEAVENLY VOLUMETRIC "POCKETS OF DUST" CLOUD FIELD (M83 Outro Aesthetic)
      //    Immense, breathing atmospheric cloud deck with sunward silver/gold rim light
      //    and radiant crepuscular sunbeams (god rays) breaking through the stratosphere.
      // -----------------------------------------------------------------------
      const cloudCanvas = document.createElement('canvas');
      const cloudCtx = cloudCanvas.getContext('2d');

      // Grand cloud pocket definitions in normalized reference coordinates (0..1)
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
      function updateCloudField(now, w, h) {
        if (now - lastCloudUpdate < 30 && cloudCanvas.width > 0) return;
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
        const t = now * 0.0004;

        for (let gy = 0; gy < gh; gy++) {
          const ny = gy / gh;
          for (let gx = 0; gx < gw; gx++) {
            const nx = gx / gw;
            let density = 0.0;

            for (let i = 0; i < cloudPockets.length; i++) {
              const p = cloudPockets[i];
              // Gentle organic breathing undulation
              const pcx = p.cx + Math.sin(t + p.phase) * 0.012;
              const pcy = p.cy + Math.cos(t * 0.75 + p.phase) * 0.008;
              const prx = p.rx + Math.sin(t * 1.1 + p.phase) * 0.006;
              const pry = p.ry + Math.cos(t * 0.85 + p.phase) * 0.005;

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
                // Radiant silver-gold sunlight crest
                data[idx] = 255;
                data[idx + 1] = Math.round(252 - (1.0 - alpha) * 8);
                data[idx + 2] = Math.round(245 - (1.0 - alpha) * 12);
              } else if (ny > 0.75) {
                // Underside catches warm twilight reflections
                data[idx] = 255;
                data[idx + 1] = Math.round(232 - (1.0 - alpha) * 18);
                data[idx + 2] = Math.round(210 - (1.0 - alpha) * 25);
              } else {
                // Soft luminous core
                data[idx] = 248;
                data[idx + 1] = Math.round(242 - (1.0 - alpha) * 14);
                data[idx + 2] = Math.round(255 - (1.0 - alpha) * 8);
              }
              data[idx + 3] = Math.round(alpha * 230);
            } else {
              data[idx + 3] = 0;
            }
          }
        }
        cloudCtx.putImageData(imgData, 0, 0);
      }

      // Dynamic Crepuscular God Rays (Sunbeams streaming from upper right)
      function drawGodRays(now, w, h) {
        const sunX = w * 0.84;
        const sunY = -h * 0.10;
        const numRays = 7;
        const rayAngles = [0.46, 0.51, 0.57, 0.63, 0.69, 0.74, 0.80];
        const rayWidths = [0.045, 0.075, 0.055, 0.085, 0.050, 0.065, 0.055];

        ctx.save();
        const rayLen = Math.max(w, h) * 1.45;

        for (let i = 0; i < numRays; i++) {
          const rayPulse = Math.sin(now * 0.0005 + i * 1.15) * 0.04 + 0.14;
          const angle = rayAngles[i] * Math.PI;
          const widthAngle = rayWidths[i] * Math.PI;

          const x1 = sunX + Math.cos(angle - widthAngle * 0.5) * rayLen;
          const y1 = sunY + Math.sin(angle - widthAngle * 0.5) * rayLen;
          const x2 = sunX + Math.cos(angle + widthAngle * 0.5) * rayLen;
          const y2 = sunY + Math.sin(angle + widthAngle * 0.5) * rayLen;

          const grad = ctx.createRadialGradient(sunX, sunY, 40, sunX, sunY, rayLen);
          grad.addColorStop(0, `rgba(255, 250, 235, ${rayPulse * 0.85})`);
          grad.addColorStop(0.45, `rgba(255, 246, 225, ${rayPulse * 0.40})`);
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
      // 3b. CELESTIAL FLOATING STARDUST & LIGHT MOTES (M83 Ethereal Breeze)
      // -----------------------------------------------------------------------
      const DUST_COUNT = 70;
      const stardustMotes = [];
      const moteColors = [
        'rgba(255, 248, 220, ', // golden starlight
        'rgba(255, 255, 255, ', // crystalline white
        'rgba(215, 242, 255, '  // ethereal cyan-azure
      ];

      for (let i = 0; i < DUST_COUNT; i++) {
        stardustMotes.push({
          x: Math.random() * width,
          y: Math.random() * height,
          sz: Math.random() < 0.75 ? 2 : 3,
          vx: 0.08 + Math.random() * 0.16,
          vy: -(0.20 + Math.random() * 0.35),
          col: moteColors[Math.floor(Math.random() * moteColors.length)],
          baseAlpha: 0.20 + Math.random() * 0.45,
          twinkleSpeed: 0.0012 + Math.random() * 0.002,
          phase: Math.random() * Math.PI * 2
        });
      }
"""

html = html[:html.find(old_cloud_section_start)] + new_cloud_section + html[html.find(old_cloud_section_end):]

# -----------------------------------------------------------------------------
# 2. Update Render Loop with Heavenly Sky Gradient, Sunbeams, and Stardust
# -----------------------------------------------------------------------------
old_render_sky = """        // 2. Cobalt Sky Gradient
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

        // 4. Floating Sensor Accent Dots"""

new_render_sky = """        // 2. Heavenly M83 Outro Sky Gradient (Midnight Cobalt -> Luminous Azure -> Twilight Glow)
        const skyGrad = ctx.createLinearGradient(0, 0, 0, height);
        skyGrad.addColorStop(0, '#101968');      // Celestial midnight zenith
        skyGrad.addColorStop(0.38, '#1e2f9e');   // Deep royal cobalt
        skyGrad.addColorStop(0.68, '#2e4fc8');   // Radiant luminous azure
        skyGrad.addColorStop(0.82, '#4870e8');   // Horizon twilight bloom above clouds
        skyGrad.addColorStop(1, '#0c1244');      // Void foundation
        ctx.fillStyle = skyGrad;
        ctx.fillRect(0, 0, width, height);

        // Subtle Analog Film Grain Overlay
        if (grainPattern) {
          ctx.fillStyle = grainPattern;
          ctx.fillRect(0, 0, width, height);
        }

        // 2b. Crepuscular God Rays (Sunbeams streaming through the atmosphere)
        drawGodRays(now, width, height);

        // 2c. Celestial Floating Stardust Motes (Gentle upward soaring drift)
        ctx.save();
        for (const m of stardustMotes) {
          m.x += m.vx;
          m.y += m.vy;

          if (m.y < -10) {
            m.y = height + 10;
            m.x = Math.random() * width;
          }
          if (m.x > width + 10) {
            m.x = -10;
          }

          const twinkle = Math.sin(now * m.twinkleSpeed + m.phase);
          const alpha = Math.max(0.10, Math.min(0.75, m.baseAlpha + twinkle * 0.18));
          const px = m.x + camX * 0.3;
          const py = m.y + camY * 0.3;

          ctx.fillStyle = `${m.col}${alpha})`;
          ctx.fillRect(px, py, m.sz, m.sz);
        }
        ctx.restore();

        // 3. Anchored Volumetric "Pockets of Dust" Cloud Deck (Sunward Rim Light & Undulation)
        updateCloudField(now, width, height);
        if (cloudCanvas.width > 0) {
          ctx.save();
          ctx.imageSmoothingEnabled = false; // Authentic quantized mosaic dust blocks!
          ctx.drawImage(cloudCanvas, camX * 0.4, camY * 0.4, width, height);
          ctx.imageSmoothingEnabled = true;
          ctx.restore();
        }

        // 4. Floating Sensor Accent Dots"""

assert old_render_sky in html, "old_render_sky not found"
html = html.replace(old_render_sky, new_render_sky)

with open(html_path, "w", encoding="utf-8") as f:
    f.write(html)

print("SUCCESS: Heavenly M83 Outro atmosphere applied to index.html!")
