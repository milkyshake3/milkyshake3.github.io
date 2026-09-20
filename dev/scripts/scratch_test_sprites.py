import cv2
import glob
import os
import numpy as np

sprites_dir = r"c:\Apps\personal site project\refrences\bird_sprites"
files = sorted(glob.glob(os.path.join(sprites_dir, "bird_*.png")))

# Create a collage on a dark blue background to verify transparency and quality
h, w, _ = cv2.imread(files[0], cv2.IMREAD_UNCHANGED).shape
test_bg = np.zeros((h * 4, w * 6, 3), dtype=np.uint8)
test_bg[:] = [150, 40, 30] # Cobalt blue in BGR

for idx, f in enumerate(files):
    img = cv2.imread(f, cv2.IMREAD_UNCHANGED)
    r = idx // 6
    c = idx % 6
    y1, y2 = r * h, (r + 1) * h
    x1, x2 = c * w, (c + 1) * w
    
    # Alpha blend
    alpha = img[:, :, 3] / 255.0
    for ch in range(3):
        test_bg[y1:y2, x1:x2, ch] = (img[:, :, ch] * alpha + test_bg[y1:y2, x1:x2, ch] * (1 - alpha)).astype(np.uint8)

cv2.imwrite(os.path.join(sprites_dir, "sprite_test_sheet.png"), test_bg)
print("Saved sprite_test_sheet.png")
