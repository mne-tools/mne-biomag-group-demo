"""
Blabla
======================

blabla
"""

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

    fig = fam.plot(spatial_colors=True, show=False, gfp=True)
    figs.append(fig)
    captions.append('Famous faces')

    fig = unfam.plot(spatial_colors=True, show=False, gfp=True)
    figs.append(fig)
    captions.append('Unfamiliar faces')

    fig = scramb.plot(spatial_colors=True, show=False, gfp=True)
    figs.append(fig)
    captions.append('Scrambled faces')

    if 'EEG070' in fam.ch_names:
        idx = fam.ch_names.index('EEG070')

        fig = mne.viz.plot_compare_evokeds({'Famous':fam, 'Unfamiliar':unfam,
                                            'Scrambled':scramb}, idx, show=False)
        figs.append(fig)

        #plt.plot(fam.data[idx], label='famous')
        #plt.plot(unfam.data[idx], label='unfamiliar')
        #plt.plot(scramb.data[idx], label='scrambled')
        #plt.legend()
        captions.append('Famous, unfamliliar and scrambled faces on EEG070')

    fname_trans = op.join(study_path, 'ds117', subject, 'MEG',
                          '%s-trans.fif' % subject)
    mne.viz.plot_trans(fam.info, fname_trans, subject=subject,
                       subjects_dir=subjects_dir, meg_sensors=True,
                       eeg_sensors=True)
    fig = mlab.gcf()
    figs.append(fig)
    captions.append('Coregistration')

    rep.add_figs_to_section(figs, captions)
    for cond in ['faces', 'famous', 'unfamiliar', 'scrambled', 'contrast']:
        fname = op.join(meg_path, 'mne_dSPM_inverse-%s' % cond)
        stc = mne.read_source_estimate(fname, subject)
        brain = stc.plot(views=['ven'], hemi='both')

        brain.set_data_time_index(112)

        fig = mlab.gcf()
        rep._add_figs_to_section(fig, cond)

    rep.save(fname=op.join(study_path, 'MEG', 'report%s.html' % subject),
                           open_browser=False, overwrite=True)

    # !mne report -p $meg_path -i $ave_fname -d $subjects_dir -s $subject --no-browser --overwrite


# Group report
faces_fname = op.join(study_path, 'MEG', 'eeg_faces-ave.fif')
rep = Report(info_fname=faces_fname, subject='fsaverage',
             subjects_dir=subjects_dir)
faces = mne.read_evokeds(faces_fname)[0]
rep.add_figs_to_section(faces.plot(spatial_colors=True, gfp=True, show=False),
                        'Average faces')

scrambled = mne.read_evokeds(op.join(study_path, 'MEG',
                                     'eeg_scrambled-ave.fif'))[0]
rep.add_figs_to_section(scrambled.plot(spatial_colors=True, gfp=True,
                                       show=False), 'Average scrambled')

fname = op.join(study_path, 'MEG', 'contrast-average')
stc = mne.read_source_estimate(fname, subject='fsaverage')
brain = stc.plot(views=['ven'], hemi='both', subject='fsaverage',
                 subjects_dir=subjects_dir)
brain.set_data_time_index(165)

fig = mlab.gcf()
rep._add_figs_to_section(fig, 'Avergae faces - scrambled')

rep.save(fname=op.join(study_path, 'MEG', 'report_average.html'),
         open_browser=False, overwrite=True)

parallel, run_func, _ = parallel_func(make_report, n_jobs=N_JOBS)
parallel(run_func(subject_id) for subject_id in range(1, 20))
