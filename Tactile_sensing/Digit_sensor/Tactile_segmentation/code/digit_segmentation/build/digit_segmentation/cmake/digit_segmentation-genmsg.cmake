# generated from genmsg/cmake/pkg-genmsg.cmake.em

message(STATUS "digit_segmentation: 1 messages, 0 services")

set(MSG_I_FLAGS "-Idigit_segmentation:/digit_segmentation/digit_segmentation/src/digit_segmentation/msg;-Istd_msgs:/opt/ros/melodic/share/std_msgs/cmake/../msg")

# Find all generators
find_package(gencpp REQUIRED)
find_package(geneus REQUIRED)
find_package(genlisp REQUIRED)
find_package(gennodejs REQUIRED)
find_package(genpy REQUIRED)

add_custom_target(digit_segmentation_generate_messages ALL)

# verify that message/service dependencies have not changed since configure



get_filename_component(_filename "/digit_segmentation/digit_segmentation/src/digit_segmentation/msg/floatArray.msg" NAME_WE)
add_custom_target(_digit_segmentation_generate_messages_check_deps_${_filename}
  COMMAND ${CATKIN_ENV} ${PYTHON_EXECUTABLE} ${GENMSG_CHECK_DEPS_SCRIPT} "digit_segmentation" "/digit_segmentation/digit_segmentation/src/digit_segmentation/msg/floatArray.msg" "std_msgs/Header"
)

#
#  langs = gencpp;geneus;genlisp;gennodejs;genpy
#

### Section generating for lang: gencpp
### Generating Messages
_generate_msg_cpp(digit_segmentation
  "/digit_segmentation/digit_segmentation/src/digit_segmentation/msg/floatArray.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/melodic/share/std_msgs/cmake/../msg/Header.msg"
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/digit_segmentation
)

### Generating Services

### Generating Module File
_generate_module_cpp(digit_segmentation
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/digit_segmentation
  "${ALL_GEN_OUTPUT_FILES_cpp}"
)

add_custom_target(digit_segmentation_generate_messages_cpp
  DEPENDS ${ALL_GEN_OUTPUT_FILES_cpp}
)
add_dependencies(digit_segmentation_generate_messages digit_segmentation_generate_messages_cpp)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/digit_segmentation/digit_segmentation/src/digit_segmentation/msg/floatArray.msg" NAME_WE)
add_dependencies(digit_segmentation_generate_messages_cpp _digit_segmentation_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(digit_segmentation_gencpp)
add_dependencies(digit_segmentation_gencpp digit_segmentation_generate_messages_cpp)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS digit_segmentation_generate_messages_cpp)

### Section generating for lang: geneus
### Generating Messages
_generate_msg_eus(digit_segmentation
  "/digit_segmentation/digit_segmentation/src/digit_segmentation/msg/floatArray.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/melodic/share/std_msgs/cmake/../msg/Header.msg"
  ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/digit_segmentation
)

### Generating Services

### Generating Module File
_generate_module_eus(digit_segmentation
  ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/digit_segmentation
  "${ALL_GEN_OUTPUT_FILES_eus}"
)

add_custom_target(digit_segmentation_generate_messages_eus
  DEPENDS ${ALL_GEN_OUTPUT_FILES_eus}
)
add_dependencies(digit_segmentation_generate_messages digit_segmentation_generate_messages_eus)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/digit_segmentation/digit_segmentation/src/digit_segmentation/msg/floatArray.msg" NAME_WE)
add_dependencies(digit_segmentation_generate_messages_eus _digit_segmentation_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(digit_segmentation_geneus)
add_dependencies(digit_segmentation_geneus digit_segmentation_generate_messages_eus)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS digit_segmentation_generate_messages_eus)

### Section generating for lang: genlisp
### Generating Messages
_generate_msg_lisp(digit_segmentation
  "/digit_segmentation/digit_segmentation/src/digit_segmentation/msg/floatArray.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/melodic/share/std_msgs/cmake/../msg/Header.msg"
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/digit_segmentation
)

### Generating Services

### Generating Module File
_generate_module_lisp(digit_segmentation
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/digit_segmentation
  "${ALL_GEN_OUTPUT_FILES_lisp}"
)

