"""
Blabla
======================

blabla
"""

import os
import os.path as op
from warnings import warn

import mne
from mne.parallel import parallel_func

from config import study_path, meg_dir, N_JOBS

if not op.exists(meg_dir):
    os.mkdir(meg_dir)

def run_filter(subject_id):
    subject = "sub%03d" % subject_id
    print("processing subject: %s" % subject)
    raw_fname_out = op.join(meg_dir, subject, 'run_%02d_filt_sss_raw.fif')

    for run in range(1, 7):
        # Note: There are couple of corrupted files in the data set. Run 2 from
        # sub004 has some seconds missing from the end and run 3 from sub006
        # has 2/3 of the data missing. Here we use cropped file from sub004 and
        # for sub006 we used tSSS to clean the data for run 3 for sub006, If
        # these files are missing, the runs are omitted from the analysis.
        raw_fname_in = op.join(study_path, 'MEG', subject,
                               'run_%02d_cropped_sss.fif')  # for sub004 run02
        if not os.path.exists(raw_fname_in % run):
            raw_fname_in = op.join(study_path, 'MEG', subject,
                                   'run_%02d_new_sss.fif')  # for sub006 run03
        if not os.path.exists(raw_fname_in % run):
            raw_fname_in = op.join(study_path, 'ds117', subject,
                                   'MEG', 'run_%02d_sss.fif')
        raw_in = raw_fname_in % run
        if not os.path.exists(raw_in):
            warn('Could not find file %s. '
                 'Skipping run %s for subject %s.' % (raw_in, run, subject))
            continue
        raw = mne.io.read_raw_fif(raw_in, preload=True)
        raw_out = raw_fname_out % run
        if not op.exists(op.join(meg_dir, subject)):
            os.mkdir(op.join(meg_dir, subject))

        raw.filter(1, 40, l_trans_bandwidth='auto', h_trans_bandwidth='auto',
                   phase='zero', fir_window='hamming', filter_length='auto',
                   n_jobs=N_JOBS)
        raw.save(raw_out, overwrite=True)


parallel, run_func, _ = parallel_func(run_filter, n_jobs=N_JOBS)
parallel(run_func(subject_id) for subject_id in range(1, 20))
