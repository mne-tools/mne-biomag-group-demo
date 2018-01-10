"""
=======================
Analysis for subject 11
=======================

Run the analysis.
"""
import os.path as op
import sys

import numpy as np
import matplotlib.pyplot as plt

import mne

sys.path.append(op.join('..', '..', 'processing'))
from library.config import (study_path, meg_dir, ylim, l_freq,
                            set_matplotlib_defaults)  # noqa: E402

set_matplotlib_defaults()

###############################################################################
# Configuration

subjects_dir = op.join(study_path, 'subjects')

subject = "sub011"
subject_dir = op.join(meg_dir, subject)

###############################################################################
# Continuous data
raw_fname = op.join(study_path, 'ds117', subject, 'MEG', 'run_01_raw.fif')
raw_filt_fname = op.join(subject_dir,
                         'run_01_filt_sss_highpass-%sHz_raw.fif' % l_freq)
raw = mne.io.read_raw_fif(raw_fname)
raw_filt = mne.io.read_raw_fif(raw_filt_fname)

###############################################################################
# Filtering :ref:`sphx_glr_auto_scripts_04-python_filtering.py`.
raw.plot_psd(n_fft=8192, average=False, xscale='log', show=False)
raw_filt.plot_psd(n_fft=8192, average=False, xscale='log')

###############################################################################
# Events :ref:`sphx_glr_auto_scripts_02-extract_events.py`.
# Epochs :ref:`sphx_glr_auto_scripts_06-make_epochs.py`.
eve_fname = op.join(subject_dir, 'run_01-eve.fif')
epo_fname = op.join(subject_dir,
                    '%s_highpass-%sHz-epo.fif' % (subject, l_freq))

events = mne.read_events(eve_fname)
fig = mne.viz.plot_events(events, show=False)
fig.suptitle('Events from run 01')

epochs = mne.read_epochs(epo_fname)
epochs.plot_drop_log()

###############################################################################
# Evoked responses :ref:`sphx_glr_auto_scripts_07-make_evoked.py`
ave_fname = op.join(subject_dir,
                    '%s_highpass-%sHz-ave.fif' % (subject, l_freq))
evoked = mne.read_evokeds(ave_fname)
famous_evo, scrambled_evo, unfamiliar_evo, contrast_evo, faces_evo = evoked[:5]

###############################################################################
# Faces
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
# ICA (ECG)
ica_fname = op.join(subject_dir, 'run_concat_highpass-%sHz-ica.fif'
                    % (l_freq,))
ica = mne.preprocessing.read_ica(ica_fname)

ecg_scores = np.load(
    op.join(subject_dir, '%s_highpass-%sHz-ecg-scores.npy'
            % (subject, l_freq)))
ica.plot_scores(ecg_scores, show=False, title='ICA ECG scores')
ecg_evoked = mne.read_evokeds(
    op.join(subject_dir, '%s_highpass-%sHz-ecg-ave.fif'
            % (subject, l_freq)))[0]
ica.plot_sources(ecg_evoked, title='ECG evoked', show=True)

###############################################################################
# ICA (EOG)
eog_scores = np.load(
    op.join(subject_dir, '%s_highpass-%sHz-eog-scores.npy'
            % (subject, l_freq)))
ica.plot_scores(eog_scores, show=False, title='ICA EOG scores')
eog_evoked = mne.read_evokeds(
    op.join(subject_dir, '%s_highpass-%sHz-eog-ave.fif'
            % (subject, l_freq)))[0]
ica.plot_sources(eog_evoked, title='EOG evoked', show=True)

###############################################################################
# Covariance :ref:`sphx_glr_auto_scripts_07-make_evoked.py`.
cov_fname = op.join(subject_dir,
                    '%s_highpass-%sHz-cov.fif' % (subject, l_freq))
cov = mne.read_cov(cov_fname)
mne.viz.plot_cov(cov, faces_evo.info)
rank_dict = dict(
    meg=raw_filt.copy().load_data().pick_types(eeg=False).estimate_rank())
for kind in ('meg', 'eeg'):
    type_dict = dict(meg=False)
    type_dict.update({kind: True})
    fig = faces_evo.copy().apply_baseline().pick_types(
        **type_dict).plot_white(cov, rank=rank_dict if kind == 'meg' else {})
    for ax, ylabel in zip(fig.axes, ('Whitened\n%s (AU)' % (kind.upper(),),
                                     'GFP ($\chi^2$)')):
        ax.set(ylabel=ylabel)
    fig.axes[-1].set(title='', ylim=[0, 20])
    fig.axes[-1].legend(loc='lower center')
    fig.set_size_inches(3.5, 3, forward=True)
    fig.tight_layout()
    fig.savefig(op.join('..', 'figures', '%s_highpass-%sHz-plot_white_%s.pdf'
                        % (subject, l_freq, kind)))

