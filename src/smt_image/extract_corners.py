import cv2

import numpy as np
np.set_printoptions(threshold=np.nan)



img = cv2.imread("../../data/smt_image/343216_20160805-142843_L.tif")
#img = cv2.imread("../../data/smt_image/342547_20160721-204408_R.tif")
left = True

imgray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

cv2.imshow("gray", imgray)

ret,thresh = cv2.threshold(imgray,60,255,0)

cv2.imshow("Thresh", thresh)

kernel = np.ones((7,7),np.uint8)

thresh = cv2.dilate(thresh,kernel,iterations = 1)
thresh = cv2.erode(thresh,kernel,iterations = 1)

#cv2.imshow("Eroded", thresh)

thresh = cv2.bitwise_not(thresh)

im, contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

#cv2.drawContours(img, contours, -1, (0,255,0), 3)

def limit(val, maxVal):
    return min(max(0, val), maxVal)

biggest_shape = max(contours, key = cv2.contourArea)
x,y,w,h = cv2.boundingRect(biggest_shape)
w += 20
h += 20
x -= 10
y -= 10

x1 = limit(x, thresh.shape[0])
y1 = limit(y, thresh.shape[1])
x2 = limit(x + w, thresh.shape[0])
y2 = limit(y + h, thresh.shape[1])

#cv2.rectangle(thresh,(x1,y1),(x2,y2),(0,255,0),2)
cornerPic = thresh[y1:y2, x1:x2]
cv2.imshow("corner", cornerPic)
stencil = np.zeros(thresh.shape).astype(img.dtype)
cv2.fillPoly(stencil, [biggest_shape], 255)
cutOut = cv2.bitwise_and(thresh, stencil)[y1:y2, x1:x2]

# Detector parameters
blockSize = 6
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
threshold = 100
for i in range(dst_norm.shape[0]):
    for j in range(dst_norm.shape[1]):
        if int(dst_norm[i,j]) > threshold:
            corners.append((j, i))
            cv2.circle(cutOut, (j,i), 5, (0), 2)

#corners.sort(key=lambda x: x[0])
corners = np.array(corners)
corners.sort(axis = 1)
clusters = []
currentCluster = []
prev = None
for corner in corners:
    if prev is None or abs(prev[1] - corner[1]) <= 2:
        currentCluster.append(corner)
    else:
        clusters.append(currentCluster)
        currentCluster = []
    prev = corner

if len(currentCluster) > 0:
    clusters.append(currentCluster)
    
import pprint
pp = pprint.PrettyPrinter(depth=6)
pp.pprint(clusters)
#print(clusters)
corners = []
for cluster in clusters:
    cluster.sort(key=lambda x: x[0])
    print("Cluster: " + str(cluster))
    if left:    # min y
        min = (np.Inf, 0)
        for corner in cluster:
            if corner[0] < min[0]:
                min = corner
        corners.append(min)
    else: # max y
        max = (np.NINF, 0)
        for corner in cluster:
            if corner[0] > max[0]:
                max = corner
        corners.append(max)
        
#    corners.append(corner)

print(corners)

print("Top Left: " + str(corners[0]))
print("Bottom Left: " + str(corners[1]))
# Transform corners back to original image space
originalCorners1 = (int(x1 + corners[0][0]), int(y1 + corners[0][1]))
originalCorners2 = (int(x1 + corners[1][0]), int(y1 + corners[1][1]))
cv2.circle(img, originalCorners1, 5, (0,255,0), 2)
cv2.circle(img, originalCorners2, 5, (0,255,0), 2)


cv2.imshow("cut out", cutOut)
cv2.drawContours(img, [biggest_shape], -1, (255,0,0), 1)


cv2.imshow("Test", img)
cv2.waitKey()