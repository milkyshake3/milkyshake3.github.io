import re

html_path = r"c:\Apps\personal site project\index.html"

with open(html_path, "r", encoding="utf-8") as f:
    html = f.read()

# -----------------------------------------------------------------------------
# Find the start and end of the cloud and sky code in index.html
# -----------------------------------------------------------------------------
start_marker = "      // -----------------------------------------------------------------------\n      // 3. MULTI-LAYERED VOLUMETRIC CLOUDS (Matching reference footage)"
end_marker = "      // -----------------------------------------------------------------------\n      // 4. INTERACTIVE MULTI-PLANE MOUSE PARALLAX & TELEMETRY TRACKER"

assert start_marker in html, "start_marker not found"
assert end_marker in html, "end_marker not found"

# -----------------------------------------------------------------------------
# New Code: Procedural "Pockets of Dust" Cloud Sprites & Atmospheric Dust Engine
# -----------------------------------------------------------------------------
new_clouds_code = """      // -----------------------------------------------------------------------
      // 3. AUTHENTIC "POCKETS OF DUST" CLOUD ENGINE (Matching reference.mp4)
      //    Blocky, dithered, mosaic dust pockets pre-rendered on offscreen canvases
      //    and blitted with nearest-neighbor scaling for authentic retro pixelation!
      // -----------------------------------------------------------------------
      function generateDustPocketSprite(wBlocks, hBlocks, pockets, seed) {
        const c = document.createElement('canvas');
        c.width = wBlocks;
        c.height = hBlocks;
        const cCtx = c.getContext('2d');
        const imgData = cCtx.createImageData(wBlocks, hBlocks);

        // Simple deterministic pseudo-random generator
        let s = seed || 12345;
        function rnd() {
          s = (s * 9301 + 49297) % 233280;
          return s / 233280;
        }

        for (let y = 0; y < hBlocks; y++) {
          for (let x = 0; x < wBlocks; x++) {
            let density = 0.0;
            for (const p of pockets) {
              const dx = (x - p.cx) / p.rx;
              const dy = (y - p.cy) / p.ry;
              const d2 = dx * dx + dy * dy;
              if (d2 < 1.0) {
                density += p.intensity * Math.pow(1.0 - d2, 1.35);
              }
            }

            const idx = (y * wBlocks + x) * 4;
            if (density > 0.02) {
              const jitter = (rnd() - 0.5) * 0.22;
              const alpha = Math.max(0, Math.min(1.0, density + jitter));
              
              // Luminous pale cloud tone (white with subtle cyan-cobalt warmth)
              imgData.data[idx] = 255;
              imgData.data[idx + 1] = Math.round(246 - (1.0 - alpha) * 15);
              imgData.data[idx + 2] = Math.round(238 - (1.0 - alpha) * 10);
              imgData.data[idx + 3] = Math.round(alpha * 225);
            } else {
              imgData.data[idx + 3] = 0;
            }
          }
        }
        cCtx.putImageData(imgData, 0, 0);
        return c;
      }

      // 4 Distinct Natural "Pockets of Dust" Cloud Formations
      // Cloud Sprite A: Large billowing cumulus dust bank (bottom right)
      const spriteA = generateDustPocketSprite(44, 28, [
        { cx: 24, cy: 17, rx: 14, ry: 9, intensity: 0.88 },
        { cx: 15, cy: 19, rx: 11, ry: 7, intensity: 0.70 },
        { cx: 33, cy: 15, rx: 11, ry: 8, intensity: 0.76 },
        { cx: 20, cy: 12, rx: 8, ry: 6, intensity: 0.52 },
        { cx: 29, cy: 22, rx: 12, ry: 8, intensity: 0.72 }
      ], 101);

      // Cloud Sprite B: Top-left high-altitude wispy dust pocket
      const spriteB = generateDustPocketSprite(32, 18, [
        { cx: 15, cy: 9, rx: 11, ry: 6, intensity: 0.70 },
        { cx: 23, cy: 8, rx: 8, ry: 5, intensity: 0.55 },
        { cx: 8, cy: 11, rx: 7, ry: 5, intensity: 0.45 }
      ], 202);

      // Cloud Sprite C: Mid-left elongated drifting dust bank
      const spriteC = generateDustPocketSprite(36, 16, [
        { cx: 17, cy: 8, rx: 13, ry: 5, intensity: 0.65 },
        { cx: 28, cy: 7, rx: 9, ry: 4, intensity: 0.50 },
        { cx: 8, cy: 9, rx: 8, ry: 5, intensity: 0.45 }
      ], 303);

      // Cloud Sprite D: Soft secondary atmospheric dust billow
      const spriteD = generateDustPocketSprite(30, 20, [
        { cx: 15, cy: 10, rx: 10, ry: 7, intensity: 0.60 },
        { cx: 22, cy: 12, rx: 8, ry: 6, intensity: 0.48 },
        { cx: 8, cy: 8, rx: 7, ry: 5, intensity: 0.42 }
      ], 404);

      // Dynamic Cloud Instances with Forward Flight Motion Vector (drifting up & sideways)
      const cloudInstances = [
        // 1. Iconic Bottom-Right Dust Bank (wraps under the eagle's tail)
        { sprite: spriteA, x: width * 0.48, y: height * 0.68, vx: 0.18, vy: -0.32, scale: 1.15, opacity: 0.84, depth: 0.9 },
        // 2. Top-Left Wispy Dust Pocket
        { sprite: spriteB, x: width * 0.08, y: height * 0.06, vx: 0.12, vy: -0.22, scale: 1.05, opacity: 0.65, depth: 0.4 },
        // 3. Mid-Left Drifting Pocket
        { sprite: spriteC, x: -width * 0.05, y: height * 0.42, vx: 0.15, vy: -0.28, scale: 1.0, opacity: 0.58, depth: 0.6 },
        // 4. Secondary Upper-Right Dust Pocket
        { sprite: spriteD, x: width * 0.72, y: height * 0.22, vx: 0.14, vy: -0.25, scale: 0.95, opacity: 0.52, depth: 0.5 },
        // 5. Far Lower-Left Atmosphere Bank
        { sprite: spriteA, x: -width * 0.22, y: height * 0.82, vx: 0.20, vy: -0.35, scale: 1.25, opacity: 0.75, depth: 0.85 }
      ];

      // -----------------------------------------------------------------------
      // 3b. ATMOSPHERIC MICRO-DUST PARTICLES (Active Living Sky Stream)
      //     Fine floating dust motes drifting across the cobalt stratosphere
      // -----------------------------------------------------------------------
      const DUST_COUNT = 65;
      const dustParticles = [];
      for (let i = 0; i < DUST_COUNT; i++) {
        dustParticles.push({
          x: Math.random() * width,
          y: Math.random() * height,
          sz: Math.random() < 0.75 ? 2 : 3,
          vx: 0.12 + Math.random() * 0.22,
          vy: -(0.25 + Math.random() * 0.45),
          baseAlpha: 0.18 + Math.random() * 0.32,
          twinkleSpeed: 0.0015 + Math.random() * 0.002,
          phase: Math.random() * Math.PI * 2
        });
      }
"""

