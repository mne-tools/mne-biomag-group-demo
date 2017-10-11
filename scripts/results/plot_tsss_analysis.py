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

subject = "sub%03d" % 3
st_duration = 10

fname = op.join(study_path, 'ds117', subject, 'MEG', 'run_01_raw.fif')
raw = mne.io.read_raw_fif(fname)

fname = op.join(meg_dir, subject, 'run_01_filt_tsss_%d_raw.fif' % st_duration)
raw_filt = mne.io.read_raw_fif(fname)

###############################################################################
# Filtering :ref:`sphx_glr_auto_scripts_02-python_filtering.py`.
raw.plot_psd(average=False, spatial_colors=True, fmax=40, show=False)
raw_filt.plot_psd(average=False, spatial_colors=True, fmax=40)

###############################################################################
# Events :ref:`sphx_glr_auto_scripts_03-run_extract_events.py`.
# Epochs :ref:`sphx_glr_auto_scripts_05-make_epochs.py`.
events = mne.read_events(op.join(meg_dir, subject, 'run_01-eve.fif'))
fig = mne.viz.plot_events(events, show=False)
fig.suptitle('Events from run 01')

epochs = mne.read_epochs(op.join(meg_dir, subject,
                                 subject + '-tsss_%d-epo.fif' % st_duration))
epochs.plot_drop_log()

###############################################################################
# Evoked responses :ref:`sphx_glr_auto_scripts_06-make_evoked.py`
evo_fname = op.join(meg_dir, subject, '%s-tsss_%d-ave.fif'
                    % (subject, st_duration))
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
famous_evo.plot_topomap(times=times, title='Famous %s' % subject,
                        show=False)
scrambled_evo.plot_topomap(times=times, title='Scrambled %s' % subject,
                           show=False)
unfamiliar_evo.plot_topomap(times=times, title='Unfamiliar %s' % subject,
                            show=False)
contrast_evo.plot_topomap(times=times, title='Faces - scrambled %s' % subject)

###############################################################################
# Covariance :ref:`sphx_glr_auto_scripts_06-make_evoked.py`.
cov = mne.read_cov(op.join(meg_dir, subject, '%s-tsss_%d-cov.fif'
                           % (subject, st_duration)))
mne.viz.plot_cov(cov, faces_evo.info)
faces_evo.plot_white(cov)
