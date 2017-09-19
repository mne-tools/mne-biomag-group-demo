"""
Baselining vs. Highpass filtering
=================================

Here we compare the evokeds when we baseline it vs.
highpass filter it.
"""

import os.path as op

import mne
from mne import Epochs

from library.config import study_path, cal, ctc

subject = "sub003"
event_ids = [5, 6, 7]  # Famous faces
filter_params = dict(fir_window='hann', phase='zero',
                     h_trans_bandwidth='auto', filter_length='auto',
                     fir_design='firwin')

###############################################################################
# Read in raw data and prepare for epoching
raw_fname = op.join(study_path, 'ds117', subject, 'MEG', 'run_01_sss.fif')
raw = mne.io.read_raw_fif(raw_fname, preload=True)

picks = mne.pick_types(raw.info, meg='mag', exclude='bads')
events = mne.find_events(raw, stim_channel='STI101', consecutive='increasing',
                         mask=4352, mask_type='not_and', min_duration=0.003,
                         verbose=True)

###############################################################################
# Just some config for plotting

import matplotlib.pyplot as plt  # noqa
from library.config import set_matplotlib_defaults  # noqa
set_matplotlib_defaults(plt)

ylim = dict(mag=(-400, 400))

###############################################################################
# First, we don't highpass filter and only baseline. Note how it creates a
# spatially varying distortation of the time-domain signal in the form
# of "fanning"
raw.filter(None, 40, **filter_params)
evoked = Epochs(raw, events, event_id=event_ids, picks=picks,
                baseline=(None, 0)).average()
fig = evoked.plot_joint(times="auto", title=None,
                        ts_args=dict(ylim=ylim, spatial_colors=True),
                        topomap_args=dict(vmin=-300, vmax=300))
fig.set_size_inches(12, 6, forward=True)
fig.savefig('FanningA.pdf', bbox_to_inches='tight')

###############################################################################
# Next, we highpass filter (but no lowpass filter as we have already done it)
# but don't baseline. Now, the late effects in the topography are no longer
# visible (see above) and the "fanning" has disappeared.
raw.filter(1, None, l_trans_bandwidth=0.5, **filter_params)
evoked = Epochs(raw, events, event_id=event_ids, picks=picks,
                baseline=None).average()
fig = evoked.plot_joint(times="auto", title=None,
                        ts_args=dict(ylim=ylim, spatial_colors=True),
                        topomap_args=dict(vmin=-300, vmax=300))
fig.set_size_inches(12, 6, forward=True)
fig.savefig('FanningB.pdf', bbox_to_inches='tight')

###############################################################################
# Finally, we can also use the tSSS data which is equivalent to doing a
# highpass filter and the "fanning" will not be visible also in this case.
from mne.preprocessing import maxwell_filter # noqa

raw_fname = op.join(study_path, 'ds117', subject, 'MEG', 'run_01_raw.fif')
raw = mne.io.read_raw_fif(raw_fname, preload=True)

raw = maxwell_filter(raw, calibration=cal, cross_talk=ctc, st_duration=1.0,
                     st_correlation=0.95)

raw.filter(None, 40, **filter_params)
evoked = Epochs(raw, events, event_id=event_ids, picks=picks,
                baseline=(None, 0)).average()
fig = evoked.plot_joint(times="auto", title=None,
                        ts_args=dict(ylim=ylim, spatial_colors=True),
                        topomap_args=dict(vmin=-300, vmax=300))
fig.set_size_inches(12, 6, forward=True)
fig.savefig('FanningC.pdf', bbox_to_inches='tight')
