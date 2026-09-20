import os

html_path = r"c:\Apps\personal site project\index.html"
js_path = r"c:\Apps\personal site project\bird_frames.js"

with open(html_path, "r", encoding="utf-8") as f:
    html = f.read()

with open(js_path, "r", encoding="utf-8") as f:
    js_frames = f.read()

semi = js_frames.find(";")
frames_decl = js_frames[:semi+1]

# 1. Update CSS for #hero-scene-canvas to be fixed full-screen
old_canvas_css = """    /* Full-screen Background Living Canvas */
    #hero-scene-canvas {
      position: absolute;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      pointer-events: none;
      z-index: 1;
    }"""

new_canvas_css = """    /* Full-screen Background Living Canvas */
    #hero-scene-canvas {
      position: fixed;
      top: 0;
      left: 0;
      width: 100vw;
      height: 100vh;
      pointer-events: none;
      z-index: 0;
    }"""

assert old_canvas_css in html, "old_canvas_css not found"
html = html.replace(old_canvas_css, new_canvas_css)

# 2. Move canvas to right after <body>
old_body_tag = "<body>\n\n  <!-- Top Navigation Bar -->"
new_body_tag = """<body>

  <!-- Full-screen Background Living Canvas (Cobalt sky, clouds, grid, 24-frame eagle, motto) -->
  <canvas id="hero-scene-canvas" aria-hidden="true"></canvas>

  <!-- Top Navigation Bar -->"""

assert old_body_tag in html, "old_body_tag not found"
html = html.replace(old_body_tag, new_body_tag)

# Remove the old canvas inside hero-container
old_hero_canvas = """      <!-- Living Background Canvas -->
      <canvas id="hero-scene-canvas" aria-hidden="true"></canvas>\n"""
if old_hero_canvas in html:
    html = html.replace(old_hero_canvas, "")

# 3. Update hero-identity padding & styling so it sits cleanly below the flight sector
old_hero_identity_css = """    .hero-identity {
      text-align: center;
      max-width: 680px;
      margin-top: auto;
      margin-bottom: 1rem;
      position: relative;
      z-index: 10;
      background: rgba(15, 22, 77, 0.5);
      backdrop-filter: blur(8px);
      padding: 1.5rem 2rem;
      border: 1px solid var(--panel-border);
      border-radius: 4px;
      box-shadow: 0 4px 30px rgba(0, 0, 0, 0.4);
    }"""

new_hero_identity_css = """    .hero-identity {
      text-align: center;
      max-width: 680px;
      margin-top: auto;
      margin-bottom: 1.5rem;
      position: relative;
      z-index: 10;
      background: rgba(15, 22, 77, 0.65);
      backdrop-filter: blur(10px);
      padding: 1.25rem 2rem;
      border: 1px solid var(--panel-border);
      border-radius: 4px;
      box-shadow: 0 4px 30px rgba(0, 0, 0, 0.4);
    }"""

if old_hero_identity_css in html:
    html = html.replace(old_hero_identity_css, new_hero_identity_css)

# 4. Replace script engine with inlined BIRD_FRAMES and optimized rendering
# Find the start of LIVING HERO BACKGROUND CANVAS
start_marker = "  <script src=\"bird_frames.js\"></script>\n  <script>"
end_marker = "    // -------------------------------------------------------------------------\n    // 2. DETAILED ROTATING WIREFRAME ASCII GLOBE"

assert start_marker in html, "start_marker not found"
assert end_marker in html, "end_marker not found"

part_before = html[:html.find(start_marker)]
part_after = html[html.find(end_marker):]

