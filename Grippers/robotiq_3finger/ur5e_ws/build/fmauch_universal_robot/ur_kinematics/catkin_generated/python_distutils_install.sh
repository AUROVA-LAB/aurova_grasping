#!/bin/sh

if [ -n "$DESTDIR" ] ; then
    case $DESTDIR in
        /*) # ok
            ;;
        *)
            /bin/echo "DESTDIR argument must be absolute... "
            /bin/echo "otherwise python's distutils will bork things."
            exit 1
    esac
fi

echo_and_run() { echo "+ $@" ; "$@" ; }

echo_and_run cd "/home/zalmanpc/ur5e_ws/src/fmauch_universal_robot/ur_kinematics"

# ensure that Python install destination exists
echo_and_run mkdir -p "$DESTDIR/home/zalmanpc/ur5e_ws/install/lib/python2.7/dist-packages"

# Note that PYTHONPATH is pulled from the environment to support installing
# into one location when some dependencies were installed in another
# location, #123.
echo_and_run /usr/bin/env \
    PYTHONPATH="/home/zalmanpc/ur5e_ws/install/lib/python2.7/dist-packages:/home/zalmanpc/ur5e_ws/build/lib/python2.7/dist-packages:$PYTHONPATH" \
    CATKIN_BINARY_DIR="/home/zalmanpc/ur5e_ws/build" \
    "/usr/bin/python2" \
    "/home/zalmanpc/ur5e_ws/src/fmauch_universal_robot/ur_kinematics/setup.py" \
     \
    build --build-base "/home/zalmanpc/ur5e_ws/build/fmauch_universal_robot/ur_kinematics" \
    install \
    --root="${DESTDIR-/}" \
    --install-layout=deb --prefix="/home/zalmanpc/ur5e_ws/install" --install-scripts="/home/zalmanpc/ur5e_ws/install/bin"
