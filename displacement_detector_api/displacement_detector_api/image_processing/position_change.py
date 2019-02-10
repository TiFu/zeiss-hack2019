import numpy
import pandas as pandas
from scipy.spatial import distance

def calculate_position_change():
    positions_array = numpy.loadtxt('../src/image_processing/displacements.csv', delimiter=',')

    pos_before = numpy.linalg.norm(positions_array[:, 2:3], axis=1)
    pos_after = numpy.linalg.norm(positions_array[:, 5:6], axis=1)

    all_pos = numpy.append(numpy.array(pos_before), numpy.array(pos_after))
    all_pos = numpy.around(all_pos, 1)
    all_pos = numpy.unique(all_pos, return_counts=True)

    return all_pos[0][:15], all_pos[1][:15]
