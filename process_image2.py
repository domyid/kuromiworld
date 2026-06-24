import cv2
import numpy as np
import os
from PIL import Image, ImageEnhance

img_path = 'Dipindai_20260624-0934_page-0001.jpg'
img = cv2.imread(img_path)
h, w = img.shape[:2]

boxes = {
    "collimo": (0.72, 0.05, 0.23, 0.20),
    "nyanmi": (0.13, 0.32, 0.25, 0.26),
    "kuromi": (0.33, 0.30, 0.32, 0.28),
    "romina": (0.62, 0.30, 0.25, 0.28),
    "bako": (0.83, 0.46, 0.16, 0.16),
    "gareco": (0.02, 0.54, 0.30, 0.26),
    "koni": (0.37, 0.60, 0.20, 0.16),
    "chumi": (0.22, 0.72, 0.20, 0.15),
    "konmi": (0.48, 0.68, 0.15, 0.17),
    "baku": (0.58, 0.58, 0.25, 0.25),
    "wanmi": (0.82, 0.63, 0.18, 0.18),
}

os.makedirs("characters", exist_ok=True)

for name, (rx, ry, rw, rh) in boxes.items():
    x = int(rx * w)
    y = int(ry * h)
    bw = int(rw * w)
    bh = int(rh * h)
    
    # Crop
    cropped_img = img[y:y+bh, x:x+bw].copy()
    
    # Enhance
    pil_img = Image.fromarray(cv2.cvtColor(cropped_img, cv2.COLOR_BGR2RGB))
    enhancer = ImageEnhance.Contrast(pil_img)
    pil_img = enhancer.enhance(1.5)
    enhancer = ImageEnhance.Color(pil_img)
    pil_img = enhancer.enhance(1.2)
    enhanced_img = cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)
    
    gray = cv2.cvtColor(enhanced_img, cv2.COLOR_BGR2GRAY)
    
    # Clean paper noise
    gray_blur = cv2.medianBlur(gray, 5)
    
    # Adaptive threshold to isolate ink lines perfectly regardless of shadow
    fg_mask = cv2.adaptiveThreshold(gray_blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 21, 10)
    
    # Dilate heavily to bridge gaps between limbs and body
    # Using 9x9 kernel, 2 iterations ensures hands and feet connect to the body
    kernel = np.ones((9, 9), np.uint8)
    dilated = cv2.dilate(fg_mask, kernel, iterations=2)
    
    # Find connected components to isolate the character from other surrounding noise/characters
    num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(dilated, connectivity=8)
    
    if num_labels > 1:
        # Find the largest component (excluding background label 0)
        largest_label = 1
        max_area = stats[1, cv2.CC_STAT_AREA]
        for i in range(2, num_labels):
            if stats[i, cv2.CC_STAT_AREA] > max_area:
                max_area = stats[i, cv2.CC_STAT_AREA]
                largest_label = i
        
        blob_mask = np.zeros_like(fg_mask)
        blob_mask[labels == largest_label] = 255
        
        # The blob_mask is currently larger than the character.
        # We find its external contours and fill it, giving a solid silhouette.
        contours, _ = cv2.findContours(blob_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        final_mask = np.zeros_like(gray)
        
        # Shrink the contour slightly before drawing to avoid a large white aura
        # We can just draw the contour, then erode the final_mask
        cv2.drawContours(final_mask, contours, -1, 255, thickness=cv2.FILLED)
        
        # Erode to reverse the dilation effect on the boundary
        final_mask = cv2.erode(final_mask, kernel, iterations=2)
        
        # Anti-aliasing
        final_mask = cv2.GaussianBlur(final_mask, (5, 5), 0)
    else:
        final_mask = np.zeros_like(gray)
        
    b, g, r = cv2.split(enhanced_img)
    rgba = cv2.merge((b, g, r, final_mask))
    
    output_path = f"characters/{name}.png"
    cv2.imwrite(output_path, rgba)
    print(f"Saved {output_path}")

print("Processing complete.")
