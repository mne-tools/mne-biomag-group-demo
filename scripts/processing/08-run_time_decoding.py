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

import mne
from mne.parallel import parallel_func

from library.config import meg_dir, N_JOBS

###############################################################################
# Then we write a function to do time decoding on one subject


def run_time_decoding(subject_id, condition1, condition2):
    print("processing subject: %s" % subject_id)

    subject = "sub%03d" % subject_id
    data_path = os.path.join(meg_dir, subject)
    epochs = mne.read_epochs(os.path.join(data_path,
                             '%s_highpass-1Hz-epo.fif' % subject))

    # We define the epochs and the labels
    n_cond1 = len(epochs[condition1])
    n_cond2 = len(epochs[condition2])
    y = np.r_[np.ones((n_cond1, )), np.zeros((n_cond2, ))]
    epochs = mne.concatenate_epochs([epochs[condition1],
                                    epochs[condition2]])
    epochs.apply_baseline()

    # Let us restrict ourselves to the occipital channels
    from mne.selection import read_selection
    ch_names = [ch_name.replace(' ', '') for ch_name
                in read_selection('occipital')]
    epochs.pick_types(meg='mag').pick_channels(ch_names)

    # Now we fit and plot the time decoder
    from mne.decoding import TimeDecoding

    times = dict(step=0.005)  # fit a classifier only every 5 ms
    # Use AUC because chance level is same regardless of the class balance
    td = TimeDecoding(predict_mode='cross-validation',
                      times=times, scorer='roc_auc')
    td.fit(epochs, y)

    # let's save the scores now
    a_vs_b = '%s_vs_%s' % (os.path.basename(condition1),
                           os.path.basename(condition2))
    fname_td = os.path.join(data_path, '%s-td-auc-%s.mat'
                            % (subject, a_vs_b))
    from scipy.io import savemat
    savemat(fname_td, {'scores': td.score(epochs),
                       'times': td.times_['times']})


###############################################################################
# Finally we make this script parallel across subjects and write the results
#
# .. warning::
#    This may take a large amount of memory because the epochs will be
#    replicated for each parallel job

parallel, run_func, _ = parallel_func(run_time_decoding, n_jobs=N_JOBS)
parallel(run_func(subject_id, 'face', 'scrambled')
         for subject_id in range(1, 20))
parallel(run_func(subject_id, 'face/famous', 'face/unfamiliar')
         for subject_id in range(1, 20))
