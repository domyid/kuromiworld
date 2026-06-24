import cv2
import os

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

# Adjusted boxes
adjusted_boxes = {
    "collimo": (0.72, 0.05, 0.23, 0.20),
    "nyanmi": (0.13, 0.32, 0.24, 0.26),
    "kuromi": (0.35, 0.30, 0.27, 0.28),  # Shifted right, narrower
    "romina": (0.62, 0.30, 0.22, 0.28),
    "bako": (0.84, 0.46, 0.15, 0.16),
    "gareco": (0.02, 0.54, 0.30, 0.26),
    "koni": (0.37, 0.60, 0.20, 0.16),
    "chumi": (0.22, 0.72, 0.20, 0.15),
    "konmi": (0.48, 0.68, 0.13, 0.17),
    "baku": (0.55, 0.58, 0.27, 0.25),    # Shifted left, wider
    "wanmi": (0.82, 0.63, 0.18, 0.18),
}

for name, (rx, ry, rw, rh) in adjusted_boxes.items():
    x = int(rx * w)
    y = int(ry * h)
    bw = int(rw * w)
    bh = int(rh * h)
    
    cv2.rectangle(img, (x, y), (x+bw, y+bh), (0, 255, 0), 5)
    cv2.putText(img, name, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 4)

cv2.imwrite("debug_boxes.jpg", img)
print("Saved debug_boxes.jpg")
