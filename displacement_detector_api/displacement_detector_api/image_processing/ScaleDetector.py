import numpy as np
import cv2
import math

class ScaleDetector:

    def __init__(self):
        pass

    def _isCircle(self, area):
        radius = math.sqrt(area / math.pi)
        print("Radius: " + str(radius))
        return (radius >= 5.3 and radius <= 5.7) or (radius >= 21.2 and radius <= 21.6)

    def _reject_outliers(self, data, m=2):
        return data[abs(data - np.mean(data)) < m * np.std(data)]

    def detectScaleAndLeftMostPoint(self, img):
        """Returns the length of 1mm in pixels and the position of the top left most point
        
        Arguments:
            img {[type]} -- [description]
        
        Returns:
            (float, (x, y)) -- [description]
        """

        imgray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

        ret,thresh = cv2.threshold(imgray,60,255,0)

        kernel = np.ones((3,3),np.uint8)
        thresh = cv2.dilate(thresh,kernel,iterations = 1)
        thresh = cv2.erode(thresh,kernel,iterations = 1)

        thresh = cv2.bitwise_not(thresh)

        contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        #print(contours)

        contour_list = []
        rejected_contours = []
        circleCenters = []
        for contour in contours:
            approx = cv2.approxPolyDP(contour,0.01*cv2.arcLength(contour,True),True)
            area = cv2.contourArea(contour)

            if self._isCircle(area):
                contour_list.append(contour)
                center = np.array(contour).sum(axis = 0) / len(contour)
                circleCenters.append(center[0])
            else:
                rejected_contours.append(contour)

        # Calculate Distance between circles
        circles = np.array(circleCenters)
        circles.sort(axis=1)

        clusters = []
        prev = None
        currentCluster =[]
        for circle in circles:
            if prev is None or abs(circle[1] - prev[1]) <= 2:
                currentCluster.append(circle)
            else:
                clusters.append(currentCluster)
                currentCluster = []
                currentCluster.append(circle)
            prev = circle

        if len(currentCluster) > 0:
            clusters.append(currentCluster)

        clusters = np.array(clusters)
        all_distances = []
        for cluster in clusters:
            print(cluster)
            cluster = np.array(cluster)[:,0]
            cluster.sort()

            ediff = np.ediff1d(cluster)
            all_distances.extend(ediff)

        xDist = self._reject_outliers(np.array(all_distances)).mean()
        topLeftCircle = self._findTopLeftMostCircle(circleCenters)

        return xDist, np.array(topLeftCircle)


    def _findTopLeftMostCircle(self, circleCenters):
        print(circleCenters)
        sortedCenters = sorted(circleCenters, key=lambda x: x[0] * x[0] + x[1] * x[1])
        print(sortedCenters)
        return sortedCenters[0]
