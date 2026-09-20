import cv2
import numpy as np

cap = cv2.VideoCapture(r'c:\Apps\personal site project\refrences\reference.mp4')
total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

k_v = np.array([[-1, 2, -1]], dtype=np.float32)
k_h = np.array([[-1], [2], [-1]], dtype=np.float32)

all_v_left = []
all_v_right = []
all_h_mid = []
all_h_bot = []

for f in range(total_frames):
    ret, frame = cap.read()
    if not ret: break
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # Vertical lines
    resp_v = cv2.filter2D(gray, -1, k_v)
    left_resp = np.mean(resp_v[50:300, 110:180], axis=0) + np.mean(resp_v[900:1200, 110:180], axis=0)
    v1 = 110 + int(np.argmax(left_resp))
    
    right_resp = np.mean(resp_v[50:200, 460:620], axis=0) + np.mean(resp_v[950:1200, 460:620], axis=0)
    v2 = 460 + int(np.argmax(right_resp))
    
    # Horizontal lines
    resp_h = cv2.filter2D(gray, -1, k_h)
    side_resp = np.mean(resp_h[:, 20:100], axis=1) + np.mean(resp_h[:, 620:700], axis=1)
    h1 = 220 + int(np.argmax(side_resp[220:560]))
    h2 = 670 + int(np.argmax(side_resp[670:950]))
    
    all_v_left.append(v1)
    all_v_right.append(v2)
    all_h_mid.append(h1)
    all_h_bot.append(h2)

cap.release()

# Let's inspect the periodicity and drift:
print(f"Total frames analyzed: {len(all_v_left)}")
print("First 48 frames (2 cycles):")
for f in range(0, 48, 4):
    print(f"Frame {f:2d}: v_left={all_v_left[f]}, v_right={all_v_right[f]}, h_mid={all_h_mid[f]}, h_bot={all_h_bot[f]}")

# Check if frame f and frame f+24 are almost identical
diff_v2 = [abs(all_v_right[f] - all_v_right[f+24]) for f in range(total_frames - 24)]
diff_h1 = [abs(all_h_mid[f] - all_h_mid[f+24]) for f in range(total_frames - 24)]
print(f"Avg diff between cycles: v_right={np.mean(diff_v2):.2f}px, h_mid={np.mean(diff_h1):.2f}px")
