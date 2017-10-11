"""
===========================================
Non-parametric statistics on one EEG sensor
===========================================

Run a non-parametric cluster stats on sensor EEG070
on the contrast faces vs. scrambled.
"""

import os.path as op
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt

import mne
from mne.stats import permutation_cluster_1samp_test

from library.config import meg_dir, l_freq, N_JOBS, set_matplotlib_defaults

exclude = [1, 5, 16]  # Excluded subjects

##############################################################################
# Read all the data

contrasts = list()

for subject_id in range(1, 20):
    if subject_id in exclude:
        continue
    subject = "sub%03d" % subject_id
    print("processing subject: %s" % subject)
    data_path = op.join(meg_dir, subject)
    contrast = mne.read_evokeds(op.join(data_path, '%s_highpass-%sHz-ave.fif'
                                        % (subject, l_freq)),
                                condition='contrast')
    contrast.pick_types(meg=False, eeg=True)
    contrast.apply_baseline((-0.2, 0.0))
    contrasts.append(contrast)

contrast = mne.combine_evoked(contrasts, 'equal')

channel = 'EEG065'
idx = contrast.ch_names.index(channel)
mne.viz.plot_compare_evokeds(contrast, [idx])

##############################################################################
# Assemble the data and run the cluster stats on channel data

data = np.array([c.data[idx] for c in contrasts])

n_permutations = 1000  # number of permutations to run

# set family-wise p-value
p_accept = 0.001

connectivity = None
tail = 0.  # for two sided test

# set cluster threshold
ppf = stats.t.ppf
p_thresh = p_accept / (1 + (tail == 0))
n_samples = len(data)
threshold = -ppf(p_thresh, n_samples - 1)
if np.sign(tail) < 0:
    threshold = -threshold

cluster_stats = permutation_cluster_1samp_test(
    data, threshold=threshold, n_jobs=N_JOBS, verbose=True, tail=tail,
    step_down_p=0.05, connectivity=connectivity,
    n_permutations=n_permutations)

T_obs, clusters, cluster_p_values, _ = cluster_stats

##############################################################################
# Visualize results

set_matplotlib_defaults(plt)

times = 1e3 * contrast.times

plt.close('all')
plt.subplot(211)
plt.title('Channel : ' + channel)
plt.plot(times, 1e6 * data.mean(axis=0), label="ERP Contrast")
plt.ylabel("EEG (uV)")
plt.ylim([-5, 2.5])
plt.legend()
plt.subplot(212)
for i_c, c in enumerate(clusters):
    c = c[0]
    if cluster_p_values[i_c] <= p_accept:
        h1 = plt.axvspan(times[c.start], times[c.stop - 1],
                         color='r', alpha=0.3)
    else:
        h0 = plt.axvspan(times[c.start], times[c.stop - 1],
                         color=(0.3, 0.3, 0.3), alpha=0.3)
hf = plt.plot(times, T_obs, 'g')
plt.legend((h0, h1),
           ('cluster p-value > %s' % p_accept,
            'cluster p-value < %s' % p_accept),
           loc='best', ncol=1, fontsize=14)
plt.xlabel("time (ms)")
plt.ylabel("T-values")
plt.ylim([-10., 10.])
plt.xlim([-200, 800])
plt.tight_layout()
plt.show()
plt.savefig('figures/sensorstat.pdf', bbox_to_inches='tight')
