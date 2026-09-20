import cv2
import os
import numpy as np

video_path = r"c:\Apps\personal site project\refrences\reference.mp4"
output_dir = r"c:\Apps\personal site project\refrences\extracted_frames"
os.makedirs(output_dir, exist_ok=True)

cap = cv2.VideoCapture(video_path)
fps = cap.get(cv2.CAP_PROP_FPS)
total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
duration = total_frames / fps if fps > 0 else 0

print(f"Video Info: {width}x{height}, FPS: {fps}, Total Frames: {total_frames}, Duration: {duration:.2f}s")

# Extract 1 frame every 0.1 seconds (or every 3 frames if 30fps)
frame_idx = 0
saved_count = 0
step = max(1, int(fps / 10)) # 10 frames per second of video

# Let's also crop the bird area if we find it
# In the 9:16 video (e.g. 720x1280), the bird is in the center-left:
# x around 0.15 to 0.7, y around 0.15 to 0.7

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    
    if frame_idx % step == 0:
        sec = frame_idx / fps
        filename = os.path.join(output_dir, f"frame_{saved_count:03d}_{sec:.2f}s.png")
        cv2.imwrite(filename, frame)
        saved_count += 1
    
    frame_idx += 1

cap.release()
print(f"Extracted {saved_count} frames to {output_dir}")
