"""
=============
Time Decoding
=============

Time decoding fits a Logistic Regression model for every time point in the
epoch. In this example, we contrast the condition 'famous' against 'scrambled'
using this approach. The end result is an averaging effect across sensors.
The contrast across different sensors are combined into a single plot.
"""

###############################################################################
# Let us first import the libraries
###############################################################################

import os
import numpy as np

import mne
from mne.parallel import parallel_func

from library.config import study_path
###############################################################################
# Then we write a function to do time decoding on one subject
###############################################################################


def run_time_decoding(subject_id):
    subject = "sub%03d" % subject_id
    meg_dir = os.path.join(study_path, 'MEG')
    data_path = os.path.join(meg_dir, subject)
    epochs = mne.read_epochs(os.path.join(data_path, '%s-epo.fif' % subject))

    # We define the epochs and the labels
    n_famous = len(epochs['face/famous'])
    n_unfamiliar = len(epochs['scrambled'])
    y = np.r_[np.ones((n_famous, )), np.zeros((n_unfamiliar, ))]
    epochs = mne.concatenate_epochs([epochs['face/famous'],
                                    epochs['scrambled']])

    # Let us restrict ourselves to the occipital channels
    from mne.selection import read_selection
    ch_names = [ch_name.replace(' ', '') for ch_name
                in read_selection('occipital')]
    epochs.pick_types(meg='mag').pick_channels(ch_names)

    # Now we fit and plot the time decoder
    from mne.decoding import TimeDecoding

    times = dict(step=0.005)  # fit a classifier only ever 5 ms
    # Use AUC because chance level is same regardless of the class balance
    td = TimeDecoding(predict_mode='cross-validation',
                      times=times, scorer='roc_auc')
    td.fit(epochs, y)

    # let's save the scores now
    fname_td = os.path.join(data_path, '%s-td-auc-famous.fif' % subject)
    from scipy.io import savemat
    savemat(fname_td, {'scores': td.score(epochs),
                       'times': td.times_['times']})


###############################################################################
# Finally we make this script parallel across subjects and write the results
# Warning: This may take a large amount of memory because the epochs will be
# replicated for each parallel job
###############################################################################
parallel, run_func, _ = parallel_func(run_time_decoding, n_jobs=-1)
parallel(run_func(subject_id) for subject_id in range(1, 20))
