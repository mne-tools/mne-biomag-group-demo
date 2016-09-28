"""
Filtering
=========

Plot filter properties.
"""
import numpy as np
import matplotlib.pyplot as plt
import os.path as op

import mne

from library.config import study_path

filt_params = dict(l_trans_bandwidth='auto', h_trans_bandwidth='auto',
                   filter_length='auto', phase='zero', fir_window='hann')

###############################################################################
# Let's look at some data from the multimodal faces data set.
# First we read in the data from run 1 of subject 2.
raw = mne.io.read_raw_fif(op.join(study_path, 'ds117', 'sub002', 'MEG',
                                  'run_01_sss.fif'), add_eeg_ref=False)

raw.set_channel_types({'EEG061': 'eog', 'EEG062': 'eog', 'EEG063': 'ecg',
                       'EEG064': 'misc'})  # EEG064 free floating el.
raw.rename_channels({'EEG061': 'EOG061', 'EEG062': 'EOG062',
                     'EEG063': 'ECG063'})
raw.set_eeg_reference()

###############################################################################
# Then we filter it at 1Hz with the defaults of MNE.
raw_1 = raw.copy()
raw_1.load_data()
raw_1.filter(1, 40, **filt_params)

raw_1.plot_psd(fmax=10)

###############################################################################
# We see that even though the attenuation close to 0Hz is sufficient enough,
# the low frequency components at around 1Hz are still quite prominent. Lets
# see how the famous faces look after averaging. (Notice that we do not
# compensate for the delay or clean the data, so the figures are not comparable
# to the final results).
events = mne.find_events(raw_1)
event_ids = [5, 6, 7]  # Famous faces
evoked_1 = mne.Epochs(raw_1, events, event_id=event_ids,
                      baseline=None).average()
evoked_1.plot(spatial_colors=True)

###############################################################################
# They're all over the place! The baselining effect of high pass filtering does
# not seem to work. Let's try removing the low frequency components by raising
# the cut-off frequency to 2.5 Hz.
raw_2 = raw.copy()
raw_2.load_data()
raw_2.filter(2.5, 40, **filt_params)
raw_2.plot_psd(fmax=10)

###############################################################################
# We see that the low frequency 'peak' is gone and the transition is more
# gradual. The 'auto' param automatically fits the transition bandwidth to
# reduce ringing as much as possible.
# Finally we plot the evoked responses, and we see that the fanning of the
# signal is gone.
evoked_2 = mne.Epochs(raw_2, events, event_id=event_ids,
                      baseline=None).average()
evoked_2.plot(spatial_colors=True)

###############################################################################
# Let's also plot the impulse response of the used filter. Here we create some
# data with 30000 samples of zeros with an impulse at the middle. Then we
# construct a raw data structure and set a sampling frequency to 1000. Thus,
# we have 30 seconds of data with an impulse at 15 seconds.
n_samples = 30000
sfreq = 1000
info = mne.create_info(ch_names=['test'], sfreq=sfreq, ch_types=['eeg'])
data = np.zeros(n_samples)
data[n_samples // 2] = 1e-6
times = np.linspace(0, n_samples // sfreq, n_samples)
raw = mne.io.RawArray(np.array([data]), info)

###############################################################################
# We low pass filter the data and plot the frequency spectrum and the impulse
# response of the filter.
raw.filter(None, 40, **filt_params)
plt.plot(times, raw[0][0][0])
plt.xlabel('Time (s)')
plt.ylabel('Amplitude')
plt.title('Impulse response')
plt.xlim((14, 16))
plt.show()
raw.plot_psd(fmin=20, fmax=60)

###############################################################################
# Let's do the same after high pass filtering at 2.5 Hz.
raw.filter(2.5, None, **filt_params)
plt.plot(times, raw[0][0][0])
plt.xlabel('Time (s)')
plt.ylabel('Amplitude')
plt.title('Impulse response')
plt.xlim((14, 16))
plt.show()
raw.plot_psd(fmax=10)
