import cv2
import numpy as np
import json

# Load BIRD_FRAMES from bird_frames.js or index.html
with open(r'c:\Apps\personal site project\bird_frames.js', 'r') as f:
    content = f.read()
    start = content.find('[[[')
    end = content.find('];', start)
    frames_json = content[start:end+1]
    bird_frames = json.loads(frames_json)

print(f"Loaded {len(bird_frames)} frames")
f0_dots = bird_frames[0]
print(f"Frame 0 has {len(f0_dots)} dots")

# Let's render f0_dots on a 720x1280 image
# Where does it align with full_f0.png?
# In index.html:
# dotPitch = 10 (or 8.8)
# Let's find best alignment (offset_x, offset_y) between f0_dots and full_f0.png!
img0 = cv2.imread(r'c:\Apps\personal site project\refrences\full_f0.png')
gray0 = cv2.cvtColor(img0, cv2.COLOR_BGR2GRAY)

best_score = 0
best_ox, best_oy = 0, 0

for ox in range(100, 300):
    for oy in range(200, 600):
        # sample dot positions
        score = 0
        for c, r in f0_dots[:50]: # test first 50 dots
            x = ox + c * 10
            y = oy + r * 10
            if 0 <= y < 1280 and 0 <= x < 720:
                if gray0[y, x] > 200:
                    score += 1
        if score > best_score:
            best_score = score
            best_ox, best_oy = ox, oy

print(f"Best alignment: ox={best_ox}, oy={best_oy}, score={best_score}/50")

# Draw f0_dots in green on img0
vis = img0.copy()
for dot in f0_dots:
    c, r = dot[0], dot[1]
    x = best_ox + c * 10
    y = best_oy + r * 10
    cv2.rectangle(vis, (x-3, y-3), (x+3, y+3), (0, 255, 0), 1)

cv2.imwrite(r'c:\Apps\personal site project\refrences\bird_alignment_f0.png', vis)
print("Saved bird_alignment_f0.png")
