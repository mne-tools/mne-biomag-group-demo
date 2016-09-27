"""
Filtering
=========

Plot filter properties.
"""
import numpy as np
import matplotlib.pyplot as plt

import mne

###############################################################################
# First we create some data with 10000 samples of zeros with an impulse at the
# middle. Then we construct a raw data structure and set a sampling frequency
# to 1000. Thus, we have 10 seconds of data with an impulse at 5 seconds.
n_samples = 10000
sfreq = 1000
info = mne.create_info(ch_names=['test'], sfreq=sfreq, ch_types=['eeg'])
data = np.zeros(n_samples)
data[n_samples // 2] = 1e-6
times = np.linspace(0, n_samples // sfreq, n_samples)
raw = mne.io.RawArray(np.array([data]), info)

###############################################################################
# We lowpass filter the data and plot the frequency spectrum and the impulse
# response of the filter.
raw.filter(None, 40)
raw.plot_psd(fmin=20, fmax=60)
plt.plot(times, raw[0][0][0])
plt.xlabel('Time (s)')
plt.ylabel('Amplitude')
plt.title('Impulse response')
plt.show()

###############################################################################
# Let's do the same after highpass filtering at 1 Hz.
raw.filter(1, None)
raw.plot_psd(fmax=10)
plt.plot(times, raw[0][0][0])
plt.xlabel('Time (s)')
plt.ylabel('Amplitude')
plt.title('Impulse response')
plt.show()
