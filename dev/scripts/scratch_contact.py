import cv2
import glob
import os
import numpy as np

frames_dir = r"c:\Apps\personal site project\refrences\extracted_frames"
files = sorted(glob.glob(os.path.join(frames_dir, "frame_*.png")))

# Let's inspect the first 24 frames (first 2 seconds, which contains at least 1-2 complete flap cycles)
# The bird dots are white squares: RGB ~ [255, 255, 255]
# Let's find the exact dot positions in frame 0 vs frame 1 vs frame 2 ... frame 24

crop_y1, crop_y2 = 200, 750
crop_x1, crop_x2 = 180, 520

# Let's save a collage or contact sheet of the bird crops for frames 0 to 23
crops = []
for i in range(24):
    img = cv2.imread(files[i])
    crop = img[crop_y1:crop_y2, crop_x1:crop_x2]
    # Add frame number text on the crop
    cv2.putText(crop, f"F{i} ({i/12.0:.2f}s)", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
    crops.append(crop)

# Arrange into 4 rows of 6
row1 = np.hstack(crops[0:6])
row2 = np.hstack(crops[6:12])
row3 = np.hstack(crops[12:18])
row4 = np.hstack(crops[18:24])
contact_sheet = np.vstack([row1, row2, row3, row4])

cv2.imwrite(os.path.join(frames_dir, "contact_sheet_f0_f23.png"), contact_sheet)
print("Saved contact_sheet_f0_f23.png")

# Now let's check between which frames the bird changes!
# To ignore clouds, we only look at local connected components of bright dots (size ~ 6-12 pixels)
# Let's find where the dots are in each frame:
for i in range(24):
    img = cv2.imread(files[i])
    crop = img[crop_y1:crop_y2, crop_x1:crop_x2]
    # High threshold for white square dots
    # Note: in BGR, white is B>220, G>220, R>220
    white = (crop[:, :, 0] > 210) & (crop[:, :, 1] > 210) & (crop[:, :, 2] > 210)
    dot_count = np.sum(white)
    print(f"Frame {i:02d} ({i/12.0:.2f}s): White pixel count = {dot_count}")
