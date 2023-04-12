# generated from genmsg/cmake/pkg-genmsg.cmake.em

message(STATUS "test_pkg: 2 messages, 0 services")

set(MSG_I_FLAGS "-Itest_pkg:/home/rq/lidar_test_ws/src/test_pkg/msg;-Istd_msgs:/opt/ros/melodic/share/std_msgs/cmake/../msg")

# Find all generators
find_package(gencpp REQUIRED)
find_package(geneus REQUIRED)
find_package(genlisp REQUIRED)
find_package(gennodejs REQUIRED)
find_package(genpy REQUIRED)

add_custom_target(test_pkg_generate_messages ALL)

# verify that message/service dependencies have not changed since configure



get_filename_component(_filename "/home/rq/lidar_test_ws/src/test_pkg/msg/LineSegment.msg" NAME_WE)
add_custom_target(_test_pkg_generate_messages_check_deps_${_filename}
  COMMAND ${CATKIN_ENV} ${PYTHON_EXECUTABLE} ${GENMSG_CHECK_DEPS_SCRIPT} "test_pkg" "/home/rq/lidar_test_ws/src/test_pkg/msg/LineSegment.msg" ""
)

get_filename_component(_filename "/home/rq/lidar_test_ws/src/test_pkg/msg/LineSegmentList.msg" NAME_WE)
add_custom_target(_test_pkg_generate_messages_check_deps_${_filename}
  COMMAND ${CATKIN_ENV} ${PYTHON_EXECUTABLE} ${GENMSG_CHECK_DEPS_SCRIPT} "test_pkg" "/home/rq/lidar_test_ws/src/test_pkg/msg/LineSegmentList.msg" "test_pkg/LineSegment:std_msgs/Header"
)

#
#  langs = gencpp;geneus;genlisp;gennodejs;genpy
#

### Section generating for lang: gencpp
### Generating Messages
_generate_msg_cpp(test_pkg
  "/home/rq/lidar_test_ws/src/test_pkg/msg/LineSegment.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/test_pkg
)
_generate_msg_cpp(test_pkg
  "/home/rq/lidar_test_ws/src/test_pkg/msg/LineSegmentList.msg"
  "${MSG_I_FLAGS}"
  "/home/rq/lidar_test_ws/src/test_pkg/msg/LineSegment.msg;/opt/ros/melodic/share/std_msgs/cmake/../msg/Header.msg"
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/test_pkg
)

### Generating Services

### Generating Module File
_generate_module_cpp(test_pkg
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/test_pkg
  "${ALL_GEN_OUTPUT_FILES_cpp}"
)

