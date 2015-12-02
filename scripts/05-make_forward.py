import os.path as op
import mne

from sklearn.externals.joblib import Parallel, delayed

from config import study_path, meg_dir, subjects_dir, spacing

mindist = 5

N_JOBS = 8


def run_forward(subject_id):
    subject = "sub%03d" % subject_id
    print("processing subject: %s" % subject)
    data_path = op.join(meg_dir, subject)

    fname_ave = op.join(data_path, '%s-ave.fif' % subject)
    fname_fwd = op.join(data_path, '%s-meg-%s-fwd.fif' % (subject, spacing))
    fname_trans = op.join(study_path, 'ds117', subject, 'MEG', '%s-trans.fif' % subject)

    src = mne.setup_source_space(subject, spacing=spacing,
                                 subjects_dir=subjects_dir, overwrite=True,
                                 n_jobs=1, add_dist=False)

    src_fname = op.join(subjects_dir, subject, '%s-src.fif' % spacing)
    mne.write_source_spaces(src_fname, src)

    bem_model = mne.make_bem_model(subject, ico=4, subjects_dir=subjects_dir,
                                   conductivity=(0.3,))
    bem = mne.make_bem_solution(bem_model)
    info = mne.read_evokeds(fname_ave, condition=0).info
    fwd = mne.make_forward_solution(info, trans=fname_trans, src=src, bem=bem,
                                    fname=None, meg=True, eeg=False,
                                    mindist=mindist, n_jobs=1, overwrite=True)
    fwd = mne.convert_forward_solution(fwd, surf_ori=True)
    mne.write_forward_solution(fname_fwd, fwd, overwrite=True)

    # mag_map = mne.sensitivity_map(fwd, ch_type=fwd_ch_type, mode=fwd_ori)
    # brain = mag_map.plot(subject=subject, time_label='Magnetometer sensitivity',
    #                      hemi='rh', subjects_dir=subjects_dir, **fwd_plot_args)
    # brain.save_image('sensitivity_mag.png')
    # report.add_images_to_section('sensitivity_mag.png', 'sensitivity map',
    #                              'forward')
    # os.remove('sensitivity_mag.png')

    # fig = plt.figure()
    # plt.hist(mag_map.data.ravel(),
    #          bins=20, label=['Magnetometers'],
    #          color=['b'])
    # plt.title('Normal orientation sensitivity')
    # plt.xlabel('sensitivity')
    # plt.ylabel('count')
    # plt.legend()


Parallel(n_jobs=N_JOBS)(delayed(run_forward)(subject_id) for subject_id in range(1, 20))
