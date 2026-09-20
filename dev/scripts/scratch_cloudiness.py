import cv2
import numpy as np

cap = cv2.VideoCapture(r'c:\Apps\personal site project\refrences\reference.mp4')

# Let's inspect how cloudy each cycle is in the bird region [200:900, 150:600]
# Average cloud brightness in sky (e.g. non-dot pixels)
for cycle in range(8):
    f = cycle * 24
    cap.set(cv2.CAP_PROP_POS_FRAMES, f)
    ret, frame = cap.read()
    if not ret: break
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # Check region around bird: y in [200, 900], x in [150, 600]
    bird_area = gray[200:900, 150:600]
    # Pixels that are NOT bird dots (e.g. gray < 180)
    bg_pixels = bird_area[bird_area < 180]
    print(f"Cycle {cycle} (frame {f}): mean background brightness = {np.mean(bg_pixels):.2f}, % cloudy (>100) = {np.mean(bg_pixels > 100)*100:.1f}%")

cap.release()
