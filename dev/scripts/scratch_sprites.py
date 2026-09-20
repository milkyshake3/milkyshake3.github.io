import cv2
import glob
import os
import numpy as np

frames_dir = r"c:\Apps\personal site project\refrences\extracted_frames"
sprites_dir = r"c:\Apps\personal site project\refrences\bird_sprites"
os.makedirs(sprites_dir, exist_ok=True)

files = sorted(glob.glob(os.path.join(frames_dir, "frame_*.png")))

# The bird bounding box:
# Across all 24 frames:
# x: ~180 to 480 (width ~ 300)
# y: ~200 to 650 (height ~ 450)
crop_y1, crop_y2 = 180, 680
crop_x1, crop_x2 = 170, 490

# Let's inspect isolating the bird from the blue background for frames 0 to 23
for i in range(24):
    img = cv2.imread(files[i])
    crop = img[crop_y1:crop_y2, crop_x1:crop_x2]
    
    # In BGR:
    # Blue background is B: 140-190, G: 40-70, R: 30-50
    # White dots are B > 200, G > 200, R > 200
    # Red dots are R > 180, G < 100, B < 100
    # Green dots are G > 180, R < 100, B < 150
    # Cloud is white/gray, but in frames 0 to 12, there are almost no clouds overlapping the bird!
    
    # Create 4-channel RGBA image
    h, w, _ = crop.shape
    rgba = np.zeros((h, w, 4), dtype=np.uint8)
    
    # White dots
    white_mask = (crop[:, :, 0] > 185) & (crop[:, :, 1] > 185) & (crop[:, :, 2] > 185)
    
    # Red dots: R is significantly higher than G and B
    red_mask = (crop[:, :, 2] > 160) & (crop[:, :, 1] < 120) & (crop[:, :, 0] < 120)
    
    # Green dots: G is significantly higher than R and B
    green_mask = (crop[:, :, 1] > 160) & (crop[:, :, 2] < 120) & (crop[:, :, 0] < 140)
    
    # Grid lines inside the crop:
    # We only want the bird itself!
    # Grid lines are thin 1px lines at specific x and y:
    # Let's check where the grid line is in the crop
    
    bird_mask = white_mask | red_mask | green_mask
    
    # Remove thin isolated lines if any (grid lines)
    # The grid line is a continuous horizontal or vertical line
    # Horizontal line in crop: check rows that are almost entirely 1px line
    
    rgba[:, :, 0] = crop[:, :, 0] # B
    rgba[:, :, 1] = crop[:, :, 1] # G
    rgba[:, :, 2] = crop[:, :, 2] # R
    rgba[:, :, 3] = bird_mask.astype(np.uint8) * 255
    
    out_path = os.path.join(sprites_dir, f"bird_{i:02d}.png")
    cv2.imwrite(out_path, rgba)

print("Extracted 24 transparent bird sprites to", sprites_dir)
