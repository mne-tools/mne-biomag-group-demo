import os
import os.path as op
import numpy as np

import mne
from mne.parallel import parallel_func
from mne.io.constants import FIFF
from mne.preprocessing import create_ecg_epochs, read_ica

from config import study_path, meg_dir, N_JOBS

autoreject = True
if autoreject:
    from autoreject import GlobalAutoReject, validation_curve

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
#baseline = (-0.2, 00.)
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
        bad_name = op.join(data_path, 'bads', 'run_%02d_raw_tr.fif_bad' % run)

        if os.path.exists(bad_name):
            with open(bad_name) as f:
                for line in f:
                    bads.append(line.strip())
        #     bads = np.loadtxt(data_path + '/MaxFilterOutput/run_%02d_bad.txt' % run)
        #     bads = np.unique(bads.ravel())
        #     bads = ['MEG%d' % b for b in bads]
        all_bads += [bad for bad in bads if bad not in all_bads]

    for run in range(1, 7):
        print " - Run %s" % run
        run_fname = op.join(data_path, 'run_%02d_filt_sss_raw.fif' % run)
        if not os.path.exists(run_fname):
            continue

        raw = mne.io.Raw(run_fname)
        for idx, proj in enumerate(raw.info['projs']):
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

        if autoreject:
            epochs = mne.Epochs(raw, events, events_id, tmin, tmax, proj=True,
                                picks=picks, baseline=baseline, preload=True,
                                reject=None)
            reject = dict()
            param_range = np.linspace(400e-15, 20000e-15, 30)
            _, test_scores = validation_curve(
                GlobalAutoReject(), epochs.copy().pick_types(meg='mag'),
                y=None, param_name="thresh", param_range=param_range, cv=5,
                n_jobs=N_JOBS)

            test_scores = -test_scores.mean(axis=1)
            reject['mag'] = param_range[np.argmin(test_scores)]


            param_range = np.linspace(400e-13, 20000e-13, 30)
            _, test_scores = validation_curve(
                GlobalAutoReject(), epochs.copy().pick_types(meg='grad'),
                y=None, param_name="thresh", param_range=param_range, cv=5,
                n_jobs=N_JOBS)
            test_scores = -test_scores.mean(axis=1)
            reject['grad'] = param_range[np.argmin(test_scores)]

            param_range = np.linspace(20e-7, 400e-6, 30)
            _, test_scores = validation_curve(
                GlobalAutoReject(), epochs.copy().pick_types(meg=False,
                                                             eeg=True),
                y=None, param_name="thresh", param_range=param_range, cv=5,
                n_jobs=N_JOBS)
            test_scores = -test_scores.mean(axis=1)
            reject['grad'] = param_range[np.argmin(test_scores)]
            epochs.drop_bad(reject=reject)
        else:
            # Read epochs
            epochs = mne.Epochs(raw, events, events_id, tmin, tmax, proj=True,
                                picks=picks, baseline=baseline, preload=True,
                                reject=reject)

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

    evoked_famous = epochs['famous'].average()
    evoked_scrambled = epochs['scrambled'].average()
    evoked_unfamiliar = epochs['unfamiliar'].average()

    # Simplify comment
    evoked_famous.comment = 'famous'
    evoked_scrambled.comment = 'scrambled'
    evoked_unfamiliar.comment = 'unfamiliar'

    contrast = mne.combine_evoked([evoked_famous, evoked_unfamiliar,
                                   evoked_scrambled], weights=[0.5, 0.5, -1.])
    contrast.comment = 'contrast'
    faces = mne.combine_evoked([evoked_famous, evoked_unfamiliar])
    faces.comment = 'faces'

    mne.evoked.write_evokeds(op.join(data_path, '%s-ave.fif' % subject),
                             [evoked_famous, evoked_scrambled,
                              evoked_unfamiliar, contrast, faces])

    # take care of noise cov
    cov = mne.compute_covariance(epochs, tmin=tmin, tmax=0)
    cov.save(op.join(data_path, '%s-cov.fif' % subject))


parallel, run_func, _ = parallel_func(run_epochs, n_jobs=N_JOBS)
parallel(run_func(subject_id) for subject_id in range(1, 20))
