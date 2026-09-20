import cv2
import numpy as np

img0 = cv2.imread(r'c:\Apps\personal site project\refrences\full_f0.png')
# Let's inspect the eagle body around y: 550, x: 250..400
# Find exact peaks in gray
gray = cv2.cvtColor(img0, cv2.COLOR_BGR2GRAY)

# Look at row 550 across columns 200..400
row = gray[550, 200:400]
# Find where row > 240
bright_x = np.where(row > 240)[0] + 200
print("Bright x coordinates at y=550:", bright_x)

# Find connected components in this local patch [y: 530..570, x: 230..350]
patch = gray[530:570, 230:350]
_, thresh = cv2.threshold(patch, 200, 255, cv2.THRESH_BINARY)
num, labels, stats, centroids = cv2.connectedComponentsWithStats(thresh)

print(f"Connected components in patch: {num-1}")
for i in range(1, num):
    cx = 230 + centroids[i, 0]
    cy = 530 + centroids[i, 1]
    w = stats[i, cv2.CC_STAT_WIDTH]
    h = stats[i, cv2.CC_STAT_HEIGHT]
    print(f"Dot {i}: center=({cx:.2f}, {cy:.2f}), size={w}x{h}")
