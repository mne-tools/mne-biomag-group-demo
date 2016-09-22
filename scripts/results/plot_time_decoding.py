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
# Let us first import the necessary libraries
###############################################################################

import os
import numpy as np
import matplotlib.pyplot as plt
from scipy.io import loadmat
from scipy.stats import sem

from library.config import study_path

meg_dir = os.path.join(study_path, 'MEG')

###############################################################################
# Now we loop over subjects to load the scores
###############################################################################

scores = list()
for subject_id in range(1, 20):
    subject = "sub%03d" % subject_id
    data_path = os.path.join(meg_dir, subject)

    # Load the scores for the subject
    fname_td = os.path.join(data_path, '%s-td-auc-famous.fif' % subject)
    mat = loadmat(fname_td)
    scores.append(mat['scores'][0])

###############################################################################
# ... and average them
###############################################################################

mean_scores = np.mean(scores, axis=0)
sem_scores = sem(scores)
times = mat['times'][0]

###############################################################################
# Let's plot the mean AUC score across subjects
###############################################################################

plt.plot(times, mean_scores, 'b')
plt.xlabel('Time (s)')
plt.ylabel('Area under curve (AUC)')
plt.fill_between(times, mean_scores - sem_scores,
                 mean_scores + sem_scores, color='b', alpha=0.2)
plt.axhline(0.5, color='k', linestyle='--', label='Chance level')
plt.axvline(0.0, linestyle='--')
plt.legend()
plt.title('Time decoding (famous vs scrambled)')
plt.show()
