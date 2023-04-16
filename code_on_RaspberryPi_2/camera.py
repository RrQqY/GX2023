#coding:utf-8

import numpy as np
import time
import serial
import cv2
from uservo import UartServoManager
import math

class Camera():
    """
    摄像头函数类
    """
    def __init__(self):
        # 初始化摄像头
        self.cap = cv2.VideoCapture(0)

        ### 物块颜色获取部分
        # 红绿蓝三色HSV阈值
        self.color_dist = {'r': {'Lower': np.array([120, 28, 0]), 'Upper': np.array([180, 255, 241])},
              'g': {'Lower': np.array([60, 28, 0]), 'Upper': np.array([120, 255, 241])},
              'b': {'Lower': np.array([0, 28, 0]), 'Upper': np.array([60, 255, 241])},
             }
        
        self.white_threshold = 200       # 白色阈值
            
        self.pos_seg_x = [0.1, 0.9]       # 物体色块在图像中位置阈值
        self.pos_seg_y = [0.1, 0.9]
        self.square_threshold = 0.2      # 检测面积占比阈值

        self.thresh_square = 0.1         # 靶标面积阈值
        self.x_bias = 0.0
        self.y_bias = 0.0

        ### 靶标位置偏差获取部分

    
    def get_obj_color(self, img):
        """
        从图像中获取色块位置和颜色
        """
        img = cv2.erode(img, None, iterations=1)          # 图像腐蚀
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)        # RGB转化为HSV
        img_height, img_width, img_channels = img.shape

        # cv2.imshow('hsv', hsv)
        # cv2.waitKey(1)

        # 遍历三个颜色
        color_list = ['red', 'green', 'blue']
        # color_list = ['red']
        for color in color_list:
            # 截取该颜色的部分
            mask = cv2.inRange(hsv, self.color_dist[color]['Lower'], self.color_dist[color]['Upper'])

            img_and = cv2.bitwise_and(img, img, mask=mask)
            gray = cv2.cvtColor(img_and, cv2.COLOR_BGR2GRAY)
            res, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

            # cv2.imshow('binary', binary)
            # cv2.waitKey(1)

            square = float(float(np.sum(binary)) / float(img_height * img_width) / 255.0)          # 计算该颜色部分的面积占比
            # print(color, np.sum(binary), img_height, img_width, square)
            contours, hierarchy = cv2.findContours(binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

            # 如果该颜色部分大于阈值
            if (len(contours) > 0) and (square > self.square_threshold):
                cnt = max(contours, key=cv2.contourArea)

                # 从边缘中获取最小包围圆和其中点
                (x, y), radius = cv2.minEnclosingCircle(cnt)
                pos_x = float(float(x) / float(img_width))
                pos_y = float(float(y) / float(img_height))
                pos = [pos_x, pos_y]
                
                # 检测该圆是否在目标范围内
                if ((pos_x > self.pos_seg_x[0]) and (pos_x < self.pos_seg_x[1])) and ((pos_y > self.pos_seg_y[0]) and (pos_y < self.pos_seg_y[1])):
                    color_obj = color

                    return color_obj, pos

        # 如果不是三个颜色
        return None, [-1, -1]
    

    def get_target_bias_circle(self, img, side=1):
        """
        利用圆环识别, 从图像中识别最大靶的靶心坐标并计算图像中心与其偏差 (百分比) 
        """
        # 压缩图像大小
        img = cv2.resize(img, (180, 135))
        # cv2.imshow("img", img)

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
        # cv2.imshow("gray", gray)
    
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
        # cv2.imshow("contoursImg", contoursImg)

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
        # cv2.imshow("binary", binary)

        gaussianResult = cv2.GaussianBlur(binary,(3,3),2.5)
        # cv2.imshow("gaussianResult", gaussianResult)

        # cv2.imshow("gray", gray)
        # cv2.imshow("binary", binary)
        # cv2.imshow("img_contours", img_contours)
        # 以上部分预处理完成, 下面开始识别十字架

        # 检测圆形
        # 不同矫正区域检测参数不同, side=1, side=2为上方 / 左侧加工区, side=3为带物块时的左侧加工区(更宽松, 因为可能出现物块和圆环重叠)
        if side == 1 or side == 2:
            circles = cv2.HoughCircles(gaussianResult, cv2.HOUGH_GRADIENT, dp=1, minDist=180, param1=75, param2=75, minRadius=10, maxRadius=40)
        elif side == 3 or side == 4:
            circles = cv2.HoughCircles(gaussianResult, cv2.HOUGH_GRADIENT, dp=1, minDist=180, param1=45, param2=45, minRadius=10, maxRadius=40)

        # 输出检测到的圆形
        max_radius = 0
        max_circle = None
        img_height, img_width, img_channels = img.shape
        img_center_x = int(float(img_width) / 2.0)
        img_center_y = int(float(img_height) / 2.0)
        x_b = img_width
        y_b = img_height
        min_center_b = img_width + img_height

        if circles is not None:
            circles = np.round(circles[0, :]).astype("int")

            # 找到最靠近中心的圆环
            for (x, y, r) in circles:
                x_b = abs(x - img_center_x)
                y_b = abs(y - img_center_y)
                center_b = math.sqrt(x_b ** 2 + y_b ** 2)
                # if r > max_radius:
                #     max_radius = r
                #     max_circle = (x, y, r)
                if center_b < min_center_b:
                    min_center_b = center_b
                    max_circle = (x, y, r)

            # 绘制圆环和最大圆环
            if max_circle is not None:
                (x, y, r) = max_circle
                cv2.circle(img, (x, y), r, (0, 0, 255), 2)
                # print(r)
            cv2.imshow("result", img)

            self.x_bias = float(float(img_center_x - x) / float(img_width))
            self.y_bias = float(float(img_center_y - y) / float(img_height))
            # return self.x_bias + 0.077, self.y_bias
            return self.x_bias + 0.036, self.y_bias

        else:
            print("no circles")
            # return self.x_bias + 0.077, self.y_bias
            return self.x_bias + 0.036, self.y_bias


    def get_target_bias_cross(self, img):
        """
        利用十字交叉点识别, 从图像中识别最大靶的靶心坐标并计算图像中心与其偏差 (百分比) 
        """
        # 压缩图像大小
        img = cv2.resize(img, (180,135))
        
        # cv2.imwrite('test.jpg',img,[int(cv2.IMWRITE_JPEG_QUALITY),70])
        
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
        norm_img = cv2.normalize(diff_img, None, 0, 255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8UC1)

        # RGB图像转灰度图
        gray = cv2.cvtColor(norm_img, cv2.COLOR_BGR2GRAY)
        # cv2.imshow("gray", gray)

        # 从二值化图中提取轮廓
        res, binary = cv2.threshold(gray, 100, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

        # # 先膨胀后腐蚀
        # kernel_dilate = np.ones((5, 5),np.uint8)
        # kernel_erode = np.ones((7, 7),np.uint8)
        # # dst = cv2.dilate(binary, kernel_dilate)
        # dst = cv2.erode(binary, kernel_erode)
        # cv2.imshow("erode", dst)

        contours_circle, hierarchy = cv2.findContours(binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

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

        kernel_h = cv2.getStructuringElement(cv2.MORPH_RECT, (70, 1), (-1, -1))       # 70列1行的kernel
        kernel_v = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 70), (-1, -1))       # 1列70行的kernel
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
        # cv2.imshow("line_h + line_v", target)

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
            # cv2.imshow("result", img)

            # 计算图像中心与靶心坐标的偏差
            img_height, img_width, img_channels = img.shape
            img_center_x = int(float(img_width) / 2.0)
            img_center_y = int(float(img_height) / 2.0)
            self.x_bias = float(float(img_center_x - center[0]) / float(img_width))
            self.y_bias = float(float(img_center_y - center[1]) / float(img_height))

            return self.x_bias+0.077, self.y_bias

        else:
            print("no cross found")
            return self.x_bias+0.077, self.y_bias
        
    
    def get_target_color(self, img, side=1):
        # 压缩图像大小
        img = cv2.resize(img, (180, 135))
        # cv2.imshow("img", img)

        # RGB图像去阴影
        dilated_img = cv2.dilate(img, np.ones((5,5), np.uint8))    # 膨胀
        blured_img = cv2.medianBlur(dilated_img, 9)                  # 中值滤波
        diff_img = 255 - cv2.absdiff(img, blured_img)
        norm_img = cv2.normalize(diff_img, None, 0, 255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8UC1)

        # RGB图像转灰度图
        gray = cv2.cvtColor(norm_img, cv2.COLOR_BGR2GRAY)
        # cv2.imshow("gray", gray)
    
        # 从二值化图中提取轮廓
        res, binary = cv2.threshold(gray, 100, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

        contours_circle, hierarchy = cv2.findContours(binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        # 找到面积最大的轮廓
        area = [cv2.contourArea(c) for c in contours_circle]
        index_max = np.argmax(area)
        contours_max = contours_circle[index_max]

        contoursImg = cv2.drawContours(img, contours_max, -1, (255,0,0), 1)  #绘制轮廓
        # cv2.imshow("contoursImg", contoursImg)

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
        # cv2.imshow("binary", binary)

        gaussianResult = cv2.GaussianBlur(binary,(3,3),2.5)
        # cv2.imshow("gaussianResult", gaussianResult)

        # cv2.imshow("gray", gray)
        # cv2.imshow("binary", binary)
        # cv2.imshow("img_contours", img_contours)
        # 以上部分预处理完成, 下面开始识别十字架

        # 检测圆形
        # 不同矫正区域检测参数不同, side=1, side=2为上方 / 左侧加工区, side=3为带物块时的左侧加工区(更宽松, 因为可能出现物块和圆环重叠)
        if side == 1 or side == 2:
            circles = cv2.HoughCircles(gaussianResult, cv2.HOUGH_GRADIENT, dp=1, minDist=180, param1=75, param2=75, minRadius=10, maxRadius=40)
        elif side == 3 or side == 4:
            circles = cv2.HoughCircles(gaussianResult, cv2.HOUGH_GRADIENT, dp=1, minDist=180, param1=45, param2=45, minRadius=10, maxRadius=40)

        # 输出检测到的圆形
        max_radius = 0
        max_circle = None
        img_height, img_width, img_channels = img.shape
        img_center_x = int(float(img_width) / 2.0)
        img_center_y = int(float(img_height) / 2.0)
        x_b = img_width
        y_b = img_height
        min_center_b = img_width + img_height

        if circles is not None:
            circles = np.round(circles[0, :]).astype("int")

            # 找到最靠近中心的圆环
            for (x, y, r) in circles:
                x_b = abs(x - img_center_x)
                y_b = abs(y - img_center_y)
                center_b = math.sqrt(x_b ** 2 + y_b ** 2)
                # if r > max_radius:
                #     max_radius = r
                #     max_circle = (x, y, r)
                if center_b < min_center_b:
                    min_center_b = center_b
                    max_circle = (x, y, r)

            # 绘制圆环和最大圆环
            if max_circle is not None:
                (x, y, r) = max_circle
                cv2.circle(img, (x, y), r, (0, 0, 255), 2)
                # print(r)
            # cv2.imshow("result", img)

            # 从圆环制作掩膜
            target_mask_circle = np.zeros(img.shape[:2], np.uint8)
            target_mask_circle = cv2.circle(target_mask_circle, (int(x),int(y)), int(r), 255, cv2.FILLED)
            target_mask = np.zeros_like(mask_circle) * 255

            # 将norm_img与掩膜相与
            target_img = cv2.bitwise_and(norm_img, norm_img, mask=target_mask_circle)
            cv2.imshow("target_binary", target_img)

            # # 将圆环中所有白色像素设置为0
            # # 将图像分解为三通道
            # (target_img_b, target_img_g, target_img_r) = cv2.split(target_img)
            # target_img_b[target_img_b >= self.white_threshold] = 0
            # target_img_g[target_img_g >= self.white_threshold] = 0
            # target_img_r[target_img_r >= self.white_threshold] = 0
            # # 将图像合并为单通道
            # target_img = cv2.merge([target_img_b, target_img_g, target_img_r])

            target_img = cv2.erode(target_img, None, iterations=8)          # 图像腐蚀
            cv2.imshow("target_binary", target_img)

            target_img = cv2.cvtColor(target_img, cv2.COLOR_BGR2HSV)        # RGB转化为HSV

            # 遍历三个颜色
            color_list = ['g']
            # color_list = ['red']
            for color in color_list:
                # 截取该颜色的部分
                mask = cv2.inRange(target_img, self.color_dist[color]['Lower'], self.color_dist[color]['Upper'])

                target_img_and = cv2.bitwise_and(target_img, target_img, mask=mask)
                gray = cv2.cvtColor(target_img_and, cv2.COLOR_BGR2GRAY)
                res, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

                # cv2.imshow('binary', binary)
                # cv2.waitKey(1)

                square = float(float(np.sum(binary)) / float(np.pi * (r **2)) / 255.0)          # 计算该颜色部分的面积占比
                # print(color, np.sum(binary), img_height, img_width, square)

                # 如果该颜色部分大于阈值
                if (square > self.square_threshold):
                    # 从边缘中获取最小包围圆和其中点
                    pos_x = float(float(x) / float(img_width))
                    pos_y = float(float(y) / float(img_height))
                    pos = [pos_x, pos_y]
                    
                    # 检测该圆是否在目标范围内
                    if ((pos_x > self.pos_seg_x[0]) and (pos_x < self.pos_seg_x[1])) and ((pos_y > self.pos_seg_y[0]) and (pos_y < self.pos_seg_y[1])):
                        color_obj = color

                        return color_obj

            # 如果不是三个颜色
            return 'n'

        else:
            print("no circles")


    def get_target_circle(self, img, side=1):
        # 压缩图像大小
        img = cv2.resize(img, (180, 135))
        # cv2.imshow("img", img)

        # RGB图像去阴影
        dilated_img = cv2.dilate(img, np.ones((5,5), np.uint8))    # 膨胀
        blured_img = cv2.medianBlur(dilated_img, 9)                  # 中值滤波
        diff_img = 255 - cv2.absdiff(img, blured_img)
        norm_img = cv2.normalize(diff_img, None, 0, 255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8UC1)
        
        # RGB图像转灰度图
        gray = cv2.cvtColor(norm_img, cv2.COLOR_BGR2GRAY)
        # cv2.imshow("gray", gray)
    
        # 从二值化图中提取轮廓
        res, binary = cv2.threshold(gray, 100, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

        contours_circle, hierarchy = cv2.findContours(binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        # 找到面积最大的轮廓
        area = [cv2.contourArea(c) for c in contours_circle]
        index_max = np.argmax(area)
        contours_max = contours_circle[index_max]

        contoursImg = cv2.drawContours(img, contours_max, -1, (255,0,0), 1)  #绘制轮廓
        # cv2.imshow("contoursImg", contoursImg)

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
        # cv2.imshow("binary", binary)

        gaussianResult = cv2.GaussianBlur(binary,(3,3),2.5)
        # cv2.imshow("gaussianResult", gaussianResult)

        # cv2.imshow("gray", gray)
        # cv2.imshow("binary", binary)
        # cv2.imshow("img_contours", img_contours)
        # 以上部分预处理完成, 下面开始识别十字架

        # 检测圆形
        # 不同矫正区域检测参数不同, side=1, side=2为上方 / 左侧加工区, side=3为带物块时的左侧加工区(更宽松, 因为可能出现物块和圆环重叠)
        if side == 1 or side == 2:
            circles = cv2.HoughCircles(gaussianResult, cv2.HOUGH_GRADIENT, dp=1, minDist=180, param1=75, param2=75, minRadius=10, maxRadius=40)
        elif side == 3 or side == 4:
            circles = cv2.HoughCircles(gaussianResult, cv2.HOUGH_GRADIENT, dp=1, minDist=180, param1=45, param2=45, minRadius=10, maxRadius=40)

        # 输出检测到的圆形
        max_radius = 0
        max_circle = None
        img_height, img_width, img_channels = img.shape
        img_center_x = int(float(img_width) / 2.0)
        img_center_y = int(float(img_height) / 2.0)
        x_b = img_width
        y_b = img_height
        min_center_b = img_width + img_height

        if circles is not None:
            circles = np.round(circles[0, :]).astype("int")

            # 找到最靠近中心的圆环
            for (x, y, r) in circles:
                x_b = abs(x - img_center_x)
                y_b = abs(y - img_center_y)
                center_b = math.sqrt(x_b ** 2 + y_b ** 2)
                # if r > max_radius:
                #     max_radius = r
                #     max_circle = (x, y, r)
                if center_b < min_center_b:
                    min_center_b = center_b
                    max_circle = (x, y, r)

            # 绘制圆环和最大圆环
            if max_circle is not None:
                (x, y, r) = max_circle
                cv2.circle(img, (x, y), r, (0, 0, 255), 2)
                # print(r)
            # cv2.imshow("result", img)

            square = float(np.pi * (r ** 2)) / float(img_width * img_height)
            if square > self.thresh_square:
                return 1
            else:
                return 0

        else:
            print("no circles")
            return 0


if __name__ == '__main__':
    pass