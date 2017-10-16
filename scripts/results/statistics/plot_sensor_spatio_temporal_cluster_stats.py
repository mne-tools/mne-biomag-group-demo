"""
=============================================
Spatio-temporal sensor-space statistics (EEG)
=============================================

Run a non-parametric spatio-temporal cluster stats on EEG sensors
on the contrast faces vs. scrambled.
"""

import os.path as op
import sys

import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable

import mne
from mne.stats import permutation_cluster_1samp_test
from mne.viz import plot_topomap

sys.path.append(op.join('..', '..', 'processing'))
from library.config import meg_dir, l_freq, exclude_subjects  # noqa: E402

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
    contrast.pick_types(meg=False, eeg=True)
    contrast.apply_baseline((-0.2, 0.0))
    contrasts.append(contrast)

contrast = mne.combine_evoked(contrasts, 'equal')

##############################################################################
# Assemble the data and run the cluster stats on channel data

data = np.array([c.data for c in contrasts])

connectivity = None
tail = 0.  # for two sided test

# set cluster threshold
p_thresh = 0.01 / (1 + (tail == 0))
n_samples = len(data)
threshold = -stats.t.ppf(p_thresh, n_samples - 1)
if np.sign(tail) < 0:
    threshold = -threshold

# Make a triangulation between EEG channels locations to
# use as connectivity for cluster level stat
connectivity = mne.channels.find_ch_connectivity(contrast.info, 'eeg')[0]

data = np.transpose(data, (0, 2, 1))  # transpose for clustering

cluster_stats = permutation_cluster_1samp_test(
    data, threshold=threshold, n_jobs=2, verbose=True, tail=1,
    connectivity=connectivity, out_type='indices',
    check_disjoint=True, step_down_p=0.05)

T_obs, clusters, p_values, _ = cluster_stats
good_cluster_inds = np.where(p_values < 0.05)[0]

print("Good clusters: %s" % good_cluster_inds)

##############################################################################
# Visualize the spatio-temporal clusters

times = contrast.times * 1e3
colors = 'r', 'steelblue'
linestyles = '-', '--'

pos = mne.find_layout(contrast.info).pos

T_obs_max = 5.
T_obs_min = -T_obs_max

# loop over significant clusters
for i_clu, clu_idx in enumerate(good_cluster_inds):

    # unpack cluster information, get unique indices
    time_inds, space_inds = np.squeeze(clusters[clu_idx])
    ch_inds = np.unique(space_inds)
    time_inds = np.unique(time_inds)

    # get topography for T0 stat
    T_obs_map = T_obs[time_inds, ...].mean(axis=0)

    # get signals at significant sensors
    signals = data[..., ch_inds].mean(axis=-1)
    sig_times = times[time_inds]

    # create spatial mask
    mask = np.zeros((T_obs_map.shape[0], 1), dtype=bool)
    mask[ch_inds, :] = True

    # initialize figure
    fig, ax_topo = plt.subplots(1, 1, figsize=(10, 3))
    title = 'Cluster #{0}'.format(i_clu + 1)
    fig.suptitle(title, fontsize=14)

    # plot average test statistic and mark significant sensors
    image, _ = plot_topomap(T_obs_map, pos, mask=mask, axes=ax_topo,
                            vmin=T_obs_min, vmax=T_obs_max,
                            show=False)

    # advanced matplotlib for showing image with figure and colorbar
    # in one plot
    divider = make_axes_locatable(ax_topo)

    # add axes for colorbar
    ax_colorbar = divider.append_axes('right', size='5%', pad=0.05)
    plt.colorbar(image, cax=ax_colorbar, format='%0.1f')
    ax_topo.set_xlabel('Averaged t-map ({:0.1f} - {:0.1f} ms)'.format(
        *sig_times[[0, -1]]
    ))

    # add new axis for time courses and plot time courses
    ax_signals = divider.append_axes('right', size='300%', pad=1.2)
    for signal, name, col, ls in zip(signals, ['Contrast'], colors,
                                     linestyles):
        ax_signals.plot(times, signal * 1e6, color=col,
                        linestyle=ls, label=name)

    # add information
    ax_signals.axvline(0, color='k', linestyle=':', label='stimulus onset')
    ax_signals.set_xlim([times[0], times[-1]])
    ax_signals.set_xlabel('Time [ms]')
    ax_signals.set_ylabel('Amplitude [uV]')

    # plot significant time range
    ymin, ymax = ax_signals.get_ylim()
    ax_signals.fill_betweenx((ymin, ymax), sig_times[0], sig_times[-1],
                             color='orange', alpha=0.3)
    ax_signals.legend(loc='lower right')
    ax_signals.set_ylim(ymin, ymax)

    # clean up viz
    mne.viz.tight_layout(fig=fig)
    fig.subplots_adjust(bottom=.05)
    plt.savefig(op.join('..', 'figures',
                        'spatiotemporal_stats_cluster-%02d.pdf' % i_clu))
    plt.show()
