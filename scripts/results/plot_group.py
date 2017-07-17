"""
==============
Group analysis
==============

Run the group analysis.
"""
import os.path as op

import matplotlib.pyplot as plt
import mne

from library.config import (meg_dir, subjects_dir, set_matplotlib_defaults,
                            l_freq)

evokeds = mne.read_evokeds(op.join(meg_dir,
                           'grand_average_highpass-%sHz-ave.fif' % l_freq))[:3]

###############################################################################
# Sensor-space. See :ref:`sphx_glr_auto_scripts_09-group_average_sensors.py`
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

scale = 1e6
plt.figure(figsize=(7, 5))
plt.plot(evoked.times * 1000, mapping['Scrambled'].data[idx] * scale,
         'r', linewidth=2, label='Scrambled')
plt.plot(evoked.times * 1000, mapping['Unfamiliar'].data[idx] * scale,
         'g', linewidth=2, label='Unfamiliar')
plt.plot(evoked.times * 1000, mapping['Famous'].data[idx] * scale, 'b',
         linewidth=2, label='Famous')
plt.grid(True)
plt.xlim([-100, 800])
ax = plt.gca()
plt.xlabel('Time (in ms after stimulus onset)')
plt.ylabel(r'Potential difference ($\mu$V)')
plt.legend()
plt.tight_layout()
plt.show()
plt.savefig('grand_average_highpass-%sHz.pdf' % l_freq)

###############################################################################
# Source-space. See :ref:`sphx_glr_auto_scripts_14-group_average_source.py`
fname = op.join(meg_dir, 'contrast-average')
stc = mne.read_source_estimate(fname, subject='fsaverage')

brain = stc.plot(views=['ven'], hemi='both', subject='fsaverage',
                 subjects_dir=subjects_dir, initial_time=0.17, time_unit='s',
                 clim={'lims': [99.75, 99.88, 99.98]})

###############################################################################
# LCMV beamformer
fname = op.join(meg_dir, 'contrast-average-lcmv')
stc = mne.read_source_estimate(fname, subject='fsaverage')

brain = stc.plot(views=['ven'], hemi='both', subject='fsaverage',
                 subjects_dir=subjects_dir, initial_time=0.17, time_unit='s',
                 clim={'lims': [99.75, 99.88, 99.98]})
