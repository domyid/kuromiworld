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

gray = cv2.cvtColor(enhanced_img, cv2.COLOR_BGR2GRAY)

# Test multiple thresholds
for thresh in [180, 200, 220, 240]:
    _, fg_mask = cv2.threshold(gray, thresh, 255, cv2.THRESH_BINARY_INV)
    cv2.imwrite(f"debug_{thresh}_fg_mask.png", fg_mask)
    
    kernel = np.ones((11, 11), np.uint8)
    dilated = cv2.dilate(fg_mask, kernel, iterations=2)
    cv2.imwrite(f"debug_{thresh}_dilated.png", dilated)
    
    num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(dilated, connectivity=8)
    
    if num_labels > 1:
        largest_label = 1
        max_area = stats[1, cv2.CC_STAT_AREA]
        for i in range(2, num_labels):
            if stats[i, cv2.CC_STAT_AREA] > max_area:
                max_area = stats[i, cv2.CC_STAT_AREA]
                largest_label = i
        
        blob_mask = np.zeros_like(fg_mask)
        blob_mask[labels == largest_label] = 255
        cv2.imwrite(f"debug_{thresh}_blob.png", blob_mask)
        
        tight_mask = cv2.bitwise_and(blob_mask, fg_mask)
        cv2.imwrite(f"debug_{thresh}_tight.png", tight_mask)
        
        contours, _ = cv2.findContours(tight_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        final_mask = np.zeros_like(gray)
        cv2.drawContours(final_mask, contours, -1, 255, thickness=cv2.FILLED)
        
        final_mask = cv2.GaussianBlur(final_mask, (3, 3), 0)
        cv2.imwrite(f"debug_{thresh}_final_mask.png", final_mask)
        
        # Test final alpha
        b, g, r = cv2.split(enhanced_img)
        rgba = cv2.merge((b, g, r, final_mask))
        cv2.imwrite(f"debug_{thresh}_kuromi.png", rgba)

print("Debug complete.")
