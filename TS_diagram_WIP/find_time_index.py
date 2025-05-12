import numpy as np
from datetime import datetime
import bisect

def find_time_indices(time, t1, t2):
    """
    Efficiently finds the indices in a sorted list of datetime objects.

    Args:
        time: A sorted list of datetime.datetime objects.
        t1: The start datetime (datetime.datetime).
        t2: The end datetime (datetime.datetime).

    Returns:
        A tuple (i1, i2) where:
        i1: Index of the last element in `time` strictly before t1.
            Returns 0 if all elements are >= t1 or -1 if `time` is empty.
        i2: Index of the first element in `time` strictly after t2.
            Returns len(time) if all elements are <= t2 or -1 if `time` is empty.
    """

    if not time:
        return -1, -1  # Handle empty list case

    i1 = bisect.bisect_left(time, t1) - 1
    i2 = bisect.bisect_right(time, t2)

    i1 = max(-1, i1)  # Ensure i1 is not negative if t1 is before the start
    i2 = min(len(time), i2)  # Ensure i2 is not beyond the end

    return i1, i2

if __name__ == '__main__':
    # --- Example Usage ---
    # Sample sorted list of datetime objects
    time = [
        datetime(2022, 9, 22, 12, 0, 0),
        datetime(2022, 9, 23, 0, 0, 0),
        datetime(2022, 9, 24, 6, 0, 0),
        datetime(2022, 9, 25, 12, 0, 0),
        datetime(2022, 10, 5, 18, 0, 0),
        datetime(2022, 10, 6, 23, 59, 59),
        datetime(2022, 10, 7, 12, 0, 0),
    ]

    t1 = datetime(2022, 9, 23, 0, 0, 0)
    t2 = datetime(2022, 10, 6, 23, 59, 59)

    i1, i2 = find_time_indices(time, t1, t2)
    print(f"Index of last element before t1: {i1}")
    print(f"Index of first element after t2: {i2}")

    t1_outside = datetime(2022, 9, 20, 0, 0, 0)
    t2_outside = datetime(2022, 10, 10, 0, 0, 0)

    i1_out, i2_out = find_time_indices(time, t1_outside, t2_outside)
    print(f"Index of last element before t1_outside: {i1_out}")
    print(f"Index of first element after t2_outside: {i2_out}")

    time_empty = []
    i1_empty, i2_empty = find_time_indices(time_empty, t1, t2)
    print(f"Index for empty time list: {i1_empty}, {i2_empty}")