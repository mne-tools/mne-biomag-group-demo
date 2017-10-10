"""
Run ICA
=======

ICA decomposition using fastICA.
"""

import os.path as op

import mne
from mne.preprocessing import ICA
from mne.parallel import parallel_func

from library.config import meg_dir, N_JOBS, l_freq


def run_ica(subject_id, tsss=None):
    subject = "sub%03d" % subject_id
    print("Processing subject: %s" % subject)
    data_path = op.join(meg_dir, subject)
    raws = list()
    print("  Loading runs")
    for run in range(1, 7):
        if tsss:
            run_fname = op.join(data_path, 'run_%02d_filt_tsss_%d_raw.fif'
                                % (run, tsss))
        else:
            run_fname = op.join(data_path, 'run_%02d_filt_sss_highpass-%sHz'
                                '_raw.fif' % (run, l_freq))
        raws.append(mne.io.read_raw_fif(run_fname))
    raw = mne.concatenate_raws(raws)
    if tsss:
        ica_name = op.join(meg_dir, subject,
                           'run_concat-tsss_%d-ica.fif' % tsss)
    else:
        ica_name = op.join(meg_dir, subject, 'run_concat-ica.fif')
    print('  Fitting ICA')
    ica = ICA(method='fastica', random_state=42, n_components=0.98)
    picks = mne.pick_types(raw.info, meg=True, eeg=True, eog=False,
                           stim=False, exclude='bads')
    ica.fit(raw, picks=picks, reject=dict(grad=4000e-13, mag=4e-12),
            decim=8)
    ica.save(ica_name)


parallel, run_func, _ = parallel_func(run_ica, n_jobs=N_JOBS)
parallel(run_func(subject_id) for subject_id in range(1, 20))
parallel(run_func(2, tsss) for tsss in (10, 1))  # Maxwell filtered data
