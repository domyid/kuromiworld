import cv2
import numpy as np
import os
from PIL import Image, ImageEnhance

img_path = 'Dipindai_20260624-0934_page-0001.jpg'
img = cv2.imread(img_path)
h, w = img.shape[:2]

# Kuromi
name = "kuromi"
rx, ry, rw, rh = (0.33, 0.30, 0.32, 0.28)

x = int(rx * w)
y = int(ry * h)
bw = int(rw * w)
bh = int(rh * h)

cropped_img = img[y:y+bh, x:x+bw].copy()

# Enhance
pil_img = Image.fromarray(cv2.cvtColor(cropped_img, cv2.COLOR_BGR2RGB))
enhancer = ImageEnhance.Contrast(pil_img)
pil_img = enhancer.enhance(1.5)
enhancer = ImageEnhance.Color(pil_img)
pil_img = enhancer.enhance(1.2)
enhanced_img = cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)

# Apply GrabCut
mask = np.zeros(enhanced_img.shape[:2], np.uint8)
bgdModel = np.zeros((1, 65), np.float64)
fgdModel = np.zeros((1, 65), np.float64)

# Rectangle for GrabCut: (x, y, w, h) within the cropped image
# Give a margin of 10 pixels to avoid the rough box edges
margin = 10
rect = (margin, margin, enhanced_img.shape[1] - 2*margin, enhanced_img.shape[0] - 2*margin)

cv2.grabCut(enhanced_img, mask, rect, bgdModel, fgdModel, 5, cv2.GC_INIT_WITH_RECT)

# where mask is 2 (PR_BGD) or 0 (BGD), change to 0, otherwise 1
mask2 = np.where((mask==2)|(mask==0), 0, 1).astype('uint8')

# Post-processing: keep only the largest connected component (the main character)
num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(mask2, connectivity=8)
if num_labels > 1:
    largest_label = 1
    max_area = stats[1, cv2.CC_STAT_AREA]
    for i in range(2, num_labels):
        if stats[i, cv2.CC_STAT_AREA] > max_area:
            max_area = stats[i, cv2.CC_STAT_AREA]
            largest_label = i
    
    mask2 = np.zeros_like(mask2)
    mask2[labels == largest_label] = 1

# Smooth edges
mask2_255 = mask2 * 255
mask2_255 = cv2.GaussianBlur(mask2_255, (5, 5), 0)

b, g, r = cv2.split(enhanced_img)
rgba = cv2.merge((b, g, r, mask2_255))
cv2.imwrite(f"debug_grabcut_{name}.png", rgba)

print("GrabCut test complete.")
