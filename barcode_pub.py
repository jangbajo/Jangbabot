#!/usr/bin/env python3
import rospy
import cv2
import pyzbar.pyzbar as pyzbar
from std_msgs.msg import Int32MultiArray,Int32

rospy.init_node('detection_pub')
pub = rospy.Publisher('HIGHWAY',Int32,queue_size=10)

barcode_number = [1,2,3,4]
num=[0,0,0,0]

cap = cv2.VideoCapture(0)
while True:
	success, frame = cap.read()
	if success:
		for code in pyzbar.decode(frame):
			my_code = Int32()
			my_code = int(code.data.decode('utf-8'))
			for i in range(4):
				if my_code == barcode_number[i] and num[i]==0 :
					print("인식 성공 : ",my_code)
					pub.publish(my_code)
					num[i]=1
#		cv2.imshow("cam",frame)
        
		key = cv2.waitKey(1)
		if key ==27:
			break
                
cap.release()
cv2.destroyALLWindows()
