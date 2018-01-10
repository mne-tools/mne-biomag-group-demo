"""
=================================
14. Group average on source level
=================================

Source estimates are morphed to the ``fsaverage`` brain.
"""

import os.path as op

import numpy as np

import mne
from mne.parallel import parallel_func

from library.config import (meg_dir, subjects_dir, N_JOBS, smooth,
                            fsaverage_vertices, exclude_subjects, l_freq)


def morph_stc(subject_id):
    subject = "sub%03d" % subject_id
    print("processing subject: %s" % subject)
    data_path = op.join(meg_dir, subject)

    # Morph STCs
    morph_mat = None
    for condition in ('contrast', 'faces_eq', 'scrambled_eq'):
        stc = mne.read_source_estimate(
            op.join(data_path, 'mne_dSPM_inverse_highpass-%sHz-%s'
                    % (l_freq, condition)), subject)
        if morph_mat is None:
            morph_mat = mne.compute_morph_matrix(
                subject, 'fsaverage', stc.vertices, fsaverage_vertices, smooth,
                subjects_dir=subjects_dir, warn=False)
        morphed = stc.morph_precomputed('fsaverage', fsaverage_vertices,
                                        morph_mat)
        morphed.save(op.join(data_path,
                             'mne_dSPM_inverse_morph_highpass-%sHz-%s'
                             % (l_freq, condition)))
        if condition == 'contrast':
            out = morphed
    return out


parallel, run_func, _ = parallel_func(morph_stc, n_jobs=N_JOBS)
stcs = parallel(run_func(subject_id) for subject_id in range(1, 20))
stcs = [stc for stc, subject_id in zip(stcs, range(1, 20))
        if subject_id not in exclude_subjects]
data = np.average([s.data for s in stcs], axis=0)
stc = mne.VectorSourceEstimate(data, stcs[0].vertices,
                               stcs[0].tmin, stcs[0].tstep, stcs[0].subject)
stc.save(op.join(meg_dir, 'contrast-average_highpass-%sHz' % l_freq))
