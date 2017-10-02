"""
=====================
Source space clusters
=====================

Clustering in source space.
"""
import os.path as op
import numpy as np
from scipy import stats
from functools import partial

import mne
from mne import spatial_tris_connectivity, grade_to_tris
from mne.stats import (spatio_temporal_cluster_1samp_test,
                       summarize_clusters_stc, ttest_1samp_no_p)

from library.config import meg_dir, subjects_dir

exclude = [1, 5, 16]  # Excluded subjects
contrasts = list()
for subject_id in range(1, 20):
    if subject_id in exclude:
        continue
    subject = "sub%03d" % subject_id
    print("processing subject: %s" % subject)
    data_path = op.join(meg_dir, subject)
    contrast = mne.read_source_estimate(op.join(data_path, 'contrast-morphed'))
    contrast.resample(100)
    contrast.crop(0., None)
    contrasts.append(contrast.data.T)

X = np.abs(np.array(contrasts))

connectivity = spatial_tris_connectivity(grade_to_tris(4))
p_threshold = 0.001
t_threshold = -stats.distributions.t.ppf(p_threshold / 2., 15)

stat_fun = partial(ttest_1samp_no_p, sigma=0.5)
T_obs, clusters, cluster_p_values, H0 = clu = \
    spatio_temporal_cluster_1samp_test(X, connectivity=connectivity, n_jobs=1,
                                       threshold=t_threshold,
                                       stat_fun=stat_fun, verbose=True)

good_cluster_inds = np.where(cluster_p_values < p_threshold)[0]
tstep = contrast.tstep
fsave_vertices = [np.arange(2562), np.arange(2562)]
stc_all_cluster_vis = summarize_clusters_stc(clu, tstep=tstep,
                                             vertices=fsave_vertices,
                                             subject='fsaverage')

brain = stc_all_cluster_vis.plot(hemi='both', subjects_dir=subjects_dir,
                                 time_label='Duration significant (ms)',
                                 views='ven',
                                 clim=dict(lims=[0, 15, 30], kind='value'))
