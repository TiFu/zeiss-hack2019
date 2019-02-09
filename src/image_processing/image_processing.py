from ScaleDetector import ScaleDetector
from CornerDetector import CornerDetector

class ImageProcessing:

    def __init__(self):
        self.scaleDetector = ScaleDetector()
        self.cornerDetector = CornerDetector()


    def determineDisplacement(beforeLeft, beforeRight, afterLeft, afterRight):
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
    
    def _convertToReal(self, corners, scaleAndLeftMost):
        leftMostPoint, scale = scaleAndLeftMost
        return map(lambda corner: self._convertToMM(self._convertCornerToCordsRelativeToLeftMostPoint(corner, leftMostPoint), scale), conrers)

    def _convertCornerToCordsRelativeToLeftMostPoint(self, corner, leftMostPoint):
        return (corner[0] - leftMostPoint[0], corner[1] - leftMostPoint[1])

    def _convertToMM(self, coordinates, scale):
        return (coordinates[0] / scale, coordinates[1] / scale)