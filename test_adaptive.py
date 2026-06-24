import cv2
import numpy as np
import os
from PIL import Image, ImageEnhance

img_path = 'Dipindai_20260624-0934_page-0001.jpg'
img = cv2.imread(img_path)
h, w = img.shape[:2]

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

gray = cv2.cvtColor(enhanced_img, cv2.COLOR_BGR2GRAY)

# Adaptive Threshold to handle shadows perfectly
# C is the constant subtracted from the mean.
fg_mask_adaptive = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 21, 10)

kernel = np.ones((5, 5), np.uint8)
dilated = cv2.dilate(fg_mask_adaptive, kernel, iterations=3)

num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(dilated, connectivity=8)

if num_labels > 1:
    largest_label = 1
    max_area = stats[1, cv2.CC_STAT_AREA]
    for i in range(2, num_labels):
        if stats[i, cv2.CC_STAT_AREA] > max_area:
            max_area = stats[i, cv2.CC_STAT_AREA]
            largest_label = i
            
    blob_mask = np.zeros_like(fg_mask_adaptive)
    blob_mask[labels == largest_label] = 255
    
    # intersection
    tight_mask = cv2.bitwise_and(blob_mask, fg_mask_adaptive)
    
    # morphological close to fill internal white parts drawn with lines
    close_kernel = np.ones((9, 9), np.uint8)
    tight_mask = cv2.morphologyEx(tight_mask, cv2.MORPH_CLOSE, close_kernel)
    
    contours, _ = cv2.findContours(tight_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    final_mask = np.zeros_like(gray)
    cv2.drawContours(final_mask, contours, -1, 255, thickness=cv2.FILLED)
    
    final_mask = cv2.GaussianBlur(final_mask, (5, 5), 0)
else:
    final_mask = np.zeros_like(gray)

b, g, r = cv2.split(enhanced_img)
rgba = cv2.merge((b, g, r, final_mask))
cv2.imwrite("debug_adaptive_kuromi.png", rgba)

print("Adaptive Threshold test complete.")
