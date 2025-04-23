import cv2
import numpy as np
from struct import pack

input_path = "data/rabbit2.jpg"
output_raw_path = "data/rabbit2.raw"

image = cv2.imread(input_path)
image_resized = cv2.resize(image, (220, 296), interpolation=cv2.INTER_AREA)
image_resized = cv2.cvtColor(image_resized, cv2.COLOR_BGR2RGB)

height, width, _ = image_resized.shape

rgb565_data = bytearray()
for y in range(height):
    for x in range(width):
        r, g, b = image_resized[y, x]
        r5 = (r >> 3) & 0x1F  # 赤 (5bit)
        g6 = (g >> 2) & 0x3F  # 緑 (6bit)
        b5 = (b >> 3) & 0x1F  # 青 (5bit)
        rgb565 = (r5 << 11) | (g6 << 5) | b5  # RGB565に変換
        rgb565_data += pack('>H', rgb565)

with open(output_raw_path, "wb") as f:
    f.write(rgb565_data)