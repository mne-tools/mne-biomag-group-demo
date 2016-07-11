import os
import os.path as op

import mne
from mne.parallel import parallel_func

from config import meg_dir, N_JOBS

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
# baseline = (-0.3, 00.)
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
        raw.del_proj(0)  # remove EEG average ref
        events = mne.read_events(op.join(data_path,
                                         'run_%02d_filt_sss-eve.fif' % run))

        raw.set_channel_types({'EEG061': 'eog',
                               'EEG062': 'eog',
                               'EEG063': 'ecg'})
        raw.rename_channels({'EEG061': 'EOG061',
                             'EEG062': 'EOG062',
                             'EEG063': 'ECG063'})

        raw.add_eeg_average_proj()

        # Add bad channels (only needed for non SSS data)
        exclude = raw.info['bads']
        # if not ("sss" in raw.info['filename']):
        #     raw.info['bads'] = all_bads
        #     exclude = all_bads
        # exclude = []  # XXX
        raw.info['bads'] = all_bads
        exclude = all_bads

        picks = mne.pick_types(raw.info, meg=True, eeg=True, stim=True,
                               eog=True, exclude=exclude)

        # Read epochs
        epochs = mne.Epochs(raw, events, events_id, tmin, tmax, proj=True,
                            picks=picks, baseline=baseline, preload=True,
                            reject=reject)
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

    mne.evoked.write_evokeds(op.join(data_path, '%s-ave.fif' % subject),
                             [evoked_famous, evoked_scrambled,
                              evoked_unfamiliar,
                              evoked_famous - evoked_scrambled,
                              evoked_unfamiliar - evoked_scrambled,
                              evoked_famous - evoked_unfamiliar])

    # take care of noise cov
    cov = mne.compute_covariance(epochs, tmin=tmin, tmax=0)
    cov.save(op.join(data_path, '%s-cov.fif' % subject))


parallel, run_func, _ = parallel_func(run_epochs, n_jobs=N_JOBS)
parallel(run_func(subject_id) for subject_id in range(1, 20))
