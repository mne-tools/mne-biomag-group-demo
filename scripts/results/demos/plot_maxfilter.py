# -*- coding: utf-8 -*-
"""
Maxwell filtering in Python
===========================

Demonstrates maxwell filtering for one run (sub003, run01) using MNE-python.
"""

import os.path as op
import sys

import mne
from mne import Epochs
from mne.preprocessing import maxwell_filter

import matplotlib.pyplot as plt
import numpy as np

sys.path.append(op.join('..', '..', 'processing'))
from library.config import (study_path, cal, ctc, l_freq,
                            set_matplotlib_defaults)  # noqa: E402

event_ids = [5, 6, 7]  # Famous faces
tmax = 0.8  # just show the constant-stimulus period here

subject = "sub001"
bads = ['MEG1031', 'MEG1111', 'MEG2113']
filter_params = dict(fir_window='hamming', filter_length='auto', phase='zero',
                     l_trans_bandwidth='auto', h_trans_bandwidth='auto',
                     fir_design='firwin')

raw_fname_in = op.join(study_path, 'ds117', subject, 'MEG', 'run_01_raw.fif')
sss_fname_in = op.join(study_path, 'ds117', subject, 'MEG', 'run_%02d_sss.fif')

###############################################################################
# First the filtered raw data.
raw = mne.io.read_raw_fif(raw_fname_in, preload=True)

raw.info['bads'] = bads
raw.filter(l_freq, 40, **filter_params)

events = mne.find_events(raw, stim_channel='STI101', consecutive='increasing',
                         mask=4352, mask_type='not_and', min_duration=0.003,
                         verbose=True)
evoked_before = Epochs(raw, events, event_id=event_ids, tmax=tmax).average()

###############################################################################
# Then Maxfiltered and SSS'd data.

raw = mne.io.read_raw_fif(raw_fname_in, preload=True)
raw_sss_mf = mne.io.read_raw_fif(sss_fname_in % 1, preload=True,
                                 verbose='error')
raw.info['bads'] = bads
raw.fix_mag_coil_types()
# Get the origin and destinations they used
destination = raw_sss_mf.info['dev_head_t']
origin = raw_sss_mf.info['proc_history'][0]['max_info']['sss_info']['origin']
# Get the head positions.
# Usually this can be done by saving to a text file with MaxFilter
# instead, and reading with :func:`mne.chpi.read_head_pos`.
chpi_picks = mne.pick_types(raw_sss_mf.info, meg=False, chpi=True)
assert len(chpi_picks) == 9
head_pos, t = raw_sss_mf[chpi_picks]
# Add first_samp.
t = t + raw_sss_mf.first_samp / raw_sss_mf.info['sfreq']
# The head positions in the FIF file are all zero for invalid positions
# so let's remove them, and then concatenate our times.
mask = (head_pos != 0).any(axis=0)
head_pos = np.concatenate((t[np.newaxis], head_pos)).T[mask]
# In this dataset due to old MaxFilter (2.2.10), data are uniformly
# sampled at 1 Hz, so we save some processing time in
# maxwell_filter by downsampling.
skip = int(round(raw_sss_mf.info['sfreq']))
head_pos = head_pos[::skip]

###############################################################################
# Run :func:`mne.preprocessing.maxwell_filter`, and band-pass filter the data.

raw_sss_py = maxwell_filter(
    raw, calibration=cal, cross_talk=ctc, origin=origin, head_pos=head_pos)
del raw

raw_sss_py.filter(l_freq, 40, **filter_params)
raw_sss_mf.filter(l_freq, 40, **filter_params)

evoked_sss_py = Epochs(raw_sss_py, events, event_id=event_ids,
                       tmax=tmax).average()
evoked_sss_mf = Epochs(raw_sss_mf, events, event_id=event_ids,
                       tmax=tmax).average()

###############################################################################
# Plotting

set_matplotlib_defaults()

ylim = dict(mag=(-600, 600) if l_freq is None else (-400, 400))

fig, axes = plt.subplots(1, 3, figsize=(7, 2))
evoked_before.pick_types(meg='mag').plot(
    axes=axes[0], spatial_colors=True, ylim=ylim, show=False)
axes[0].set_title('Raw data')
evoked_sss_py.pick_types(meg='mag').plot(
    axes=axes[1], spatial_colors=True, ylim=ylim, show=False)
axes[1].set(title=r'$\mathtt{maxwell\_filter}$', ylabel='')
diff = mne.combine_evoked([evoked_sss_py.pick_types(meg='mag'),
                           evoked_sss_mf.pick_types(meg='mag')],
                          weights=[-1, 1])
diff.plot(
    axes=axes[2], spatial_colors=True, ylim=ylim, show=False)
axes[2].set(title=u'$\mathtt{maxwell\_filter}$ -\nMaxfilter™', ylabel='')
mne.viz.utils.tight_layout(fig=fig)
fig.delaxes(fig.axes[3])
fig.delaxes(fig.axes[3])
fig.axes[3].collections[0].set(sizes=[3])
fig.savefig(op.join('..', 'figures', 'Maxfilter.pdf'), bbox_to_inches='tight')
plt.show()
