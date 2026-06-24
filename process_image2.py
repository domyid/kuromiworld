import cv2
import numpy as np
import os
from PIL import Image, ImageEnhance

# Load image
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

abs_boxes = {}
for name, (rx, ry, rw, rh) in boxes.items():
    x = int(rx * w)
    y = int(ry * h)
    bw = int(rw * w)
    bh = int(rh * h)
    abs_boxes[name] = (x, y, bw, bh)

os.makedirs("characters", exist_ok=True)

for name, (x, y, bw, bh) in abs_boxes.items():
    cropped = img[y:y+bh, x:x+bw]
    pil_img = Image.fromarray(cv2.cvtColor(cropped, cv2.COLOR_BGR2RGB))
    
    # Enhance contrast
    enhancer = ImageEnhance.Contrast(pil_img)
    pil_img = enhancer.enhance(1.5)
    
    # Enhance color
    enhancer = ImageEnhance.Color(pil_img)
    pil_img = enhancer.enhance(1.2)
    
    # Make white background transparent
    pil_img = pil_img.convert("RGBA")
    datas = pil_img.getdata()
    
    newData = []
    # threshold for paper background
    for item in datas:
        if item[0] > 180 and item[1] > 180 and item[2] > 180:
            newData.append((255, 255, 255, 0))
        else:
            newData.append(item)
            
    pil_img.putdata(newData)
    
    # Save image
    output_path = f"characters/{name}.png"
    pil_img.save(output_path, "PNG")
    print(f"Saved {output_path}")

print("Processing complete.")
