from ScaleDetector import ScaleDetector
from CornerDetector import CornerDetector
from LeastSquaresSolver import LeastSquaresSolver
import numpy as np

class ImageProcessing:

    def __init__(self):
        self.scaleDetector = ScaleDetector()
        self.cornerDetector = CornerDetector()
        self.leastSquaresSolver = LeastSquaresSolver()

    def determineDisplacement(self, beforeLeft, beforeRight, afterLeft, afterRight):
        """Returns displacement (angle, tx, ty) for (left, right)
        
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
        return (left, None)
    
    def _convertToReal(self, corners, scaleAndLeftMost):
        corners = list(corners)
        print("Corners: ", corners)
        print("SCale and left most: " + str(scaleAndLeftMost))
        scale, leftMostPoint = scaleAndLeftMost
        print("LEft most: " + str(leftMostPoint))
        print("Scale: " + str(scale))
        return map(lambda corner: self._convertToMM(self._convertCornerToCordsRelativeToLeftMostPoint(corner, leftMostPoint), scale), corners)

    def _convertCornerToCordsRelativeToLeftMostPoint(self, corner, leftMostPoint):
        return (corner[0] - leftMostPoint[0], corner[1] - leftMostPoint[1])

    def _convertToMM(self, coordinates, scale):
        return (coordinates[0] / scale, coordinates[1] / scale)