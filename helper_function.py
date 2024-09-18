import math
import cv2

def arrowdraw(img, x1, y1, x2, y2):
    radians = math.atan2(y2-y1, x2-x1)  # 修改为 atan2(y2-y1, x2-x1) 以获取正确的角度
    arrow_length = 8  # 箭头长度减小为 8
    arrow_width = 5  # 箭头宽度为 5

    # 箭头尖端部分
    x11 = arrow_length * math.cos(radians + math.pi / 6)
    y11 = arrow_length * math.sin(radians + math.pi / 6)
    x12 = arrow_length * math.cos(radians - math.pi / 6)
    y12 = arrow_length * math.sin(radians - math.pi / 6)

    # 计算箭头尖端的终点坐标
    x11_ = x2 - x11
    y11_ = y2 - y11
    x12_ = x2 - x12
    y12_ = y2 - y12

    # 画主线
    img = cv2.line(img, (x1, y1), (x2, y2), (255, 255, 255), 2)
    # 画箭头翼
    img = cv2.line(img, (int(x2), int(y2)), (int(x11_), int(y11_)), (255, 255, 255), 1)
    img = cv2.line(img, (int(x2), int(y2)), (int(x12_), int(y12_)), (255, 255, 255), 1)
    
    return img