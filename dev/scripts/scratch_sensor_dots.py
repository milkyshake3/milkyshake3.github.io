import cv2
import numpy as np

cap = cv2.VideoCapture(r'c:\Apps\personal site project\refrences\reference.mp4')

# Let's inspect frame 0, 6, 12, 18
frames_to_inspect = [0, 6, 12, 18]

for f in frames_to_inspect:
    cap.set(cv2.CAP_PROP_POS_FRAMES, f)
    ret, frame = cap.read()
    if not ret: continue
    
    # Let's find where colored dots are (Red, Green)
    # In BGR:
    # Red dot: R high (> 180), G low (< 100), B low (< 100)
    # Green dot: G high (> 180), R low (< 100), B low (< 100) or cyan/green
    b, g, r = frame[:,:,0], frame[:,:,1], frame[:,:,2]
    
    red_mask = (r > 160) & (g < 90) & (b < 90)
    green_mask = (g > 160) & (r < 90) & (b < 120)
    
    red_pts = np.argwhere(red_mask)
    green_pts = np.argwhere(green_mask)
    
    print(f"--- FRAME {f} ---")
    if len(red_pts) > 0:
        # cluster or list unique locations
        print(f"Red pixels count: {len(red_pts)}, center ~ (y={int(np.mean(red_pts[:,0]))}, x={int(np.mean(red_pts[:,1]))})")
        for pt in red_pts[:5]:
            print(f"  Red pixel at: (x={pt[1]}, y={pt[0]}), color={frame[pt[0], pt[1]]}")
    else:
        print("No red pixels found")
        
    if len(green_pts) > 0:
        print(f"Green pixels count: {len(green_pts)}, center ~ (y={int(np.mean(green_pts[:,0]))}, x={int(np.mean(green_pts[:,1]))})")
        for pt in green_pts[:5]:
            print(f"  Green pixel at: (x={pt[1]}, y={pt[0]}), color={frame[pt[0], pt[1]]}")
    else:
        print("No green pixels found")

cap.release()
