import cv2
import numpy as np

# Let's inspect full_f0.png and full_f60.png and full_f120.png
img0 = cv2.imread(r'c:\Apps\personal site project\refrences\full_f0.png')
# Let's draw the detected lines on img0 and save as an overlay to see exactly how they align!
with open(r'c:\Apps\personal site project\refrences\frame_kinematics_24.json', 'r') as f_in:
    import json
    kinematics = json.load(f_in)

k0 = kinematics[0] # frame 0
overlay0 = img0.copy()

# Draw detected lines in yellow
cv2.line(overlay0, (0, k0['h_mid']), (720, k0['h_mid']), (0, 255, 255), 1)
cv2.line(overlay0, (0, k0['h_bot']), (720, k0['h_bot']), (0, 255, 255), 1)
cv2.line(overlay0, (k0['v_left'], 0), (k0['v_left'], 1280), (0, 255, 255), 1)
cv2.line(overlay0, (k0['v_right'], 0), (k0['v_right'], 1280), (0, 255, 255), 1)

cv2.imwrite(r'c:\Apps\personal site project\refrences\overlay_f0.png', overlay0)
print("Saved overlay_f0.png")

# Now let's do frame 12
cap = cv2.VideoCapture(r'c:\Apps\personal site project\refrences\reference.mp4')
cap.set(cv2.CAP_PROP_POS_FRAMES, 12)
ret, frame12 = cap.read()
cap.release()

k12 = kinematics[12]
overlay12 = frame12.copy()
cv2.line(overlay12, (0, k12['h_mid']), (720, k12['h_mid']), (0, 255, 255), 1)
cv2.line(overlay12, (0, k12['h_bot']), (720, k12['h_bot']), (0, 255, 255), 1)
cv2.line(overlay12, (k12['v_left'], 0), (k12['v_left'], 1280), (0, 255, 255), 1)
cv2.line(overlay12, (k12['v_right'], 0), (k12['v_right'], 1280), (0, 255, 255), 1)

cv2.imwrite(r'c:\Apps\personal site project\refrences\overlay_f12.png', overlay12)
print("Saved overlay_f12.png")
