import cv2
import numpy as np

cap = cv2.VideoCapture(r'c:\Apps\personal site project\refrences\reference.mp4')

for f in [0, 6, 12, 18]:
    cap.set(cv2.CAP_PROP_POS_FRAMES, f)
    ret, frame = cap.read()
    if not ret: continue
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # In earlier session, text_crop.png was created.
    # Let's search for the text "grow wings and fly"
    # It is vertical, near the right vertical line.
    # In frame 0, V-line 2 is at x=581.
    # Let's inspect the region x: 550..650, y: 400..1000
    crop = frame[400:1000, 540:650]
    cv2.imwrite(f"c:\\Apps\\personal site project\\refrences\\text_region_f{f}.png", crop)
    print(f"Saved text_region_f{f}.png")

cap.release()
