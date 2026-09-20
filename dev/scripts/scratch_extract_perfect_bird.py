import cv2
import numpy as np
import json

cap = cv2.VideoCapture(r'c:\Apps\personal site project\refrences\reference.mp4')
total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

# We know:
# pitch = 10
# dot center: (c * 10 + 4.5, r * 10 + 5.5) -> round to integer: x = c * 10 + 5, y = r * 10 + 5
# Dot size: 6x6, from [y-2:y+4, x-2:x+4]
# Grid bounds:
# columns: c in [10 .. 65] (x from 100 to 650)
# rows: r in [15 .. 95] (y from 150 to 950)

# Pre-load all frames into memory (196 frames @ 720x1280 is ~1.5 GB in uint8, or just read on demand)
print("Analyzing 24-frame cycle across all 8 cycles in video...")

perfect_bird_frames = []

for k in range(24):
    equiv_frames = [k + 24 * i for i in range(8) if k + 24 * i < total_frames]
    
    # Read all equivalent frames
    frames_bgr = []
    for f in equiv_frames:
        cap.set(cv2.CAP_PROP_POS_FRAMES, f)
        ret, frame = cap.read()
        if ret:
            frames_bgr.append(frame)
            
    # For each cell (c, r), determine if it's a dot
    # A dot is a 6x6 bright square.
    # We test:
    # 1. Contrast: central 4x4 patch vs surrounding border (x-4, x+5, y-4, y+5)
    # In a dot, center is bright, but gap between dots is darker.
    # 2. Voting across cycles: if at least 2 cycles have a clear dot, and background is not cloud.
    
    frame_dots = []
    
    for r in range(15, 96):
        y = r * 10 + 5
        for c in range(10, 66):
            x = c * 10 + 5
            
            # Check across all cycles
            dot_votes = []
            for frame in frames_bgr:
                patch = frame[y-2:y+4, x-2:x+4] # 6x6 patch
                if patch.shape[0] < 6 or patch.shape[1] < 6: continue
                
                # Colors
                b_mean = np.mean(patch[:, :, 0])
                g_mean = np.mean(patch[:, :, 1])
                r_mean = np.mean(patch[:, :, 2])
                
                # Check for Red dot
                if r_mean > 150 and g_mean < 115 and b_mean < 115:
                    dot_votes.append('R')
                    continue
                    
                # Check for Green dot
                if g_mean > 150 and r_mean < 115 and b_mean < 140:
                    dot_votes.append('G')
                    continue
                    
                # Check for White dot:
                # White dots have high intensity in all channels (> 190)
                # AND they must be distinct from a cloud or grid line:
                # Surrounding gap: check points at (x-4, y), (x+5, y), (x, y-4), (x, y+5)
                if r_mean > 185 and g_mean > 185 and b_mean > 185:
                    # check if it's a grid line:
                    # Grid line is 1px wide: if patch has bright center row or col but not whole 6x6
                    # A dot has high brightness across the whole 6x6 patch
                    patch_min = np.min(patch)
                    if patch_min > 140: # entire 6x6 is bright
                        dot_votes.append('W')
                        
            # Vote:
            if len(dot_votes) >= 3: # at least 3 cycles agree
                # Take majority vote
                vals, counts = np.unique(dot_votes, return_counts=True)
                winner = vals[np.argmax(counts)]
                frame_dots.append([c, r, winner])
                
    perfect_bird_frames.append(frame_dots)
    print(f"Frame {k:2d}: extracted {len(frame_dots)} dots (W: {sum(1 for d in frame_dots if d[2]=='W')}, R: {sum(1 for d in frame_dots if d[2]=='R')}, G: {sum(1 for d in frame_dots if d[2]=='G')})")

cap.release()

# Save as JSON
with open(r'c:\Apps\personal site project\refrences\perfect_bird_frames_24.json', 'w') as f_out:
    json.dump(perfect_bird_frames, f_out)
print("Saved perfect_bird_frames_24.json")

# Create a master visual collage of all 24 frames
# 4 rows x 6 cols
# Each cell: 720 x 1280 scaled down to 240 x 426
cell_w, cell_h = 240, 426
collage = np.zeros((cell_h * 4, cell_w * 6, 3), dtype=np.uint8)
collage[:] = [158, 50, 34] # Cobalt blue in BGR

for idx, f_dots in enumerate(perfect_bird_frames):
    row_idx = idx // 6
    col_idx = idx % 6
    x_off = col_idx * cell_w
    y_off = row_idx * cell_h
    
    scale = cell_w / 720.0
    for d in f_dots:
        c, r, col = d[0], d[1], d[2]
        px = int((c * 10 + 5) * scale) + x_off
        py = int((r * 10 + 5) * scale) + y_off
        sz = max(1, int(6 * scale))
        
        if col == 'R':
            color = (0, 0, 255)
        elif col == 'G':
            color = (0, 255, 0)
        else:
            color = (255, 255, 255)
        cv2.rectangle(collage, (px, py), (px + sz, py + sz), color, -1)

cv2.imwrite(r'c:\Apps\personal site project\refrences\master_bird_collage_24.png', collage)
print("Saved master_bird_collage_24.png")
