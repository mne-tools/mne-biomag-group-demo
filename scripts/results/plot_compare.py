"""
===========================
Comparison between subjects
===========================

All the subjects compared.
"""

import os.path as op
import numpy as np

import mne
from library.config import meg_dir, ylim, l_freq

evokeds = list()
for subject_id in range(1, 20):
    subject = "sub%03d" % subject_id
    fname_in = op.join(meg_dir, subject,
                       '%s_highpass-%sHz-ave.fif' % (subject, l_freq))
    evokeds.append(mne.read_evokeds(fname_in))
times = np.arange(0.1, 0.26, 0.025)

###############################################################################
# Evoked responses on EEG and MEG, see
# :ref:`sphx_glr_auto_scripts_06-make_evoked.py`.

ch_type_kwargs = [dict(meg=False, eeg=True), dict(meg='grad'), dict(meg='mag')]
for ch_type_kwarg in ch_type_kwargs:
    for idx, evoked in enumerate(evokeds):
        for cond in range(3):
            picks = mne.pick_types(evoked[cond].info, **ch_type_kwarg)
            comm = evoked[cond].comment
            evoked[cond].plot_joint(picks=picks, ts_args={'ylim': ylim},
                                    title='Subject %s %s' % (idx + 1, comm))

###############################################################################
# Topomaps
for ch_type in ['eeg', 'mag', 'grad']:
    for idx, evoked in enumerate(evokeds):
        for cond in range(3):
            comm = evoked[cond].comment
            evoked[cond].plot_topomap(ch_type=ch_type, times=times,
                                      title='Subject %s %s (%s)'
                                      % (idx + 1, comm, ch_type))
