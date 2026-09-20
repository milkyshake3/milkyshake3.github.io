import cv2
import numpy as np

cap = cv2.VideoCapture(r'c:\Apps\personal site project\refrences\reference.mp4')

def analyze_frame(f_idx, frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # 1. Horizontal lines:
    # Look for thin bright horizontal lines
    # Compute horizontal line kernel: [-1, 2, -1] vertically
    kernel_h = np.array([[-1], [2], [-1]], dtype=np.float32)
    resp_h = cv2.filter2D(gray, -1, kernel_h)
    
    # Average response across columns (excluding bird center x: 200..500)
    # Check left strip (x: 20..140) and right strip (x: 580..700)
    left_strip_h = resp_h[:, 20:140]
    right_strip_h = resp_h[:, 580:700]
    
    row_scores = np.maximum(np.mean(left_strip_h, axis=1), np.mean(right_strip_h, axis=1))
    # Find peaks above threshold
    h_lines = []
    for y in range(2, 1278):
        if row_scores[y] > 15 and row_scores[y] > row_scores[y-1] and row_scores[y] >= row_scores[y+1]:
            # verify it is a continuous line
            # count how many pixels across the row are bright (> 150)
            bright_count = np.sum(gray[y, :] > 150)
            if bright_count > 300: # at least half the width
                h_lines.append((y, int(row_scores[y]), int(bright_count)))
                
    # 2. Vertical lines:
    # Compute vertical line kernel: [-1, 2, -1] horizontally
    kernel_v = np.array([[-1, 2, -1]], dtype=np.float32)
    resp_v = cv2.filter2D(gray, -1, kernel_v)
    
    # Look in top strip (y: 20..200) and bottom strip (y: 900..1200)
    top_strip_v = resp_v[20:200, :]
    bot_strip_v = resp_v[900:1200, :]
    col_scores = np.maximum(np.mean(top_strip_v, axis=0), np.mean(bot_strip_v, axis=0))
    v_lines = []
    for x in range(2, 718):
        if col_scores[x] > 15 and col_scores[x] > col_scores[x-1] and col_scores[x] >= col_scores[x+1]:
            bright_count = np.sum(gray[:, x] > 150)
            if bright_count > 400:
                v_lines.append((x, int(col_scores[x]), int(bright_count)))
                
    # 3. Bird center:
    # White dots of bird are in region y: 150..850, x: 150..570
    bird_region = gray[150:850, 150:570]
    # bird dots are very bright (> 220)
    bird_dots = np.where(bird_region > 220)
    if len(bird_dots[0]) > 0:
        bird_y = int(np.mean(bird_dots[0]) + 150)
        bird_x = int(np.mean(bird_dots[1]) + 150)
        bird_min_y = int(np.min(bird_dots[0]) + 150)
        bird_max_y = int(np.max(bird_dots[0]) + 150)
        bird_min_x = int(np.min(bird_dots[1]) + 150)
        bird_max_x = int(np.max(bird_dots[1]) + 150)
    else:
        bird_x, bird_y = 0, 0
        bird_min_x, bird_max_x, bird_min_y, bird_max_y = 0, 0, 0, 0
        
    return {
        'h_lines': h_lines,
        'v_lines': v_lines,
        'bird_center': (bird_x, bird_y),
        'bird_bbox': (bird_min_x, bird_min_y, bird_max_x, bird_max_y)
    }

results = []
for f in range(0, 196, 12): # Every 1 second (12 frames)
    cap.set(cv2.CAP_PROP_POS_FRAMES, f)
    ret, frame = cap.read()
    if not ret: break
    info = analyze_frame(f, frame)
    results.append((f, info))
    print(f"Frame {f:3d} (t={f/12:.2f}s): bird center=({info['bird_center'][0]}, {info['bird_center'][1]}), "
          f"bbox=({info['bird_bbox'][0]},{info['bird_bbox'][1]} to {info['bird_bbox'][2]},{info['bird_bbox'][3]}), "
          f"H-lines={[h[0] for h in info['h_lines']]}, V-lines={[v[0] for v in info['v_lines']]}")

cap.release()
