import cv2
import numpy as np

img0 = cv2.imread(r'c:\Apps\personal site project\refrences\full_f0.png')
# Crop a clean patch of dots on the eagle body in frame 0
# Look around y: 550..650, x: 250..400
patch = img0[550:650, 250:400]
gray = cv2.cvtColor(patch, cv2.COLOR_BGR2GRAY)

# Find centroids of bright dots
_, thresh = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY)
num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(thresh)

# Filter for dots of size between 10 and 100 pixels
dots = []
for i in range(1, num_labels):
    area = stats[i, cv2.CC_STAT_AREA]
    w = stats[i, cv2.CC_STAT_WIDTH]
    h = stats[i, cv2.CC_STAT_HEIGHT]
    if 10 <= area <= 100 and 3 <= w <= 12 and 3 <= h <= 12:
        dots.append(centroids[i])

dots = np.array(dots)
print(f"Found {len(dots)} dots in patch")

# Compute distances between neighboring dots
diffs_x = []
diffs_y = []
for i in range(len(dots)):
    for j in range(i+1, len(dots)):
        dx = abs(dots[i, 0] - dots[j, 0])
        dy = abs(dots[i, 1] - dots[j, 1])
        if 7 < dx < 13 and dy < 3:
            diffs_x.append(dx)
        if 7 < dy < 13 and dx < 3:
            diffs_y.append(dy)

print(f"Mean horizontal pitch: {np.mean(diffs_x):.3f}px (std: {np.std(diffs_x):.3f})")
print(f"Mean vertical pitch: {np.mean(diffs_y):.3f}px (std: {np.std(diffs_y):.3f})")

# Measure dot width/height
dot_widths = [stats[i, cv2.CC_STAT_WIDTH] for i in range(1, num_labels) if 10 <= stats[i, cv2.CC_STAT_AREA] <= 100]
dot_heights = [stats[i, cv2.CC_STAT_HEIGHT] for i in range(1, num_labels) if 10 <= stats[i, cv2.CC_STAT_AREA] <= 100]
print(f"Mean dot width: {np.mean(dot_widths):.2f}px, height: {np.mean(dot_heights):.2f}px")
