from image_processing import ImageProcessing

import cv2

beforeL = cv2.imread("/home/tino/smt_image_data/SmtImageData/342411_20161007-175850_L.tif")
afterL = cv2.imread("/home/tino/smt_image_data/SmtImageData/342411_20161007-183433_L.tif")

beforeR = cv2.imread("/home/tino/smt_image_data/SmtImageData/388903_20161028-044310_R.tif")
afterR = cv2.imread("/home/tino/smt_image_data/SmtImageData/388903_20161028-044623_R.tif")

processing = ImageProcessing()
result = processing.determineDisplacement(beforeL, beforeR, afterL, afterR)
print(result)