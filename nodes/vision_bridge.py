#!/usr/bin/env python
""" A python node to read images from a web camera and process with opencv 
    Subscribes: usb_cam/image_raw (sensor_msgs/Image) - The input raw image
    Publishes: image_processed (sensor_msgs/Image) - The processed image
"""

import rospy
from cv_bridge import CvBridge
from sensor_msgs.msg import Image
import cv2
import vision.vision1 as v1


class Bridge:

    def __init__(self):
        self.take_image = rospy.Service('ImageCapture', ImageCapture, self.capture_callback)
        
        self.bridge = CvBridge()
        self._pub = rospy.Publisher("image_processed", Image, queue_size = 10)
        self.rospy.init_node("vision_bridge")

    def callback(self,data):

        # Output debugging information to the terminal
        rospy.loginfo("receiving video frame")
        
        # Convert ROS Image message to OpenCV image
        current_frame = self.bridge.imgmsg_to_cv2(data)
        
        # Display image
        cv2.imshow("camera", current_frame)
        
        cv2.waitKey(1)


        # manipulate with open cv
        # low_res = cv2.blur(cv_image, (50, 50))
        image_contour,grid = v1.detect_contour(current_frame, grid_size = (1,3), pixel_size = [475,125], starting_pixel = [125,200])


        # convert to ROS
        msg = self._bridge.cv2_to_imgmsg(image_contour, "bgr8")

        self._pub.publish(msg)

    def capture_callback(self, req):
        image_subscriber = rospy.Subscriber("/camera/color/image_raw", Image, self.callback)


        
if __name__ == "__main__":
    b = Bridge()
    rospy.spin()


