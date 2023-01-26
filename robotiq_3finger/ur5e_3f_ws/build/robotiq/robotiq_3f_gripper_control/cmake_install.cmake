# Install script for directory: /home/julio/Escritorio/julio/doctorado/primer_anyo/florian/ur5e_/ur5e_3f_ws/src/robotiq/robotiq_3f_gripper_control

# Set the install prefix
if(NOT DEFINED CMAKE_INSTALL_PREFIX)
  set(CMAKE_INSTALL_PREFIX "/home/julio/Escritorio/julio/doctorado/primer_anyo/florian/ur5e_/ur5e_3f_ws/install")
endif()
string(REGEX REPLACE "/$" "" CMAKE_INSTALL_PREFIX "${CMAKE_INSTALL_PREFIX}")

# Set the install configuration name.
if(NOT DEFINED CMAKE_INSTALL_CONFIG_NAME)
  if(BUILD_TYPE)
    string(REGEX REPLACE "^[^A-Za-z0-9_]+" ""
           CMAKE_INSTALL_CONFIG_NAME "${BUILD_TYPE}")
  else()
    set(CMAKE_INSTALL_CONFIG_NAME "")
  endif()
  message(STATUS "Install configuration: \"${CMAKE_INSTALL_CONFIG_NAME}\"")
endif()

# Set the component getting installed.
if(NOT CMAKE_INSTALL_COMPONENT)
  if(COMPONENT)
    message(STATUS "Install component: \"${COMPONENT}\"")
    set(CMAKE_INSTALL_COMPONENT "${COMPONENT}")
  else()
    set(CMAKE_INSTALL_COMPONENT)
  endif()
endif()

# Install shared libraries without execute permission?
if(NOT DEFINED CMAKE_INSTALL_SO_NO_EXE)
  set(CMAKE_INSTALL_SO_NO_EXE "1")
endif()

