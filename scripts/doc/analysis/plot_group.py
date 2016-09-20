"""
==============
Group analysis
==============

Run the group analysis.
"""

from pyface.qt import QtCore, QtGui
import os.path as op

import mne

study_path = op.join(op.dirname("__file__"), '..', '..')
subjects_dir = op.join(study_path, 'subjects')
meg_dir = op.join(study_path, 'MEG')

faces_fname = op.join(study_path, 'MEG', 'eeg_faces-ave.fif')
faces = mne.read_evokeds(faces_fname)[0]
faces.plot_joint()

famous_fname = op.join(study_path, 'MEG', 'eeg_famous-ave.fif')
famous = mne.read_evokeds(famous_fname)[0]

unfamiliar_fname = op.join(study_path, 'MEG', 'eeg_unfamiliar-ave.fif')
unfamiliar = mne.read_evokeds(unfamiliar_fname)[0]

scrambled = mne.read_evokeds(op.join(study_path, 'MEG',
                                     'eeg_scrambled-ave.fif'))[0]
scrambled.plot_joint()

idx = faces.ch_names.index('EEG070')
mne.viz.plot_compare_evokeds({'Famous': famous, 'Unfamiliar': unfamiliar,
                              'Scrambled': scrambled}, [idx])

fname = op.join(study_path, 'MEG', 'contrast-average')
stc = mne.read_source_estimate(fname, subject='fsaverage')
brain = stc.plot(views=['cau'], hemi='both', subject='fsaverage',
                 subjects_dir=subjects_dir)
brain.set_data_time_index(407)
