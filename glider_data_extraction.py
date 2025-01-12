import pandas as pd
from datetime_formating import combine_date_time
import pickle


def extract_glider_data(extraction_file: str, saving_path: str):
	# Read extraction_file
	df = pd.read_csv(extraction_file)
	# Extract longitudes, latitudes, dates and times
	glider_mat = [df['Longitude'].tolist(), df['Latitude'].tolist(), df['GPS_date'].tolist(), df['GPS_time'].tolist()]
	# Combine dates and times into datetime object
	glider_mat[2] = combine_date_time(glider_mat[2], glider_mat[3])
	# Get rid of last list
	glider_mat.pop(3)

	# Sort according to datetime by creating matching indexes tuples
	zipped = list(zip(glider_mat[0], glider_mat[1], glider_mat[2]))
	# Sort by ascending order according to the 3 element
	zipped.sort(key = lambda x: x[2])
	# unzip to a matrix sorted in datetime order
	glider_mat[0], glider_mat[1], glider_mat[2] = zip(*zipped)

	# Save the matrix to an extraction_file
	with open(saving_path, 'wb') as f:
		# noinspection PyTypeChecker
		pickle.dump(glider_mat, f)

	return glider_mat


if __name__ == "__main__":
	file=r'C:\Users\G to the A\PycharmProjects\Paper\glider\Glider.gps.csv'
	save_path=r'C:\Users\G to the A\PycharmProjects\Paper\glider\glider_GPS.pkl'
	glider_data = extract_glider_data(file,save_path)