# Is this installation the result of a crosscompile?
if(NOT DEFINED CMAKE_CROSSCOMPILING)
  set(CMAKE_CROSSCOMPILING "FALSE")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  include("/home/julio/Escritorio/julio/doctorado/primer_anyo/florian/ur5e_/ur5e_3f_ws/build/robotiq/robotiq_3f_gripper_control/catkin_generated/safe_execute_install.cmake")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include/robotiq_3f_gripper_control" TYPE FILE FILES "/home/julio/Escritorio/julio/doctorado/primer_anyo/florian/ur5e_/ur5e_3f_ws/devel/include/robotiq_3f_gripper_control/Robotiq3FGripperConfig.h")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  execute_process(COMMAND "/home/julio/Escritorio/julio/doctorado/primer_anyo/digit/ros/python3_ws/py3env/bin/python" -m compileall "/home/julio/Escritorio/julio/doctorado/primer_anyo/florian/ur5e_/ur5e_3f_ws/devel/lib/python3/dist-packages/robotiq_3f_gripper_control/cfg")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/python3/dist-packages/robotiq_3f_gripper_control" TYPE DIRECTORY FILES "/home/julio/Escritorio/julio/doctorado/primer_anyo/florian/ur5e_/ur5e_3f_ws/devel/lib/python3/dist-packages/robotiq_3f_gripper_control/cfg")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/pkgconfig" TYPE FILE FILES "/home/julio/Escritorio/julio/doctorado/primer_anyo/florian/ur5e_/ur5e_3f_ws/build/robotiq/robotiq_3f_gripper_control/catkin_generated/installspace/robotiq_3f_gripper_control.pc")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/robotiq_3f_gripper_control/cmake" TYPE FILE FILES
    "/home/julio/Escritorio/julio/doctorado/primer_anyo/florian/ur5e_/ur5e_3f_ws/build/robotiq/robotiq_3f_gripper_control/catkin_generated/installspace/robotiq_3f_gripper_controlConfig.cmake"
    "/home/julio/Escritorio/julio/doctorado/primer_anyo/florian/ur5e_/ur5e_3f_ws/build/robotiq/robotiq_3f_gripper_control/catkin_generated/installspace/robotiq_3f_gripper_controlConfig-version.cmake"
    )
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/robotiq_3f_gripper_control" TYPE FILE FILES "/home/julio/Escritorio/julio/doctorado/primer_anyo/florian/ur5e_/ur5e_3f_ws/src/robotiq/robotiq_3f_gripper_control/package.xml")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/robotiq_3f_gripper_control" TYPE PROGRAM FILES
    "/home/julio/Escritorio/julio/doctorado/primer_anyo/florian/ur5e_/ur5e_3f_ws/src/robotiq/robotiq_3f_gripper_control/nodes/Robotiq3FGripperController.py"
    "/home/julio/Escritorio/julio/doctorado/primer_anyo/florian/ur5e_/ur5e_3f_ws/src/robotiq/robotiq_3f_gripper_control/nodes/Robotiq3FGripperMainProgram.py"
    "/home/julio/Escritorio/julio/doctorado/primer_anyo/florian/ur5e_/ur5e_3f_ws/src/robotiq/robotiq_3f_gripper_control/nodes/Robotiq3FGripperSimpleController.py"
    "/home/julio/Escritorio/julio/doctorado/primer_anyo/florian/ur5e_/ur5e_3f_ws/src/robotiq/robotiq_3f_gripper_control/nodes/Robotiq3FGripperStatusListener.py"
    "/home/julio/Escritorio/julio/doctorado/primer_anyo/florian/ur5e_/ur5e_3f_ws/src/robotiq/robotiq_3f_gripper_control/nodes/Robotiq3FGripperTcpNode.py"
    )
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  if(EXISTS "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/librobotiq_3f_gripper_control.so" AND
     NOT IS_SYMLINK "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/librobotiq_3f_gripper_control.so")
    file(RPATH_CHECK
         FILE "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/librobotiq_3f_gripper_control.so"
         RPATH "")
  endif()
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib" TYPE SHARED_LIBRARY FILES "/home/julio/Escritorio/julio/doctorado/primer_anyo/florian/ur5e_/ur5e_3f_ws/devel/lib/librobotiq_3f_gripper_control.so")
  if(EXISTS "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/librobotiq_3f_gripper_control.so" AND
     NOT IS_SYMLINK "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/librobotiq_3f_gripper_control.so")
    file(RPATH_CHANGE
         FILE "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/librobotiq_3f_gripper_control.so"
         OLD_RPATH "/opt/ros/noetic/lib:/home/julio/Escritorio/julio/doctorado/primer_anyo/florian/ur5e_/ur5e_3f_ws/devel/lib:"
         NEW_RPATH "")
    if(CMAKE_INSTALL_DO_STRIP)
      execute_process(COMMAND "/usr/bin/strip" "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/librobotiq_3f_gripper_control.so")
    endif()
  endif()
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  if(EXISTS "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/robotiq_3f_gripper_control/robotiq_3f_gripper_can_node" AND
     NOT IS_SYMLINK "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/robotiq_3f_gripper_control/robotiq_3f_gripper_can_node")
    file(RPATH_CHECK
         FILE "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/robotiq_3f_gripper_control/robotiq_3f_gripper_can_node"
         RPATH "")
  endif()
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/robotiq_3f_gripper_control" TYPE EXECUTABLE FILES "/home/julio/Escritorio/julio/doctorado/primer_anyo/florian/ur5e_/ur5e_3f_ws/devel/lib/robotiq_3f_gripper_control/robotiq_3f_gripper_can_node")
  if(EXISTS "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/robotiq_3f_gripper_control/robotiq_3f_gripper_can_node" AND
     NOT IS_SYMLINK "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/robotiq_3f_gripper_control/robotiq_3f_gripper_can_node")
    file(RPATH_CHANGE
         FILE "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/robotiq_3f_gripper_control/robotiq_3f_gripper_can_node"
         OLD_RPATH "/home/julio/Escritorio/julio/doctorado/primer_anyo/florian/ur5e_/ur5e_3f_ws/devel/lib:/opt/ros/noetic/lib:"
         NEW_RPATH "")
    if(CMAKE_INSTALL_DO_STRIP)
      execute_process(COMMAND "/usr/bin/strip" "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/robotiq_3f_gripper_control/robotiq_3f_gripper_can_node")
    endif()
  endif()
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  if(EXISTS "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/robotiq_3f_gripper_control/robotiq_3f_gripper_ethercat_node" AND
     NOT IS_SYMLINK "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/robotiq_3f_gripper_control/robotiq_3f_gripper_ethercat_node")
    file(RPATH_CHECK
         FILE "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/robotiq_3f_gripper_control/robotiq_3f_gripper_ethercat_node"
         RPATH "")
  endif()
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/robotiq_3f_gripper_control" TYPE EXECUTABLE FILES "/home/julio/Escritorio/julio/doctorado/primer_anyo/florian/ur5e_/ur5e_3f_ws/devel/lib/robotiq_3f_gripper_control/robotiq_3f_gripper_ethercat_node")
  if(EXISTS "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/robotiq_3f_gripper_control/robotiq_3f_gripper_ethercat_node" AND
     NOT IS_SYMLINK "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/robotiq_3f_gripper_control/robotiq_3f_gripper_ethercat_node")
    file(RPATH_CHANGE
         FILE "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/robotiq_3f_gripper_control/robotiq_3f_gripper_ethercat_node"
         OLD_RPATH "/home/julio/Escritorio/julio/doctorado/primer_anyo/florian/ur5e_/ur5e_3f_ws/devel/lib:/opt/ros/noetic/lib:"
         NEW_RPATH "")
    if(CMAKE_INSTALL_DO_STRIP)
      execute_process(COMMAND "/usr/bin/strip" "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/robotiq_3f_gripper_control/robotiq_3f_gripper_ethercat_node")
    endif()
  endif()
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include/robotiq_3f_gripper_control" TYPE DIRECTORY FILES "/home/julio/Escritorio/julio/doctorado/primer_anyo/florian/ur5e_/ur5e_3f_ws/src/robotiq/robotiq_3f_gripper_control/include/robotiq_3f_gripper_control/" FILES_MATCHING REGEX "/[^/]*\\.h$" REGEX "/\\.svn$" EXCLUDE)
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/robotiq_3f_gripper_control" TYPE DIRECTORY FILES "/home/julio/Escritorio/julio/doctorado/primer_anyo/florian/ur5e_/ur5e_3f_ws/src/robotiq/robotiq_3f_gripper_control/launch")
endif()

