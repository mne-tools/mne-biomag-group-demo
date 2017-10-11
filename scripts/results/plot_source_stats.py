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
from mne import spatial_src_connectivity
from mne.stats import (spatio_temporal_cluster_1samp_test,
                       summarize_clusters_stc, ttest_1samp_no_p)

from library.config import meg_dir, subjects_dir, fsaverage_vertices

exclude = [1, 5, 16]  # Excluded subjects
contrasts = list()
for subject_id in range(1, 20):
    if subject_id in exclude:
        continue
    subject = "sub%03d" % subject_id
    print("processing subject: %s" % subject)
    data_path = op.join(meg_dir, subject)
    contrast = mne.read_source_estimate(op.join(data_path, 'contrast-morphed'))
    contrast.crop(0., None)
    contrast.bin(1. / 100.)  # simple way to get to 160 Hz sample rate
    assert contrast.tstep == 0.01
    contrasts.append(contrast.data.T)

X = np.array(contrasts)
assert X.min() >= 0  # these already have the absolute value taken during inv

fsaverage_src = mne.read_source_spaces(op.join(subjects_dir, 'fsaverage',
                                               'fsaverage-ico-5-src.fif'))
connectivity = spatial_src_connectivity(fsaverage_src)
p_threshold = 0.001
t_threshold = -stats.distributions.t.ppf(p_threshold / 2., len(contrasts) - 1)

stat_fun = partial(ttest_1samp_no_p, sigma=0.01)
T_obs, clusters, cluster_p_values, H0 = clu = \
    spatio_temporal_cluster_1samp_test(X, connectivity=connectivity, n_jobs=1,
                                       threshold=t_threshold,
                                       stat_fun=stat_fun, verbose=True)

good_cluster_inds = np.where(cluster_p_values < 0.05)[0]
tstep = contrast.tstep
stc_all_cluster_vis = summarize_clusters_stc(
    clu, tstep=tstep, vertices=fsaverage_vertices, subject='fsaverage')

brain = stc_all_cluster_vis.plot(
    hemi='split', subjects_dir=subjects_dir,
    time_label='Duration significant (ms)', views=['lat', 'med', 'ven'],
    clim=dict(lims=[0, 15, 30], kind='value'), size=(1000, 1000))
brain.save_image(op.join('figures', 'source_stats.png'))
