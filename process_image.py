import cv2
import numpy as np
import os
from PIL import Image, ImageEnhance

# Load image
img_path = 'Dipindai_20260624-0934_page-0001.jpg'
img = cv2.imread(img_path)
h, w = img.shape[:2]
print(f'Image size: {w}x{h}')

# Define bounding boxes based on relative positions (x, y, w, h)
# Estimating based on a 1x1 grid relative coordinates:
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

# Convert relative to absolute
abs_boxes = {}
for name, (rx, ry, rw, rh) in boxes.items():
    x = int(rx * w)
    y = int(ry * h)
    bw = int(rw * w)
    bh = int(rh * h)
    abs_boxes[name] = (x, y, bw, bh)

# Draw these boxes on a debug image
debug_img = img.copy()
for name, (x, y, bw, bh) in abs_boxes.items():
    cv2.rectangle(debug_img, (x, y), (x+bw, y+bh), (0, 255, 0), 5)
    cv2.putText(debug_img, name, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 255), 3)

cv2.imwrite('debug_boxes.jpg', debug_img)
print("Saved debug_boxes.jpg")
