"""
Baselining vs. Highpass filtering
=================================

Here we compare the evokeds when we baseline it vs.
highpass filter it.
"""

import os.path as op

import mne
from mne import Epochs

from library.config import study_path

subject = "sub003"
event_ids = [5, 6, 7]  # Famous faces
filter_params = dict(fir_window='hann', phase='zero',
                     h_trans_bandwidth='auto', filter_length='auto')

###############################################################################
# Read in raw data and prepare for epoching
raw_fname = op.join(study_path, 'ds117', subject, 'MEG', 'run_01_sss.fif')
raw = mne.io.read_raw_fif(raw_fname, preload=True, add_eeg_ref=False)

picks = mne.pick_types(raw.info, meg=True, exclude='bads')
events = mne.find_events(raw, stim_channel='STI101', consecutive='increasing',
                         mask=4352, mask_type='not_and', min_duration=0.003,
                         verbose=True)

###############################################################################
# First, we don't highpass filter and only baseline. Note how it creates a
# spatially varying distortation of the time-domain signal in the form
# of "fanning"
raw.filter(None, 40, **filter_params)
evoked = Epochs(raw, events, event_id=event_ids, picks=picks,
                baseline=(None, 0)).average()
evoked.plot()
evoked.plot_topomap()

###############################################################################
# Next, we highpass filter (but no lowpass filter as we have already done it)
# but don't baseline. Now, the late effects in the topography are no longer
# visible and the "fanning" has disappeared.
raw.filter(1, None, l_trans_bandwidth=0.5, **filter_params)
evoked = Epochs(raw, events, event_id=event_ids, picks=picks,
                baseline=None).average()
evoked.plot()
evoked.plot_topomap()
