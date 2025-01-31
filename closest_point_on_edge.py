import numpy as np


def get_closest_point_on_edge(point, center, radius):
	"""
	Finds the closest point on the circle's edge to the given point.

	Args:
		point: (x, y) coordinates of the point.
		center: (x, y) coordinates of the center of the circle.
		radius: Radius of the circle.

	Returns:
		(x, y) coordinates of the closest point on the edge.
	"""
	vector_to_point = np.array(point) - np.array(center)
	unit_vector = vector_to_point / np.linalg.norm(vector_to_point)
	closest_point = center + radius * unit_vector
	return closest_point
