"""
===========================
Comparison between subjects
===========================

All the subjects compared.
"""

import os.path as op

import mne

evokeds = list()
for subject_id in range(1, 20):
    subject = "sub%03d" % subject_id
    fname_in = op.join('../..', 'MEG', subject, '%s-ave.fif' % subject)
    evokeds.append(mne.read_evokeds(fname_in))

###############################################################################
# Evoked responses on EEG.
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
        evoked[cond].plot_topomap(title='Subject %s %s' % (idx + 1, comm))
