import cv2
import glob
import os
import numpy as np

frames_dir = r"c:\Apps\personal site project\refrences\extracted_frames"
files = sorted(glob.glob(os.path.join(frames_dir, "*.png")))

# Let's inspect frame 0 and frame 12 (1 second in)
# The bird consists of bright white square dots on cobalt blue background
# Cobalt blue is roughly R: 20-50, G: 30-70, B: 140-200 in BGR: [140-200, 30-70, 20-50]
# White dots are R>200, G>200, B>200

# Let's find the crop rectangle of the bird
sample_img = cv2.imread(files[12]) # Frame at 1s (Wing Up)
h, w, _ = sample_img.shape

# White mask: high brightness in all channels
gray = cv2.cvtColor(sample_img, cv2.COLOR_BGR2GRAY)
white_mask = (sample_img[:, :, 0] > 200) & (sample_img[:, :, 1] > 200) & (sample_img[:, :, 2] > 200)

# The bird is in the upper-middle quadrant: x in [150, 550], y in [150, 750]
crop_y1, crop_y2 = 180, 850
crop_x1, crop_x2 = 150, 560

bird_crop_up = sample_img[crop_y1:crop_y2, crop_x1:crop_x2]
cv2.imwrite(os.path.join(frames_dir, "crop_wing_up.png"), bird_crop_up)

sample_img_down = cv2.imread(files[0]) # Frame at 0s (Wing Down)
bird_crop_down = sample_img_down[crop_y1:crop_y2, crop_x1:crop_x2]
cv2.imwrite(os.path.join(frames_dir, "crop_wing_down.png"), bird_crop_down)

print("Saved crop_wing_up.png and crop_wing_down.png")

# Now let's compare consecutive frames across the entire 196 frames to find ALL unique bird states!
# We can compute MSE / diff of the bird crop area between frames
crop_diffs = []
unique_states = []

for i in range(len(files)):
    img = cv2.imread(files[i])
    crop = img[crop_y1:crop_y2, crop_x1:crop_x2]
    # filter out clouds by taking white square dot threshold
    dot_mask = ((crop[:, :, 0] > 220) & (crop[:, :, 1] > 220) & (crop[:, :, 2] > 220)).astype(np.uint8) * 255
    
    if i == 0:
        unique_states.append((0, dot_mask, files[0]))
    else:
        # Check diff with existing unique states
        matched = False
        for s_idx, (u_idx, u_mask, u_file) in enumerate(unique_states):
            diff = np.mean(np.abs(dot_mask.astype(float) - u_mask.astype(float)))
            if diff < 5.0: # Very similar
                matched = True
                break
        if not matched:
            unique_states.append((i, dot_mask, files[i]))

print(f"Total unique bird poses found: {len(unique_states)}")
for idx, (f_idx, mask, f_file) in enumerate(unique_states):
    cv2.imwrite(os.path.join(frames_dir, f"unique_state_{idx}_frame_{f_idx}.png"), mask)
    print(f"State {idx}: from frame {f_idx} ({os.path.basename(f_file)})")
