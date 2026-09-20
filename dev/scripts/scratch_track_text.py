import cv2
import numpy as np

cap = cv2.VideoCapture(r'c:\Apps\personal site project\refrences\reference.mp4')

# Track text position across 24 frames
# We know the text says "grow wings and fly", written vertically along v_right
# Let's find the text by looking for bright pixels just to the right of v_right (v_right + 5 to v_right + 35)
with open(r'c:\Apps\personal site project\refrences\frame_kinematics_24.json', 'r') as f_in:
    import json
    kinematics = json.load(f_in)

text_positions = []

for f in range(24):
    cap.set(cv2.CAP_PROP_POS_FRAMES, f)
    ret, frame = cap.read()
    if not ret: break
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    k = kinematics[f]
    v_r = k['v_right']
    h_m = k['h_mid']
    
    # Strip to the right of v_r: x in [v_r + 5, v_r + 30]
    # y in [h_m, h_m + 500]
    strip = gray[h_m:min(1280, h_m + 500), v_r + 2:min(720, v_r + 35)]
    # Text pixels are bright (> 170)
    pts = np.argwhere(strip > 170)
    if len(pts) > 0:
        text_y_min = h_m + int(np.min(pts[:, 0]))
        text_y_max = h_m + int(np.max(pts[:, 0]))
        text_x_mean = v_r + 2 + int(np.mean(pts[:, 1]))
        text_positions.append((f, text_x_mean, text_y_min, text_y_max, v_r, h_m))
        print(f"Frame {f:2d}: Text x={text_x_mean} (v_right={v_r}), y=[{text_y_min}, {text_y_max}] (h_mid={h_m}, offset={text_y_min - h_m})")
    else:
        print(f"Frame {f:2d}: No text detected")

cap.release()
