"""
=============
Time Decoding
=============

Time decoding fits a Logistic Regression model for every time point in the
epoch. In this example, we contrast the condition 'famous' against 'scrambled'
using this approach. The end result is an averaging effect across sensors.
The contrast across different sensors are combined into a single plot.

Results script: :ref:`sphx_glr_auto_examples_plot_time_decoding.py`
"""

###############################################################################
# Let us first import the libraries

import os
import numpy as np
from scipy.io import savemat

import mne
from mne.decoding import TimeDecoding
from mne.selection import read_selection

from library.config import meg_dir, l_freq, N_JOBS

###############################################################################
# Then we write a function to do time decoding on one subject


def run_time_decoding(subject_id, condition1, condition2):
    print("processing subject: %s (%s vs %s)"
          % (subject_id, condition1, condition2))

    subject = "sub%03d" % subject_id
    data_path = os.path.join(meg_dir, subject)
    epochs = mne.read_epochs(os.path.join(data_path,
                             '%s_highpass-%sHz-epo.fif' % (subject, l_freq)))

    # We define the epochs and the labels
    n_cond1 = len(epochs[condition1])
    n_cond2 = len(epochs[condition2])
    y = np.r_[np.ones((n_cond1, )), np.zeros((n_cond2, ))]
    epochs = mne.concatenate_epochs([epochs[condition1],
                                    epochs[condition2]])
    epochs.apply_baseline()

    # Let us restrict ourselves to the occipital channels
    ch_names = [ch_name.replace(' ', '') for ch_name
                in read_selection('occipital')]
    epochs.pick_types(meg='mag').pick_channels(ch_names)

    # Use AUC because chance level is same regardless of the class balance
    td = TimeDecoding(predict_mode='cross-validation', scorer='roc_auc',
                      n_jobs=N_JOBS)
    td.fit(epochs, y)

    # let's save the scores now
    a_vs_b = '%s_vs_%s' % (os.path.basename(condition1),
                           os.path.basename(condition2))
    fname_td = os.path.join(data_path, '%s-td-auc-%s.mat'
                            % (subject, a_vs_b))
    savemat(fname_td, {'scores': td.score(epochs),
                       'times': td.times_['times']})


for subject_id in range(1, 20):
    for conditions in (('face', 'scrambled'),
                       ('face/famous', 'face/unfamiliar')):
        run_time_decoding(subject_id, *conditions)
