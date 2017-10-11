"""
Forward solution
================

Calculate forward solution for MEG channels.
"""

import os.path as op
import mne

from mne.parallel import parallel_func

from library.config import (study_path, meg_dir, subjects_dir, spacing, N_JOBS,
                            mindist, l_freq)


def run_forward(subject_id):
    subject = "sub%03d" % subject_id
    print("processing subject: %s" % subject)
    data_path = op.join(meg_dir, subject)

    fname_ave = op.join(data_path,
                        '%s_highpass-%sHz-ave.fif' % (subject, l_freq))
    fname_fwd = op.join(data_path, '%s-meg-eeg-%s-fwd.fif'
                        % (subject, spacing))
    fname_trans = op.join(study_path, 'ds117', subject, 'MEG',
                          '%s-trans.fif' % subject)
    fname_src = op.join(subjects_dir, subject, 'bem', '%s-%s-src.fif'
                        % (subject, spacing))
    # Here we only use 1-layer BEM because the 3-layer is unreliable
    fname_bem = op.join(subjects_dir, subject, 'bem',
                        '%s-5120-bem-sol.fif' % subject)

    info = mne.io.read_info(fname_ave)
    # Because we use a 1-layer BEM, we do MEG only
    fwd = mne.make_forward_solution(info, fname_trans, fname_src, fname_bem,
                                    meg=True, eeg=False, mindist=mindist)
    mne.write_forward_solution(fname_fwd, fwd, overwrite=True)


parallel, run_func, _ = parallel_func(run_forward, n_jobs=N_JOBS)
parallel(run_func(subject_id) for subject_id in range(1, 20))
