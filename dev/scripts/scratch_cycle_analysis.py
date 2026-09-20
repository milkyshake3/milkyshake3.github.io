import cv2
import numpy as np

cap = cv2.VideoCapture(r'c:\Apps\personal site project\refrences\reference.mp4')

# Let's inspect frames 0 to 24 (one complete 24-frame loop @ 12fps = 2.0s)
for f in range(24):
    cap.set(cv2.CAP_PROP_POS_FRAMES, f)
    ret, frame = cap.read()
    if not ret: break
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # Let's find:
    # 1. The bird's exact white dot bounds (x_min, x_max, y_min, y_max)
    # The bird dots are very bright (> 210)
    # Exclude the lines themselves if possible, or crop near the bird
    bird_crop = gray[100:900, 100:650]
    # bird dots
    dots_y, dots_x = np.where(bird_crop > 220)
    # adjust for crop
    dots_y += 100
    dots_x += 100
    
    # 2. Horizontal lines:
    # Look for sharp horizontal lines across columns 20..140 and 600..700
    k_h = np.array([[-1], [2], [-1]], dtype=np.float32)
    resp_h = cv2.filter2D(gray, -1, k_h)
    
    # Find peaks in row average
    row_avg = np.mean(resp_h[:, 20:130], axis=1)
    h_peaks = []
    for y in range(50, 1200):
        if row_avg[y] > 12 and row_avg[y] > row_avg[y-1] and row_avg[y] >= row_avg[y+1]:
            if np.sum(gray[y, :] > 140) > 250:
                h_peaks.append(y)
                
    # 3. Vertical lines:
    k_v = np.array([[-1, 2, -1]], dtype=np.float32)
    resp_v = cv2.filter2D(gray, -1, k_v)
    col_avg_top = np.mean(resp_v[30:150, :], axis=0)
    col_avg_bot = np.mean(resp_v[950:1150, :], axis=0)
    col_avg = np.maximum(col_avg_top, col_avg_bot)
    v_peaks = []
    for x in range(50, 680):
        if col_avg[x] > 10 and col_avg[x] > col_avg[x-1] and col_avg[x] >= col_avg[x+1]:
            if np.sum(gray[:, x] > 140) > 300:
                v_peaks.append(x)
                
    b_min_x, b_max_x = int(np.min(dots_x)), int(np.max(dots_x))
    b_min_y, b_max_y = int(np.min(dots_y)), int(np.max(dots_y))
    print(f"Frame {f:2d}: Bird X=[{b_min_x:3d}, {b_max_x:3d}] (w={b_max_x-b_min_x:3d}), Y=[{b_min_y:3d}, {b_max_y:3d}] (h={b_max_y-b_min_y:3d}) | V-lines={v_peaks} | H-lines={h_peaks}")

cap.release()
