import cv2
import numpy as np

img = cv2.imread("./SmtImageData/346604_20160916-194444_L.tif")
imgray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
cv2.imshow("gray", imgray)
ret,thresh = cv2.threshold(imgray,60,255,0)
cv2.imshow("Thresh", thresh)
kernel = np.ones((3,3),np.uint8)
thresh = cv2.dilate(thresh,kernel,iterations = 1)
cv2.imshow("Eroded", thresh)
thresh = cv2.bitwise_not(thresh)
im2, contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
print(contours)
cv2.drawContours(img, contours, -1, (0,255,0), 3)
cv2.imshow("Test", img)