html = html[:html.find(start_marker)] + new_clouds_code + html[html.find(end_marker):]

# -----------------------------------------------------------------------------
# Now update the render function where clouds are drawn and the sky gradient is painted
# -----------------------------------------------------------------------------
old_render_clouds = """        // 1. Cobalt Sky Gradient
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
        }"""

new_render_clouds = """        // 1. Dynamic Living Cobalt Sky Gradient (Breathing with atmospheric flight)
        const skyTime = now * 0.00025;
        const skyPulse = Math.sin(skyTime) * 0.04;
        const skyGrad = ctx.createLinearGradient(0, 0, 0, height);
        skyGrad.addColorStop(0, '#22329e');
        skyGrad.addColorStop(Math.max(0.38, 0.45 + skyPulse), '#2b3ca8');
        skyGrad.addColorStop(Math.min(0.92, 0.85 + skyPulse * 0.5), '#192477');
        skyGrad.addColorStop(1, '#0f1752');
        ctx.fillStyle = skyGrad;
        ctx.fillRect(0, 0, width, height);

        // Subtle Analog Film Grain Overlay
        if (grainPattern) {
          ctx.fillStyle = grainPattern;
          ctx.fillRect(0, 0, width, height);
        }

        // 2a. Floating Atmospheric Micro-Dust Particles (Active Wind Stream)
        ctx.save();
        for (const p of dustParticles) {
          p.x += p.vx;
          p.y += p.vy;

          // Seamless wrap-around for endless soaring flow
          if (p.y < -10) {
            p.y = height + 10;
            p.x = Math.random() * width;
          }
          if (p.x > width + 10) {
            p.x = -10;
          }

          const twinkle = Math.sin(now * p.twinkleSpeed + p.phase);
          const alpha = Math.max(0.08, Math.min(0.65, p.baseAlpha + twinkle * 0.12));
          const px = p.x + cloudParallaxX * 0.3;
          const py = p.y + cloudParallaxY * 0.3;

          ctx.fillStyle = `rgba(255, 255, 255, ${alpha})`;
          ctx.fillRect(px, py, p.sz, p.sz);
        }
        ctx.restore();

        // 2b. "Pockets of Dust" Cloud Formations (Nearest-Neighbor Pixelated Blit)
        ctx.save();
        ctx.imageSmoothingEnabled = false; // Guaranteed crisp, mosaic dust pockets!

        for (const cloud of cloudInstances) {
          cloud.x += cloud.vx;
          cloud.y += cloud.vy;

          // Base block size calibrated to 9.6px (matching eagle pitch)
          const blockSz = 9.6 * (scale || 1) * cloud.scale;
          const drawW = cloud.sprite.width * blockSz;
          const drawH = cloud.sprite.height * blockSz;

          // Wrap around top/right boundaries
          if (cloud.y < -drawH - 20) {
            cloud.y = height + 30;
            cloud.x = (Math.random() * (width * 1.2)) - (width * 0.1);
          }
          if (cloud.x > width + 40) {
            cloud.x = -drawW - 20;
          }

          const drawX = cloud.x + cloudParallaxX * cloud.depth;
          const drawY = cloud.y + cloudParallaxY * cloud.depth;

          ctx.globalAlpha = cloud.opacity;
          ctx.drawImage(cloud.sprite, drawX, drawY, drawW, drawH);
        }
        ctx.globalAlpha = 1.0;
        ctx.imageSmoothingEnabled = true; // Restore for crisp vector reticle & motto
        ctx.restore();"""

assert old_render_clouds in html, "old_render_clouds not found"
html = html.replace(old_render_clouds, new_render_clouds)

with open(html_path, "w", encoding="utf-8") as f:
    f.write(html)

print("SUCCESS: index.html updated with authentic pockets of dust and living moving sky!")
