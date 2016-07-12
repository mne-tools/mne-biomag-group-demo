"""
===========================
Plotting the analysis chain
===========================

Run the analysis.
"""

import os.path as op
import numpy as np

import mne

study_path = op.join(op.dirname("__file__"), '..', '..')
subjects_dir = op.join(study_path, 'subjects')
meg_dir = op.join(study_path, 'MEG')

# Configuration
subject = 'sub015'
# Raw data
fname = op.join(study_path, 'ds117', subject, 'MEG', 'run_01_raw.fif')
raw = mne.io.Raw(fname)

fname = op.join(meg_dir, subject, 'run_01_filt_sss_raw.fif')
raw_filt = mne.io.Raw(fname)

def plot_stc(cond):
    fname = op.join(meg_dir, subject, 'mne_dSPM_inverse-%s' % cond)
    stc = mne.read_source_estimate(fname, subject)
    brain = stc.plot(subject=subject, subjects_dir=subjects_dir, views=['ven'],
                     hemi='both')
    brain.set_data_time_index(135)

###############################################################################
# Filtering
raw.plot_psd()
raw_filt.plot_psd()

###############################################################################
# Evoked responses
evo_fname = op.join(meg_dir, subject, '%s-ave.fif' % subject)
evoked = mne.read_evokeds(evo_fname)

###############################################################################
# Faces
faces = mne.combine_evoked([evoked[0], evoked[2]])
faces.plot(spatial_colors=True, gfp=True, window_title='Faces %s' % subject)

###############################################################################
# Famous
famous_evo, scrambled_evo, unfamiliar_evo, contrast_evo = evoked
famous_evo.plot(spatial_colors=True, gfp=True,
                window_title='Famous %s' % subject)

###############################################################################
# Scrambled
scrambled_evo.plot(spatial_colors=True, gfp=True,
                   window_title='Scrambled %s' % subject)

###############################################################################
# Unfamiliar
unfamiliar_evo.plot(spatial_colors=True, gfp=True,
                    window_title='Unfamiliar %s' % subject)

###############################################################################
# Faces - scrambled
contrast_evo.plot(spatial_colors=True, gfp=True,
                  window_title='Faces - scrambled %s' % subject)

###############################################################################
# Topomaps
times = np.arange(0.05, 0.3, 0.05)
famous_evo.plot_topomap(times=times, title='Famous %s' % subject)
scrambled_evo.plot_topomap(times=times, title='Scrambled %s' % subject)
unfamiliar_evo.plot_topomap(times=times, title='Unfamiliar %s' % subject)
contrast_evo.plot_topomap(times=times, title='Faces - scrambled %s' % subject)

###############################################################################
# Trans
fname_trans = op.join(study_path, 'ds117', subject, 'MEG',
                      '%s-trans.fif' % subject)
mne.viz.plot_trans(raw.info, fname_trans, subject=subject,
                   subjects_dir=subjects_dir, meg_sensors=True,
                   eeg_sensors=True)

###############################################################################
# Famous
plot_stc('famous')

###############################################################################
# Unfamiliar
plot_stc('unfamiliar')

###############################################################################
# Scrambled
plot_stc('scrambled')

###############################################################################
# Famous - scrambled
plot_stc('famous - scrambled')

###############################################################################
# Unfamiliar - scrambled
plot_stc('unfamiliar - scrambled')

###############################################################################
# Famous - unfamiliar
plot_stc('famous - unfamiliar')