add_custom_target(test_pkg_generate_messages_cpp
  DEPENDS ${ALL_GEN_OUTPUT_FILES_cpp}
)
add_dependencies(test_pkg_generate_messages test_pkg_generate_messages_cpp)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/home/rq/lidar_test_ws/src/test_pkg/msg/LineSegment.msg" NAME_WE)
add_dependencies(test_pkg_generate_messages_cpp _test_pkg_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/rq/lidar_test_ws/src/test_pkg/msg/LineSegmentList.msg" NAME_WE)
add_dependencies(test_pkg_generate_messages_cpp _test_pkg_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(test_pkg_gencpp)
add_dependencies(test_pkg_gencpp test_pkg_generate_messages_cpp)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS test_pkg_generate_messages_cpp)

### Section generating for lang: geneus
### Generating Messages
_generate_msg_eus(test_pkg
  "/home/rq/lidar_test_ws/src/test_pkg/msg/LineSegment.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/test_pkg
)
_generate_msg_eus(test_pkg
  "/home/rq/lidar_test_ws/src/test_pkg/msg/LineSegmentList.msg"
  "${MSG_I_FLAGS}"
  "/home/rq/lidar_test_ws/src/test_pkg/msg/LineSegment.msg;/opt/ros/melodic/share/std_msgs/cmake/../msg/Header.msg"
  ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/test_pkg
)

### Generating Services

### Generating Module File
_generate_module_eus(test_pkg
  ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/test_pkg
  "${ALL_GEN_OUTPUT_FILES_eus}"
)

add_custom_target(test_pkg_generate_messages_eus
  DEPENDS ${ALL_GEN_OUTPUT_FILES_eus}
)
add_dependencies(test_pkg_generate_messages test_pkg_generate_messages_eus)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/home/rq/lidar_test_ws/src/test_pkg/msg/LineSegment.msg" NAME_WE)
add_dependencies(test_pkg_generate_messages_eus _test_pkg_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/rq/lidar_test_ws/src/test_pkg/msg/LineSegmentList.msg" NAME_WE)
add_dependencies(test_pkg_generate_messages_eus _test_pkg_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(test_pkg_geneus)
add_dependencies(test_pkg_geneus test_pkg_generate_messages_eus)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS test_pkg_generate_messages_eus)

### Section generating for lang: genlisp
### Generating Messages
_generate_msg_lisp(test_pkg
  "/home/rq/lidar_test_ws/src/test_pkg/msg/LineSegment.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/test_pkg
)
_generate_msg_lisp(test_pkg
  "/home/rq/lidar_test_ws/src/test_pkg/msg/LineSegmentList.msg"
  "${MSG_I_FLAGS}"
  "/home/rq/lidar_test_ws/src/test_pkg/msg/LineSegment.msg;/opt/ros/melodic/share/std_msgs/cmake/../msg/Header.msg"
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/test_pkg
)

### Generating Services

### Generating Module File
_generate_module_lisp(test_pkg
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/test_pkg
  "${ALL_GEN_OUTPUT_FILES_lisp}"
)

add_custom_target(test_pkg_generate_messages_lisp
  DEPENDS ${ALL_GEN_OUTPUT_FILES_lisp}
)
add_dependencies(test_pkg_generate_messages test_pkg_generate_messages_lisp)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/home/rq/lidar_test_ws/src/test_pkg/msg/LineSegment.msg" NAME_WE)
add_dependencies(test_pkg_generate_messages_lisp _test_pkg_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/rq/lidar_test_ws/src/test_pkg/msg/LineSegmentList.msg" NAME_WE)
add_dependencies(test_pkg_generate_messages_lisp _test_pkg_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(test_pkg_genlisp)
add_dependencies(test_pkg_genlisp test_pkg_generate_messages_lisp)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS test_pkg_generate_messages_lisp)

### Section generating for lang: gennodejs
### Generating Messages
_generate_msg_nodejs(test_pkg
  "/home/rq/lidar_test_ws/src/test_pkg/msg/LineSegment.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/test_pkg
)
_generate_msg_nodejs(test_pkg
  "/home/rq/lidar_test_ws/src/test_pkg/msg/LineSegmentList.msg"
  "${MSG_I_FLAGS}"
  "/home/rq/lidar_test_ws/src/test_pkg/msg/LineSegment.msg;/opt/ros/melodic/share/std_msgs/cmake/../msg/Header.msg"
  ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/test_pkg
)

### Generating Services

### Generating Module File
_generate_module_nodejs(test_pkg
  ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/test_pkg
  "${ALL_GEN_OUTPUT_FILES_nodejs}"
)

add_custom_target(test_pkg_generate_messages_nodejs
  DEPENDS ${ALL_GEN_OUTPUT_FILES_nodejs}
)
add_dependencies(test_pkg_generate_messages test_pkg_generate_messages_nodejs)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/home/rq/lidar_test_ws/src/test_pkg/msg/LineSegment.msg" NAME_WE)
add_dependencies(test_pkg_generate_messages_nodejs _test_pkg_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/rq/lidar_test_ws/src/test_pkg/msg/LineSegmentList.msg" NAME_WE)
add_dependencies(test_pkg_generate_messages_nodejs _test_pkg_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(test_pkg_gennodejs)
add_dependencies(test_pkg_gennodejs test_pkg_generate_messages_nodejs)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS test_pkg_generate_messages_nodejs)

### Section generating for lang: genpy
### Generating Messages
_generate_msg_py(test_pkg
  "/home/rq/lidar_test_ws/src/test_pkg/msg/LineSegment.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/test_pkg
)
_generate_msg_py(test_pkg
  "/home/rq/lidar_test_ws/src/test_pkg/msg/LineSegmentList.msg"
  "${MSG_I_FLAGS}"
  "/home/rq/lidar_test_ws/src/test_pkg/msg/LineSegment.msg;/opt/ros/melodic/share/std_msgs/cmake/../msg/Header.msg"
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/test_pkg
)

### Generating Services

### Generating Module File
_generate_module_py(test_pkg
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/test_pkg
  "${ALL_GEN_OUTPUT_FILES_py}"
)

add_custom_target(test_pkg_generate_messages_py
  DEPENDS ${ALL_GEN_OUTPUT_FILES_py}
)
add_dependencies(test_pkg_generate_messages test_pkg_generate_messages_py)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/home/rq/lidar_test_ws/src/test_pkg/msg/LineSegment.msg" NAME_WE)
add_dependencies(test_pkg_generate_messages_py _test_pkg_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/rq/lidar_test_ws/src/test_pkg/msg/LineSegmentList.msg" NAME_WE)
add_dependencies(test_pkg_generate_messages_py _test_pkg_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(test_pkg_genpy)
add_dependencies(test_pkg_genpy test_pkg_generate_messages_py)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS test_pkg_generate_messages_py)



if(gencpp_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/test_pkg)
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/test_pkg
    DESTINATION ${gencpp_INSTALL_DIR}
  )
endif()
if(TARGET std_msgs_generate_messages_cpp)
  add_dependencies(test_pkg_generate_messages_cpp std_msgs_generate_messages_cpp)
endif()

if(geneus_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/test_pkg)
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/test_pkg
    DESTINATION ${geneus_INSTALL_DIR}
  )
endif()
if(TARGET std_msgs_generate_messages_eus)
  add_dependencies(test_pkg_generate_messages_eus std_msgs_generate_messages_eus)
endif()

if(genlisp_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/test_pkg)
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/test_pkg
    DESTINATION ${genlisp_INSTALL_DIR}
  )
endif()
if(TARGET std_msgs_generate_messages_lisp)
  add_dependencies(test_pkg_generate_messages_lisp std_msgs_generate_messages_lisp)
endif()

if(gennodejs_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/test_pkg)
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/test_pkg
    DESTINATION ${gennodejs_INSTALL_DIR}
  )
endif()
if(TARGET std_msgs_generate_messages_nodejs)
  add_dependencies(test_pkg_generate_messages_nodejs std_msgs_generate_messages_nodejs)
endif()

if(genpy_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/test_pkg)
  install(CODE "execute_process(COMMAND \"/usr/bin/python2\" -m compileall \"${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/test_pkg\")")
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/test_pkg
    DESTINATION ${genpy_INSTALL_DIR}
  )
endif()
if(TARGET std_msgs_generate_messages_py)
  add_dependencies(test_pkg_generate_messages_py std_msgs_generate_messages_py)
endif()
