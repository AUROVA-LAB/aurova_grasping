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

echo_and_run cd "/gripper/src/robotiq/robotiq_modbus_tcp"

# ensure that Python install destination exists
echo_and_run mkdir -p "$DESTDIR/gripper/install/lib/python2.7/dist-packages"

# Note that PYTHONPATH is pulled from the environment to support installing
# into one location when some dependencies were installed in another
# location, #123.
echo_and_run /usr/bin/env \
    PYTHONPATH="/gripper/install/lib/python2.7/dist-packages:/gripper/build/lib/python2.7/dist-packages:$PYTHONPATH" \
    CATKIN_BINARY_DIR="/gripper/build" \
    "/usr/bin/python2" \
    "/gripper/src/robotiq/robotiq_modbus_tcp/setup.py" \
     \
    build --build-base "/gripper/build/robotiq/robotiq_modbus_tcp" \
    install \
    --root="${DESTDIR-/}" \
    --install-layout=deb --prefix="/gripper/install" --install-scripts="/gripper/install/bin"
