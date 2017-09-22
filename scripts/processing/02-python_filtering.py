"""
Filter using MNE-python
=======================

The data are bandpass filtered (1 - 40 Hz) using linear-phase fir filter with
delay compensation. For the lowpass filter the transition bandwidth is
automatically defined. See
`Background information on filtering <http://mne-tools.github.io/dev/auto_tutorials/plot_background_filtering.html>`_
for more. The filtered data are saved to separate files to the subject's'MEG'
directory.
"""

import os
import os.path as op
from warnings import warn

import mne
from mne import pick_types
from mne.parallel import parallel_func

from library.config import study_path, meg_dir, N_JOBS, l_freq


if not op.exists(meg_dir):
    os.mkdir(meg_dir)


def run_filter(subject_id):
    subject = "sub%03d" % subject_id
    print("processing subject: %s" % subject)
    raw_fname_out = op.join(meg_dir, subject,
                            'run_%02d_filt_sss_highpass-%sHz_raw.fif')
    raw_fname_in = op.join(study_path, 'ds117', subject, 'MEG',
                           'run_%02d_sss.fif')
    for run in range(1, 7):
        raw_in = raw_fname_in % run
        try:
            raw = mne.io.read_raw_fif(raw_in, preload=True)
        except AttributeError:
            # Some files on openfmri are corrupted and cannot be read.
            warn('Could not read file %s. '
                 'Skipping run %s from subject %s.' % (raw_in, run, subject))
            continue

        raw.set_channel_types({'EEG061': 'eog',
                               'EEG062': 'eog',
                               'EEG063': 'ecg',
                               'EEG064': 'misc'})  # EEG064 free floating el.
        raw.rename_channels({'EEG061': 'EOG061',
                             'EEG062': 'EOG062',
                             'EEG063': 'ECG063'})

        if not op.exists(op.join(meg_dir, subject)):
            os.mkdir(op.join(meg_dir, subject))

        raw.filter(l_freq, 40, l_trans_bandwidth='auto',
                   h_trans_bandwidth='auto', filter_length='auto',
                   phase='zero', fir_window='hann',
                   fir_design='firwin')
        # high-pass eog channel to get reasonable thresholds in autoreject
        picks_eog = pick_types(raw.info, meg=False, eog=True)
        raw.filter(l_freq, None, picks=picks_eog, l_trans_bandwidth='auto',
                   filter_length='auto', phase='zero', fir_window='hann',
                   fir_design='firwin')
        raw_out = raw_fname_out % (run, l_freq)
        raw.save(raw_out, overwrite=True)


parallel, run_func, _ = parallel_func(run_filter, n_jobs=N_JOBS)
parallel(run_func(subject_id) for subject_id in range(1, 20))
