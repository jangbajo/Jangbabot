#!/usr/bin/env python3
import rospy
import cv2
import pyzbar.pyzbar as pyzbar
from std_msgs.msg import Int32MultiArray,Int32

rospy.init_node('detection_pub')
#섭이랑은 항상 스핀 원스가 있어야한다

pub = rospy.Publisher('detection_success',Int32,queue_size=10)
ok = Int32()
ok = 1;
num=[0,0,0,0]



def callback(msg):
    print('msg.data는 {}입니다'.format(msg.data))
    cap = cv2.VideoCapture(0)
    while True:
        success, frame = cap.read()
        if success:
            for code in pyzbar.decode(frame):
                my_code = Int32()
                my_code = int(code.data.decode('utf-8'))
                print('{}을 인식했습니다'.format(my_code))
                for i in range(4):
                    if msg.data == my_code and num[i]==0 :
                        print('인식 성공 : ',my_code)
                        pub.publish(ok)
                        num[i]=1

    cap.release()
    cv2.destroyALLWindows()


sub = rospy.Subscriber("detection_start",Int32,callback)

rospy.spin()

