"""
Group average on LCMV beamformer
================================

Source estimates are computed for contrast between faces and scrambled and
morphed to average brain,
"""

import os.path as op
import numpy as np

import mne

from library.config import subjects_dir, meg_dir, N_JOBS
stcs = list()
exclude = [1, 5, 16]  # Excluded subjects

for run in range(1, 20):
    if run in exclude:
        continue
    subject = "sub%03d" % run
    print("processing subject: %s" % subject)
    data_path = op.join(meg_dir, subject)

    stc = mne.read_source_estimate(op.join(data_path,
                                           'mne_LCMV_inverse-contrast'))
    morphed = stc.morph(subject_from=subject, subject_to='fsaverage',
                        subjects_dir=subjects_dir, grade=4, n_jobs=N_JOBS,
                        verbose=True)
    stcs.append(morphed)

data = np.average([s.data for s in stcs], axis=0)
stc = mne.SourceEstimate(data, stcs[0].vertices, stcs[0].tmin, stcs[0].tstep)
stc.save(op.join(meg_dir, 'contrast-average-lcmv'))
