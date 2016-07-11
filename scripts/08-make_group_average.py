import os.path as op
import numpy as np

import mne
from mne.minimum_norm import apply_inverse, read_inverse_operator

from config import meg_dir, subjects_dir, spacing

stcs = list()
contrasts = list()
fams = list()
unfams = list()
scrambs = list()
for run in range(1, 19):  # run 19 left out
    subject = "sub%03d" % run
    print("processing subject: %s" % subject)
    data_path = op.join(meg_dir, subject)

    evokeds = mne.read_evokeds(op.join(meg_dir, subject,
                                       '%s-ave.fif' % subject))
    fams.append(evokeds[0])
    scrambs.append(evokeds[1])
    unfams.append(evokeds[2])
    contrast = mne.combine_evoked(evokeds[:3], weights=[0.5, -1, 0.5])
    fname_inv = op.join(data_path, '%s-meg-%s-inv.fif' % (subject, spacing))
    inv = read_inverse_operator(fname_inv)

    # Compute inverse solution
    snr = 3.0
    lambda2 = 1.0 / snr ** 2
    stc = apply_inverse(contrast, inv, lambda2, "dSPM", pick_ori=None)
    stcs.append(stc.morph(subject_from=subject, subject_to='fsaverage',
                          subjects_dir=subjects_dir))
    contrasts.append(contrast)

data = np.average([s.data for s in stcs], axis=0)

stc = mne.SourceEstimate(data, stcs[0].vertices, stcs[0].tmin, stcs[0].tstep)
stc.save(op.join(meg_dir, 'contrast-average'))
