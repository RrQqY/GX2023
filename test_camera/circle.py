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

    # RGB图像去阴影
    dilated_img = cv2.dilate(img, np.ones((5,5), np.uint8))    # 膨胀
    blured_img = cv2.medianBlur(dilated_img, 9)                  # 中值滤波
    diff_img = 255 - cv2.absdiff(img, blured_img)
    norm_img = cv2.normalize(diff_img, None, 0, 255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8UC1)
    
    # # 对每个通道单独进行归一化
    # norm_img = np.zeros_like(img)
    # for i in range(3):
    #     channel = diff_img[:,:,i]
    #     channel_min = channel.min()
    #     channel_max = channel.max()
    #     norm_channel = (channel - channel_min) / (channel_max - channel_min)
    #     norm_img[:,:,i] = np.uint8(255 * norm_channel)

    # RGB图像转灰度图
    gray = cv2.cvtColor(norm_img, cv2.COLOR_BGR2GRAY)
    cv2.imshow("gray", gray)
 
    # 从二值化图中提取轮廓
    res, binary = cv2.threshold(gray, 100, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

    # # 先膨胀后腐蚀
    # kernel_dilate = np.ones((5, 5),np.uint8)
    # kernel_erode = np.ones((7, 7),np.uint8)
    # dst = cv2.dilate(binary, kernel_dilate)
    # dst = cv2.erode(binary, kernel_erode)
    # cv2.imshow("erode", dst)

    contours_circle, hierarchy = cv2.findContours(binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # 找到面积最大的轮廓
    area = [cv2.contourArea(c) for c in contours_circle]
    index_max = np.argmax(area)
    contours_max = contours_circle[index_max]

    contoursImg = cv2.drawContours(img, contours_max, -1, (255,0,0), 1)  #绘制轮廓
    cv2.imshow("contoursImg", contoursImg)

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

    gaussianResult = cv2.GaussianBlur(binary,(3,3),2.5)
    cv2.imshow("gaussianResult", gaussianResult)

    # cv2.imshow("gray", gray)
    cv2.imshow("binary", binary)
    # cv2.imshow("img_contours", img_contours)
    # 以上部分预处理完成，下面开始识别十字架

    # 检测圆形
    circles = cv2.HoughCircles(gaussianResult, cv2.HOUGH_GRADIENT, dp=1, minDist=180, param1=40, param2=30, minRadius=15, maxRadius=100)

    # 输出检测到的圆形
    max_radius = 0
    max_circle = None
    if circles is not None:
        circles = np.round(circles[0, :]).astype("int")
        for (x, y, r) in circles:
            if r > max_radius:
                max_radius = r
                max_circle = (x, y, r)

        # 绘制圆环和最大圆环
        if max_circle is not None:
            (x, y, r) = max_circle
            cv2.circle(img, (x, y), r, (0, 0, 255), 2)
            print(r)
        cv2.imshow("output", img)

        img_height, img_width, img_channels = img.shape
        img_center_x = int(float(img_width) / 2.0)
        img_center_y = int(float(img_height) / 2.0)
        x_bias = float(float(img_center_x - x) / float(img_width))
        y_bias = float(float(img_center_y - y) / float(img_height))
        return x_bias+0.077, y

    else:
        print("no circles")
        return x_bias+0.077, y_bias



if __name__ == '__main__':
    cap = cv2.VideoCapture(1)

    # while cap.isOpened():
        # ret, frame = cap.read()
    frame = cv2.imread('./t1.jpg')     # 根据路径读取一张图片
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