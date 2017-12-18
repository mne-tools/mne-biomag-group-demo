"""
====================
06. Construct epochs
====================

The epochs are constructed by using the events created in script 03. MNE
supports hierarchical events that allows selection to different groups more
easily. Some channels were not properly defined during acquisition, so they
are redefined before epoching. Bad EEG channels are interpolated and epochs
containing blinks are rejected. ECG artifacts are corrected using ICA. Finally
the epochs are saved to disk. To save space, the epoch data is decimated by
a factor of 5 (from a sample rate of 1100 Hz to 220 Hz).
"""

import os
import os.path as op

import numpy as np

import mne
from mne.parallel import parallel_func
from mne.preprocessing import create_ecg_epochs, create_eog_epochs, read_ica

from autoreject import get_rejection_threshold

from library.config import (meg_dir, map_subjects, l_freq, tmin, tmax,
                            reject_tmax, random_state, N_JOBS)

###############################################################################
# We define the events and the onset and offset of the epochs

events_id = {
    'face/famous/first': 5,
    'face/famous/immediate': 6,
    'face/famous/long': 7,
    'face/unfamiliar/first': 13,
    'face/unfamiliar/immediate': 14,
    'face/unfamiliar/long': 15,
    'scrambled/first': 17,
    'scrambled/immediate': 18,
    'scrambled/long': 19,
}

baseline = (None, 0) if l_freq is None else None


###############################################################################
# Now we define a function to extract epochs for one subject
def run_epochs(subject_id, tsss=False):
    subject = "sub%03d" % subject_id
    print("Processing subject: %s%s"
          % (subject, (' (tSSS=%d)' % tsss) if tsss else ''))

    data_path = op.join(meg_dir, subject)

    # map to correct subject for bad channels
    mapping = map_subjects[subject_id]

    raw_list = list()
    events_list = list()
    print("  Loading raw data")
    for run in range(1, 7):
        bads = list()
        bad_name = op.join('bads', mapping, 'run_%02d_raw_tr.fif_bad' % run)
        if os.path.exists(bad_name):
            with open(bad_name) as f:
                for line in f:
                    bads.append(line.strip())

        if tsss:
            run_fname = op.join(data_path, 'run_%02d_filt_tsss_%d_raw.fif'
                                % (run, tsss))
        else:
            run_fname = op.join(data_path, 'run_%02d_filt_sss_'
                                'highpass-%sHz_raw.fif' % (run, l_freq))

        raw = mne.io.read_raw_fif(run_fname, preload=True)

        delay = int(round(0.0345 * raw.info['sfreq']))
        events = mne.read_events(op.join(data_path, 'run_%02d-eve.fif' % run))
        events[:, 0] = events[:, 0] + delay
        events_list.append(events)

        raw.info['bads'] = bads
        raw.interpolate_bads()
        raw_list.append(raw)

    raw, events = mne.concatenate_raws(raw_list, events_list=events_list)
    raw.set_eeg_reference(projection=True)
    del raw_list

    picks = mne.pick_types(raw.info, meg=True, eeg=True, stim=True,
                           eog=True, exclude=())

    # Epoch the data
    print('  Epoching')
    epochs = mne.Epochs(raw, events, events_id, tmin, tmax, proj=True,
                        picks=picks, baseline=baseline, preload=False,
                        decim=5, reject=None, reject_tmax=reject_tmax)

    # ICA
    if tsss:
        ica_name = op.join(meg_dir, subject, 'run_concat-tsss_%d-ica.fif'
                           % (tsss,))
        ica_out_name = ica_name
    else:
        ica_name = op.join(meg_dir, subject, 'run_concat-ica.fif')
        ica_out_name = op.join(meg_dir, subject,
                               'run_concat_highpass-%sHz-ica.fif' % (l_freq,))
    print('  Using ICA')
    ica = read_ica(ica_name)
    ica.exclude = []

    filter_label = '-tsss_%d' % tsss if tsss else '_highpass-%sHz' % l_freq
    ecg_epochs = create_ecg_epochs(raw, tmin=-.3, tmax=.3, preload=False)
    eog_epochs = create_eog_epochs(raw, tmin=-.5, tmax=.5, preload=False)
    del raw

    n_max_ecg = 3  # use max 3 components
    ecg_epochs.decimate(5)
    ecg_epochs.load_data()
    ecg_epochs.apply_baseline((None, None))
    ecg_inds, scores_ecg = ica.find_bads_ecg(ecg_epochs, method='ctps',
                                             threshold=0.8)
    print('    Found %d ECG indices' % (len(ecg_inds),))
    ica.exclude.extend(ecg_inds[:n_max_ecg])
    ecg_epochs.average().save(op.join(data_path, '%s%s-ecg-ave.fif'
                                      % (subject, filter_label)))
    np.save(op.join(data_path, '%s%s-ecg-scores.npy'
                    % (subject, filter_label)), scores_ecg)
    del ecg_epochs

    n_max_eog = 3  # use max 2 components
    eog_epochs.decimate(5)
    eog_epochs.load_data()
    eog_epochs.apply_baseline((None, None))
    eog_inds, scores_eog = ica.find_bads_eog(eog_epochs)
    print('    Found %d EOG indices' % (len(eog_inds),))
    ica.exclude.extend(eog_inds[:n_max_eog])
    eog_epochs.average().save(op.join(data_path, '%s%s-eog-ave.fif'
                                      % (subject, filter_label)))
    np.save(op.join(data_path, '%s%s-eog-scores.npy'
                    % (subject, filter_label)), scores_eog)
    del eog_epochs

    ica.save(ica_out_name)
    epochs.load_data()
    ica.apply(epochs)

    print('  Getting rejection thresholds')
    reject = get_rejection_threshold(epochs.copy().crop(None, reject_tmax),
                                     random_state=random_state)
    epochs.drop_bad(reject=reject)
    print('  Dropped %0.1f%% of epochs' % (epochs.drop_log_stats(),))

    print('  Writing to disk')
    if tsss:
        epochs.save(op.join(data_path, '%s-tsss_%d-epo.fif' % (subject, tsss)))
    else:
        epochs.save(op.join(data_path, '%s_highpass-%sHz-epo.fif'
                    % (subject, l_freq)))


###############################################################################
# Let us make the script parallel across subjects

# Here we use fewer N_JOBS to prevent potential memory problems
parallel, run_func, _ = parallel_func(run_epochs, n_jobs=max(N_JOBS // 4, 1))
parallel(run_func(subject_id) for subject_id in range(1, 20))
if l_freq is None:
    parallel(run_func(3, tsss) for tsss in (10, 1))  # Maxwell filtered data
