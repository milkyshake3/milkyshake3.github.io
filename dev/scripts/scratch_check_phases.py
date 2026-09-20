import cv2
import numpy as np

cap = cv2.VideoCapture(r'c:\Apps\personal site project\refrences\reference.mp4')

grid_phases = []

for f in range(24):
    cap.set(cv2.CAP_PROP_POS_FRAMES, f)
    ret, frame = cap.read()
    if not ret: break
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # Let's inspect patch [500:600, 260:360] or wherever the body is
    # In frame f, where is the body?
    # Let's find connected components in the bird area [300:700, 200:500]
    # Filter for 6x6 dots
    _, thresh = cv2.threshold(gray[300:700, 200:500], 200, 255, cv2.THRESH_BINARY)
    num, labels, stats, centroids = cv2.connectedComponentsWithStats(thresh)
    
    xs, ys = [], []
    for i in range(1, num):
        w = stats[i, cv2.CC_STAT_WIDTH]
        h = stats[i, cv2.CC_STAT_HEIGHT]
        area = stats[i, cv2.CC_STAT_AREA]
        if 5 <= w <= 8 and 5 <= h <= 8 and 20 <= area <= 60:
            cx = 200 + centroids[i, 0]
            cy = 300 + centroids[i, 1]
            xs.append(cx)
            ys.append(cy)
            
    if len(xs) > 10:
        # Phase is mode/mean of (x % 10) and (y % 10)
        phase_x = np.median([x % 10 for x in xs])
        phase_y = np.median([y % 10 for y in ys])
        grid_phases.append((f, phase_x, phase_y, len(xs)))
        print(f"Frame {f:2d}: phase_x={phase_x:.2f}, phase_y={phase_y:.2f} (from {len(xs)} dots)")
    else:
        print(f"Frame {f:2d}: Not enough dots found in patch ({len(xs)})")

cap.release()
