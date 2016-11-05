#!/usr/bin/env python
# coding=utf-8
import numpy as np
import os
import shutil
import sys
from cv_bridge import CvBridge, CvBridgeError

import cv2
import rospy
from sensor_msgs.msg import Image
from std_msgs.msg import String

Nshot = 50
image_path = "/home/nizar/Images/tpROS/"


def mse(imageA, imageB):
    # the 'Mean Squared Error' between the two images is the
    # sum of the squared difference between the two images;
    # NOTE: the two images must have the same dimension
    err = np.sum((imageA.astype("float") - imageB.astype("float")) ** 2)
    err /= float(imageA.shape[0] * imageA.shape[1])

    # return the MSE, the lower the error, the more "similar"
    # the two images are
    return err


def init():
    if not os.path.isdir(image_path):
        os.mkdir(image_path, 777)
    else:
        shutil.rmtree(image_path)
        os.mkdir(image_path)
    l = []
    for i in range(Nshot):
        c = []
        l.append(c)
        for j in range(Nshot):
            l[i].append(0)


def compare_images(imageA, imageB, title):
    # compute the mean squared error and structural similarity
    # index for the images
    m = mse(imageA, imageB)
    # print "MSE : "+ str(m)
    return m


class image_converter:
    def __init__(self):
        self.i = 0
        self.x = int(Nshot / 2)
        self.y = int(Nshot / 2)
        self.bridge = CvBridge()
        # self.image_sub = rospy.Subscriber("ardrone/front/image_raw",Image,self.callback)
        self.image_sub = rospy.Subscriber("/usb_cam/image_raw", Image, self.callback)
        self.pub_pos = rospy.Publisher("position", String, queue_size=10)

    def whereiam(self, current_image):
        score = {}
        for (dirpath, dirnames, filenames) in os.walk(image_path):
            for file in filenames:
                img_tmp = os.path.join(dirpath, file)
                image_tmp = cv2.imread(img_tmp)
                score[file] = compare_images(current_image, image_tmp, "compares les")

        res = min(score.values())
        if res > 12000:
            return False
        else:
            coord = score.get
            for name, pourcentage in score.iteritems():
                if pourcentage == res:
                    return name

    def callback(self, data):
        try:
            cv_image = self.bridge.imgmsg_to_cv2(data, "bgr8")

        except CvBridgeError as e:
            print(e)
        cv2.imshow("cam de merde", cv_image)

        if self.i == 0:
            cv2.imwrite(image_path + str(self.x) + "_" + str(self.y) + ".jpg", cv_image)
            self.i += 1

        # RETOURNE L'IMAGE À LAQUELLE ON RESSEMBLE LE PLUS OU FALSE
        res = self.whereiam(cv_image)

        # cas d'une image inconnue
        if not res and self.i < Nshot:
            self.i += 1
            # ajouter les bonnes coordonné avec l'imu
            res = "/new_image" + str(self.i) + ".jpg"
            print "inconnue " + str(res)
            cv2.imwrite(image_path + res, cv_image)

        # publication du nom de l'image dans laquelle on est ....
        self.pub_pos.publish(str(res))
        #
        print res

        k = cv2.waitKey(20)


def main(args):
    init()
    ic = image_converter()
    rospy.init_node('image_converter', anonymous=True)
    try:
        rospy.spin()
    except KeyboardInterrupt:
        print("Shutting down")
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main(sys.argv)
