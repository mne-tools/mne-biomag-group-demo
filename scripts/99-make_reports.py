from mayavi import mlab
import os.path as op

import matplotlib.pyplot as plt

from mne.parallel import parallel_func
from mne import Report
import mne

from config import study_path, subjects_dir, N_JOBS


def make_report(subject_id):
    subject = "sub%03d" % subject_id
    print("processing %s" % subject)

    meg_path = op.join(study_path, 'MEG', subject)
    ave_fname = op.join(meg_path, "%s-ave.fif" % subject)

    rep = Report(info_fname=ave_fname, subject=subject,
                 subjects_dir=subjects_dir)
    rep.parse_folder(meg_path)

    evokeds = mne.read_evokeds(op.join(meg_path, '%s-ave.fif' % subject))
    fam = evokeds[0]
    scramb = evokeds[1]
    unfam = evokeds[2]

    figs = list()
    captions = list()

    fig = fam.plot(spatial_colors=True, show=False)
    figs.append(fig)
    captions.append('Famous faces')

    fig = unfam.plot(spatial_colors=True, show=False)
    figs.append(fig)
    captions.append('Unfamiliar faces')

    fig = scramb.plot(spatial_colors=True, show=False)
    figs.append(fig)
    captions.append('Scrambled faces')

    if 'EEG070' in fam.ch_names:
        idx = fam.ch_names.index('EEG070')

        figs.append(plt.figure())

        plt.plot(fam.data[idx], label='famous')
        plt.plot(unfam.data[idx], label='unfamiliar')
        plt.plot(scramb.data[idx], label='scrambled')
        plt.legend()
        captions.append('Famous, unfamliliar and scrambled faces on EEG070')

    figs.append(mne.viz.plot_evoked_topo(evokeds, show=False))
    captions.append('Evoked responses')

    fname_trans = op.join(study_path, 'ds117', subject, 'MEG',
                          '%s-trans.fif' % subject)
    mne.viz.plot_trans(fam.info, fname_trans, subject=subject,
                       subjects_dir=subjects_dir, meg_sensors=True,
                       eeg_sensors=True)
    fig = mlab.gcf()
    figs.append(fig)
    captions.append('Coregistration')

    rep.add_figs_to_section(figs, captions)
    for cond in ['famous', 'unfamiliar', 'scrambled', 'famous - scrambled',
                 'unfamiliar - scrambled', 'famous - unfamiliar']:
        fname = op.join(meg_path, 'mne_dSPM_inverse-%s' % cond)
        stc = mne.read_source_estimate(fname, subject)
        brain = stc.plot(views=['ven'], hemi='both')

        brain.set_data_time_index(135)

        fig = mlab.gcf()
        rep._add_figs_to_section(fig, cond)

    rep.save(open_browser=False, overwrite=True)

    # !mne report -p $meg_path -i $ave_fname -d $subjects_dir -s $subject --no-browser --overwrite


parallel, run_func, _ = parallel_func(make_report, n_jobs=N_JOBS)
parallel(run_func(subject_id) for subject_id in range(17, 20))
