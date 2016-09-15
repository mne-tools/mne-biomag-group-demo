import os
import os.path as op

import mne
from mne.preprocessing import ICA
from mne.parallel import parallel_func

from config import study_path, meg_dir, N_JOBS

def run_ica(subject_id):
    subject = "sub%03d" % subject_id
    print("processing subject: %s" % subject)
    data_path = op.join(meg_dir, subject)
    for run in range(1, 7):
        run_fname = op.join(data_path, 'run_%02d_filt_sss_raw.fif' % run)
        raw = mne.io.read_raw_fif(run_fname)
        ica_name = op.join(study_path, 'MEG', subject,
                           'run_%02d-ica.fif' % run)

        ica = ICA(method='fastica', random_state=42, n_components=0.95)
        picks = mne.pick_types(raw.info, meg=True, eeg=False, eog=False,
                               stim=False, exclude='bads')
        ica.fit(raw, picks=picks, reject=dict(grad=4000e-13, mag=4e-12))
        ica.save(ica_name)


parallel, run_func, _ = parallel_func(run_ica, n_jobs=N_JOBS)
parallel(run_func(subject_id) for subject_id in range(1, 20))
