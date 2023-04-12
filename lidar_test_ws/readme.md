## 用法

1. 查看雷达是否接入

   `ls /dev/ttyUSB*`

2. 打开激光雷达驱动

   `roslaunch lslidar_x10_driver lslidar_x10_serial.launch`    N10雷达

   `roslaunch ldlidar_stl_ros ld19.launch`    LD19雷达

3. 开启Rviz

   `roslaunch ldlidar_stl_ros viewer_ld19_noetic.launch`    LD19雷达

4. 开启直线拟合程序

   `roslaunch laser_line_extraction test_example.launch`

5. 打开客户端代码

   `cd /lidar_test_ws/src/test_pkg/src`

   `python test_line.py`



**SCP：fillzilla**



## 通信结构

![rosgraph](/home/rq/lidar_test_ws/image/rosgraph.png)