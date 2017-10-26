"""
Baselining vs. Highpass filtering
=================================

Here we compare the evokeds when we baseline it vs.
highpass filter it.
"""

import os
import os.path as op
import sys

import matplotlib.pyplot as plt

import mne
from mne import Epochs

sys.path.append(op.join('..', '..', 'processing'))
from library.config import (study_path, meg_dir, tmin, tmax,
                            set_matplotlib_defaults)  # noqa: E402

subject = "sub003"
event_ids = [5, 6, 7]  # Famous faces
filter_params = dict(fir_window='hamming', phase='zero',
                     h_trans_bandwidth='auto', filter_length='auto',
                     fir_design='firwin')

###############################################################################
# Read in raw data and prepare for epoching
raw_fname = op.join(study_path, 'ds117', subject, 'MEG', 'run_01_sss.fif')
raw = mne.io.read_raw_fif(raw_fname, preload=True, verbose='error')

picks = mne.pick_types(raw.info, meg='mag', exclude='bads')
events = mne.find_events(raw, stim_channel='STI101', consecutive='increasing',
                         mask=4352, mask_type='not_and', min_duration=0.003,
                         verbose=True)

###############################################################################
# Just some config for plotting

set_matplotlib_defaults(plt)

ylim = dict(mag=(-600, 600))
times = [0, 0.12, 0.4, tmax-0.1]

if not op.isdir('figures'):
    os.mkdir('figures')

###############################################################################
# First, we don't highpass filter and only baseline correct.
# Note how it creates a spatially varying distortation of the time-domain
# signal in the formof "fanning".

raw.filter(None, 40, **filter_params)
evoked = Epochs(raw, events, event_id=event_ids, picks=picks,
                tmin=tmin, tmax=tmax, baseline=(None, 0)).average()
fig = evoked.plot_joint(times=times, title=None,
                        ts_args=dict(ylim=ylim, spatial_colors=True),
                        topomap_args=dict(vmin=-300, vmax=300))
fig.set_size_inches(12, 6, forward=True)
fig.savefig(op.join('..', 'figures', 'FanningA.pdf'), bbox_to_inches='tight')

###############################################################################
# Next, we highpass filter (but no lowpass filter as we have already done it)
# but don't baseline. Now, the late effects in the topography are no longer
# visible (see above) and the "fanning" has disappeared.

raw.filter(1, None, l_trans_bandwidth=0.5, **filter_params)
evoked = Epochs(raw, events, event_id=event_ids, picks=picks,
                tmin=tmin, tmax=tmax, baseline=None).average()
fig = evoked.plot_joint(times=times, title=None,
                        ts_args=dict(ylim=ylim, spatial_colors=True),
                        topomap_args=dict(vmin=-300, vmax=300))
fig.set_size_inches(12, 6, forward=True)
fig.savefig(op.join('..', 'figures', 'FanningB.pdf'), bbox_to_inches='tight')

###############################################################################
# Finally, we can also use the tSSS data which has a highpass
# filtering effect and the "fanning" will not be visible also in this case.
# See :ref:`sphx_glr_auto_scripts_03-maxwell_filtering.py`.

raw_fname = op.join(meg_dir, subject, 'run_01_filt_tsss_1_raw.fif')
raw = mne.io.read_raw_fif(raw_fname, preload=True)
evoked = Epochs(raw, events, event_id=event_ids, picks=picks,
                tmin=tmin, tmax=tmax, baseline=(None, 0)).average()
fig = evoked.plot_joint(times=times, title=None,
                        ts_args=dict(ylim=ylim, spatial_colors=True),
                        topomap_args=dict(vmin=-300, vmax=300))
fig.set_size_inches(12, 6, forward=True)
fig.savefig(op.join('..', 'figures', 'FanningC.pdf'), bbox_to_inches='tight')
