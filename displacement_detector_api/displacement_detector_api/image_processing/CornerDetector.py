import cv2
import numpy as np

from displacement_detector_api.image_processing.CornersNotFoundException import CornersNotFoundException


class CornerDetector:

    def __init__(self):
        pass

    def limit(self, val, maxVal):
        return min(max(0, val), maxVal)

    def detectCorners(self, img, left):
        """Returns the top left and bottom left (or right if left is False) points of the mirror

        Arguments:
            img {[type]} -- [description]
            left {[type]} -- [description]

        Returns:
            ((x, y), (x, y)) -- [description]
        """

        imgray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        #        cv2.imshow("Gray", imgray)
        thresh = imgray
        ret, thresh = cv2.threshold(imgray, 60, 255, 0)
        #        cv2.imshow("Thresh 1", thresh)

        kernel = np.ones((7, 7), np.uint8)
        thresh = cv2.dilate(thresh, kernel, iterations=1)
        thresh = cv2.erode(thresh, kernel, iterations=1)

        thresh = cv2.bitwise_not(thresh)
        contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        #        cv2.imshow("Thresh", thresh)

        biggest_shape = max(contours, key=cv2.contourArea)
        x, y, w, h = cv2.boundingRect(biggest_shape)
        w += 20
        h += 20
        x -= 10
        y -= 10

        x1 = self.limit(x, thresh.shape[0])
        y1 = self.limit(y, thresh.shape[1])
        x2 = self.limit(x + w, thresh.shape[0])
        y2 = self.limit(y + h, thresh.shape[1])

        # cv2.rectangle(thresh,(x1,y1),(x2,y2),(0,255,0),2)
        cornerPic = thresh[y1:y2, x1:x2]

        stencil = np.zeros(thresh.shape).astype(img.dtype)
        cv2.fillPoly(stencil, [biggest_shape], 255)
        hull = cv2.convexHull(biggest_shape, False)
        cv2.fillPoly(stencil, [hull], 255)
        cutOut = cv2.bitwise_and(thresh, stencil)[y1:y2, x1:x2]
        cutOut = cv2.bitwise_or(cutOut, stencil[y1:y2, x1:x2])
        #       cv2.imshow("cut out 1", cutOut)
        # Detector parameters
        blockSize = 10
        apertureSize = 3
        k = 0.05

        # Detecting corners
        dst = cv2.cornerHarris(cutOut, blockSize, apertureSize, k)
        dst_norm = np.empty(dst.shape, dtype=np.float32)
        cv2.normalize(dst, dst_norm, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX)
        dst_norm_scaled = cv2.convertScaleAbs(dst_norm)
        # Drawing a circle around corners
        # Cluster around y
        corners = []
        threshold = 65
        for i in range(dst_norm.shape[0]):
            for j in range(dst_norm.shape[1]):
                if int(dst_norm[i, j]) > threshold:
                    corners.append((j, i))
                    cv2.circle(cutOut, (j, i), 5, (128), 2)
        #        print("Circle Count: " + str(len(corners)))
        #        cv2.imshow("cut out", cutOut)
        #        cv2.waitKey()
        corners.sort(key=lambda x: x[1])
        corners = np.array(corners)
        # corners.sort(axis = 1)
        clusters = []
        currentCluster = []
        prev = None
        for corner in corners:
            if prev is None or abs(prev[1] - corner[1]) <= 2:
                currentCluster.append(corner)
            else:
                clusters.append(currentCluster)
                currentCluster = []
                currentCluster.append(corner)
            prev = corner

        if len(currentCluster) > 0:
            clusters.append(currentCluster)

        import pprint
        pp = pprint.PrettyPrinter(depth=6)
        #     pp.pprint(clusters)

        corners = []
        for cluster in clusters:
            cluster.sort(key=lambda x: x[0])
            #     print("Cluster: " + str(cluster))
            if left:  # min y
                minimum = (np.Inf, 0)
                for corner in cluster:
                    if corner[0] < minimum[0]:
                        minimum = corner
                corners.append(minimum)
            else:  # max y
                maximum = (np.NINF, 0)
                for corner in cluster:
                    if corner[0] > maximum[0]:
                        maximum = corner
                corners.append(maximum)

        #    corners.append(corner)
        if len(corners) != 2:
            raise CornersNotFoundException("Failed to identify corners.");
        #        print(corners)

        #        print("Top Left: " + str(corners[0]))
        #        print("Bottom Left: " + str(corners[1]))
        # Transform corners back to original image space
        originalCorners1 = (int(x1 + corners[0][0]), int(y1 + corners[0][1]))
        originalCorners2 = (int(x1 + corners[1][0]), int(y1 + corners[1][1]))
        #       cv2.circle(img, originalCorners1, 5, (0,255,0), 2)
        #       cv2.circle(img, originalCorners2, 5, (0,255,0), 2)

        #        cv2.drawContours(img, [biggest_shape], -1, (255,0,0), 1)
        #        cv2.imshow("Test", img)
        #        cv2.waitKey()
        return originalCorners1, originalCorners2
