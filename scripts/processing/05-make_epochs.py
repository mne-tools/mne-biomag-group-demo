"""
Construct epochs
================

The epochs are constructed by using the events created in script 03. MNE
supports hierarchical events that allows selection to different groups more
easily. Some channels were not properly defined during acquisition, so they
are redefined before epoching. Bad EEG channels are interpolated and epochs
containing blinks are rejected. ECG artifacts are corrected using ICA. Finally
the epochs are saved to disk. To save space, the epoch data is decimated by
a factor of 2.
"""

import os
import tempfile
import os.path as op

import mne
from mne.parallel import parallel_func
from mne.preprocessing import create_ecg_epochs, read_ica

from autoreject import get_rejection_threshold

from library.config import meg_dir, N_JOBS, map_subjects, l_freq

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

tmin, tmax = -0.2, 0.8
baseline = None

tempdir = tempfile.mkdtemp()


###############################################################################
# Now we define a function to extract epochs for one subject
def run_epochs(subject_id, tsss=False):
    subject = "sub%03d" % subject_id
    print("processing subject: %s" % subject)

    data_path = op.join(meg_dir, subject)

    all_epochs = list()

    # Get all bad channels
    mapping = map_subjects[subject_id]  # map to correct subject
    all_bads = list()
    for run in range(1, 7):
        bads = list()
        bad_name = op.join('bads', mapping, 'run_%02d_raw_tr.fif_bad' % run)
        if os.path.exists(bad_name):
            with open(bad_name) as f:
                for line in f:
                    bads.append(line.strip())
        all_bads += [bad for bad in bads if bad not in all_bads]

    for run in range(1, 7):
        print(" - Run %s" % run)
        if tsss:
            run_fname = op.join(data_path, 'run_%02d_filt_tsss_raw.fif' % run)
        else:
            run_fname = op.join(data_path, 'run_%02d_filt_sss_'
                                'highpass-%sHz_raw.fif' % (run, l_freq))
        if not os.path.exists(run_fname):
            continue

        raw = mne.io.Raw(run_fname, preload=True)

        delay = int(0.0345 * raw.info['sfreq'])
        events = mne.read_events(op.join(data_path,
                                         'run_%02d_filt_sss-eve.fif' % run))

        events[:, 0] = events[:, 0] + delay

        raw.info['bads'] = all_bads
        raw.interpolate_bads()
        raw.set_eeg_reference()

        picks = mne.pick_types(raw.info, meg=True, eeg=True, stim=True,
                               eog=True)

        # Read epochs
        epochs = mne.Epochs(raw, events, events_id, tmin, tmax, proj=True,
                            picks=picks, baseline=baseline, preload=True,
                            decim=2, reject=None)
        reject = get_rejection_threshold(epochs)
        epochs.drop_bad(reject=reject)
        # XXX: workaround for memory leak in MNE where a reference to
        # raw object is kept in epochs. The downside is that it will
        # lead to some loss in precision but we can live with it.
        temp_fname = op.join(tempdir, 'run_%d.fif' % run)
        epochs.save(temp_fname)
        epochs = mne.read_epochs(temp_fname)

        # ICA
        if tsss:
            ica_name = op.join(meg_dir, subject, 'run_%02d-tsss-ica.fif' % run)
        else:
            ica_name = op.join(meg_dir, subject, 'run_%02d-ica.fif' % run)
        if l_freq is not None:
            ica = read_ica(ica_name)
            n_max_ecg = 3  # use max 3 components
            ecg_epochs = create_ecg_epochs(raw, tmin=-.5, tmax=.5)
            ecg_inds, scores_ecg = ica.find_bads_ecg(ecg_epochs, method='ctps',
                                                     threshold=0.8)
            ica.exclude = ecg_inds[:n_max_ecg]
            ica.save(ica_name)
            ica.apply(epochs)
        del raw
        all_epochs.append(epochs)

    epochs = mne.epochs.concatenate_epochs(all_epochs)
    if tsss:
        epochs.save(op.join(data_path, '%s-tsss-epo.fif' % subject))
    else:
        epochs.save(op.join(data_path, '%s_highpass-%sHz-epo.fif'
                    % (subject, l_freq)))


###############################################################################
# Let us make the script parallel across subjects

parallel, run_func, _ = parallel_func(run_epochs, n_jobs=1)
parallel(run_func(subject_id) for subject_id in range(1, 20))
run_epochs(1, True)  # run on maxwell filtered data
