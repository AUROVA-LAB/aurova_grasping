#!/usr/bin/env python  
import roslib

import rospy
import tf

if __name__ == '__main__':
    rospy.init_node('fixed_tf_broadcaster')
    br = tf.TransformBroadcaster()
    rate = rospy.Rate(10.0)
    while not rospy.is_shutdown():
        br.sendTransform((0.0, -0.065, -0.037),
                         #(0.0, 0.0, 0.0, 1.0),
                         #(0.7068252,0.0, 0.0,  0.7073883),
                         #(0.9659253, 0.0, 0.0, 0.2588209),
                         (0.6517669, 0.2747322, 0.6512481, -0.274951),
                         rospy.Time.now(),
                         "camera_link",
                         "wrist_3_link")
        rate.sleep()