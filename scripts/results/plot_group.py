"""
==============
Group analysis
==============

Run the group analysis.
"""
import os.path as op

import mne

from library.config import meg_dir, subjects_dir

evokeds = mne.read_evokeds(op.join(meg_dir, 'grand_average-ave.fif'))
evoked_famous, evoked_scrambled, evoked_unfamiliar = evokeds[:3]

###############################################################################
# Sensor-space. See :ref:`sphx_glr_auto_scripts_09-group_average_sensors.py`
evoked_famous.plot_joint(title='Famous')
evoked_scrambled.plot_joint(title='Scrambled')
evoked_unfamiliar.plot_joint(title='Unfamiliar')

idx = evoked_famous.ch_names.index('EEG070')
assert evoked_unfamiliar.ch_names[idx] == 'EEG0070'
assert evoked_scrambled.ch_names[idx] == 'EEG0070'
mapping = {'Famous': evoked_famous, 'Scrambled': evoked_scrambled,
           'Unfamiliar': evoked_unfamiliar}
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
