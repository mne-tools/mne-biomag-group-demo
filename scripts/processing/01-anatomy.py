"""
Run Freesurfer/MNE anatomical pipeline
======================================

This runs Freesurfer recon-all on all subjects and computes the BEM surfaces
later used for forward modeling. BEM extraction is done using flash MRI data.

Make sure that Freesurfer is properly configured before running this script.
See the `Setup & Configuration`_ section of the Freesurfer manual.

.. _Setup & Configuration: https://surfer.nmr.mgh.harvard.edu/fswiki/DownloadAndInstall#Setup.26Configuration  # noqa: E501
"""
import os
import os.path as op
import glob
import shutil
import subprocess
import time

import mne
from mne.parallel import parallel_func
import nibabel as nib

from library.config import study_path, subjects_dir, N_JOBS, spacing


def tee_output(command, log_file):
    with open(log_file, 'wb') as fid:
        proc = subprocess.Popen(
            command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        for line in proc.stdout:
            # print(line.decode('utf-8'))
            fid.write(line)
    if proc.wait() != 0:
        raise RuntimeError('Command failed')


def process_subject_anat(subject_id, force_recon_all=False):
    subject = "sub%03d" % subject_id
    print("Processing %s" % subject)

    t1_fname = "%s/ds117/%s/anatomy/highres001.nii.gz" % (study_path, subject)
    log_fname = "%s/ds117/%s/my-recon-all.txt" % (study_path, subject)
    subject_dir = op.join(subjects_dir, subject)
    if op.isdir(subject_dir):
        print('  Skipping reconstruction (folder exists)')
    else:
        print('  Running reconstruction (usually takes hours)...')
        t0 = time.time()
        tee_output(
            ['recon-all', '-all', '-s', subject, '-sd', subjects_dir,
             '-i', t1_fname], log_fname)
        print('  Recon for %s complete in %0.1f hours'
              % (subject_id, (time.time() - t0) / 60. / 60.))

    # Move flash data
    fnames = glob.glob("%s/ds117/%s/anatomy/FLASH/meflash*"
                       % (study_path, subject))
    dst_flash = "%s/%s/mri/flash" % (subjects_dir, subject)
    if not op.isdir(dst_flash):
        print('  Copying FLASH files')
        os.makedirs(dst_flash)
        for f_src in fnames:
            f_dst = op.basename(f_src).replace("meflash_", "mef")
            f_dst = op.join(dst_flash, f_dst)
            shutil.copy(f_src, f_dst)

        # Fix the headers for subject 19
        if subject_id == 19:
            print('  Fixing FLASH files for subject 19')
            fnames = (['mef05_%d.mgz' % x for x in range(7)] +
                      ['mef30_%d.mgz' % x for x in range(7)])
            for fname in fnames:
                dest_fname = op.join(dst_flash, fname)
                dest_img = nib.load(dest_fname)
                print("Fixing %s" % dest_fname)

                # Copy the headers from subjects 1
                src_img = nib.load(op.join(
                    subjects_dir, "sub001", "mri", "flash", fname))
                hdr = src_img.header
                fixed = nib.MGHImage(dest_img.get_data(), dest_img.affine, hdr)
                nib.save(fixed, dest_fname)

    # Make flash BEM
    if not op.isfile("%s/%s/mri/flash/parameter_maps/flash5.mgz"
                     % (subjects_dir, subject)):
        print('  Converting flash MRIs')
        mne.bem.convert_flash_mris(subject, convert=False,
                                   subjects_dir=subjects_dir, verbose=False)
    if not op.isfile("%s/%s/bem/flash/outer_skin.surf"
                     % (subjects_dir, subject)):
        print('  Making BEM')
        mne.bem.make_flash_bem(subject, subjects_dir=subjects_dir,
                               show=False, verbose=False)
    fname_bem_surfaces = op.join(subjects_dir, subject, 'bem',
                                 '%s-5120-5120-5120-bem.fif' % subject)
    if not op.isfile(fname_bem_surfaces):
        print('  Setting up BEM model')
        bem_model = mne.make_bem_model(
            subject, ico=4, subjects_dir=subjects_dir)
        mne.write_bem_surfaces(fname_bem_surfaces, bem_model)
    fname_bem = op.join(subjects_dir, subject, 'bem',
                        '%s-5120-5120-5120-bem-sol.fif' % subject)
    if not op.isfile(fname_bem):
        print('  Computing BEM solution')
        bem = mne.make_bem_solution(bem_model)
        mne.write_bem_solution(fname_bem, bem)

    # Create the surface source space
    fname_src = op.join(subjects_dir, subject, 'bem', '%s-%s-src.fif'
                        % (subject, spacing))
    if not op.isfile(fname_src):
        print('  Setting up source spcae')
        src = mne.setup_source_space(subject, spacing,
                                     subjects_dir=subjects_dir)
        mne.write_source_spaces(fname_src, src)


parallel, run_func, _ = parallel_func(process_subject_anat, n_jobs=N_JOBS)
parallel(run_func(subject_id) for subject_id in range(1, 20))
