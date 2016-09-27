"""
==============
Group analysis
==============

Run the group analysis.
"""
import os.path as op

import mne

from library.config import meg_dir, subjects_dir

evokeds = mne.read_evokeds(op.join(meg_dir, 'grand_average-ave.fif'))[:3]
# evoked_famous, evoked_scrambled, evoked_unfamiliar = evokeds[:3]

###############################################################################
# Sensor-space. See :ref:`sphx_glr_auto_scripts_09-group_average_sensors.py`
evokeds[0].plot_joint(title='Famous')
evokeds[1].plot_joint(title='Scrambled')
evokeds[2].plot_joint(title='Unfamiliar')

for evoked in evokeds:  # pick only EEG channels
    evoked.pick_types(meg=False, eeg=True)
idx = evokeds[0].ch_names.index('EEG070')
assert evokeds[1].ch_names[idx] == 'EEG0070'
assert evokeds[2].ch_names[idx] == 'EEG0070'
mapping = {'Famous': evokeds[0], 'Scrambled': evokeds[1],
           'Unfamiliar': evokeds[2]}
mne.viz.plot_compare_evokeds(mapping, [idx], title='EEG070 (No baseline)')

for evoked in evokeds:
    evoked.apply_baseline()
mne.viz.plot_compare_evokeds(mapping, [idx],
                             title='EEG070 (Baseline from -200ms to 0ms)',)

###############################################################################
# Source-space. See :ref:`sphx_glr_auto_scripts_14-group_average_source.py`
fname = op.join(meg_dir, 'contrast-average')
stc = mne.read_source_estimate(fname, subject='fsaverage')

brain = stc.plot(views=['ven'], hemi='both', subject='fsaverage',
                 subjects_dir=subjects_dir, initial_time=0.17, time_unit='s',
                 clim={'lims': [99.75, 99.88, 99.98]})
