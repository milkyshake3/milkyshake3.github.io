import numpy as np
import cv2

# We want to create a procedural generator for "pockets of dust" clouds
# matching the exact blocky, dithered, mosaic texture in cloud_tl_crop.png and cloud_br_crop.png.

width, height = 720, 1280
img = np.zeros((height, width, 3), dtype=np.uint8)

# 1. Cobalt sky background
# BGR: #22329e -> [158, 50, 34], #2b3ca8 -> [168, 60, 43], #0f1752 -> [82, 23, 15]
for y in range(height):
    t = y / height
    b = int(158 * (1 - t) + 82 * t)
    g = int(50 * (1 - t) + 23 * t)
    r = int(34 * (1 - t) + 15 * t)
    img[y, :] = [b, g, r]

# 2. Add fine particulate analog grain to sky
noise = np.random.normal(0, 7, (height, width, 3)).astype(np.int16)
img = np.clip(img.astype(np.int16) + noise, 0, 255).astype(np.uint8)

# 3. Generate a "pocket of dust" cloud
# A cloud is defined by a cluster of pocket centers
# We render it onto a downsampled grid (e.g. cell_size = 10px), with smooth falloff + random noise per cell
cell_size = 10
grid_w = width // cell_size + 1
grid_h = height // cell_size + 1

# Cloud 1: Bottom Right (similar to reference)
# Center around (x=600, y=850), width ~ 250, height ~ 180
# Let's create an offscreen opacity grid
opacity_grid = np.zeros((grid_h, grid_w), dtype=np.float32)

cloud_pockets = [
    # (center_x, center_y, radius_x, radius_y, intensity)
    (580, 850, 160, 90, 0.85),
    (480, 880, 110, 60, 0.65),
    (660, 820, 130, 80, 0.75),
    (530, 800, 90, 50, 0.50),
    (620, 920, 140, 70, 0.70),
    # Top Left cloud
    (100, 120, 120, 70, 0.60),
    (160, 90, 90, 50, 0.45),
    (60, 150, 80, 50, 0.40),
]

for gx in range(grid_w):
    for gy in range(grid_h):
        px = gx * cell_size
        py = gy * cell_size
        val = 0.0
        for cx, cy, rx, ry, intensity in cloud_pockets:
            # Elliptical distance
            d = ((px - cx) / rx)**2 + ((py - cy) / ry)**2
            if d < 1.0:
                # Soft falloff with cellular noise
                val += intensity * (1.0 - d)**1.5
        opacity_grid[gy, gx] = min(1.0, val)

# Apply cellular/mosaic noise to make it look like pockets of dust
for gx in range(grid_w):
    for gy in range(grid_h):
        if opacity_grid[gy, gx] > 0.02:
            # add block jitter
            cell_noise = np.random.uniform(-0.12, 0.12)
            alpha = np.clip(opacity_grid[gy, gx] + cell_noise, 0.0, 1.0)
            
            # draw the cell block
            x0 = gx * cell_size
            y0 = gy * cell_size
            x1 = min(width, x0 + cell_size)
            y1 = min(height, y0 + cell_size)
            
            # Color: bright white/pale blue [255, 250, 245]
            # with subtle vertical gradient inside the cloud
            cloud_color = np.array([255, 248, 240], dtype=np.float32)
            
            # Blend
            for c in range(3):
                img[y0:y1, x0:x1, c] = np.clip(
                    img[y0:y1, x0:x1, c] * (1.0 - alpha * 0.85) + cloud_color[c] * (alpha * 0.85),
                    0, 255
                ).astype(np.uint8)

# Save test result
cv2.imwrite(r'c:\Apps\personal site project\refrences\test_dust_clouds.png', img)
print("Saved test_dust_clouds.png")
