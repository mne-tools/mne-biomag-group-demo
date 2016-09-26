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

import os
import numpy as np
import matplotlib.pyplot as plt
from scipy.io import loadmat
from scipy.stats import sem

from library.config import meg_dir

###############################################################################
# Now we loop over subjects to load the scores
a_vs_bs = ['famous_vs_scrambled', 'famous_vs_unfamiliar']
scores = {'famous_vs_scrambled': list(), 'famous_vs_unfamiliar': list()}
for subject_id in range(1, 20):
    subject = "sub%03d" % subject_id
    data_path = os.path.join(meg_dir, subject)

    # Load the scores for the subject
    for a_vs_b in a_vs_bs:
        fname_td = os.path.join(data_path, '%s-td-auc-%s.mat'
                                % (subject, a_vs_b))
        mat = loadmat(fname_td)
        scores[a_vs_b].append(mat['scores'][0])

###############################################################################
# ... and average them
times = mat['times'][0]
mean_scores, sem_scores = dict(), dict()
for a_vs_b in a_vs_bs:
    mean_scores[a_vs_b] = np.mean(scores[a_vs_b], axis=0)
    sem_scores[a_vs_b] = sem(scores[a_vs_b])

###############################################################################
# Let's plot the mean AUC score across subjects
for a_vs_b in a_vs_bs:
    plt.figure()
    plt.plot(times, mean_scores[a_vs_b], 'b')
    plt.xlabel('Time (s)')
    plt.ylabel('Area under curve (AUC)')
    plt.fill_between(times, mean_scores[a_vs_b] - sem_scores[a_vs_b],
                     mean_scores[a_vs_b] + sem_scores[a_vs_b],
                     color='b', alpha=0.2)
    plt.axhline(0.5, color='k', linestyle='--', label='Chance level')
    plt.axvline(0.0, linestyle='--')
    plt.legend()
    plt.title('Time decoding (%s)' % a_vs_b)
    plt.show()
