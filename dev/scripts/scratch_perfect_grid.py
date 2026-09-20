import cv2
import numpy as np

img0 = cv2.imread(r'c:\Apps\personal site project\refrences\full_f0.png')
gray0 = cv2.cvtColor(img0, cv2.COLOR_BGR2GRAY)

# Let's find the phase / offset of the 10px grid in frame 0:
# x0 in [0..9], y0 in [0..9]
# To find (x0, y0), we can test all 10x10 = 100 possible phase offsets!
# For each phase (ox, oy), sample points (ox + 10*c, oy + 10*r) in the eagle region [y: 500..850, x: 200..550]
# Compute variance or brightness contrast of the sampled points:
# Because dots are 6x6 bright squares on a 10px pitch, sampling at the center of the dots will yield
# high brightness for dots and low brightness for gaps.

best_contrast = 0
best_phase = (0, 0)

for ox in range(10):
    for oy in range(10):
        # Sample points
        xs = np.arange(ox + 180, 560, 10)
        ys = np.arange(oy + 500, 850, 10)
        grid_x, grid_y = np.meshgrid(xs, ys)
        samples = gray0[grid_y, grid_x]
        
        # High contrast means many samples are either very bright (>200) or very dark (<80)
        contrast = np.sum(samples > 200) + np.sum(samples < 60)
        if contrast > best_contrast:
            best_contrast = contrast
            best_phase = (ox, oy)

print(f"Best grid phase in Frame 0: ox={best_phase[0]}, oy={best_phase[1]}, contrast score={best_contrast}")

# Now let's extract all dots on this grid!
ox, oy = best_phase
xs = np.arange(ox, 720, 10)
ys = np.arange(oy, 1280, 10)

extracted_dots = []
vis = img0.copy()

for r_idx, y in enumerate(ys):
    for c_idx, x in enumerate(xs):
        # check 4x4 central patch of the dot to avoid border noise
        patch = img0[y-2:y+3, x-2:x+3]
        if patch.shape[0] < 5 or patch.shape[1] < 5: continue
        
        # Check color
        b = np.mean(patch[:, :, 0])
        g = np.mean(patch[:, :, 1])
        r = np.mean(patch[:, :, 2])
        
        # Is it a white dot?
        if r > 180 and g > 180 and b > 180:
            extracted_dots.append((c_idx, r_idx, 'W', x, y))
            cv2.rectangle(vis, (x-3, y-3), (x+3, y+3), (0, 255, 0), 1)
        elif r > 150 and g < 110 and b < 110:
            extracted_dots.append((c_idx, r_idx, 'R', x, y))
            cv2.rectangle(vis, (x-3, y-3), (x+3, y+3), (0, 0, 255), 1)
        elif g > 150 and r < 110 and b < 130:
            extracted_dots.append((c_idx, r_idx, 'G', x, y))
            cv2.rectangle(vis, (x-3, y-3), (x+3, y+3), (255, 0, 0), 1)

print(f"Total dots extracted on perfect 10px grid: {len(extracted_dots)}")
cv2.imwrite(r'c:\Apps\personal site project\refrences\perfect_grid_f0.png', vis)
print("Saved perfect_grid_f0.png")
