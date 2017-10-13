"""
==================================
Analysis for one subject with tSSS
==================================

Show analysis of tSSS data.
"""
import os.path as op
import sys

import numpy as np

import mne

sys.path.append(op.join('..', '..', 'processing'))
from library.config import study_path, meg_dir, ylim  # noqa: E402

###############################################################################
# Configuration

subjects_dir = op.join(study_path, 'subjects')

subject = "sub003"
subject_dir = op.join(meg_dir, subject)
st_duration = 1

###############################################################################
# Continuous data
raw_fname = op.join(study_path, 'ds117', subject, 'MEG', 'run_01_raw.fif')
raw_filt_fname = op.join(subject_dir,
                         'run_01_filt_tsss_%d_raw.fif' % st_duration)

raw = mne.io.read_raw_fif(raw_fname)
raw_filt = mne.io.read_raw_fif(raw_filt_fname)

###############################################################################
# Filtering :ref:`sphx_glr_auto_scripts_04-python_filtering.py`.
raw.plot_psd(n_fft=8192, average=False, xscale='log', show=False)
raw_filt.plot_psd(n_fft=8192, average=False, xscale='log')

###############################################################################
# Events :ref:`sphx_glr_auto_scripts_02-extract_events.py`.
# Epochs :ref:`sphx_glr_auto_scripts_06-make_epochs.py`.
eve_fname = op.join(subject_dir, 'run_01_filt_sss-eve.fif')
epo_fname = op.join(subject_dir, '%s-tsss_%d-epo.fif' % (subject, st_duration))

events = mne.read_events(eve_fname)
fig = mne.viz.plot_events(events, show=False)
fig.suptitle('Events from run 01')

epochs = mne.read_epochs(epo_fname)
epochs.plot_drop_log()

###############################################################################
# Evoked responses :ref:`sphx_glr_auto_scripts_07-make_evoked.py`
ave_fname = op.join(subject_dir, '%s-tsss_%d-ave.fif' % (subject, st_duration))
evoked = mne.read_evokeds(ave_fname)

###############################################################################
# Faces
famous_evo, scrambled_evo, unfamiliar_evo, contrast_evo, faces_evo = evoked[:5]
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
famous_evo.plot_topomap(times=times, title='Famous %s' % subject,
                        show=False)
scrambled_evo.plot_topomap(times=times, title='Scrambled %s' % subject,
                           show=False)
unfamiliar_evo.plot_topomap(times=times, title='Unfamiliar %s' % subject,
                            show=False)
contrast_evo.plot_topomap(times=times, title='Faces - scrambled %s' % subject,
                          show=True)

###############################################################################
# Covariance :ref:`sphx_glr_auto_scripts_07-make_evoked.py`.
cov_fname = op.join(subject_dir,
                    '%s-tsss_%d-cov.fif' % (subject, st_duration))
cov = mne.read_cov(cov_fname)
mne.viz.plot_cov(cov, faces_evo.info)
faces_evo.copy().apply_baseline().plot_white(cov)
