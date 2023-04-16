#coding:utf-8

import cv2
import numpy as np


def get_obj_pos(img, color):
    img = cv2.erode(img, None, iterations=2)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, color_dist[color]['Lower'], color_dist[color]['Upper'])
    square = np.sum(mask)
    print(square)
    res = cv2.bitwise_and(img, img, mask=mask)
    gray = cv2.cvtColor(res, cv2.COLOR_BGR2GRAY)
    ret, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY)
    contours, hierarchy = cv2.findContours(binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    if (len(contours) > 0) and (square > 1600):
        c = max(contours, key=cv2.contourArea)
        x, y, w, h = cv2.boundingRect(c)
        pos_x = x + w / 2
        pos_y = y + h / 2

        if (pos_x > pos_seg_x[1] and pos_x < pos_seg_x[2]) and (pos_y > pos_seg_y[0] and pos_y < pos_seg_y[1]):
            pos = 1
        elif (pos_x > pos_seg_x[2] and pos_x < pos_seg_x[3]) and (pos_y > pos_seg_y[0] and pos_y < pos_seg_y[1]):
            pos = 2
        elif (pos_x > pos_seg_x[3] and pos_x < pos_seg_x[4]) and (pos_y > pos_seg_y[0] and pos_y < pos_seg_y[1]):
            pos = 3
        elif (pos_x > pos_seg_x[1] and pos_x < pos_seg_x[2]) and (pos_y > pos_seg_y[1] and pos_y < pos_seg_y[2]):
            pos = 4
        elif (pos_x > pos_seg_x[2] and pos_x < pos_seg_x[3]) and (pos_y > pos_seg_y[1] and pos_y < pos_seg_y[2]):
            pos = 5
        elif (pos_x > pos_seg_x[3] and pos_x < pos_seg_x[4]) and (pos_y > pos_seg_y[1] and pos_y < pos_seg_y[2]):
            pos = 6
        else :
            pos = 0

        cv2.imshow('res', res)
        cv2.waitKey(1)
        return pos
    else:
        return None


if __name__ == '__main__':
    ball_color = 1

    color_dist = {'red': {'Lower': np.array([0, 50, 50]), 'Upper': np.array([6, 255, 255])},
                'blue': {'Lower': np.array([100, 80, 46]), 'Upper': np.array([124, 255, 255])},
                'green': {'Lower': np.array([35, 43, 35]), 'Upper': np.array([90, 255, 255])},
                }

    pos_seg_x = [0, 213, 427, 640]
    pos_seg_y = [0, 240, 480]

    cap = cv2.VideoCapture(0)

    while cap.isOpened():
        ret, frame = cap.read()
        frame = cv2.erode(frame, None, iterations=2)

        if frame is not None:
            # 上下图像分割
            frame_up = frame[0:240, 0:320]
            frame_down = frame[240:480, 0:320]

            # 获取目标位置
            pos_red_up = get_obj_pos(frame_up, 'red')
            print(pos_red_up)
            # pos_blue_up = get_obj_pos(frame_up, 'blue')
            # pos_green_up = get_obj_pos(frame_up, 'green')
            # pos_red_down = get_obj_pos(frame_down, 'red')
            # pos_blue_down = get_obj_pos(frame_down, 'blue')
            # pos_green_down = get_obj_pos(frame_down, 'green')

            # # 结果显示
            # cv2.imshow("Keypoints", im_with_keypoints)
            # cv2.waitKey(1)

        else:
            print("无画面")
    
    cap.release()
    cv2.waitKey(0)
    cv2.destroyAllWindows()




