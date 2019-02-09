from ScaleDetector import ScaleDetector
from CornerDetector import CornerDetector
from LeastSquaresSolver import LeastSquaresSolver
from OverlayProcessor import OverlayProcessor
import cv2
import numpy as np

class ImageProcessing:

    def __init__(self):
        self.scaleDetector = ScaleDetector()
        self.cornerDetector = CornerDetector()
        self.leastSquaresSolver = LeastSquaresSolver()
        self.overlayProcessor = OverlayProcessor()

    def determineDisplacement(self, beforeLeft, beforeRight, afterLeft, afterRight):
        """Returns displacement (angle, tx, ty) for (left, right, overlayLeft, overlayRight)
        
        Arguments:
            beforeLeft {[type]} -- [description]
            beforeRight {[type]} -- [description]
            afterLeft {[type]} -- [description]
            afterRight {[type]} -- [description]
        
        Returns:
            [type] -- [description]
        """

        scaleBL =  self.scaleDetector.detectScaleAndLeftMostPoint(beforeLeft) # (scale, leftMostPoint)
        scaleAL = self.scaleDetector.detectScaleAndLeftMostPoint(afterLeft)
        scaleBR = self.scaleDetector.detectScaleAndLeftMostPoint(beforeRight)
        scaleAR = self.scaleDetector.detectScaleAndLeftMostPoint(afterRight)

        pointsBL = self.cornerDetector.detectCorners(beforeLeft, True) # (corner, corner)
        pointsAL = self.cornerDetector.detectCorners(afterLeft, True)
        pointsBR = self.cornerDetector.detectCorners(beforeRight, False)
        pointsAR = self.cornerDetector.detectCorners(afterRight, False)

        realBL = self._convertToReal(pointsBL, scaleBL)
        realAL = self._convertToReal(pointsAL, scaleAL)
        realBR = self._convertToReal(pointsBR, scaleBR)
        realAR = self._convertToReal(pointsAR, scaleAR)

        # TODO: calculate
        left = self.leastSquaresSolver.solve(np.array(realBL), np.array(realAL))
        right = self.leastSquaresSolver.solve(np.array(realBR), np.array(realAR))

        # Calculate overlay image
        overlayImageLeft = self.overlayProcessor.overlay(beforeLeft, afterLeft, scaleBL[1], scaleAL[1])
        overlayImageRight = self.overlayProcessor.overlay(beforeRight, afterRight, scaleBR[1], scaleAR[1])

#        cv2.imshow("Left", overlayImageLeft)
#        cv2.imshow("Right", overlayImageRight)
#        cv2.waitKey()
        return (left, right, overlayImageLeft, overlayImageRight)
    
    def _convertToReal(self, corners, scaleAndLeftMost):
        corners = list(corners)
        scale, leftMostPoint = scaleAndLeftMost
        return map(lambda corner: self._convertToMM(self._convertCornerToCordsRelativeToLeftMostPoint(corner, leftMostPoint), scale), corners)

    def _convertCornerToCordsRelativeToLeftMostPoint(self, corner, leftMostPoint):
        return (corner[0] - leftMostPoint[0], corner[1] - leftMostPoint[1])

    def _convertToMM(self, coordinates, scale):
        return (coordinates[0] / scale, coordinates[1] / scale)