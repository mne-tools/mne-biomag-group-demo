"""
===========================
Plotting the analysis chain
===========================

Run the analysis.
"""

import os.path as op
import numpy as np

from mayavi import mlab
import mne

mlab.close(all=True)

def plot_stc(cond):
    fname = op.join(meg_dir, subject, 'mne_dSPM_inverse-%s' % cond)
    stc = mne.read_source_estimate(fname, subject)
    brain = stc.plot(subject=subject, subjects_dir=subjects_dir, views=['cau'],
                     hemi='both', time_viewer=False)
    del stc
    return brain

study_path = op.join(op.dirname("__file__"), '..', '..')
subjects_dir = op.join(study_path, 'subjects')
meg_dir = op.join(study_path, 'MEG')


#subject_id = os.getenv("SUBJECT_ID")
#print(subject_id)
#subject_id = 1
# Configuration

# Raw data
#fname = op.join(study_path, 'ds117', subject, 'MEG', 'run_01_raw.fif')
#raw = mne.io.Raw(fname)

#fname = op.join(meg_dir, subject, 'run_01_filt_sss_raw.fif')
#raw_filt = mne.io.Raw(fname)
subject = "sub%03d" % int({{subject_id}})

###############################################################################
# Filtering
#raw.plot_psd()
#raw_filt.plot_psd()

###############################################################################
# Evoked responses
evo_fname = op.join(meg_dir, subject, '%s-ave.fif' % subject)
evoked = mne.read_evokeds(evo_fname)

###############################################################################
# Faces
famous_evo, scrambled_evo, unfamiliar_evo, contrast_evo, faces_evo = evoked
faces_evo.plot(spatial_colors=True, gfp=True, ylim={'eeg': (-10, 10)},
               window_title='Faces %s' % subject)

###############################################################################
# Famous

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
# TFR
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
# Covariance
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
# Faces
brain = plot_stc('faces')
brain.set_data_time_index(407)

###############################################################################
# Famous
brain = plot_stc('famous')
brain.set_data_time_index(407)

###############################################################################
# Unfamiliar
brain = plot_stc('unfamiliar')
brain.set_data_time_index(407)

###############################################################################
# Scrambled
brain = plot_stc('scrambled')
brain.set_data_time_index(407)

###############################################################################
# Faces - scrambled
brain = plot_stc('contrast')
brain.set_data_time_index(407)
