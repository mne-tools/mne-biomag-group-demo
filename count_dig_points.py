import os
import os.path as op

import mne

study_path = '/tsi/doctorants/data_gramfort/dgw_faces'


subjects_dir = os.path.join(study_path, 'subjects')
meg_dir = os.path.join(study_path, 'MEG')

counts = 0
for subject_id in range(1, 20):

    subject = "sub%03d" % subject_id
    print("processing subject: %s" % subject)

    data_path = op.join(meg_dir, subject)
    run_fname = op.join(data_path, 'run_01_filt_sss_raw.fif')

    raw = mne.io.Raw(run_fname, preload=False)
    counts += len(raw.info['dig'])
    print('Number of dig points %s' % counts)
counts /= 19.
