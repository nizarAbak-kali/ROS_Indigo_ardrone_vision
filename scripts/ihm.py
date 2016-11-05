#!/usr/bin/env python
# coding=utf-8
import os
import sys
from cv_bridge import CvBridge

import cv2
import rospy
from rospy import Rate
from std_msgs.msg import String

Nshot = 3
image_path = "/home/nizar/Images/tpROS/"


def init():
    if not os.path.isdir(image_path):
        raise Exception("pas de dossier")


class Ihm:
    def __init__(self):
        self.last = ""
        self.bridge = CvBridge()
        self.image_sub = rospy.Subscriber("position", String, self.callback)

    def draw(self, filename):
        img_tmp = image_path + filename
        print img_tmp
        image_tmp = cv2.imread(img_tmp)
        cv2.imshow(filename, image_tmp)
        return

    def callback(self, data):
        if self.last is not data.data and data.data != "False":
            self.last = data.data
            self.draw(self.last)

        cv2.waitKey(0)
        cv2.destroyAllWindows()


def main(args):
    init()
    ihm = Ihm()
    rospy.init_node('ihm', anonymous=True)
    try:
        rate = Rate(1)
        rate.sleep()
        rospy.spin()

    except KeyboardInterrupt:
        print("Shutting down")
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main(sys.argv)
