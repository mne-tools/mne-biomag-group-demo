"""
===================
15. LCMV beamformer
===================

Compute LCMV beamformer.
"""

import os.path as op

import mne
from mne.parallel import parallel_func
from mne.beamformer import lcmv

from library.config import meg_dir, spacing, N_JOBS, l_freq


def run_lcmv(subject_id):
    subject = "sub%03d" % subject_id
    print("processing subject: %s" % subject)
    data_path = op.join(meg_dir, subject)

    fname_epo = op.join(data_path,
                        '%s_highpass-%sHz-epo.fif' % (subject, l_freq))
    fname_ave = op.join(data_path,
                        '%s_highpass-%sHz-ave.fif' % (subject, l_freq))
    fname_cov = op.join(data_path,
                        '%s_highpass-%sHz-cov.fif' % (subject, l_freq))
    fname_fwd = op.join(data_path, '%s-meg-eeg-%s-fwd.fif'
                        % (subject, spacing))

    epochs = mne.read_epochs(fname_epo, preload=False)
    data_cov = mne.compute_covariance(
        epochs[['face', 'scrambled']], tmin=0.03, tmax=0.3, method='shrunk')
    evoked = mne.read_evokeds(fname_ave, condition='contrast')
    noise_cov = mne.read_cov(fname_cov)
    forward = mne.read_forward_solution(fname_fwd)
    forward = mne.convert_forward_solution(forward, surf_ori=True)
    stc = abs(lcmv(evoked, forward, noise_cov, data_cov, pick_ori='max-power',
                   max_ori_out='signed'))
    stc.save(op.join(data_path, 'mne_LCMV_inverse_highpass-%sHz-contrast'
                     % (l_freq,)))


parallel, run_func, _ = parallel_func(run_lcmv, n_jobs=N_JOBS)
parallel(run_func(subject_id) for subject_id in range(1, 20))
