import cv2
import numpy as np
import math
def isCircle(area):
    radius = math.sqrt(area / math.pi)
#    print("Radius: " + str(radius))
    return radius >= 4.1 and radius <= 4.4
#    print("Contour: " + str(contour))
#    print("--")
    return True

def reject_outliers(data, m=2):
    return data[abs(data - np.mean(data)) < m * np.std(data)]

np.set_printoptions(threshold=np.nan)
img = cv2.imread("../../data/smt_image/343216_20160805-142843_L.tif")
imgray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
#cv2.imshow("gray", imgray)
ret,thresh = cv2.threshold(imgray,60,255,0)
cv2.imshow("Thresh", thresh)
kernel = np.ones((3,3),np.uint8)
thresh = cv2.dilate(thresh,kernel,iterations = 1)
cv2.imshow("Eroded", thresh)
thresh = cv2.bitwise_not(thresh)
cv2.imshow("Thresh2", thresh)
im2, contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
#print(contours)

contour_list = []
rejected_contours = []
circleCenters = []
for contour in contours:
    approx = cv2.approxPolyDP(contour,0.01*cv2.arcLength(contour,True),True)
    area = cv2.contourArea(contour)

    if isCircle(area):
        contour_list.append(contour)
        center = np.array(contour).sum(axis = 0) / len(contour)
        circleCenters.append(center[0])
    else:
        rejected_contours.append(contour)


for circle in circleCenters:
    cv2.circle(img, (circle[0], circle[1]), 4, (255,0,0), -1)
# Calculate Distance between circles
print(circleCenters)
circles = np.array(circleCenters)
circles.sort(axis=1)
print(circles)
clusters = []
prev = None
currentCluster =[]
for circle in circles:
#    print("Is circle: " + str(circle))
    if prev is None or abs(circle[1] - prev[1]) <= 2:
        currentCluster.append(circle)
    else:
        clusters.append(currentCluster)
        currentCluster = []
    prev = circle

if len(currentCluster) > 0:
    clusters.append(currentCluster)

clusters = np.array(clusters)
all_distances = []
for cluster in clusters:
    cluster = np.array(cluster)[:,0]
    cluster.sort()

    ediff = np.ediff1d(cluster)
    all_distances.extend(ediff)

xDist = reject_outliers(np.array(all_distances)).mean()
print("Distance in x-Direction: " + str(xDist))

#cv2.drawContours(img, rejected_contours, -1, (255,0,0), 3)

#canny = cv2.Canny(imgray,100,30)
#cv2.imshow("Canny", canny)
#print(canny)


    
#rows = imgray.shape[0]
#print(rows)
#circles = cv2.HoughCircles(imgray, cv2.HOUGH_GRADIENT, 1.1, rows / 50,
#                            param1=100, param2=30)


#if circles is not None:
#    circles = np.uint16(np.around(circles))
#    for i in circles[0, :]:
#        center = (i[0], i[1])
        # circle center
#        cv2.circle(img, center, 1, (0, 100, 100), 3)
        # circle outline
#        radius = i[2]
#        cv2.circle(img, center, radius, (255, 0, 255), 3)



cv2.imshow("Test", img)

cv2.waitKey()