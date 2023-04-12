#coding:utf-8
import cv2
import numpy as np

color_dist = {'red': {'Lower': np.array([120, 120, 120]), 'Upper': np.array([180, 255, 255])},
              'blue': {'Lower': np.array([60, 120, 120]), 'Upper': np.array([120, 255, 255])},
              'green': {'Lower': np.array([0, 120, 120]), 'Upper': np.array([60, 255, 255])},
             }

pos_seg_x = [0, 1000]
pos_seg_y = [0, 1000]
square_threshold = 0.3


def get_pos_color(img):
    """
    从图像中获取色块位置和颜色
    """
    img = cv2.erode(img, None, iterations=1)          # 图像腐蚀
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)        # RGB转化为HSV
    img_height, img_width, img_channels = img.shape

    # 遍历三个颜色
    color_list = ['red', 'blue', 'green']
    # color_list = ['red']
    for color in color_list:
        # 截取该颜色的部分
        mask = cv2.inRange(hsv, color_dist[color]['Lower'], color_dist[color]['Upper'])

        img_and = cv2.bitwise_and(img, img, mask=mask)
        gray = cv2.cvtColor(img_and, cv2.COLOR_BGR2GRAY)
        res, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        square = np.sum(binary) / (img_height * img_width) / 255              # 计算该颜色部分的面积占比
        # print(color, square)
        contours, hierarchy = cv2.findContours(binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        # 如果该颜色部分大于阈值
        if (len(contours) > 0) and (square > square_threshold):
            cnt = max(contours, key=cv2.contourArea)

            # 从边缘中获取最小包围圆和其中点
            (x, y), radius = cv2.minEnclosingCircle(cnt)
            pos_x = x
            pos_y = y
            pos = [pos_x, pos_y]
            
            # 检测该圆是否在目标范围内
            if ((pos_x > pos_seg_x[0]) and (pos_x < pos_seg_x[1])) and ((pos_y > pos_seg_y[0]) and (pos_y < pos_seg_y[1])):
                color_obj = color

                return binary, pos, color_obj

    # 如果不是三个颜色
    return binary, [-1, -1], None

    # cv2.imshow('res', binary)
    # cv2.waitKey(1)


if __name__ == '__main__':
    cap = cv2.VideoCapture(1)

    while cap.isOpened():
        ret, frame = cap.read()
        # frame = cv2.imread('./green_circle.png') # 根据路径读取一张图片

        if frame is not None:
            # 获取色块位置和颜色
            binary, pos, color = get_pos_color(frame)
            print(pos, color)

            # 结果显示
            cv2.imshow("frame", frame)
            # cv2.imshow('binary', binary)
            cv2.waitKey(1)

        else:
            print("无画面")
    
    cap.release()
    cv2.waitKey(0)
    cv2.destroyAllWindows()
