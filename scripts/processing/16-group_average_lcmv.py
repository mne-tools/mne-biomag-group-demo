"""
====================================
16. Group average on LCMV beamformer
====================================

Source estimates are computed for contrast between faces and scrambled and
morphed to average brain,
"""

import os.path as op
import numpy as np

import mne

from library.config import (subjects_dir, meg_dir, exclude_subjects, smooth,
                            fsaverage_vertices, l_freq)


stcs = list()
for subject_id in range(1, 20):
    if subject_id in exclude_subjects:
        continue
    subject = "sub%03d" % subject_id
    print("processing subject: %s" % subject)
    data_path = op.join(meg_dir, subject)

    stc = mne.read_source_estimate(
        op.join(data_path, 'mne_LCMV_inverse_highpass-%sHz-contrast' % l_freq),
        subject)
    morph_mat = mne.compute_morph_matrix(
        subject, 'fsaverage', stc.vertices, fsaverage_vertices, smooth,
        subjects_dir=subjects_dir, warn=False)
    morphed = stc.morph_precomputed('fsaverage', fsaverage_vertices, morph_mat)
    stcs.append(morphed)

data = np.average([s.data for s in stcs], axis=0)
stc = mne.SourceEstimate(data, stcs[0].vertices, stcs[0].tmin, stcs[0].tstep)
stc.save(op.join(meg_dir, 'contrast-average-lcmv_highpass-%sHz' % l_freq))
