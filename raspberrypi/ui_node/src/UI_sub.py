#! /usr/bin/python3

import rospy
from std_msgs.msg import Int32

'''
    rospy.init_node('ui_pub')
    pub = rospy.Publisher('listorder',Int32, queue_size=10)
    rate = rospy.Rate(2)
'''

rospy.init_node('ui_sub')

def callback(msg):
	print("list order : {}".format(msg.data))

sub = rospy.Subscriber('listorder',Int32,callback)
rate = rospy.Rate(2)

rospy.spin()
