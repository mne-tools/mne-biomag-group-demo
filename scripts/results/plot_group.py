"""
==============
Group analysis
==============

Run the group analysis.
"""
import os.path as op

import mne

from library.config import meg_dir, subjects_dir, study_path

evokeds = mne.read_evokeds(op.join(study_path, 'MEG', 'grand_average-ave.fif'))
evoked_famous, evoked_scrambled, evoked_unfamiliar = evokeds[:3]

evokeds[0].plot_joint(title='Famous')
evokeds[1].plot_joint(title='Scrambled')
evokeds[2].plot_joint(title='Unfamiliar')

idx = evoked_famous.ch_names.index('EEG070')
mapping = {'Famous': evokeds[0], 'Scrambled': evokeds[1],
           'Unfamiliar': evokeds[2]}
mne.viz.plot_compare_evokeds(mapping, [idx], title='EEG070 (No baseline)')

for evoked in evokeds:
    evoked.apply_baseline()
mne.viz.plot_compare_evokeds(mapping, [idx],
                             title='EEG070 (Baseline from -200ms to 0ms)',)

fname = op.join(meg_dir, 'contrast-average')
stc = mne.read_source_estimate(fname, subject='fsaverage')
t_idx = stc.time_as_index(0.17)  # Plot at 170 ms
brain = stc.plot(views=['ven'], hemi='both', subject='fsaverage',
                 subjects_dir=subjects_dir, initial_time=0.17, time_unit='s')

brain.set_data_time_index(t_idx)
