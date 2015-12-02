import os
import os.path as op
import numpy as np
import mne
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.preprocessing import LabelEncoder

from sklearn.externals.joblib import Parallel, delayed

le = LabelEncoder()
le.fit(['Familiar', 'Famous', 'Scrambled', 'Unfamiliar'])

mne.set_log_level('WARNING')

from config import meg_dir

all_events_id = dict(famous=[5, 6, 7], unfamiliar=[13, 14, 15], scrambled=[17, 18, 19])
events_id = dict(famous=1, unfamiliar=2, scrambled=3)

N_JOBS = 8

def run_evoked(subject_id):
    subject = "sub%03d" % subject_id
    print("processing subject: %s" % subject)
    data_path = op.join(meg_dir, subject)
    for run in range(1, 7):
        run_fname = op.join(data_path, 'run_%02d_filt_sss_raw.fif' % run)
        if not os.path.exists(run_fname):
            continue

        raw = mne.io.Raw(run_fname)

        events = mne.find_events(raw, stim_channel='STI101', consecutive='increasing',
                                 min_duration=0.003, verbose=True)
        for key in all_events_id:
            events = mne.merge_events(events, all_events_id[key], events_id[key])

        mask = (events[:, 2] == 1) | (events[:, 2] == 2) | (events[:, 2] == 3)
        events = events[mask]

        # df = pd.read_csv(data_path + '/Trials/run_%02d_trldef.txt' % run, sep='\t', header=None)
        # ev = np.c_[df[1], np.zeros_like(df[0]), le.transform(df[3])]
        # ev[:, 0] = np.round(ev[:, 0] / 3.)  # decimation by 3
        # ev[:, 0] += raw.first_samp
        # ev[:, 0] -= 452
        # ev[ev[:, 2] == 3, 2] = 4
        # ev[ev[:, 2] == 2, 2] = 3
        # ev[ev[:, 2] == 4, 2] = 2

        # print events - ev
        print "S %s - R %s" % (subject, run)
        # print (events - ev)[:, 2]
        # assert not np.any((events - ev)[:, 1:])
        # assert np.max(np.abs((events - ev)[:, 0])) == 1

        mne.write_events(op.join(data_path, 'run_%02d_filt_sss-eve.fif' % run), events)

        # mne.viz.plot_events(events, raw.info['sfreq'], raw.first_samp, show=False)
        # plt.savefig('img/eve/run_subj%s_%02d_events.png' % (subject, run))
        # plt.close('all')

Parallel(n_jobs=N_JOBS)(delayed(run_evoked)(subject_id) for subject_id in range(1, 20))
