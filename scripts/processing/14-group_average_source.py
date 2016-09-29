"""
Group average on source level
=============================

Source estimates are computed for contrast between faces and scrambled and
morphed to average brain,
"""

import os.path as op
import numpy as np

import mne
from mne.minimum_norm import apply_inverse, read_inverse_operator

from library.config import meg_dir, subjects_dir, spacing

stcs = list()
exclude = [1, 5, 16]  # Excluded subjects

for run in range(1, 20):
    if run in exclude:
        continue
    subject = "sub%03d" % run
    print("processing subject: %s" % subject)
    data_path = op.join(meg_dir, subject)

    evokeds = mne.read_evokeds(op.join(meg_dir, subject,
                                       '%s-ave.fif' % subject))

    contrast = evokeds[3]
    fname_inv = op.join(data_path, '%s-meg-%s-inv.fif' % (subject, spacing))
    inv = read_inverse_operator(fname_inv)

    # Compute inverse solution
    snr = 3.0
    lambda2 = 1.0 / snr ** 2
    stc = apply_inverse(contrast, inv, lambda2, "dSPM", pick_ori=None)
    morphed = stc.morph(subject_from=subject, subject_to='fsaverage',
                        subjects_dir=subjects_dir, grade=4)
    morphed.save(op.join(data_path, 'contrast-morphed'))
    stcs.append(morphed)


data = np.average([s.data for s in stcs], axis=0)
stc = mne.SourceEstimate(data, stcs[0].vertices, stcs[0].tmin, stcs[0].tstep)
stc.save(op.join(meg_dir, 'contrast-average'))
