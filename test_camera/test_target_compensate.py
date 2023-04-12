#coding:utf-8
import cv2
import numpy as np
import time


def get_target_bias(img):
    """
    从图像中识别最大靶的靶心坐标并计算图像中心与其偏差（百分比）
    """
    # 压缩图像大小
    img = cv2.resize(img, (180, 135))
    
    # # RGB图像去阴影
    # rgb_frame = cv2.split(img)
    # without_shadow_list = []
    # for plane in rgb_frame:
    #     dilated_img = cv2.dilate(plane, np.ones((7,7), np.uint8))    # 膨胀
    #     blured_img = cv2.medianBlur(dilated_img, 9)                  # 中值滤波
    #     diff_img = 255 - cv2.absdiff(plane, blured_img)
    #     norm_img = cv2.normalize(diff_img, None, 0, 255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8UC1)
    #     without_shadow_list.append(norm_img)
    # without_shadow = cv2.merge(without_shadow_list)

    # RGB图像去阴影
    dilated_img = cv2.dilate(img, np.ones((5,5), np.uint8))    # 膨胀
    blured_img = cv2.medianBlur(dilated_img, 9)                  # 中值滤波
    diff_img = 255 - cv2.absdiff(img, blured_img)
    # norm_img = cv2.normalize(diff_img, None, 0, 255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8UC1)
    
    # 对每个通道单独进行归一化
    norm_img = np.zeros_like(img)
    for i in range(3):
        channel = diff_img[:,:,i]
        channel_min = channel.min()
        channel_max = channel.max()
        norm_channel = (channel - channel_min) / (channel_max - channel_min)
        norm_img[:,:,i] = np.uint8(255 * norm_channel)

    # RGB图像转灰度图
    gray = cv2.cvtColor(norm_img, cv2.COLOR_BGR2GRAY)
    cv2.imshow("gray", gray)

    # 从二值化图中提取轮廓
    res, binary = cv2.threshold(gray, 100, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

    # # 先膨胀后腐蚀
    kernel_dilate = np.ones((5, 5),np.uint8)
    # kernel_erode = np.ones((7, 7),np.uint8)
    dst = cv2.dilate(binary, kernel_dilate)
    # dst = cv2.erode(binary, kernel_erode)
    cv2.imshow("erode", dst)

    contours_circle, hierarchy = cv2.findContours(dst, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # 找到面积最大的轮廓
    area = [cv2.contourArea(c) for c in contours_circle]
    index_max = np.argmax(area)
    contours_max = contours_circle[index_max]

    # 找到最大轮廓的外包围圆
    # temp = np.zeros(img.shape,np.uint8)
    # img_contours = cv2.drawContours(temp, contours_max, -1, (0, 0, 255), 3)  # 绘制轮廓
    (x, y), radius = cv2.minEnclosingCircle(contours_max)
    # img_contours = cv2.circle(img_contours, (int(x), int(y)), int(radius), (255, 0, 0), 3)

    # 从二值化图中截取圆形部分
    mask_circle = np.zeros(img.shape[:2], np.uint8)
    mask_circle = cv2.circle(mask_circle, (int(x),int(y)), int(radius), 255, cv2.FILLED)
    mask = np.zeros_like(mask_circle) * 255
    binary = cv2.bitwise_and(binary, binary, mask=mask_circle)

    # cv2.imshow("gray", gray)
    # cv2.imshow("binary", binary)
    # cv2.imshow("img_contours", img_contours)

    kernel_h = cv2.getStructuringElement(cv2.MORPH_RECT, (20, 1), (-1, -1))       # 70列1行的kernel
    kernel_v = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 20), (-1, -1))       # 1列70行的kernel
    line_h = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel_h, (-1, -1))
    line_v = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel_v, (-1, -1))

    # cv2.imshow("hline", line_h)
    # cv2.imshow("vline", line_v)

    # 获得十字架横线
    contours_h, hierarchy = cv2.findContours(line_h, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)      # 获取所有横线边缘
    target = np.zeros_like(line_h, np.uint8)
    area = [cv2.contourArea(contour_h) for contour_h in contours_h]                                 # 获取面积最大的横线
    if len(area) > 0:
        index_max = np.argmax(area)
        cv2.drawContours(target, contours_h, index_max, (255, 255, 255), -1, 8)
    
    # cv2.imshow("line_h", target)

    # 获得十字架竖线
    contours_v, hierarchy = cv2.findContours(line_v, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    area = [cv2.contourArea(contour_v) for contour_v in contours_v]
    if len(area) > 0:
        index_max = np.argmax(area)
        cv2.drawContours(target, contours_v, index_max, (255, 255, 255), -1, 8)

    cv2.imshow("line_h + line_v", target)

    # 获得中心十字靶
    kernel_cross = cv2.getStructuringElement(cv2.MORPH_CROSS, (13, 13), (-1, -1))
    target = cv2.morphologyEx(target, cv2.MORPH_OPEN, kernel_cross, (-1, -1))

    # cv2.imshow("cross", target)

    # 获取靶心坐标
    contours_cross, hierarchy = cv2.findContours(target, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    if len(contours_cross) > 0:
        rect = cv2.minAreaRect(contours_cross[0])
        center = (int(rect[0][0]), int(rect[0][1]))

        img = cv2.circle(img, center, 4, (0, 0, 255), 1, 8)
        cv2.imshow("result", img)

        # 计算图像中心与靶心坐标的偏差
        img_height, img_width, img_channels = img.shape
        img_center_x = int(float(img_width) / 2.0)
        img_center_y = int(float(img_height) / 2.0)
        x_bias = float(float(img_center_x - center[0]) / float(img_width))
        y_bias = float(float(img_center_y - center[1]) / float(img_height))

        return x_bias+0.077, y_bias

    else:
        return 0, 0


if __name__ == '__main__':
    cap = cv2.VideoCapture(1)

    # while cap.isOpened():
        # ret, frame = cap.read()
    frame = cv2.imread('./test2.png')     # 根据路径读取一张图片
    # frame = cv2.imread('./test.jpg')     # 根据路径读取一张图片

    start_time = time.time()
    if frame is not None:
        x_bias, y_bias = get_target_bias(frame)
        # cv2.imshow("result", frame)
        cv2.waitKey(1)
    
    end_time = time.time()
    time.sleep(0.1)

    print("time:", end_time - start_time)

    cap.release()
    cv2.waitKey(0)
    cv2.destroyAllWindows()