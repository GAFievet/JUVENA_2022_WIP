from datetime import datetime, time

def combine_date_time(date_ints, time_strings):
  """
  Combines lists of integers representing dates (YYYYMMDD) and strings representing
  times (HH:MM:SS.fff) into a list of datetime objects.

  Args:
    date_ints: A list of integers representing dates.
    time_strings: A list of strings representing times.

  Returns:
    A list of datetime objects.
  """

  if len(date_ints) != len(time_strings):
    raise ValueError("date_ints and time_strings must have the same length")

  time_strings = [item.strip() for item in time_strings]
  combined_datetimes = []
  for date_int, time_str in zip(date_ints, time_strings):
    date_str = str(date_int)
    date_obj = datetime.strptime(date_str, '%Y%m%d')
    time_obj = datetime.strptime(time_str, '%H:%M:%S.%f').time()
    combined_datetime = datetime.combine(date_obj, time_obj)
    combined_datetimes.append(combined_datetime)

  return combined_datetimes

if __name__=="__main__":
	# Example usage
	date_ints = [20220904, 20230115, 20240708]
	time_strings = [' 10:56:01.6480', ' 15:23:45.1234', ' 08:00:00.0000']

	combined_datetimes = combine_date_time(date_ints, time_strings)

	print(type(combined_datetimes))
	for dt in combined_datetimes:
	  print(type(dt))
	  print(dt)