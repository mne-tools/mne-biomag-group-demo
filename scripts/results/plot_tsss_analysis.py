"""
===========================================================
Analysis for subject 1 with maxwell filtered data with tSSS
===========================================================

Run the analysis.
"""

import os
import os.path as op
import numpy as np

import mne

from library.config import study_path, meg_dir, ylim

###############################################################################
# Configuration

subjects_dir = os.path.join(study_path, 'subjects')

subject = "sub%03d" % int(1)

fname = op.join(study_path, 'ds117', subject, 'MEG', 'run_01_raw.fif')
raw = mne.io.read_raw_fif(fname)

fname = op.join(meg_dir, subject, 'run_01_filt_sss_raw.fif')
raw_filt = mne.io.read_raw_fif(fname)

###############################################################################
# Filtering :ref:`sphx_glr_auto_scripts_02-python_filtering.py`.
raw.plot_psd()
raw_filt.plot_psd()

###############################################################################
# Events :ref:`sphx_glr_auto_scripts_03-run_extract_events.py`.
# Epochs :ref:`sphx_glr_auto_scripts_05-make_epochs.py`.
events = mne.read_events(op.join(meg_dir, subject, 'run_01_filt_sss-eve.fif'))
fig = mne.viz.plot_events(events, show=False)
fig.suptitle('Events from run 01')

epochs = mne.read_epochs(op.join(meg_dir, subject, subject + '-epo.fif'))
epochs.plot_drop_log()

###############################################################################
# Evoked responses :ref:`sphx_glr_auto_scripts_06-make_evoked.py`
evo_fname = op.join(meg_dir, subject, '%s-ave.fif' % subject)
evoked = mne.read_evokeds(evo_fname)

###############################################################################
# Faces
famous_evo, scrambled_evo, unfamiliar_evo, contrast_evo, faces_evo = evoked
faces_evo.plot(spatial_colors=True, gfp=True, ylim=ylim,
               window_title='Faces %s' % subject)

###############################################################################
# Famous
famous_evo.plot(spatial_colors=True, gfp=True, ylim=ylim,
                window_title='Famous %s' % subject)

###############################################################################
# Scrambled
scrambled_evo.plot(spatial_colors=True, gfp=True, ylim=ylim,
                   window_title='Scrambled %s' % subject)

###############################################################################
# Unfamiliar
unfamiliar_evo.plot(spatial_colors=True, gfp=True, ylim=ylim,
                    window_title='Unfamiliar %s' % subject)

###############################################################################
# Faces - scrambled
contrast_evo.plot(spatial_colors=True, gfp=True, ylim=ylim,
                  window_title='Faces - scrambled %s' % subject)

###############################################################################
# Topomaps
times = np.arange(0.05, 0.3, 0.025)
famous_evo.plot_topomap(times=times, title='Famous %s' % subject)
scrambled_evo.plot_topomap(times=times, title='Scrambled %s' % subject)
unfamiliar_evo.plot_topomap(times=times, title='Unfamiliar %s' % subject)
contrast_evo.plot_topomap(times=times, title='Faces - scrambled %s' % subject)

###############################################################################
# Covariance :ref:`sphx_glr_auto_scripts_06-make_evoked.py`.
cov = mne.read_cov(op.join(meg_dir, subject, '%s-cov.fif' % subject))
mne.viz.plot_cov(cov, faces_evo.info)
faces_evo.plot_white(cov)
