"""
====================
13. Inverse solution
====================

Compute and apply a dSPM inverse solution for each evoked data set.
"""

import os.path as op

import mne
from mne.parallel import parallel_func
from mne.minimum_norm import (make_inverse_operator, apply_inverse,
                              write_inverse_operator)

from library.config import meg_dir, spacing, N_JOBS, l_freq


def run_inverse(subject_id):
    subject = "sub%03d" % subject_id
    print("processing subject: %s" % subject)
    data_path = op.join(meg_dir, subject)

    fname_ave = op.join(data_path,
                        '%s_highpass-%sHz-ave.fif' % (subject, l_freq))
    fname_cov = op.join(data_path,
                        '%s_highpass-%sHz-cov.fif' % (subject, l_freq))
    fname_fwd = op.join(data_path, '%s-meg-eeg-%s-fwd.fif'
                        % (subject, spacing))
    fname_inv = op.join(data_path, '%s_highpass-%sHz-meg-eeg-%s-inv.fif'
                        % (subject, l_freq, spacing))

    evokeds = mne.read_evokeds(
        fname_ave, condition=['scrambled', 'unfamiliar', 'famous',
                              'faces', 'contrast',
                              'faces_eq', 'scrambled_eq'])
    cov = mne.read_cov(fname_cov)
    forward = mne.read_forward_solution(fname_fwd)

    # This will be an MEG-only inverse because the 3-layer BEMs are not
    # reliable, so our forward only has MEG channels.
    info = evokeds[0].info
    inverse_operator = make_inverse_operator(
        info, forward, cov, loose=0.2, depth=0.8)
    write_inverse_operator(fname_inv, inverse_operator)

    # Apply inverse
    snr = 3.0
    lambda2 = 1.0 / snr ** 2

    for evoked in evokeds:
        stc = apply_inverse(evoked, inverse_operator, lambda2, "dSPM",
                            pick_ori='vector')
        stc.save(op.join(data_path, 'mne_dSPM_inverse_highpass-%sHz-%s'
                         % (l_freq, evoked.comment)))


parallel, run_func, _ = parallel_func(run_inverse, n_jobs=N_JOBS)
parallel(run_func(subject_id) for subject_id in range(1, 20))
