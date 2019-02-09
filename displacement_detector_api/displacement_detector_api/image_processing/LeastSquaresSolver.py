import numpy as np
import math

class LeastSquaresSolver:

    def __init__(self):
        pass

    def solve(self, before, after):
        print("Before: "+ str(before))
        print("After: " + str(after))
        # Centro
        beforeCentroid = (before[0] + before[1]) / 2.0
        afterCentroid = (after[1] + after[0]) / 2.0

        beforeCentered = [ before[0] - beforeCentroid, before[1] - beforeCentroid]
        afterCentered = [ after[0] - afterCentroid, after[1] - afterCentroid]

        beforeVector = beforeCentered[0] - beforeCentered[1]
        afterVector = afterCentered[0] - afterCentered[1]

        angle = self._angle_between(beforeVector, afterVector)

        rotationMatrix = np.array([
            [ np.cos(angle), -np.sin(angle)],
            [ np.sin(angle), np.cos(angle)]
        ])

        rotatedCentroidA = np.dot(rotationMatrix, beforeCentroid)

        translation = - rotatedCentroidA + afterCentroid

        print("Angle: " + str(np.rad2deg(angle)) + ", Translation: "+ str(translation))
        return (angle, translation)
        # cos(theta) = u dot v / (|u| * |v|)


    def _unit_vector(self, vector):
        """ Returns the unit vector of the vector.  """
        return vector / np.linalg.norm(vector)

    def _angle_between(self, v1, v2):
        """ Returns the angle in radians between vectors 'v1' and 'v2'::

                >>> angle_between((1, 0, 0), (0, 1, 0))
                1.5707963267948966
                >>> angle_between((1, 0, 0), (1, 0, 0))
                0.0
                >>> angle_between((1, 0, 0), (-1, 0, 0))
                3.141592653589793
        """
        v1_u = self._unit_vector(v1)
        v2_u = self._unit_vector(v2)
        return np.arccos(np.clip(np.dot(v1_u, v2_u), -1.0, 1.0))

