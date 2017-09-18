"""
Maxwell filtering
=================

Demonstrates maxwell filtering for one run (sub003, run01) using MNE-python.
"""

import os.path as op

import mne
from mne import Epochs
from mne.preprocessing import maxwell_filter

from library.config import study_path, cal, ctc, set_matplotlib_defaults

event_ids = [5, 6, 7]  # Famous faces

subject = "sub001"
bads = ['MEG1031', 'MEG1111', 'MEG2113']
filter_params = dict(fir_window='hann', l_trans_bandwidth=0.5, phase='zero',
                     h_trans_bandwidth='auto', filter_length='auto',
                     fir_design='firwin')

raw_fname_in = op.join(study_path, 'ds117', subject, 'MEG', 'run_01_raw.fif')
sss_fname_in = op.join(study_path, 'ds117', subject, 'MEG', 'run_01_sss.fif')

###############################################################################
# First the filtered raw data.
raw = mne.io.read_raw_fif(raw_fname_in, preload=True)

raw.info['bads'] = bads
picks = mne.pick_types(raw.info, meg=True, exclude='bads')
raw.filter(1., 40, **filter_params)

events = mne.find_events(raw, stim_channel='STI101', consecutive='increasing',
                         mask=4352, mask_type='not_and', min_duration=0.003,
                         verbose=True)
evoked_before = Epochs(raw, events, event_id=event_ids, picks=picks).average()

###############################################################################
# Then Maxfiltered and SSS'd data.
raw = mne.io.read_raw_fif(raw_fname_in, preload=True)
raw_sss = mne.io.read_raw_fif(sss_fname_in, preload=True)
raw.info['bads'] = bads
raw_sss.info['bads'] = bads

raw = maxwell_filter(raw, calibration=cal, cross_talk=ctc, st_duration=None)

raw.filter(1., 40, **filter_params)
raw_sss.filter(1., 40, **filter_params)

evoked_after = Epochs(raw, events, event_id=event_ids, picks=picks).average()
evoked_sss = Epochs(raw_sss, events, event_id=event_ids, picks=picks).average()

###############################################################################
# Plotting
import matplotlib.pyplot as plt  # noqa
set_matplotlib_defaults(plt)

ylim = dict(mag=(-400, 400))

fig, axes = plt.subplots(1, 3, figsize=(18, 6))
plt.tight_layout()
evoked_before.pick_types(meg='mag').plot(axes=axes[0], spatial_colors=True,
                                         ylim=ylim,
                                         titles={'mag': 'Before SSS'})
axes[0].set_title('A')
evoked_after.pick_types(meg='mag').plot(axes=axes[1], spatial_colors=True,
                                        ylim=ylim, titles={'mag': 'After SSS'})
axes[1].set_title('B')
evoked_sss.pick_types(meg='mag').plot(axes=axes[2], spatial_colors=True,
                                      ylim=ylim,
                                      titles={'mag': 'After Maxfilter (TM)'})
axes[2].set_title('C')
fig.savefig('Maxfilter.pdf', bbox_to_inches='tight')
