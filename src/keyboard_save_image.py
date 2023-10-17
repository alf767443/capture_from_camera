#!/usr/bin/env python3

import rospy
import cv2
import os

from sensor_msgs.msg import Image
from cv_bridge import CvBridge
from std_msgs.msg import Empty
from datetime import datetime

class KeyPressCapture():
    def __init__(self):
        rospy.init_node('keyboard_capture_image')

        self.bridge = CvBridge()

        self.save_directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/captures/' 

        rospy.Subscriber("/camera/image_raw", Image, self.show_image_and_capture)    
        
        self.image_count = 0

        # Inicialize a janela OpenCV
        cv2.namedWindow("Press Space to Capture", cv2.WINDOW_NORMAL)

    
        # Loop principal
        self.run()

    def show_image_and_capture(self, msg):
        cv_image = self.bridge.imgmsg_to_cv2(msg, "bgr8")
        cv2.imshow("Press Space to Capture", cv_image)


    def capture_image_and_save(self):
        msg = rospy.wait_for_message("/camera/image_raw", Image, timeout=5)
        now_str = datetime.now().strftime("%Y_%m_%d-%H_%M_%S")
        
        cv_image = self.bridge.imgmsg_to_cv2(msg, "bgr8")
        image_filename = self.save_directory + f'{now_str}.jpeg'
        cv2.imwrite(image_filename, cv_image)
        self.image_count += 1
        rospy.loginfo('Imagem salva como %s', image_filename)

    def run(self):
        while not rospy.is_shutdown():
            key = cv2.waitKey(10)
            if key == ord(' '):
                self.capture_image_and_save()
            if key == ord('q'):
                break

if __name__ == '__main__':
    try:
        KeyPressCapture()
    except rospy.ROSInterruptException:
        pass