###############################################################################
# TFR :ref:`sphx_glr_auto_scripts_09-time_frequency.py`.
fpower = mne.time_frequency.read_tfrs(
    op.join(subject_dir, '%s_highpass-%sHz-faces-tfr.h5'
            % (subject, l_freq)))[0]
fitc = mne.time_frequency.read_tfrs(
    op.join(subject_dir, '%s_highpass-%sHz-itc_faces-tfr.h5'
            % (subject, l_freq)))[0]
spower = mne.time_frequency.read_tfrs(
    op.join(subject_dir, '%s_highpass-%sHz-scrambled-tfr.h5'
            % (subject, l_freq)))[0]
sitc = mne.time_frequency.read_tfrs(
    op.join(subject_dir, '%s_highpass-%sHz-itc_scrambled-tfr.h5'
            % (subject, l_freq)))[0]
channel = 'EEG065'
idx = [fpower.ch_names.index(channel)]
fpower.plot(idx, title='Faces power %s' % channel, baseline=(-0.1, 0.0),
            mode='logratio', show=False)
spower.plot(idx, title='Scrambled power %s' % channel, baseline=(-0.1, 0.0),
            mode='logratio', show=False)
fitc.plot(idx, title='Faces ITC %s' % channel, baseline=(-0.1, 0.0),
          mode='logratio', show=False)
sitc.plot(idx, title='Scrambled ITC %s' % channel, baseline=(-0.1, 0.0),
          mode='logratio')

###############################################################################
# Trans
fname_trans = op.join(study_path, 'ds117', subject, 'MEG',
                      '%s-trans.fif' % subject)
bem = mne.read_bem_surfaces(op.join(subjects_dir, subject, 'bem',
                                    '%s-5120-bem.fif' % subject))
src = mne.read_source_spaces(
    op.join(subjects_dir, subject, 'bem', '%s-oct6-src.fif' % subject))
aln = mne.viz.plot_alignment(
    raw.info, fname_trans, subject=subject, subjects_dir=subjects_dir, src=src,
    surfaces=['outer_skin', 'inner_skull'], dig=True, coord_frame='meg')
aln.scene.parallel_projection = True
fig, axes = plt.subplots(1, 3, figsize=(6.5, 2.5), facecolor='k')
from mayavi import mlab  # noqa: E402
for ai, angle in enumerate((180, 90, 0)):
    mlab.view(angle, 90, focalpoint=(0., 0., 0.), distance=0.6)
    view = mlab.screenshot()
    mask_w = (view == 0).all(axis=-1).all(axis=1)
    mask_h = (view == 0).all(axis=-1).all(axis=0)
    view = view[~mask_w][:, ~mask_h]
    axes[ai].set_axis_off()
    axes[ai].imshow(view, interpolation='bicubic')
mlab.close(aln)
fig.subplots_adjust(left=0, right=1, top=1, bottom=0, wspace=0.05, hspace=0)
fig.savefig(op.join('..', 'figures', '%s_alignment.pdf' % subject),
            dpi=150, facecolor=fig.get_facecolor(), edgecolor='none')

###############################################################################
# Faces :ref:`sphx_glr_auto_scripts_13-make_inverse.py`.


def plot_stc(cond, figure=None):
    fname = op.join(subject_dir, 'mne_dSPM_inverse_highpass-%sHz-%s'
                    % (l_freq, cond))
    stc = mne.read_source_estimate(fname, subject).magnitude()
    brain = stc.plot(subject=subject, subjects_dir=subjects_dir, views=['ven'],
                     hemi='both', initial_time=0.17, time_unit='s',
                     figure=figure)
    return brain


brain_faces = plot_stc('faces', figure=1)

###############################################################################
# Faces - scrambled
brain_contrast = plot_stc('contrast', figure=2)

###############################################################################
# LCMV Faces - scrambled
fname = op.join(subject_dir, 'mne_LCMV_inverse_highpass-%sHz-contrast'
                % (l_freq,))
stc = mne.read_source_estimate(fname, subject)
stc.plot(subject=subject, subjects_dir=subjects_dir, views=['ven'],
         hemi='both', initial_time=0.17, time_unit='s', figure=3)

###############################################################################
# BEM
fig = mne.viz.plot_bem(subject, subjects_dir, slices=[40, 100, 140, 180])
fig.savefig(op.join('..', 'figures', '%s_bem.pdf' % subject))
