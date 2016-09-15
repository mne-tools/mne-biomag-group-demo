"""
Blabla
======================

blabla
"""

import os.path as op
import numpy as np

import mne
from mne.parallel import parallel_func

from config import study_path, meg_dir, N_JOBS

freqs = np.arange(6, 40)
n_cycles = freqs / 2.

def run_time_frequency(subject_id):
    print("processing subject: %s" % subject_id)
    subject = "sub%03d" % subject_id
    data_path = op.join(meg_dir, subject)
    epochs = mne.read_epochs(op.join(data_path, '%s-epo.fif' % subject))
    #evokeds = mne.read_evokeds(op.join(data_path, '%s-ave.fif' % subject))
    #faces = evokeds[-1]
    faces = mne.concatenate_epochs([epochs['famous'], epochs['unfamiliar']])
    idx = [faces.ch_names.index('EEG070')]
    power_faces, itc_faces = mne.time_frequency.tfr_morlet(
        faces, freqs=freqs, return_itc=True, n_cycles=n_cycles, picks=idx)
    power_scrambled, itc_scrambled = mne.time_frequency.tfr_morlet(
        epochs['scrambled'], freqs=freqs, return_itc=True, n_cycles=n_cycles,
        picks=idx)
    #power = mne.time_frequency.tfr_morlet(faces, freqs=freqs, return_itc=False,
    #                                      n_cycles=n_cycles)
    power_faces.save(op.join(data_path, '%s-faces-tfr.h5' % subject),
                     overwrite=True)
    itc_faces.save(op.join(data_path, '%s-itc_faces-tfr.h5' % subject),
                   overwrite=True)
    power_scrambled.save(op.join(data_path, '%s-scrambled-tfr.h5' % subject),
                         overwrite=True)
    itc_scrambled.save(op.join(data_path, '%s-itc_scrambled-tfr.h5' % subject),
                         overwrite=True)

    #power, itc = mne.time_frequency.tfr_morlet(epochs['famous'], freqs=freqs,
    #                                           return_itc=True,
    #                                           n_cycles=n_cycles)
    #power.plot_topo()
    #mne.time_frequency.tfr_multitaper()

parallel, run_func, _ = parallel_func(run_time_frequency, n_jobs=N_JOBS)
parallel(run_func(subject_id) for subject_id in range(1, 20))