"""
Group average on sensor level
=============================

The EEG-channel data are averaged for group averages.
"""

import os.path as op

import mne

from library.config import meg_dir

famous = list()
unfamiliar = list()
scrambled = list()
exclude = [1, 5, 16]  # Excluded subjects

for run in range(1, 20):
    if run in exclude:
        continue
    subject = "sub%03d" % run
    print("processing subject: %s" % subject)
    data_path = op.join(meg_dir, subject)

    evokeds = mne.read_evokeds(op.join(meg_dir, subject,
                                       '%s-ave.fif' % subject))
    for evoked in evokeds[:3]:
        evoked.pick_types(meg=False, eeg=True)  # pick only EEG channels
    famous.append(evokeds[0])
    scrambled.append(evokeds[1])
    unfamiliar.append(evokeds[2])


famous = mne.combine_evoked(famous)
famous.save(op.join(meg_dir, 'eeg_famous-ave.fif'))
unfamiliar = mne.combine_evoked(unfamiliar)
unfamiliar.save(op.join(meg_dir, 'eeg_unfamiliar-ave.fif'))
scrambled = mne.combine_evoked(scrambled)
scrambled.save(op.join(meg_dir, 'eeg_scrambled-ave.fif'))
