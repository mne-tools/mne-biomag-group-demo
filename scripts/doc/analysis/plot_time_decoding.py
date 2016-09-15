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
import os.path as op
import mne

###############################################################################
# We analyze only one subject. Change ``meg_dir`` to point to your directory

subject_id = 1
subject = "sub%03d" % subject_id

meg_dir = '/tsi/doctorants/data_gramfort/dgw_faces/MEG/'
data_path = op.join(meg_dir, subject)
epochs = mne.read_epochs(op.join(data_path, '%s-epo.fif' % subject))

###############################################################################
# We define the labels for the epochs by pooling together all 'famous'
# and all 'scrambled' epochs
import numpy as np

n_famous, n_unfamiliar = len(epochs['famous']), len(epochs['scrambled'])
y = np.r_[np.ones((n_famous, )), np.zeros((n_unfamiliar, ))]
epochs = mne.concatenate_epochs([epochs['famous'], epochs['scrambled']])

###############################################################################
# Let us restrict ourselves to the occipital channels
from mne.selection import read_selection
ch_names = [ch_name.replace(' ', '') for ch_name
            in read_selection('occipital')]
epochs.pick_channels(ch_names)

###############################################################################
# Now we fit and plot the time decoder
from mne.decoding import TimeDecoding

times = dict(step=0.005) # fit a classifier only ever 5 ms
td = TimeDecoding(predict_mode='cross-validation', times=times)
td.fit(epochs, y)
td.score(epochs)
td.plot(title="Generalization Across Time (faces vs. scrambled)")
