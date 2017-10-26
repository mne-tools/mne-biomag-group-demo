# -*- coding: utf-8 -*-
"""
====================
Group grand averages
====================

Grand-average group contrasts for sensor space, dSPM, and LCMV.
"""
# sphinx_gallery_thumbnail_number = 1

import os.path as op
import sys

import matplotlib.pyplot as plt

import mne

sys.path.append(op.join('..', '..', 'processing'))
from library.config import (meg_dir, subjects_dir, set_matplotlib_defaults,
                            l_freq, tmax)  # noqa: E402

evokeds = mne.read_evokeds(op.join(meg_dir,
                           'grand_average_highpass-%sHz-ave.fif' % l_freq))[:3]

###############################################################################
# Sensor-space. See :ref:`sphx_glr_auto_scripts_11-group_average_sensors.py`
# We use the same sensor EEG065 as in Wakeman et al.

idx = evokeds[0].ch_names.index('EEG065')
assert evokeds[1].ch_names[idx] == 'EEG065'
assert evokeds[2].ch_names[idx] == 'EEG065'
mapping = {'Famous': evokeds[0], 'Scrambled': evokeds[1],
           'Unfamiliar': evokeds[2]}

###############################################################################
# Let us apply baseline correction now. Here we are dealing with a single
# sensor

for evoked in evokeds:
    evoked.apply_baseline(baseline=(-100, 0))

###############################################################################
# We could have used the one-line MNE function for the comparison.

# mne.viz.plot_compare_evokeds(mapping, [idx],
#                              title='EEG065 (Baseline from -200ms to 0ms)',)

###############################################################################
# But here we prefer a slightly more involved plotting script to make a
# publication ready graph.

set_matplotlib_defaults(plt)

fig, ax = plt.subplots(1, figsize=(7, 5))
scale = 1e6
ax.plot(evoked.times * 1000, mapping['Scrambled'].data[idx] * scale,
        'r', linewidth=2, label='Scrambled')
ax.plot(evoked.times * 1000, mapping['Unfamiliar'].data[idx] * scale,
        'g', linewidth=2, label='Unfamiliar')
ax.plot(evoked.times * 1000, mapping['Famous'].data[idx] * scale, 'b',
        linewidth=2, label='Famous')
ax.grid(True)
ax.set(xlim=[-100, 1000 * tmax], xlabel='Time (in ms after stimulus onset)',
       ylim=[-12.5, 5], ylabel=u'Potential difference (μV)')
ax.axvline(700, ls='--', color='k')
ax.legend()
fig.tight_layout()
fig.savefig(op.join('..', 'figures',
                    'grand_average_highpass-%sHz.pdf' % l_freq))
plt.show()

###############################################################################
# Source-space. See :ref:`sphx_glr_auto_scripts_14-group_average_source.py`
fname = op.join(meg_dir, 'contrast-average_highpass-%sHz' % (l_freq,))
stc = mne.read_source_estimate(fname, subject='fsaverage').magnitude()
lims = (1, 3, 5) if l_freq is None else (0.5, 1.5, 2.5)
brain_dspm = stc.plot(
    views=['ven'], hemi='both', subject='fsaverage', subjects_dir=subjects_dir,
    initial_time=0.17, time_unit='s', figure=1, background='w',
    clim=dict(kind='value', lims=lims), foreground='k')
brain_dspm.save_image(op.join('..', 'figures',
                              'dspm-ave_highpass-%sHz.png' % (l_freq,)))

###############################################################################
# LCMV beamformer
fname = op.join(meg_dir, 'contrast-average-lcmv_highpass-%sHz' % (l_freq,))
stc = mne.read_source_estimate(fname, subject='fsaverage')
lims = (0.015, 0.03, 0.045) if l_freq is None else (0.01, 0.02, 0.03)
brain_lcmv = stc.plot(
    views=['ven'], hemi='both', subject='fsaverage', subjects_dir=subjects_dir,
    initial_time=0.17, time_unit='s', figure=2, background='w',
    clim=dict(kind='value', lims=lims), foreground='k')
brain_lcmv.save_image(op.join('..', 'figures',
                              'lcmv-ave_highpass-%sHz.png' % (l_freq,)))
