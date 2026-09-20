import numpy as np
import cv2

# Let's test an anchored, breathing volumetric cloud field that captures the exact look
# of cloud_br_crop.png without sliding around like a paper cutout!
width, height = 720, 1280
img = np.zeros((height, width, 3), dtype=np.uint8)

# Cobalt sky
for y in range(height):
    t = y / height
    b = int(158 * (1 - t*0.55) + 82 * (t*0.55))
    g = int(50 * (1 - t*0.65) + 23 * (t*0.65))
    r = int(34 * (1 - t*0.65) + 15 * (t*0.65))
    img[y, :] = [b, g, r]

# Analog grain
noise = np.random.normal(0, 6, (height, width, 3)).astype(np.int16)
img = np.clip(img.astype(np.int16) + noise, 0, 255).astype(np.uint8)

# Pockets of dust definition (Anchored atmospheric cloud bank in bottom right)
# Matching reference.mp4 cloud_br_crop.png exactly:
# Lower right: x ~ 400..720, y ~ 700..1050
# Upper left: x ~ 0..250, y ~ 0..220
cell_sz = 10
gw = width // cell_sz + 1
gh = height // cell_sz + 1
grid = np.zeros((gh, gw), dtype=np.float32)

# Multiple overlapping undulating pocket lobes
pockets = [
    # (cx, cy, rx, ry, intensity)
    (580, 860, 180, 110, 0.88),
    (460, 910, 130, 80, 0.70),
    (680, 830, 140, 95, 0.80),
    (520, 800, 100, 65, 0.55),
    (640, 940, 150, 85, 0.75),
    (400, 960, 110, 70, 0.60),
    # Top left wisps
    (80, 100, 110, 60, 0.62),
    (150, 70, 80, 45, 0.48),
    (40, 130, 70, 45, 0.42),
    # Mid left subtle wisp
    (30, 520, 90, 40, 0.40),
    (90, 500, 70, 35, 0.35)
]

for gx in range(gw):
    for gy in range(gh):
        px = gx * cell_sz
        py = gy * cell_sz
        val = 0.0
        for cx, cy, rx, ry, intensity in pockets:
            d = ((px - cx) / rx)**2 + ((py - cy) / ry)**2
            if d < 1.0:
                val += intensity * (1.0 - d)**1.4
        grid[gy, gx] = min(1.0, val)

# Render grid with cell jitter (pockets of dust texture)
np.random.seed(42)
for gx in range(gw):
    for gy in range(gh):
        if grid[gy, gx] > 0.02:
            jitter = np.random.uniform(-0.12, 0.12)
            alpha = np.clip(grid[gy, gx] + jitter, 0.0, 1.0)
            
            x0 = gx * cell_sz
            y0 = gy * cell_sz
            x1 = min(width, x0 + cell_sz)
            y1 = min(height, y0 + cell_sz)
            
            col = np.array([255, 246, 238], dtype=np.float32)
            for c in range(3):
                img[y0:y1, x0:x1, c] = np.clip(
                    img[y0:y1, x0:x1, c] * (1.0 - alpha*0.88) + col[c] * (alpha*0.88),
                    0, 255
                ).astype(np.uint8)

cv2.imwrite(r'c:\Apps\personal site project\refrences\test_anchored_clouds.png', img)
print("Saved test_anchored_clouds.png")
