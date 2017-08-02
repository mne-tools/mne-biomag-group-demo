"""
LCMV beamformer
===============

Compute LCMV beamformer.
"""

import os.path as op

import mne
from mne.parallel import parallel_func
from mne.beamformer import lcmv

from library.config import meg_dir, spacing, N_JOBS, l_freq


def run_inverse(subject_id):
    subject = "sub%03d" % subject_id
    print("processing subject: %s" % subject)
    data_path = op.join(meg_dir, subject)

    fname_ave = op.join(data_path, '%s-ave.fif' % subject)
    fname_cov = op.join(data_path, '%s_highpass-%sHz-cov.fif' % (subject,
                                                                 l_freq))
    fname_fwd = op.join(data_path, '%s-meg-%s-fwd.fif' % (subject, spacing))

    epochs = mne.read_epochs(op.join(data_path, '%s-epo.fif' % subject),
                             preload=False)
    data_cov = mne.compute_covariance(epochs, tmin=0.03, tmax=0.3)
    evoked = mne.read_evokeds(fname_ave, condition=[4])[0]
    noise_cov = mne.read_cov(fname_cov)
    forward = mne.read_forward_solution(fname_fwd, surf_ori=True)

    stc = lcmv(evoked, forward, noise_cov, data_cov, reg=0.)
    stc.save(op.join(data_path, 'mne_LCMV_inverse-contrast'))


parallel, run_func, _ = parallel_func(run_inverse, n_jobs=N_JOBS)
parallel(run_func(subject_id) for subject_id in range(1, 20))
