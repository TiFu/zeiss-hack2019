
import cv2
import numpy as np

class OverlayProcessor:

    def __init__(self):
        pass

    def overlay(self, img1, img2, leftMostPoint1, leftMostPoint2, alpha = 0.5):
        biggest_shape1 = self._findBiggestShape(img1)
        biggest_shape2 = self._findBiggestShape(img2)


        translationVector = leftMostPoint2 - leftMostPoint1

        biggest_shape2_aligned = self._alignContour(biggest_shape2, translationVector)

        stencil1 = np.zeros((img1.shape[0], img1.shape[1], 3)).astype(img1.dtype)
        cv2.fillPoly(stencil1, [biggest_shape1], (0, 0, 255))

        stencil2 = np.zeros((img1.shape[0], img1.shape[1], 3)).astype(img1.dtype)
        cv2.fillPoly(stencil2, [biggest_shape2_aligned], (0, 0, 255))

        xor = cv2.bitwise_and(cv2.bitwise_not(stencil1), stencil2)        
    
        alpha = 0.8
        result = cv2.addWeighted( img1, alpha, xor, 1 - alpha, 0.0);

        return result;

    def _img2BGRA(self, img):
        b_channel, g_channel, r_channel = cv2.split(img)
        alpha_channel = np.ones(b_channel.shape, dtype=b_channel.dtype) * 255 #creating a dummy alpha channel image.
        img_BGRA = cv2.merge((b_channel, g_channel, r_channel, alpha_channel))

        return img_BGRA

    def _alignContour(self, contour, translationVector):
        for elem in contour[0]:
            elem[0] -= translationVector[0]
            elem[1] -= translationVector[1]

        return contour

    def _findBiggestShape(self, img):
        imgray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        ret,thresh = cv2.threshold(imgray,60,255,0)

        kernel = np.ones((7,7),np.uint8)
        thresh = cv2.dilate(thresh,kernel,iterations = 1)
        thresh = cv2.erode(thresh,kernel,iterations = 1)

        thresh = cv2.bitwise_not(thresh)

        contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

        biggest_shape = max(contours, key = cv2.contourArea)
        return biggest_shape
