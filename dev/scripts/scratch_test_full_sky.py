import numpy as np
import cv2
import json

# Generate a sample frame to verify the look of the new "pockets of dust" cloud system
width, height = 720, 1280
img = np.zeros((height, width, 3), dtype=np.uint8)

# 1. Cobalt Sky Gradient
for y in range(height):
    t = y / height
    b = int(158 * (1 - t*0.6) + 82 * (t*0.6))
    g = int(50 * (1 - t*0.7) + 23 * (t*0.7))
    r = int(34 * (1 - t*0.7) + 15 * (t*0.7))
    img[y, :] = [b, g, r]

# Film grain
noise = np.random.normal(0, 6, (height, width, 3)).astype(np.int16)
img = np.clip(img.astype(np.int16) + noise, 0, 255).astype(np.uint8)

# 2. Procedural "Pockets of Dust" Cloud Generator
def create_cloud_sprite(w_blocks, h_blocks, pockets, seed=42):
    np.random.seed(seed)
    grid = np.zeros((h_blocks, w_blocks), dtype=np.float32)
    for cx, cy, rx, ry, intensity in pockets:
        for gy in range(h_blocks):
            for gx in range(w_blocks):
                d = ((gx - cx) / rx)**2 + ((gy - cy) / ry)**2
                if d < 1.0:
                    grid[gy, gx] += intensity * (1.0 - d)**1.4
    
    # Cellular block jitter / dust pockets
    for gy in range(h_blocks):
        for gx in range(w_blocks):
            if grid[gy, gx] > 0.03:
                jitter = np.random.uniform(-0.10, 0.10)
                grid[gy, gx] = np.clip(grid[gy, gx] + jitter, 0.0, 1.0)
            else:
                grid[gy, gx] = 0.0
    return grid

# Cloud A (Large bottom-right cumulus dust bank)
pockets_A = [
    (24, 18, 14, 9, 0.85),
    (15, 20, 10, 7, 0.65),
    (32, 16, 11, 8, 0.75),
    (20, 13, 8, 6, 0.50),
    (28, 22, 12, 8, 0.70)
]
sprite_A = create_cloud_sprite(42, 28, pockets_A, seed=101)

# Cloud B (Top-left wispy dust cluster)
pockets_B = [
    (14, 10, 10, 6, 0.65),
    (22, 8, 8, 5, 0.50),
    (8, 12, 7, 5, 0.40)
]
sprite_B = create_cloud_sprite(30, 18, pockets_B, seed=202)

# Cloud C (Mid-left elongated drifting pocket)
pockets_C = [
    (16, 8, 12, 5, 0.55),
    (26, 7, 10, 4, 0.45),
    (8, 9, 8, 5, 0.40)
]
sprite_C = create_cloud_sprite(34, 16, pockets_C, seed=303)

# Function to stamp cloud onto image with block scaling (nearest neighbor)
def stamp_cloud(img, sprite, top_x, top_y, block_sz=9, base_opacity=0.75):
    sh, sw = sprite.shape
    for gy in range(sh):
        for gx in range(sw):
            alpha = sprite[gy, gx] * base_opacity
            if alpha <= 0.01: continue
            
            x0 = int(top_x + gx * block_sz)
            y0 = int(top_y + gy * block_sz)
            x1 = min(width, x0 + block_sz)
            y1 = min(height, y0 + block_sz)
            if x0 >= width or y0 >= height or x1 <= 0 or y1 <= 0: continue
            x0 = max(0, x0)
            y0 = max(0, y0)
            
            # Cloud color: crisp luminous white with soft pale blue tint
            cloud_col = np.array([255, 245, 238], dtype=np.float32)
            for c in range(3):
                img[y0:y1, x0:x1, c] = np.clip(
                    img[y0:y1, x0:x1, c] * (1.0 - alpha) + cloud_col[c] * alpha,
                    0, 255
                ).astype(np.uint8)

# Stamp clouds at their authentic positions
stamp_cloud(img, sprite_A, top_x=380, top_y=720, block_sz=10, base_opacity=0.82)
stamp_cloud(img, sprite_B, top_x=10, top_y=50, block_sz=9, base_opacity=0.60)
stamp_cloud(img, sprite_C, top_x=-40, top_y=420, block_sz=8, base_opacity=0.50)

# 3. Add atmospheric dust motes
np.random.seed(999)
for _ in range(50):
    dx = np.random.randint(0, width)
    dy = np.random.randint(0, height)
    sz = np.random.choice([2, 3])
    a = np.random.uniform(0.2, 0.5)
    img[dy:dy+sz, dx:dx+sz] = np.clip(img[dy:dy+sz, dx:dx+sz] * (1-a) + 255 * a, 0, 255)

cv2.imwrite(r'c:\Apps\personal site project\refrences\test_full_sky.png', img)
print("Saved test_full_sky.png")
