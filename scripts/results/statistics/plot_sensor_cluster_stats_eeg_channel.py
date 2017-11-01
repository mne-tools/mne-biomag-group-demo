# -*- coding: utf-8 -*-
"""
=======================================
Temporal clustering on a single channel
=======================================

Run a non-parametric cluster stats on sensor EEG070
on the contrast faces vs. scrambled.
"""

import os.path as op
import sys

import numpy as np
from scipy import stats
import matplotlib.pyplot as plt

import mne
from mne.stats import permutation_cluster_1samp_test

sys.path.append(op.join('..', '..', 'processing'))
from library.config import (meg_dir, l_freq, N_JOBS, set_matplotlib_defaults,
                            exclude_subjects, annot_kwargs)  # noqa: E402

##############################################################################
# Read all the data

contrasts = list()

for subject_id in range(1, 20):
    if subject_id in exclude_subjects:
        continue
    subject = "sub%03d" % subject_id
    print("processing subject: %s" % subject)
    data_path = op.join(meg_dir, subject)
    contrast = mne.read_evokeds(op.join(data_path, '%s_highpass-%sHz-ave.fif'
                                        % (subject, l_freq)),
                                condition='contrast')
    contrast.apply_baseline((-0.2, 0.0)).crop(None, 0.8)
    contrast.pick_types(meg=False, eeg=True)
    contrasts.append(contrast)

contrast = mne.combine_evoked(contrasts, 'equal')

channel = 'EEG065'
idx = contrast.ch_names.index(channel)
mne.viz.plot_compare_evokeds(contrast, [idx], show_sensors=4,
                             truncate_xaxis=False)

##############################################################################
# Assemble the data and run the cluster stats on channel data

data = np.array([c.data[idx] for c in contrasts])

n_permutations = 1000  # number of permutations to run

# set initial threshold
p_initial = 0.001

# set family-wise p-value
p_thresh = 0.01

connectivity = None
tail = 0.  # for two sided test

# set cluster threshold
n_samples = len(data)
threshold = -stats.t.ppf(p_initial / (1 + (tail == 0)), n_samples - 1)
if np.sign(tail) < 0:
    threshold = -threshold

cluster_stats = permutation_cluster_1samp_test(
    data, threshold=threshold, n_jobs=N_JOBS, verbose=True, tail=tail,
    step_down_p=0.05, connectivity=connectivity,
    n_permutations=n_permutations)

T_obs, clusters, cluster_p_values, _ = cluster_stats

##############################################################################
# Visualize results

set_matplotlib_defaults()

times = 1e3 * contrast.times

fig, axes = plt.subplots(2, sharex=True, figsize=(3.5, 2.5))
ax = axes[0]
ax.plot(times, 1e6 * data.mean(axis=0), label="ERP Contrast")
ax.set(title='Channel : ' + channel, ylabel="EEG (uV)", ylim=[-5, 2.5])
ax.legend()
ax.annotate('A', (-0.16, 1.15), **annot_kwargs)

ax = axes[1]
for i_c, c in enumerate(clusters):
    c = c[0]
    if cluster_p_values[i_c] < p_thresh:
        h1 = ax.axvspan(times[c.start], times[c.stop - 1],
                        color='r', alpha=0.3)
hf = ax.plot(times, T_obs, 'g')
ax.legend((h1,), (u'p < %s' % p_thresh,), loc='upper right', ncol=1)
ax.set(xlabel="time (ms)", ylabel="T-values",
       ylim=[-10., 10.], xlim=contrast.times[[0, -1]] * 1000)
fig.tight_layout(pad=0.5)
fig.savefig(op.join('..', 'figures', 'sensorstat_highpass-%sHz.pdf'
                    % (l_freq,)), bbox_to_inches='tight')
plt.show()
