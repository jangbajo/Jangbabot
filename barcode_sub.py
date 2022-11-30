#!/usr/bin/env python

import rospy
from std_msgs.msg import Int32

rospy.init_node('detection_sub')



def callback(msg):
	print("detection clear : {}".format(msg.data))

sub = rospy.Subscriber("detection",Int32,callback)

rospy.spin()