add_custom_target(digit_segmentation_generate_messages_lisp
  DEPENDS ${ALL_GEN_OUTPUT_FILES_lisp}
)
add_dependencies(digit_segmentation_generate_messages digit_segmentation_generate_messages_lisp)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/digit_segmentation/digit_segmentation/src/digit_segmentation/msg/floatArray.msg" NAME_WE)
add_dependencies(digit_segmentation_generate_messages_lisp _digit_segmentation_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(digit_segmentation_genlisp)
add_dependencies(digit_segmentation_genlisp digit_segmentation_generate_messages_lisp)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS digit_segmentation_generate_messages_lisp)

### Section generating for lang: gennodejs
### Generating Messages
_generate_msg_nodejs(digit_segmentation
  "/digit_segmentation/digit_segmentation/src/digit_segmentation/msg/floatArray.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/melodic/share/std_msgs/cmake/../msg/Header.msg"
  ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/digit_segmentation
)

### Generating Services

### Generating Module File
_generate_module_nodejs(digit_segmentation
  ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/digit_segmentation
  "${ALL_GEN_OUTPUT_FILES_nodejs}"
)

add_custom_target(digit_segmentation_generate_messages_nodejs
  DEPENDS ${ALL_GEN_OUTPUT_FILES_nodejs}
)
add_dependencies(digit_segmentation_generate_messages digit_segmentation_generate_messages_nodejs)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/digit_segmentation/digit_segmentation/src/digit_segmentation/msg/floatArray.msg" NAME_WE)
add_dependencies(digit_segmentation_generate_messages_nodejs _digit_segmentation_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(digit_segmentation_gennodejs)
add_dependencies(digit_segmentation_gennodejs digit_segmentation_generate_messages_nodejs)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS digit_segmentation_generate_messages_nodejs)

### Section generating for lang: genpy
### Generating Messages
_generate_msg_py(digit_segmentation
  "/digit_segmentation/digit_segmentation/src/digit_segmentation/msg/floatArray.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/melodic/share/std_msgs/cmake/../msg/Header.msg"
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/digit_segmentation
)

### Generating Services

### Generating Module File
_generate_module_py(digit_segmentation
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/digit_segmentation
  "${ALL_GEN_OUTPUT_FILES_py}"
)

add_custom_target(digit_segmentation_generate_messages_py
  DEPENDS ${ALL_GEN_OUTPUT_FILES_py}
)
add_dependencies(digit_segmentation_generate_messages digit_segmentation_generate_messages_py)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/digit_segmentation/digit_segmentation/src/digit_segmentation/msg/floatArray.msg" NAME_WE)
add_dependencies(digit_segmentation_generate_messages_py _digit_segmentation_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(digit_segmentation_genpy)
add_dependencies(digit_segmentation_genpy digit_segmentation_generate_messages_py)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS digit_segmentation_generate_messages_py)



if(gencpp_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/digit_segmentation)
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/digit_segmentation
    DESTINATION ${gencpp_INSTALL_DIR}
  )
endif()
if(TARGET std_msgs_generate_messages_cpp)
  add_dependencies(digit_segmentation_generate_messages_cpp std_msgs_generate_messages_cpp)
endif()

if(geneus_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/digit_segmentation)
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/digit_segmentation
    DESTINATION ${geneus_INSTALL_DIR}
  )
endif()
if(TARGET std_msgs_generate_messages_eus)
  add_dependencies(digit_segmentation_generate_messages_eus std_msgs_generate_messages_eus)
endif()

if(genlisp_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/digit_segmentation)
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/digit_segmentation
    DESTINATION ${genlisp_INSTALL_DIR}
  )
endif()
if(TARGET std_msgs_generate_messages_lisp)
  add_dependencies(digit_segmentation_generate_messages_lisp std_msgs_generate_messages_lisp)
endif()

if(gennodejs_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/digit_segmentation)
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/digit_segmentation
    DESTINATION ${gennodejs_INSTALL_DIR}
  )
endif()
if(TARGET std_msgs_generate_messages_nodejs)
  add_dependencies(digit_segmentation_generate_messages_nodejs std_msgs_generate_messages_nodejs)
endif()

if(genpy_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/digit_segmentation)
  install(CODE "execute_process(COMMAND \"/usr/bin/python2\" -m compileall \"${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/digit_segmentation\")")
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/digit_segmentation
    DESTINATION ${genpy_INSTALL_DIR}
  )
endif()
if(TARGET std_msgs_generate_messages_py)
  add_dependencies(digit_segmentation_generate_messages_py std_msgs_generate_messages_py)
endif()
