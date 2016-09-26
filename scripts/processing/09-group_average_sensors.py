"""
Group average on sensor level
=============================

The EEG-channel data are averaged for group averages.
"""

import os.path as op

import mne

from library.config import meg_dir

all_evokeds = list()

exclude = [1, 5, 16]  # Excluded subjects

for run in range(1, 20):
    if run in exclude:
        continue
    subject = "sub%03d" % run
    print("processing subject: %s" % subject)
    data_path = op.join(meg_dir, subject)

    evokeds = mne.read_evokeds(op.join(meg_dir, subject,
                                       '%s-ave.fif' % subject))
    for evoked in evokeds:
        evoked.pick_types(meg=False, eeg=True)  # pick only EEG channels


for idx, evokeds in enumerate(all_evokeds):
    all_evokeds[idx] = mne.combine_evoked(evokeds)

mne.evoked.write_evokeds(op.join(meg_dir, 'grand_average-ave.fif'),
                         all_evokeds)
