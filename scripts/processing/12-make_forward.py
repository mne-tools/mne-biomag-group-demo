"""
Forward solution
================

Calculate forward solution for MEG channels.
"""

import os.path as op
import mne

from mne.parallel import parallel_func

from library.config import (study_path, meg_dir, subjects_dir, spacing, N_JOBS,
                            mindist)


def run_forward(subject_id):
    subject = "sub%03d" % subject_id
    print("processing subject: %s" % subject)
    data_path = op.join(meg_dir, subject)

    fname_ave = op.join(data_path, '%s-ave.fif' % subject)
    fname_fwd = op.join(data_path, '%s-meg-%s-fwd.fif' % (subject, spacing))
    fname_trans = op.join(study_path, 'ds117', subject, 'MEG',
                          '%s-trans.fif' % subject)

    src = mne.setup_source_space(subject, spacing=spacing,
                                 subjects_dir=subjects_dir,
                                 n_jobs=1, add_dist=False)

    src_fname = op.join(subjects_dir, subject, '%s-src.fif' % spacing)
    mne.write_source_spaces(src_fname, src, overwrite=True)

    bem_model = mne.make_bem_model(subject, ico=4, subjects_dir=subjects_dir,
                                   conductivity=(0.3,))
    bem = mne.make_bem_solution(bem_model)
    info = mne.read_evokeds(fname_ave, condition=0).info
    fwd = mne.make_forward_solution(info, trans=fname_trans, src=src, bem=bem,
                                    meg=True, eeg=False, mindist=mindist,
                                    n_jobs=1)
    fwd = mne.convert_forward_solution(fwd, surf_ori=True)
    mne.write_forward_solution(fname_fwd, fwd, overwrite=True)


parallel, run_func, _ = parallel_func(run_forward, n_jobs=N_JOBS)
parallel(run_func(subject_id) for subject_id in range(1, 20))
