#!/usr/bin/env python
# coding=utf-8

import rospy
from sensor_msgs.msg import LaserScan
from test_pkg.msg import LineSegmentList
import matplotlib.pyplot as plt
import numpy as np

angle_dev = 5

def process_line(line):
    x_dist = 0
    y_dist = 0
    x_dist_sum = 0
    y_dist_sum = 0
    x_dist_n = 0
    y_dist_n = 0
    line_num = len(line)

    for i in range(line_num):
        angle = line[i]["angle"]
        if abs(abs(angle) - 90) < angle_dev:        # 如果是垂直的
            x_dist_sum += line[i]["dist"]
            x_dist_n += 1
        elif abs(abs(angle) - 0) < angle_dev:        # 如果是水平的
            y_dist_sum += line[i]["dist"]
            y_dist_n += 1

    x_dist = x_dist_sum / x_dist_n
    y_dist = y_dist_sum / y_dist_n

    return x_dist, y_dist


def  callback(scan):
    line_num = len(scan.line_segments)
    line = []
    line_i = {}

    for i in range(line_num):
        start_x = scan.line_segments[i].start[0]
        start_y = scan.line_segments[i].start[1]
        end_x = scan.line_segments[i].end[0]
        end_y = scan.line_segments[i].end[1]

        # 计算线段长度和倾角
        length = (abs(start_x - end_x)**2 + abs(start_y - end_y)**2)**0.5
        slope = (end_y - start_y) / (end_x - start_x)
        angle = np.arctan(slope) / np.pi * 180

        # 计算线段到原点距离
        vec1 = [start_x, start_y]
        vec2 = [end_x, end_y]
        dist = abs(np.cross(vec1, vec2)) / np.linalg.norm(np.array(vec1) - np.array(vec2))

        line_i["start_x"] = start_x
        line_i["start_y"] = start_y
        line_i["end_x"] = end_x
        line_i["end_y"] = end_y
        line_i["length"] = length
        line_i["angle"] = angle
        line_i["dist"] = dist

        line.insert(i, line_i)
        line_i = {}

        # print(scan.line_segments[i].start)
        # print(scan.line_segments[i].end)
        # print("---------------------")

    # print(line)

    x_dist, y_dist = process_line(line)
    print(x_dist, y_dist)

    line = []
    print("@@@@@@@@@")


def  listener():
    rospy.init_node('line_listener', anonymous=False)
    rospy.Subscriber('line_segments',  LineSegmentList, callback)
    rospy.spin()


if __name__ == '__main__':
    listener()

    # plt.xlim(-2,2)
    # plt.ylim(-2,2)

    # plt.plot([-0.851, -0.804], [0, -1.112])
    # plt.plot([0.597, -0.568], [0.802, 0.781])
    # plt.plot([-0.855, -0.848], [0.747, 0.063])
    # plt.show()

