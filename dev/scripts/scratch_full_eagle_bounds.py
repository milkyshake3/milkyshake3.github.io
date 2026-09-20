import cv2
import numpy as np

cap = cv2.VideoCapture(r'c:\Apps\personal site project\refrences\reference.mp4')

# Let's inspect all 24 frames (0 to 23)
# We know the video is 720x1280.
# The eagle is inside [100..650] in X, and [150..950] in Y.
# Let's find the exact min/max bounds of all eagle dots in every frame!

all_bounds = []

for f in range(24):
    cap.set(cv2.CAP_PROP_POS_FRAMES, f)
    ret, frame = cap.read()
    if not ret: break
    
    # In BGR:
    # Cobalt blue sky: B is 120-200, G is 30-80, R is 15-50
    # White dots: R > 190, G > 190, B > 190
    # Red dots: R > 150, G < 120, B < 120
    # Green dots: G > 150, R < 120, B < 150
    # Grid lines: 1px thin white lines
    
    # Let's crop the whole flight area: y in [150, 950], x in [100, 650]
    sub = frame[150:950, 100:650]
    
    # White dots
    white = (sub[:,:,0] > 190) & (sub[:,:,1] > 190) & (sub[:,:,2] > 190)
    red = (sub[:,:,2] > 150) & (sub[:,:,1] < 120) & (sub[:,:,0] < 120)
    green = (sub[:,:,1] > 150) & (sub[:,:,2] < 120) & (sub[:,:,0] < 150)
    
    bird_mask = white | red | green
    
    # Let's find connected components or contours to remove the 1px grid lines!
    # Grid lines are thin (1px) and very long (> 200px)
    # Bird dots are square blocks (~6x6 to 8x8 pixels with pitch ~10px)
    
    # Let's save the raw mask for this frame
    cv2.imwrite(f"c:\\Apps\\personal site project\\refrences\\raw_bird_mask_f{f:02d}.png", (bird_mask * 255).astype(np.uint8))
    
    pts = np.argwhere(bird_mask)
    if len(pts) > 0:
        min_y, min_x = np.min(pts, axis=0) + [150, 100]
        max_y, max_x = np.max(pts, axis=0) + [150, 100]
        all_bounds.append((f, min_x, max_x, min_y, max_y))
        print(f"Frame {f:02d}: x in [{min_x}, {max_x}] (w={max_x-min_x}), y in [{min_y}, {max_y}] (h={max_y-min_y})")

cap.release()
