import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import butter, filtfilt


def butfilt(ff_filt, signal, sr):
	"""
	This is a lowpass digital filter.

	Args:
		ff_filt: Frequencies to filter > ff_filt (in hours).
				 For example, if you want to filter everything with a frequency higher than 20 hours, ff_filt = 20.
		signal: Time series to be filtered.
		sr: Sampling rate (samples per second).

	Returns:
		Xfilt: Filtered time series.
	"""

	fs = 1 / sr  # Sampling frequency of our signal (Hz)
	nf = 0.5 * fs  # Nyquist frequency

	x = signal  # Signal [cite: 3]

	filtf = 1 / (ff_filt * 60 * 60)  # Upper limit of frequencies to be passed in Hertz

	# Normalize the filtering frequencies with the Nyquist frequency to
	# obtain the coefficients for the Butterworth filter
	filtc = filtf / nf

	b, a = butter(10, filtc, btype = 'low')

	# Filtering
	Xfilt = filtfilt(b, a, x)

	return Xfilt


if __name__ == '__main__':
	# Example Usage
	ff_filt = 20  # Example: filter frequencies > 20 hours
	sr = 100  # Example: 100 samples per second
	t = np.arange(0, 10, 1 / sr)  # Time vector for plotting
	signal = np.sin(2 * np.pi * 1 * t) + np.sin(2 * np.pi * 5 * t) + np.random.randn(
		len(t))  # Example: signal with 1 Hz and 5 Hz components + noise

	Xfilt = butfilt(ff_filt, signal, sr)

	print("Filtered signal calculated successfully!")

	# Plotting to visualize the result
	plt.figure(figsize = (12, 6))
	plt.plot(t, signal, label = 'Original Signal')
	plt.plot(t, Xfilt, label = 'Filtered Signal')
	plt.xlabel('Time (seconds)')
	plt.ylabel('Amplitude')
	plt.title('Original vs. Filtered Signal')
	plt.legend()
	plt.grid(True)
	plt.show()
