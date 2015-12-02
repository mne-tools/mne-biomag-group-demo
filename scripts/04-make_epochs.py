import os
import os.path as op
import numpy as np
import matplotlib.pyplot as plt
import mne

from config import meg_dir

events_id = dict(famous=1, unfamiliar=2, scrambled=3)
tmin, tmax = -0.2, 0.8
reject = dict(grad=4000e-13, mag=4e-12, eog=180e-6)
# baseline = (-0.3, 00.)
baseline = None

N_JOBS = 1

subjects = range(1, 20)
runs = range(1, 7)

mne.set_log_level('WARNING')

for subject_id in range(1, 20):
    subject = "sub%03d" % subject_id
    print("processing subject: %s" % subject)

    data_path = op.join(meg_dir, subject)

    drop_log = []
    all_epochs = []

    # # Get all bad channels
    # all_bads = []
    # for run in runs:
    #     bads = np.loadtxt(data_path + '/MaxFilterOutput/run_%02d_bad.txt' % run)
    #     bads = np.unique(bads.ravel())
    #     bads = ['MEG%d' % b for b in bads]
    #     all_bads += [bad for bad in bads if bad not in all_bads]

    for run in runs:
        print " - Run %s" % run
        run_fname = op.join(data_path, 'run_%02d_filt_sss_raw.fif' % run)
        if not os.path.exists(run_fname):
            continue

        raw = mne.io.Raw(run_fname)
        events = mne.read_events(op.join(data_path, 'run_%02d_filt_sss-eve.fif' % run))

        # fix_info(raw.info)
        raw.set_channel_types({'EEG061': 'eog',
                               'EEG062': 'eog',
                                'EEG063': 'ecg'})
        raw.rename_channels({'EEG061': 'EOG061',
                             'EEG062': 'EOG062',
                             'EEG063': 'ECG063'})

        # # Add bad channels (only needed for non SSS data)
        # exclude = raw.info['bads']
        # if not ("sss" in raw.info['filename']):
        #     raw.info['bads'] = bads
        #     exclude = bads
        exclude = []  # XXX

        picks = mne.pick_types(raw.info, meg=True, eeg=True, stim=True, eog=True,
                               exclude=exclude)

        # Read epochs
        epochs = mne.Epochs(raw, events, events_id, tmin, tmax, proj=True,
                            picks=picks, baseline=baseline, preload=True,
                            reject=reject)
        del raw
        epochs.save(op.join(data_path, 'run_%02d_filt_sss-epo.fif' % run))

        drop_log.append([subject, run, len(epochs)])

        # epochs.plot_drop_log()
        # plt.savefig('img/droplog/run_subj%s_%02d_droplog.pdf' % (subject, run))
        # plt.close('all')

        all_epochs.append(epochs)
        if run == 1:
            evoked_famous = epochs['famous'].average()
            evoked_scrambled = epochs['scrambled'].average()
            evoked_unfamiliar = epochs['unfamiliar'].average()
        else:
            evoked_famous += epochs['famous'].average()
            evoked_scrambled += epochs['scrambled'].average()
            evoked_unfamiliar += epochs['unfamiliar'].average()

    evoked_famous.comment = 'famous'
    evoked_scrambled.comment = 'scrambled'
    evoked_unfamiliar.comment = 'unfamiliar'

    mne.evoked.write_evokeds(op.join(data_path, '%s-ave.fif' % subject),
                             [evoked_famous, evoked_scrambled, evoked_unfamiliar,
                              evoked_famous - evoked_scrambled,
                              evoked_unfamiliar - evoked_scrambled,
                              evoked_famous - evoked_unfamiliar])

    # take care of noise cov
    cov = mne.compute_covariance(all_epochs, tmin=tmin, tmax=0)
    cov.save(op.join(data_path, '%s-cov.fif' % subject))

    # # import matplotlib
    # # matplotlib.use('Agg')
    # import matplotlib.pyplot as plt
    # plt.close('all')
    # mne.viz.plot_cov(cov, epochs.info)
    # plt.tight_layout()
    # plt.figure(1)
    # plt.tight_layout()
    # plt.savefig('img/cov/Sub%02d-cov.pdf' % subject)

    # plt.figure(3)
    # titles = dict(eeg='EEG - nave:%d' % evoked_famous.nave, grad='Gradiometers', mag='Magnetometers')
    # evoked_famous.plot(titles=titles)
    # plt.tight_layout()
    # plt.savefig('img/ave/Sub%02d_famous-ave.pdf' % subject)
    # plt.show()

    # plt.figure(4)
    # titles = dict(eeg='EEG - nave:%d' % evoked_scrambled.nave, grad='Gradiometers', mag='Magnetometers')
    # evoked_scrambled.plot(titles=titles)
    # plt.tight_layout()
    # plt.savefig('img/ave/Sub%02d_scrambled-ave.pdf' % subject)
    # plt.show()

    # plt.figure(5)
    # titles = dict(eeg='EEG - nave:%d' % evoked_unfamiliar.nave, grad='Gradiometers', mag='Magnetometers')
    # evoked_unfamiliar.plot(titles=titles)
    # plt.tight_layout()
    # plt.savefig('img/ave/Sub%02d_unfamiliar-ave.pdf' % subject)
    # plt.show()

    np_drop_log = np.array(drop_log)

    import pandas as pd
    dl = pd.DataFrame(np_drop_log)
    dl.columns = ['subject', 'run', 'n_epochs']
    dl.to_csv(op.join(data_path, 'droplog.csv'))
