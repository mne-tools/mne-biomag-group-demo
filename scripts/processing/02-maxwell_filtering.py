"""
Maxwell filter using MNE-python
===============================

The data are maxwell filtered using tSSS. This works as an alternative for
highpass filtering. It is critical to mark bad channels before maxwell
filtering. Here we exploit the log files for determining the bad channels.
The data are also lowpass filtered at 40 Hz using linear-phase fir filter with
delay compensation. The transition bandwidth is automatically defined. See
`Background information on filtering <http://mne-tools.github.io/dev/auto_tutorials/plot_background_filtering.html>`_
for more. The filtered data are saved to separate files to the subject's'MEG'
directory.
"""

import os
import os.path as op
from warnings import warn
import numpy as np

import mne
from mne.parallel import parallel_func

from library.config import study_path, meg_dir, N_JOBS, cal, ctc


if not op.exists(meg_dir):
    os.mkdir(meg_dir)


def run_filter(subject_id):
    subject = "sub%03d" % subject_id
    print("processing subject: %s" % subject)
    raw_fname_out = op.join(meg_dir, subject, 'run_%02d_filt_tsss_raw.fif')

    raw_fname_in = op.join(study_path, 'ds117', subject, 'MEG',
                           'run_%02d_raw.fif')
    # Use average head position over all runs.
    destinations = list()
    for run in range(1, 7):
        raw_in = raw_fname_in % run
        raw = mne.io.read_raw_fif(raw_in)
        destinations.append(raw.info['dev_head_t']['trans'][:3, 3])
    destination = np.mean(destinations, axis=0)

    for run in range(1, 7):
        raw_in = raw_fname_in % run
        try:
            raw = mne.io.read_raw_fif(raw_in, preload=True)
        except AttributeError:
            # Some files on openfmri are corrupted and cannot be read.
            warn('Could not read file %s. '
                 'Skipping run %s from subject %s.' % (raw_in, run, subject))
            continue

        # Hackish way of reading bad channels from the log.
        with open(op.join(study_path, 'ds117', subject, 'MEG',
                          'run_%02d_sss_log.txt' % run)) as fid:
            for line in fid:
                if line.startswith('Static bad channels'):
                    chs = line.split(':')[-1].split()
                    bads = ['MEG%04d' % int(ch) for ch in chs]
                    break
        raw.info['bads'] += bads
        print("BAD CHANNELS:\n")
        print(raw.info['bads'])
        raw = mne.preprocessing.maxwell_filter(raw, calibration=cal,
                                               cross_talk=ctc,
                                               st_duration=10.,
                                               origin=(0., 0., 0.04),
                                               destination=destination)

        raw_out = raw_fname_out % run
        if not op.exists(op.join(meg_dir, subject)):
            os.mkdir(op.join(meg_dir, subject))

        raw.filter(None, 40, l_trans_bandwidth=0.5, h_trans_bandwidth='auto',
                   filter_length='auto', phase='zero', fir_window='hann')
        raw.save(raw_out, overwrite=True)


parallel, run_func, _ = parallel_func(run_filter, n_jobs=N_JOBS)
parallel(run_func(subject_id) for subject_id in range(1, 2))  # Only for sub01.
