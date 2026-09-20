import cv2
import numpy as np
import json

cap = cv2.VideoCapture(r'c:\Apps\personal site project\refrences\reference.mp4')

# Let's inspect all 24 frames (f=0..23)
frame_data = []

for f in range(24):
    cap.set(cv2.CAP_PROP_POS_FRAMES, f)
    ret, frame = cap.read()
    if not ret: break
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # 1. Detect vertical lines
    # Vertical line 1 is around x ~ 120..180
    # Vertical line 2 is around x ~ 460..620
    # Let's use 1D horizontal derivative / peak finding
    k_v = np.array([[-1, 2, -1]], dtype=np.float32)
    resp_v = cv2.filter2D(gray, -1, k_v)
    
    # Left strip: x in [110, 180], check rows [50..300] and [900..1200]
    left_resp = np.mean(resp_v[50:300, 110:180], axis=0) + np.mean(resp_v[900:1200, 110:180], axis=0)
    v1 = 110 + int(np.argmax(left_resp))
    
    # Right strip: x in [460, 620]
    right_resp = np.mean(resp_v[50:200, 460:620], axis=0) + np.mean(resp_v[950:1200, 460:620], axis=0)
    v2 = 460 + int(np.argmax(right_resp))
    
    # 2. Detect horizontal lines
    # Horizontal line 1 (upper) is around y ~ 230..540
    # Horizontal line 2 (lower) is around y ~ 670..930
    k_h = np.array([[-1], [2], [-1]], dtype=np.float32)
    resp_h = cv2.filter2D(gray, -1, k_h)
    
    # Check columns [20..100] (far left) and [620..700] (far right)
    side_resp = np.mean(resp_h[:, 20:100], axis=1) + np.mean(resp_h[:, 620:700], axis=1)
    
    # Peak in [220, 560]
    h1_range = side_resp[220:560]
    h1 = 220 + int(np.argmax(h1_range))
    
    # Peak in [670, 950]
    h2_range = side_resp[670:950]
    h2 = 670 + int(np.argmax(h2_range))
    
    # Check if there is another horizontal line (e.g. at top or bottom)
    # Check y in [20, 220]
    top_range = side_resp[20:220]
    top_max = np.max(top_range)
    h_top = (20 + int(np.argmax(top_range))) if top_max > 10 else None
    
    # Check y in [950, 1260]
    bot_range = side_resp[950:1260]
    bot_max = np.max(bot_range)
    h_bot = (950 + int(np.argmax(bot_range))) if bot_max > 10 else None
    
    # 3. Bird dot bounds
    # In earlier analysis, bird dots were extracted. Let's find min/max x,y of the bird in this frame:
    # Bird is in the central region [v1, v2] roughly, or [100..600]
    # To avoid counting the grid lines, look at pixels not on v1, v2, h1, h2
    mask = (gray > 220).astype(np.uint8)
    # erase lines from mask
    mask[:, max(0, v1-2):min(720, v1+3)] = 0
    mask[:, max(0, v2-2):min(720, v2+3)] = 0
    mask[max(0, h1-2):min(1280, h1+3), :] = 0
    mask[max(0, h2-2):min(1280, h2+3), :] = 0
    # Also ignore text region: x in [v2, v2+30], y in [h1, h1+400]
    mask[h1:min(1280, h1+400), max(0, v2):min(720, v2+35)] = 0
    
    bird_pts = np.argwhere(mask[150:900, 100:600])
    if len(bird_pts) > 0:
        bird_pts[:, 0] += 150
        bird_pts[:, 1] += 100
        bx_min, bx_max = int(np.min(bird_pts[:, 1])), int(np.max(bird_pts[:, 1]))
        by_min, by_max = int(np.min(bird_pts[:, 0])), int(np.max(bird_pts[:, 0]))
        bc_x, bc_y = int(np.mean(bird_pts[:, 1])), int(np.mean(bird_pts[:, 0]))
    else:
        bx_min, bx_max, by_min, by_max, bc_x, bc_y = 0, 0, 0, 0, 0, 0
        
    frame_data.append({
        'frame': f,
        'v_left': v1,
        'v_right': v2,
        'h_mid': h1,
        'h_bot': h2,
        'h_top': h_top,
        'bird_bbox': [bx_min, by_min, bx_max, by_max],
        'bird_center': [bc_x, bc_y]
    })
    
    print(f"Frame {f:2d}: v_left={v1:3d}, v_right={v2:3d} (w={v2-v1:3d}) | h_mid={h1:3d}, h_bot={h2:3d} (h={h2-h1:3d}) | bird_x=[{bx_min:3d},{bx_max:3d}] (w={bx_max-bx_min:3d}), bird_y=[{by_min:3d},{by_max:3d}] (h={by_max-by_min:3d})")

cap.release()

with open(r'c:\Apps\personal site project\refrences\frame_kinematics_24.json', 'w') as f_out:
    json.dump(frame_data, f_out, indent=2)
print("Saved frame_kinematics_24.json")
