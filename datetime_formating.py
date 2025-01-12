from datetime import datetime


def combine_date_time(ldates: list, ltimes: list):
	"""
	Combines lists of integers or strings representing dates (YYYYMMDD)  and strings representing
	times (HH:MM:SS.fff) into a list of datetime objects.

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


if __name__ == "__main__":
	# Example usage
	date_ints = [20220904, 20230115, 20240708]
	time_strings = [' 10:56:01.6480', ' 15:23:45.1234', ' 08:00:00.0000']

	combined_datetimes = combine_date_time(date_ints, time_strings)

	print(type(combined_datetimes))
	for dt in combined_datetimes:
		print(type(dt))
		print(dt)
