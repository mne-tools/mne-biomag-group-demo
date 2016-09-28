"""
====================
Remove ECG using ICA
====================

Remove ICA using ECG.
"""
import os
import os.path as op
import numpy as np

import mne
from mne.preprocessing import create_ecg_epochs, read_ica

from library.config import meg_dir, map_subjects

###############################################################################
# We define the events and the onset and offset of the epochs.

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
reject = dict(grad=4000e-13, mag=4e-12, eog=180e-6)
baseline = None

subject_id, run = 5, 1
subject = "sub%03d" % subject_id
print("processing subject: %s" % subject)

data_path = op.join(meg_dir, subject)

###############################################################################
# Now we get the bad channels.

# Get all bad channels
mapping = map_subjects[subject_id]  # map to correct subject
all_bads = list()

bads = list()
bad_name = op.join('bads', mapping, 'run_%02d_raw_tr.fif_bad' % run)
if os.path.exists(bad_name):
    with open(bad_name) as f:
        for line in f:
            bads.append(line.strip())

###############################################################################
# We read the data.

run_fname = op.join(data_path, 'run_%02d_filt_sss_raw.fif' % run)
raw = mne.io.Raw(run_fname, preload=True, add_eeg_ref=False)

###############################################################################
# We change the channel type for ECG and EOG.

raw.set_channel_types({'EEG061': 'eog', 'EEG062': 'eog', 'EEG063': 'ecg',
                       'EEG064': 'misc'})  # EEG064 free floating el.
raw.rename_channels({'EEG061': 'EOG061', 'EEG062': 'EOG062',
                     'EEG063': 'ECG063'})

###############################################################################
# We remove the bad eye blink segments from the raw by marking
# ``raw.annotations``. They will be removed before constructing epochs.

eog_events = mne.preprocessing.find_eog_events(raw)
eog_events[:, 0] -= int(0.25 * raw.info['sfreq'])
annotations = mne.Annotations(eog_events[:, 0] / raw.info['sfreq'],
                              np.repeat(0.5, len(eog_events)),
                              'BAD_blink', raw.info['meas_date'])
raw.annotations = annotations  # Remove epochs with blinks

###############################################################################
# Must take into account the 34 ms delay in the trigger channel.

delay = int(0.0345 * raw.info['sfreq'])
events = mne.read_events(op.join(data_path,
                                 'run_%02d_filt_sss-eve.fif' % run))
events[:, 0] = events[:, 0] + delay

###############################################################################
# Bad sensors are repaired.

raw.info['bads'] = bads
raw.interpolate_bads()
raw.set_eeg_reference()

###############################################################################
# ... and finally ``Epochs`` are constructed

picks = mne.pick_types(raw.info, meg=True, eeg=True, stim=True,
                       eog=True)

# Read epochs
epochs = mne.Epochs(raw, events, events_id, tmin, tmax, proj=True,
                    picks=picks, baseline=baseline, preload=True,
                    decim=2, reject=reject)

###############################################################################
# Now let's get to some serious ICA preprocessing

ica_name = op.join(meg_dir, subject, 'run_%02d-ica.fif' % run)
ica = read_ica(ica_name)
n_max_ecg = 3  # use max 3 components
ecg_epochs = create_ecg_epochs(raw, tmin=-.5, tmax=.5)
ecg_inds, scores_ecg = ica.find_bads_ecg(ecg_epochs, method='ctps',
                                         threshold=0.8)
ica.plot_sources(raw, exclude=ecg_inds)
ica.plot_scores(scores_ecg, exclude=ecg_inds)
ica.plot_components(ecg_inds)
ica.exclude += ecg_inds[:n_max_ecg]

ica.apply(epochs)
