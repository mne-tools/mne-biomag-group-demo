"""
======================
Analysis for subject 1
======================

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
# TFR :ref:`sphx_glr_auto_scripts_07-time_frequency.py`.
fpower = mne.time_frequency.read_tfrs(
    op.join(meg_dir, subject, '%s-faces-tfr.h5' % subject))[0]
fitc = mne.time_frequency.read_tfrs(
    op.join(meg_dir, subject, '%s-itc_faces-tfr.h5' % subject))[0]
spower = mne.time_frequency.read_tfrs(
    op.join(meg_dir, subject, '%s-scrambled-tfr.h5' % subject))[0]
sitc = mne.time_frequency.read_tfrs(
    op.join(meg_dir, subject, '%s-itc_scrambled-tfr.h5' % subject))[0]
channel = 'EEG070'
idx = [fpower.ch_names.index(channel)]
fpower.plot(idx, title='Faces power %s' % channel, baseline=(-0.1, 0.0),
            mode='logratio')
spower.plot(idx, title='Scrambled power %s' % channel, baseline=(-0.1, 0.0),
            mode='logratio')
fitc.plot(idx, title='Faces ITC %s' % channel, baseline=(-0.1, 0.0),
          mode='logratio')
sitc.plot(idx, title='Scrambled ITC %s' % channel, baseline=(-0.1, 0.0),
          mode='logratio')


###############################################################################
# Covariance :ref:`sphx_glr_auto_scripts_06-make_evoked.py`.
cov = mne.read_cov(op.join(meg_dir, subject, '%s-cov.fif' % subject))
mne.viz.plot_cov(cov, faces_evo.info)
faces_evo.plot_white(cov)

###############################################################################
# Trans
fname_trans = op.join(study_path, 'ds117', subject, 'MEG',
                      '%s-trans.fif' % subject)
mne.viz.plot_trans(famous_evo.info, fname_trans, subject=subject,
                   subjects_dir=subjects_dir, meg_sensors=True,
                   eeg_sensors=True)

###############################################################################
# Faces :ref:`sphx_glr_auto_scripts_13-make_inverse.py`.


def plot_stc(cond):
    fname = op.join(meg_dir, subject, 'mne_dSPM_inverse-%s' % cond)
    stc = mne.read_source_estimate(fname, subject)
    brain = stc.plot(subject=subject, subjects_dir=subjects_dir, views=['ven'],
                     hemi='both', initial_time=0.17, time_unit='s')
    return brain

brain = plot_stc('faces')

###############################################################################
# Faces - scrambled
brain = plot_stc('contrast')

###############################################################################
# BEM
mne.viz.plot_bem(subject, subjects_dir)
