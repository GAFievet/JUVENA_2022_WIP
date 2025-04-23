from datetime import datetime, timedelta

def combine_date_time(ldates: list, ltimes: list):
	"""
	Combines lists of integers or strings representing dates (YYYYMMDD)  and strings representing
	times (HH:MM:SS.fff) into a list of datetime objects.

	Used in Vessel_echo_data_extraction & glider_data_extraction

	Args:
	  ldates: A list of integers or strings representing dates.
	  ltimes: A list of strings representing times.

	Returns:
	  A list of datetime objects.
	"""
	if len(ldates) != len(ltimes):
		raise ValueError("ldates and ltimes must have the same length")

	# Convert ldates to str
	if isinstance(ldates[0], int):
		ldates = [str(item) for item in ldates]
	# Get rid of useless spaces before and after
	ltimes = [item.strip() for item in ltimes]
	ldates = [item.strip() for item in ldates]

	# Create future list of datetimes
	lcombined_datetime = []
	for date_str, time_str in zip(ldates, ltimes):
		try:
			date_obj = datetime.strptime(date_str, '%Y%m%d')
		except ValueError:
			date_obj = datetime.strptime(date_str, "%d-%b-%Y")
		try:
			time_obj = datetime.strptime(time_str, '%H:%M:%S.%f').time()
		except ValueError:
			time_obj = datetime.strptime(time_str, "%I:%M %p").time()

		combined_datetime = datetime.combine(date_obj, time_obj)
		lcombined_datetime.append(combined_datetime)

	return lcombined_datetime

def matlab2python(matlab_datenum):
	"""
	   Converts a MATLAB serial date number to a Python datetime object.

	   Args:
	       matlab_datenum (float): The MATLAB serial date number.

	   Returns:
	       datetime.datetime: The corresponding Python datetime object.
	   """
	# MATLAB reference date: January 0, 0000 (proleptic Gregorian), which is equivalent to Dec 31, year -1
	matlab_reference_base = datetime(1, 1, 1)  # Start with a valid Python date

	# Calculate the total timedelta from the MATLAB reference
	# Subtract 2 because MATLAB starts counting from day 1 of its reference plus year 0 doesn't exist in Pyhon
	days_since_reference = matlab_datenum - 2
	delta = timedelta(days = days_since_reference)
	python_datetime = matlab_reference_base + delta

	return python_datetime

if __name__ == "__main__":
	# # Example usage
	# date_ints = [20220904, 20230115, 20240708]
	# time_strings = [' 10:56:01.6480', ' 15:23:45.1234', ' 08:00:00.0000']
	#
	# combined_datetimes = combine_date_time(date_ints, time_strings)
	#
	# print(type(combined_datetimes))
	# for dt in combined_datetimes:
	# 	print(type(dt))
	# 	print(dt)


	# Example MATLAB to Python
	matlab_dates = [[738783.9791666666], [738784.0208333334], [738784.0625], [738784.1041666666], [738784.1458333334]]

	# Convert each MATLAB date to a Python date
	python_dates = [matlab2python(date[0]).strftime("%d/%m/%Y %H:%M:%S") for date in matlab_dates]

	# Display the results
	for i, python_date in enumerate(python_dates):
		print(f"MATLAB Date: {matlab_dates[i][0]}, Python Date: {python_date}")