html_path = r"c:\Apps\personal site project\index.html"

with open(html_path, "r", encoding="utf-8") as f:
    html = f.read()

# Locate render(now)
old_render_start = """      function render(now) {
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

        // 1. Dynamic Living Cobalt Sky Gradient (Breathing with atmospheric flight)
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
        ctx.restore();

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
        }"""

new_render_start = """      function render(now) {
        ctx.clearRect(0, 0, width, height);

        // 1. Responsive Proportions & Scaling (Declared first for all systems)
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

        // 2. Dynamic Living Cobalt Sky Gradient (Breathing with atmospheric flight)
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

        // 3a. Floating Atmospheric Micro-Dust Particles (Active Wind Stream)
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

        // 3b. "Pockets of Dust" Cloud Formations (Nearest-Neighbor Pixelated Blit)
        ctx.save();
        ctx.imageSmoothingEnabled = false; // Guaranteed crisp, mosaic dust pockets!

        for (const cloud of cloudInstances) {
          cloud.x += cloud.vx;
          cloud.y += cloud.vy;

          // Base block size calibrated to 9.6px (matching eagle pitch)
          const blockSz = 9.6 * scale * cloud.scale;
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

assert old_render_start in html, "old_render_start not found in html"
html = html.replace(old_render_start, new_render_start)

with open(html_path, "w", encoding="utf-8") as f:
    f.write(html)

print("SUCCESS: scale declaration order fixed at top of render()!")
