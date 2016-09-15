import os
import os.path as op
import numpy as np

import mne
from mne.parallel import parallel_func
from mne.io.constants import FIFF
from mne.preprocessing import create_ecg_epochs, read_ica

from config import study_path, meg_dir, N_JOBS, map_subjects

events_id = {
    'famous/first': 5,
    'famous/immediate': 6,
    'famous/long': 7,
    'unfamiliar/first': 13,
    'unfamiliar/immediate': 14,
    'unfamiliar/long': 15,
    'scrambled/first': 17,
    'scrambled/immediate': 18,
    'scrambled/long': 19,
}

tmin, tmax = -0.2, 0.8
reject = dict(grad=4000e-13, mag=4e-12, eog=180e-6)
baseline = None


def run_epochs(subject_id):
    subject = "sub%03d" % subject_id
    print("processing subject: %s" % subject)

    data_path = op.join(meg_dir, subject)

    all_epochs = []

    # # Get all bad channels
    all_bads = []
    for run in range(1, 7):
        bads = list()
        mapping = map_subjects[subject_id]
        bad_name = op.join('bads', mapping, 'run_%02d_raw_tr.fif_bad' % run)

        if os.path.exists(bad_name):
            with open(bad_name) as f:
                for line in f:
                    bads.append(line.strip())
        all_bads += [bad for bad in bads if bad not in all_bads]

    for run in range(1, 7):
        print " - Run %s" % run
        run_fname = op.join(data_path, 'run_%02d_filt_sss_raw.fif' % run)
        if not os.path.exists(run_fname):
            continue

        raw = mne.io.Raw(run_fname)
        for idx, proj in enumerate(raw.info['projs']):  # find idx for EEG-ref
            if proj['kind'] == FIFF.FIFFV_MNE_PROJ_ITEM_EEG_AVREF:
                proj_idx = idx
                break
        raw.del_proj(proj_idx)  # remove EEG average ref

        raw.set_channel_types({'EEG061': 'eog',
                               'EEG062': 'eog',
                               'EEG063': 'ecg',
                               'EEG064': 'misc'})  # EEG064 free floating el.)
        raw.rename_channels({'EEG061': 'EOG061',
                             'EEG062': 'EOG062',
                             'EEG063': 'ECG063'})

        eog_events = mne.preprocessing.find_eog_events(raw)
        eog_events[:, 0] -= int(0.25 * raw.info['sfreq'])
        annotations = mne.Annotations(eog_events[:, 0] / raw.info['sfreq'],
                                      np.repeat(0.5, len(eog_events)),
                                      'BAD_blink', raw.info['meas_date'])
        raw.annotations = annotations  # Remove epochs with blinks

        delay = int(0.0345 * raw.info['sfreq'])
        events = mne.read_events(op.join(data_path,
                                         'run_%02d_filt_sss-eve.fif' % run))

        events[:, 0] = events[:, 0] + delay

        raw.info['bads'] = all_bads
        raw.interpolate_bads()
        raw.add_eeg_average_proj()

        picks = mne.pick_types(raw.info, meg=True, eeg=True, stim=True,
                               eog=True)

        # Read epochs
        epochs = mne.Epochs(raw, events, events_id, tmin, tmax, proj=True,
                            picks=picks, baseline=baseline, preload=True,
                            decim=2, reject=reject)

        # ICA
        ica_name = op.join(study_path, 'MEG', subject,
                           'run_%02d-ica.fif' % run)
        ica = read_ica(ica_name)
        n_max_ecg = 3  # use max 3 components
        ecg_epochs = create_ecg_epochs(raw, tmin=-.5, tmax=.5)
        ecg_inds, scores_ecg = ica.find_bads_ecg(ecg_epochs, method='ctps',
                                                 threshold=0.8)
        ica.exclude += ecg_inds[:n_max_ecg]

        ica.apply(epochs)
        all_epochs.append(epochs)

    epochs = mne.epochs.concatenate_epochs(all_epochs)
    epochs.save(op.join(data_path, '%s-epo.fif' % subject))


parallel, run_func, _ = parallel_func(run_epochs, n_jobs=N_JOBS)
parallel(run_func(subject_id) for subject_id in range(1, 20))
