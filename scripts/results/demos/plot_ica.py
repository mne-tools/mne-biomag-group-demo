"""
====================
Remove ECG using ICA
====================

Remove ECG for sub005 using ICA.
"""
import os
import os.path as op
import sys

import mne
from mne.preprocessing import create_ecg_epochs, read_ica

sys.path.append(op.join('..', '..', 'processing'))
from library.config import meg_dir, map_subjects, l_freq  # noqa: E402

subject_id, run = 5, 1
subject = "sub%03d" % subject_id
print("processing subject: %s" % subject)

data_path = op.join(meg_dir, subject)

###############################################################################
# Now we get the bad channels.

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

run_fname = op.join(data_path, 'run_%02d_filt_sss_highpass-%sHz_raw.fif'
                    % (run, l_freq))
raw = mne.io.read_raw_fif(run_fname, preload=True)

###############################################################################
# Bad sensors are repaired.

raw.info['bads'] = bads
raw.interpolate_bads()
raw.set_eeg_reference(projection=True)

###############################################################################
# Now let's get to some serious ICA preprocessing

ica_name = op.join(meg_dir, subject, 'run_%02d-ica.fif' % run)
ica = read_ica(ica_name)
n_max_ecg = 3  # use max 3 components
ecg_epochs = create_ecg_epochs(raw, tmin=-.5, tmax=.5)
ecg_epochs.decimate(11, verbose='error')
ecg_inds, scores_ecg = ica.find_bads_ecg(ecg_epochs, method='ctps',
                                         threshold=0.8)
ica.plot_sources(raw, exclude=ecg_inds)
ica.plot_scores(scores_ecg, exclude=ecg_inds)
ica.plot_properties(raw, ecg_inds)
ica.exclude += ecg_inds[:n_max_ecg]
