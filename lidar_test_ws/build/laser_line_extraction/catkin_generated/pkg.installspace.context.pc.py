# generated from catkin/cmake/template/pkg.context.pc.in
CATKIN_PACKAGE_PREFIX = ""
PROJECT_PKG_CONFIG_INCLUDE_DIRS = "${prefix}/include".split(';') if "${prefix}/include" != "" else []
PROJECT_CATKIN_DEPENDS = "geometry_msgs;message_runtime;roscpp;sensor_msgs;visualization_msgs".replace(';', ' ')
PKG_CONFIG_LIBRARIES_WITH_PREFIX = "-lline;-lline_extraction;-lline_extraction_ros".split(';') if "-lline;-lline_extraction;-lline_extraction_ros" != "" else []
PROJECT_NAME = "laser_line_extraction"
PROJECT_SPACE_DIR = "/home/rq/lidar_test_ws/install"
PROJECT_VERSION = "0.1.0"
