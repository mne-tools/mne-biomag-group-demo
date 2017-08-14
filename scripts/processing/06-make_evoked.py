"""
Evoked data and covariance
==========================

The evoked data sets are created by averaging different categories of epochs.
The evoked data is saved using categories 'famous', 'scrambled', 'unfamiliar',
'contrast' and 'faces'. Covariance matrix is also computed and saved,
"""

import os.path as op

import mne
from mne.parallel import parallel_func

from library.config import meg_dir, N_JOBS, l_freq


def run_evoked(subject_id, tsss=False):
    subject = "sub%03d" % subject_id
    print("processing subject: %s" % subject)

    data_path = op.join(meg_dir, subject)
    if tsss:
        epochs = mne.read_epochs(op.join(data_path,
                                         '%s-tsss-epo.fif' % subject),
                                 preload=False)
    else:
        epochs = mne.read_epochs(op.join(data_path, '%s_highpass-%sHz'
                                 '-epo.fif' % (subject, l_freq)),
                                 preload=False)

    evoked_famous = epochs['face/famous'].average()
    evoked_scrambled = epochs['scrambled'].average()
    evoked_unfamiliar = epochs['face/unfamiliar'].average()

    # Simplify comment
    evoked_famous.comment = 'famous'
    evoked_scrambled.comment = 'scrambled'
    evoked_unfamiliar.comment = 'unfamiliar'

    contrast = mne.combine_evoked([evoked_famous, evoked_unfamiliar,
                                   evoked_scrambled], weights=[0.5, 0.5, -1.])
    contrast.comment = 'contrast'
    faces = mne.combine_evoked([evoked_famous, evoked_unfamiliar], 'nave')
    faces.comment = 'faces'

    if tsss:
        mne.evoked.write_evokeds(op.join(data_path,
                                         '%s-tsss-ave.fif' % subject),
                                 [evoked_famous, evoked_scrambled,
                                  evoked_unfamiliar, contrast, faces])

    else:
        mne.evoked.write_evokeds(op.join(data_path, '%s_highpass-%sHz'
                                 '-ave.fif' % (subject, l_freq)),
                                 [evoked_famous, evoked_scrambled,
                                  evoked_unfamiliar, contrast, faces])

    # take care of noise cov
    cov = mne.compute_covariance(epochs, tmax=0, method='shrunk')
    if tsss:
        cov.save(op.join(data_path, '%s-tsss-cov.fif' % subject))
    else:
        cov.save(op.join(data_path, '%s_highpass-%sHz-cov.fif'
                 % (subject, l_freq)))


parallel, run_func, _ = parallel_func(run_evoked, n_jobs=N_JOBS)
parallel(run_func(subject_id) for subject_id in range(1, 20))
run_evoked(1, True)  # run on maxwell filtered data
