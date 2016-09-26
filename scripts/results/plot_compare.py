"""
===========================
Comparison between subjects
===========================

All the subjects compared.
"""

import os.path as op
import numpy as np

import mne
from library.config import study_path

meg_dir = op.join(study_path, 'MEG')
evokeds = list()
for subject_id in range(1, 20):
    subject = "sub%03d" % subject_id
    fname_in = op.join(meg_dir, subject, '%s-ave.fif' % subject)
    evokeds.append(mne.read_evokeds(fname_in))
times = np.arange(0.1, 0.26, 0.025)

###############################################################################
# Evoked responses on EEG. :ref:`sphx_glr_auto_scripts_06-make_evoked.py`
picks = mne.pick_types(evokeds[0][0].info, meg=False, eeg=True)
for idx, evoked in enumerate(evokeds):
    for cond in range(3):
        comm = evoked[cond].comment
        evoked[cond].plot_joint(picks=picks, title='Subject %s %s' % (idx + 1,
                                                                      comm))

###############################################################################
# Topomaps
for idx, evoked in enumerate(evokeds):
    for cond in range(3):
        comm = evoked[cond].comment
        evoked[cond].plot_topomap(times=times,
                                  title='Subject %s %s' % (idx + 1, comm))
