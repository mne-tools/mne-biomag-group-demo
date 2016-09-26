"""
Sensor level statistics
=======================

Compute statistics on the sensors
"""

import os.path as op
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable

import mne
from mne.stats import permutation_cluster_1samp_test
from mne.channels import read_ch_connectivity
from mne.viz import plot_topomap

from library.config import meg_dir

fsave_vertices = [np.arange(10242), np.arange(10242)]
contrast_data = list()
for subject_id in range(1, 20):
    subject = "sub%03d" % subject_id
    print("processing subject: %s" % subject)
    data_path = op.join(meg_dir, subject)
    evoked = mne.read_evokeds(op.join(data_path, '%s-ave.fif' % subject))
    contrast = evoked[3]
    contrast.pick_types(meg='mag')
    contrast.apply_baseline((-0.2, 0.0))
    contrast_data.append(contrast.data.T)
contrast_data = np.array(contrast_data)
# set cluster threshold
threshold = 5.0
# set family-wise p-value
p_accept = 0.01

connectivity, ch_names = read_ch_connectivity('neuromag306mag')

cluster_stats = permutation_cluster_1samp_test(
    contrast_data, threshold=threshold, n_jobs=2, verbose=True, tail=1,
    step_down_p=0.05, connectivity=connectivity, out_type='indices',
    check_disjoint=True)

T_obs, clusters, p_values, _ = cluster_stats
good_cluster_inds = np.where(p_values < p_accept)[0]

print("Good clusters: %s" % good_cluster_inds)

times = contrast.times * 1e3
colors = 'r', 'steelblue'
linestyles = '-', '--'

pos = mne.find_layout(contrast.info).pos

# loop over significant clusters
for i_clu, clu_idx in enumerate(good_cluster_inds):
    # unpack cluster information, get unique indices
    time_inds, space_inds = np.squeeze(clusters[clu_idx])
    ch_inds = np.unique(space_inds)
    time_inds = np.unique(time_inds)

    # get topography for F stat
    f_map = T_obs[time_inds, ...].mean(axis=0)

    # get signals at significant sensors
    signals = contrast_data[..., ch_inds].mean(axis=-1)
    sig_times = times[time_inds]

    # create spatial mask
    mask = np.zeros((f_map.shape[0], 1), dtype=bool)
    mask[ch_inds, :] = True

    # initialize figure
    fig, ax_topo = plt.subplots(1, 1, figsize=(10, 3))
    title = 'Cluster #{0}'.format(i_clu + 1)
    fig.suptitle(title, fontsize=14)

    # plot average test statistic and mark significant sensors
    image, _ = plot_topomap(f_map, pos, mask=mask, axes=ax_topo,
                            cmap='Reds', vmin=np.min, vmax=np.max,
                            show=False)

    # advanced matplotlib for showing image with figure and colorbar
    # in one plot
    divider = make_axes_locatable(ax_topo)

    # add axes for colorbar
    ax_colorbar = divider.append_axes('right', size='5%', pad=0.05)
    plt.colorbar(image, cax=ax_colorbar)
    ax_topo.set_xlabel('Averaged F-map ({:0.1f} - {:0.1f} ms)'.format(
        *sig_times[[0, -1]]
    ))

    # add new axis for time courses and plot time courses
    ax_signals = divider.append_axes('right', size='300%', pad=1.2)
    for signal, name, col, ls in zip(signals, ['Contrast'], colors,
                                     linestyles):
        ax_signals.plot(times, signal, color=col, linestyle=ls, label=name)

    # add information
    ax_signals.axvline(0, color='k', linestyle=':', label='stimulus onset')
    ax_signals.set_xlim([times[0], times[-1]])
    ax_signals.set_xlabel('time [ms]')
    ax_signals.set_ylabel('evoked magnetic fields [fT]')

    # plot significant time range
    ymin, ymax = ax_signals.get_ylim()
    ax_signals.fill_betweenx((ymin, ymax), sig_times[0], sig_times[-1],
                             color='orange', alpha=0.3)
    ax_signals.legend(loc='lower right')
    ax_signals.set_ylim(ymin, ymax)

    # clean up viz
    mne.viz.tight_layout(fig=fig)
    fig.subplots_adjust(bottom=.05)
    plt.show()
