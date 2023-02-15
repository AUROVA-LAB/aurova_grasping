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

echo_and_run cd "/home/julio/Escritorio/julio/doctorado/primer_anyo/florian/ur5e_/ur5e_3f_ws/src/robotiq/robotiq_3f_gripper_control"

# ensure that Python install destination exists
echo_and_run mkdir -p "$DESTDIR/home/julio/Escritorio/julio/doctorado/primer_anyo/florian/ur5e_/ur5e_3f_ws/install/lib/python3/dist-packages"

# Note that PYTHONPATH is pulled from the environment to support installing
# into one location when some dependencies were installed in another
# location, #123.
echo_and_run /usr/bin/env \
    PYTHONPATH="/home/julio/Escritorio/julio/doctorado/primer_anyo/florian/ur5e_/ur5e_3f_ws/install/lib/python3/dist-packages:/home/julio/Escritorio/julio/doctorado/primer_anyo/florian/ur5e_/ur5e_3f_ws/build/lib/python3/dist-packages:$PYTHONPATH" \
    CATKIN_BINARY_DIR="/home/julio/Escritorio/julio/doctorado/primer_anyo/florian/ur5e_/ur5e_3f_ws/build" \
    "/home/julio/Escritorio/julio/doctorado/primer_anyo/digit/ros/python3_ws/py3env/bin/python" \
    "/home/julio/Escritorio/julio/doctorado/primer_anyo/florian/ur5e_/ur5e_3f_ws/src/robotiq/robotiq_3f_gripper_control/setup.py" \
     \
    build --build-base "/home/julio/Escritorio/julio/doctorado/primer_anyo/florian/ur5e_/ur5e_3f_ws/build/robotiq/robotiq_3f_gripper_control" \
    install \
    --root="${DESTDIR-/}" \
    --install-layout=deb --prefix="/home/julio/Escritorio/julio/doctorado/primer_anyo/florian/ur5e_/ur5e_3f_ws/install" --install-scripts="/home/julio/Escritorio/julio/doctorado/primer_anyo/florian/ur5e_/ur5e_3f_ws/install/bin"