new_script_section = f"""  <script>
    // =========================================================================
    // INLINED AUTHENTIC 24-FRAME EAGLE DATASET (100% Offline & Self-Contained)
    // Extracted directly from reference.mp4 on a 36x56 grid (10px pitch)
    // =========================================================================
    {frames_decl}

    // -------------------------------------------------------------------------
    // 1. LIVING HERO BACKGROUND CANVAS
    // -------------------------------------------------------------------------
    (function initLivingHeroScene() {{
      const canvas = document.getElementById('hero-scene-canvas');
      if (!canvas) return;
      const ctx = canvas.getContext('2d');

      let width = window.innerWidth;
      let height = window.innerHeight;

      function resize() {{
        width = window.innerWidth;
        height = window.innerHeight;
        canvas.width = width;
        canvas.height = height;
      }}
      resize();
      window.addEventListener('resize', resize);

      // -----------------------------------------------------------------------
      // CLOUDS SYSTEM (Soft pixelated clouds drifting across the sky)
      // -----------------------------------------------------------------------
      const clouds = [
        {{ x: width * 0.10, y: height * 0.48, speed: 0.22, scale: 1.1, opacity: 0.65 }},
        {{ x: width * 0.60, y: height * 0.18, speed: 0.14, scale: 0.9, opacity: 0.50 }},
        {{ x: width * 0.82, y: height * 0.65, speed: 0.26, scale: 1.3, opacity: 0.70 }},
        {{ x: -width * 0.25, y: height * 0.30, speed: 0.18, scale: 1.0, opacity: 0.60 }}
      ];

      function drawPixelCloud(cx, cy, scale, opacity) {{
        ctx.save();
        ctx.fillStyle = `rgba(255, 255, 255, ${{opacity}})`;
        ctx.shadowColor = 'rgba(255, 255, 255, 0.4)';
        ctx.shadowBlur = 15;

        const puffs = [
          {{ dx: 0, dy: 0, r: 45 * scale }},
          {{ dx: -35 * scale, dy: 10 * scale, r: 35 * scale }},
          {{ dx: 40 * scale, dy: 15 * scale, r: 38 * scale }},
          {{ dx: -70 * scale, dy: 22 * scale, r: 28 * scale }},
          {{ dx: 75 * scale, dy: 25 * scale, r: 30 * scale }},
          {{ dx: 0, dy: 20 * scale, r: 40 * scale }}
        ];

        for (const p of puffs) {{
          ctx.beginPath();
          ctx.arc(cx + p.dx, cy + p.dy, p.r, 0, Math.PI * 2);
          ctx.fill();
        }}
        ctx.restore();
      }}

      // -----------------------------------------------------------------------
      // FLOATING SENSOR ACCENT DOTS (Red, Green, White floating in sky)
      // -----------------------------------------------------------------------
      const floatingDots = [
        {{ x: 0.12, y: 0.38, color: '#ff4747', size: 5, speed: 0.08, phase: 0 }},
        {{ x: 0.25, y: 0.72, color: '#00ff66', size: 5, speed: 0.05, phase: 1.5 }},
        {{ x: 0.45, y: 0.18, color: '#ffffff', size: 4, speed: 0.04, phase: 3.0 }},
        {{ x: 0.85, y: 0.15, color: '#ff4747', size: 5, speed: 0.06, phase: 4.2 }},
        {{ x: 0.78, y: 0.68, color: '#00ff66', size: 4, speed: 0.05, phase: 2.1 }},
        {{ x: 0.92, y: 0.42, color: '#ffffff', size: 4, speed: 0.07, phase: 5.5 }}
      ];

      // -----------------------------------------------------------------------
      // ANIMATION LOOP (12 FPS Flapping Eagle matching reference.mp4)
      // -----------------------------------------------------------------------
      const fps = 12;
      const frameDuration = 1000 / fps; // 83.33ms per frame (24 frames = 2.0s loop)

      function render(now) {{
        ctx.clearRect(0, 0, width, height);

        // 1. Cobalt Sky Gradient
        const skyGrad = ctx.createLinearGradient(0, 0, 0, height);
        skyGrad.addColorStop(0, '#22329e');
        skyGrad.addColorStop(0.45, '#2b3ca8');
        skyGrad.addColorStop(0.85, '#192477');
        skyGrad.addColorStop(1, '#0f1752');
        ctx.fillStyle = skyGrad;
        ctx.fillRect(0, 0, width, height);

        // 2. Drifting Soft Clouds
        for (const cloud of clouds) {{
          cloud.x += cloud.speed;
          if (cloud.x - 150 * cloud.scale > width) {{
            cloud.x = -180 * cloud.scale;
          }}
          drawPixelCloud(cloud.x, cloud.y, cloud.scale, cloud.opacity);
        }}

        // 3. Responsive Dot & Grid Geometry
        const isMobile = width < 768;
        const isShortScreen = height < 800;

        let dotSize = 5.5;
        let dotPitch = 8.8;
        if (isMobile) {{
          dotSize = 3.8;
          dotPitch = 5.8;
        }} else if (isShortScreen) {{
          dotSize = 4.8;
          dotPitch = 7.4;
        }}

        const birdWidth = 36 * dotPitch;
        const birdHeight = 56 * dotPitch;

        // Position bird in the right-center flight quadrant
        const cellLeft = isMobile ? Math.max(10, width * 0.08) : Math.max(80, width * 0.32);
        const cellRight = cellLeft + birdWidth + (isMobile ? 25 : 45);

        // Subtle floating breath (float up/down by 3px)
        const floatY = Math.sin(now * 0.002) * 3;

        // Eagle coordinates
        const eagleX = cellLeft + 15;
        const eagleY = (isShortScreen ? 60 : Math.max(70, height * 0.10)) + floatY;

        // Grid lines framing the flight sector
        const gridTop = eagleY - 20;
        const gridMid = eagleY + birdHeight * 0.52;
        const gridBot = eagleY + birdHeight + 20;

        // 4. Architectural White Coordinate Grid Lines
        ctx.save();
        ctx.strokeStyle = 'rgba(255, 255, 255, 0.65)';
        ctx.lineWidth = 1;

        // Horizontal lines across entire screen
        ctx.beginPath();
        ctx.moveTo(0, gridTop);
        ctx.lineTo(width, gridTop);
        ctx.moveTo(0, gridMid);
        ctx.lineTo(width, gridMid);
        ctx.moveTo(0, gridBot);
        ctx.lineTo(width, gridBot);
        ctx.stroke();

        // Vertical lines
        ctx.beginPath();
        ctx.moveTo(cellLeft, 0);
        ctx.lineTo(cellLeft, height);
        ctx.moveTo(cellRight, 0);
        ctx.lineTo(cellRight, height);

        if (cellLeft > 200) {{
          ctx.moveTo(cellLeft - 200, 0);
          ctx.lineTo(cellLeft - 200, height);
        }}
        if (cellRight < width - 200) {{
          ctx.moveTo(cellRight + 200, 0);
          ctx.lineTo(cellRight + 200, height);
        }}
        ctx.stroke();
        ctx.restore();

        // 5. Floating Sensor Accent Dots (Red, Green, White)
        ctx.save();
        for (const dot of floatingDots) {{
          const dx = (dot.x * width + Math.sin(now * 0.001 + dot.phase) * 15);
          const dy = (dot.y * height + Math.cos(now * 0.001 + dot.phase) * 10);
          ctx.fillStyle = dot.color;
          ctx.shadowColor = dot.color;
          ctx.shadowBlur = 8;
          ctx.fillRect(Math.round(dx), Math.round(dy), dot.size, dot.size);
        }}
        ctx.restore();

        // 6. Authentic 24-Frame 12 FPS Flapping Eagle
        if (typeof BIRD_FRAMES !== 'undefined' && BIRD_FRAMES && BIRD_FRAMES.length > 0) {{
          const frameIndex = Math.floor(now / frameDuration) % BIRD_FRAMES.length;
          const currentDots = BIRD_FRAMES[frameIndex];

          ctx.save();
          for (let i = 0; i < currentDots.length; i++) {{
            const d = currentDots[i];
            const c = d[0];
            const r = d[1];
            const col = d[2]; // 'R', 'G', or undefined ('W')

            const px = Math.round(eagleX + c * dotPitch);
            const py = Math.round(eagleY + r * dotPitch);

            if (col === 'R') {{
              ctx.fillStyle = '#ff4747';
              ctx.shadowColor = '#ff4747';
              ctx.shadowBlur = 8;
            }} else if (col === 'G') {{
              ctx.fillStyle = '#00ff66';
              ctx.shadowColor = '#00ff66';
              ctx.shadowBlur = 8;
            }} else {{
              ctx.fillStyle = '#ffffff';
              ctx.shadowColor = 'rgba(255, 255, 255, 0.75)';
              ctx.shadowBlur = 4;
            }}
            ctx.fillRect(px, py, dotSize, dotSize);
          }}
          ctx.restore();

          // 7. Vertical Motto ("grow wings and fly") in White Italic Serif along the right grid line
          ctx.save();
          ctx.fillStyle = '#ffffff';
          ctx.shadowColor = 'rgba(255, 255, 255, 0.85)';
          ctx.shadowBlur = 6;
          ctx.font = 'italic 500 17px Georgia, "Times New Roman", serif';

          const textX = cellRight + (isMobile ? 12 : 16);
          const textY = eagleY + birdHeight - 10; // aligns with bottom of bird

          ctx.translate(textX, textY);
          ctx.rotate(-Math.PI / 2);
          ctx.fillText('grow wings and fly', 0, 0);
          ctx.restore();
        }}

        requestAnimationFrame(render);
      }}

      requestAnimationFrame(render);
    }})();\n\n"""

full_updated_html = part_before + new_script_section + part_after

with open(html_path, "w", encoding="utf-8") as f:
    f.write(full_updated_html)

print(f"Updated {html_path} successfully! New size: {len(full_updated_html)} bytes")
