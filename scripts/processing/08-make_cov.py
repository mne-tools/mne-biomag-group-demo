"""
Baseline covariance
===================

Covariance matrices are computed and saved.
"""

import os.path as op

import mne
from mne.parallel import parallel_func

from library.config import meg_dir, N_JOBS, l_freq


def run_covariance(subject_id, tsss=False):
    subject = "sub%03d" % subject_id
    print("Processing subject: %s%s"
          % (subject, (' (tSSS=%d)' % tsss) if tsss else ''))

    data_path = op.join(meg_dir, subject)
    if tsss:
        fname_epo = op.join(data_path, '%s-tsss_%d-epo.fif' % (subject, tsss))
        fname_cov = op.join(data_path, '%s-tsss_%d-cov.fif' % (subject, tsss))
    else:
        fname_epo = op.join(data_path, '%s_highpass-%sHz-epo.fif'
                            % (subject, l_freq))
        fname_cov = op.join(data_path, '%s_highpass-%sHz-cov.fif'
                            % (subject, l_freq))
    print('  Computing regularized covariance')
    epochs = mne.read_epochs(fname_epo, preload=True)
    cov = mne.compute_covariance(epochs, tmax=0, method='shrunk')
    cov.save(fname_cov)


parallel, run_func, _ = parallel_func(run_covariance, n_jobs=N_JOBS)
parallel(run_func(subject_id) for subject_id in range(1, 20))
parallel(run_func(3, tsss) for tsss in (10, 1))  # Maxwell filtered data
