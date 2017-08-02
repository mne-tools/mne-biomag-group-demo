"""
Inverse solution
================

Compute inverse solution for each evoked data set.
"""

import os.path as op

import mne
from mne.parallel import parallel_func
from mne.minimum_norm import (make_inverse_operator, apply_inverse,
                              write_inverse_operator)

from library.config import meg_dir, spacing, N_JOBS, l_freq


exclude = [1, 5, 16]  # Excluded subjects


def run_inverse(subject_id):
    if subject_id in exclude:
        return
    subject = "sub%03d" % subject_id
    print("processing subject: %s" % subject)
    data_path = op.join(meg_dir, subject)

    fname_ave = op.join(data_path, '%s_highpass-1Hz_ave.fif' % subject)
    fname_cov = op.join(data_path, '%s_highpass-%sHz-cov.fif' % (subject,
                                                                 l_freq))
    fname_fwd = op.join(data_path, '%s-meg-%s-fwd.fif' % (subject, spacing))
    fname_inv = op.join(data_path, '%s-meg-%s-inv.fif' % (subject, spacing))

    evokeds = mne.read_evokeds(fname_ave, condition=[0, 1, 2, 3, 4])
    cov = mne.read_cov(fname_cov)

    forward = mne.read_forward_solution(fname_fwd, surf_ori=True)

    # make an M/EEG, MEG-only, and EEG-only inverse operators
    info = evokeds[0].info
    inverse_operator = make_inverse_operator(info, forward, cov, loose=0.2,
                                             depth=0.8)

    write_inverse_operator(fname_inv, inverse_operator)

    # Compute inverse solution
    snr = 3.0
    lambda2 = 1.0 / snr ** 2

    for evoked in evokeds:
        stc = apply_inverse(evoked, inverse_operator, lambda2, "dSPM",
                            pick_ori=None)

        stc.save(op.join(data_path, 'mne_dSPM_inverse-%s' % evoked.comment))


parallel, run_func, _ = parallel_func(run_inverse, n_jobs=N_JOBS)
parallel(run_func(subject_id) for subject_id in range(1, 20))
