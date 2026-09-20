import numpy as np
import cv2

width, height = 720, 1280
img = np.zeros((height, width, 3), dtype=np.uint8)

# 1. Heavenly M83 Outro Sky Gradient
# Celestial deep midnight cobalt at top -> radiant azure -> warm golden twilight glow above cloud deck
for y in range(height):
    t = y / height
    if t < 0.45:
        # Midnight cobalt to deep azure
        k = t / 0.45
        b = int(140 * (1 - k) + 185 * k)
        g = int(32 * (1 - k) + 68 * k)
        r = int(18 * (1 - k) + 40 * k)
    elif t < 0.75:
        # Azure to luminous twilight horizon
        k = (t - 0.45) / 0.30
        b = int(185 * (1 - k) + 210 * k)
        g = int(68 * (1 - k) + 115 * k)
        r = int(40 * (1 - k) + 85 * k)
    else:
        # Horizon depth into void
        k = (t - 0.75) / 0.25
        b = int(210 * (1 - k) + 95 * k)
        g = int(115 * (1 - k) + 30 * k)
        r = int(85 * (1 - k) + 20 * k)
    img[y, :] = [b, g, r]

# 2. Crepuscular Sunbeams (God Rays)
# Emanating from upper-right / sun source (x=620, y=-100)
sun_x, sun_y = 650, -80
num_rays = 7
ray_angles = np.linspace(np.pi * 0.48, np.pi * 0.78, num_rays)
ray_widths = [0.06, 0.09, 0.05, 0.08, 0.06, 0.07, 0.05]
ray_intensities = [0.14, 0.22, 0.16, 0.25, 0.18, 0.15, 0.12]

ray_layer = np.zeros((height, width), dtype=np.float32)
y_indices, x_indices = np.indices((height, width))
dx = x_indices - sun_x
dy = y_indices - sun_y
dist = np.sqrt(dx**2 + dy**2)
angle = np.arctan2(dy, dx)

for ra, rw, ri in zip(ray_angles, ray_widths, ray_intensities):
    diff = np.abs(angle - ra)
    mask = diff < rw
    fade = np.clip(1.0 - (dist / 1400.0), 0.0, 1.0)
    ray_layer += (np.cos(diff / rw * np.pi * 0.5) ** 2) * mask * ri * fade

ray_layer = np.clip(ray_layer, 0.0, 0.35)
for c in range(3):
    # Sunbeam tint: warm golden white [255, 250, 235]
    beam_col = [255, 248, 230][c]
    img[:, :, c] = np.clip(img[:, :, c] * (1.0 - ray_layer) + beam_col * ray_layer, 0, 255).astype(np.uint8)

# 3. Heavenly Volumetric Clouds (Mosaic Pockets of Dust with Golden/Silver Rim Light)
cell_sz = 10
gw = width // cell_sz + 1
gh = height // cell_sz + 1
grid = np.zeros((gh, gw), dtype=np.float32)

pockets = [
    # Bottom-Right Grand Cloud Deck (behind eagle)
    (580, 860, 200, 120, 0.92),
    (450, 920, 140, 85, 0.75),
    (680, 820, 160, 100, 0.85),
    (520, 790, 110, 70, 0.60),
    (640, 950, 160, 90, 0.78),
    (380, 970, 120, 75, 0.65),
    # Top-Left Stratospheric Wisps
    (80, 100, 120, 65, 0.65),
    (160, 70, 90, 50, 0.50),
    (40, 130, 80, 50, 0.45),
    # Mid-Left Ethereal Cloud Bank
    (40, 500, 110, 45, 0.48),
    (110, 480, 80, 38, 0.40)
]

for gx in range(gw):
    for gy in range(gh):
        px = gx * cell_sz
        py = gy * cell_sz
        val = 0.0
        for cx, cy, rx, ry, intensity in pockets:
            d = ((px - cx) / rx)**2 + ((py - cy) / ry)**2
            if d < 1.0:
                val += intensity * (1.0 - d)**1.35
        grid[gy, gx] = min(1.0, val)

# Render grid with silver-white and golden rim lighting
np.random.seed(42)
for gx in range(gw):
    for gy in range(gh):
        if grid[gy, gx] > 0.02:
            jitter = np.random.uniform(-0.10, 0.10)
            alpha = np.clip(grid[gy, gx] + jitter, 0.0, 1.0)
            
            x0 = gx * cell_sz
            y0 = gy * cell_sz
            x1 = min(width, x0 + cell_sz)
            y1 = min(height, y0 + cell_sz)
            
            # Sunward rim light: top & right edges of clouds catch radiant golden-white light
            py = gy * cell_sz
            px = gx * cell_sz
            is_top_edge = (py < 850 and px > 400) or (py < 110)
            if is_top_edge:
                col = np.array([255, 252, 245], dtype=np.float32) # pure radiant sunlight
            else:
                col = np.array([245, 235, 220], dtype=np.float32) # soft warm cloud body
                
            for c in range(3):
                img[y0:y1, x0:x1, c] = np.clip(
                    img[y0:y1, x0:x1, c] * (1.0 - alpha*0.90) + col[c] * (alpha*0.90),
                    0, 255
                ).astype(np.uint8)

# 4. Celestial Light Motes (Floating Stardust / Sun Motes)
np.random.seed(777)
for _ in range(70):
    dx = np.random.randint(0, width)
    dy = np.random.randint(0, height)
    sz = np.random.choice([2, 3])
    mote_cols = [[255, 245, 200], [255, 255, 255], [220, 245, 255]]
    mote_col = mote_cols[np.random.randint(0, 3)]
    a = np.random.uniform(0.25, 0.70)
    for c in range(3):
        img[dy:dy+sz, dx:dx+sz, c] = np.clip(img[dy:dy+sz, dx:dx+sz, c] * (1-a) + mote_col[c] * a, 0, 255)

cv2.imwrite(r'c:\Apps\personal site project\refrences\test_heavenly_sky.png', img)
print("Saved test_heavenly_sky.png")
