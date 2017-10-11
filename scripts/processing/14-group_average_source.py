"""
Group average on source level
=============================

Source estimates are computed for contrast between faces and scrambled and
morphed to average brain,
"""

import os.path as op
import numpy as np

import mne
from mne.parallel import parallel_func
from mne.minimum_norm import apply_inverse, read_inverse_operator

from library.config import (meg_dir, subjects_dir, spacing, l_freq, N_JOBS,
                            exclude_subjects, smooth, fsaverage_vertices)


def morph_stc(subject_id):
    subject = "sub%03d" % subject_id
    print("processing subject: %s" % subject)
    data_path = op.join(meg_dir, subject)

    evokeds = mne.read_evokeds(op.join(
        meg_dir, subject, '%s_highpass-%sHz-ave.fif' % (subject, l_freq)))

    contrast = evokeds[3]
    fname_inv = op.join(data_path, '%s-meg-eeg-%s-inv.fif'
                        % (subject, spacing))
    inv = read_inverse_operator(fname_inv)

    # Apply inverse
    snr = 3.0
    lambda2 = 1.0 / snr ** 2
    stc = apply_inverse(contrast, inv, lambda2, "dSPM", pick_ori='vector')
    morph_mat = mne.compute_morph_matrix(
        subject, 'fsaverage', stc.vertices, fsaverage_vertices, smooth,
        subjects_dir=subjects_dir, warn=False)
    morphed = stc.morph_precomputed('fsaverage', fsaverage_vertices, morph_mat)
    return morphed


parallel, run_func, _ = parallel_func(morph_stc, n_jobs=N_JOBS)
stcs = parallel(run_func(subject_id) for subject_id in range(1, 20)
                if subject_id not in exclude_subjects)
data = np.average([s.data for s in stcs], axis=0)
stc = mne.VectorSourceEstimate(data, stcs[0].vertices,
                               stcs[0].tmin, stcs[0].tstep, stcs[0].subject)
stc.save(op.join(meg_dir, 'contrast-average'))
