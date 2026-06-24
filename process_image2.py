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
    
    # Crop the image first
    cropped_img = img[y:y+bh, x:x+bw].copy()
    
    # Enhance
    pil_img = Image.fromarray(cv2.cvtColor(cropped_img, cv2.COLOR_BGR2RGB))
    enhancer = ImageEnhance.Contrast(pil_img)
    pil_img = enhancer.enhance(1.5)
    enhancer = ImageEnhance.Color(pil_img)
    pil_img = enhancer.enhance(1.2)
    enhanced_img = cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)
    
    # Apply GrabCut for precise foreground extraction
    mask = np.zeros(enhanced_img.shape[:2], np.uint8)
    bgdModel = np.zeros((1, 65), np.float64)
    fgdModel = np.zeros((1, 65), np.float64)
    
    # We define a rectangle that leaves a small margin (e.g., 5 pixels)
    # Everything outside the rectangle is definitely background.
    # Everything inside is probably foreground.
    margin = 5
    rect = (margin, margin, enhanced_img.shape[1] - 2*margin, enhanced_img.shape[0] - 2*margin)
    
    cv2.grabCut(enhanced_img, mask, rect, bgdModel, fgdModel, 5, cv2.GC_INIT_WITH_RECT)
    
    # mask==2 or mask==0 means background. mask==1 or mask==3 means foreground.
    mask2 = np.where((mask==2)|(mask==0), 0, 1).astype('uint8')
    
    # Keep only the largest connected component
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
    
    # Find contours to fill internal holes (like white eyes or stomach)
    contours, _ = cv2.findContours(mask2, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    final_mask = np.zeros(enhanced_img.shape[:2], np.uint8)
    cv2.drawContours(final_mask, contours, -1, 255, thickness=cv2.FILLED)
    
    # Smooth the edges
    final_mask = cv2.GaussianBlur(final_mask, (5, 5), 0)
    
    # Merge with original image alpha
    b, g, r = cv2.split(enhanced_img)
    rgba = cv2.merge((b, g, r, final_mask))
    
    output_path = f"characters/{name}.png"
    cv2.imwrite(output_path, rgba)
    print(f"Saved {output_path}")

print("Processing complete.")
