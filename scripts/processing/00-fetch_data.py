"""
==========================
00. Fetch data on OpenfMRI
==========================

This script gives some basic code that can be adapted to fetch data.
"""

import os
from library.config import study_path, subjects_dir

pwd = os.getcwd()

if not os.path.exists(study_path):
    os.mkdir(study_path)

if not os.path.exists(os.path.join(study_path, 'ds117')):
    os.mkdir(os.path.join(study_path, 'ds117'))
os.chdir(os.path.join(study_path, 'ds117'))

archive_dir = os.path.join(os.getcwd(), 'archive')

if not os.path.isdir(archive_dir):
    os.mkdir(archive_dir)

os.system('http://openfmri.s3.amazonaws.com/tarballs/ds117_R0.1.1_metadata.tgz')  # noqa: E501
os.system('tar xvzf ds117_R0.1.1_metadata.tgz')
os.system('mkdir metadata')
os.chdir(os.path.join(study_path, 'ds117', 'ds117'))
os.system('mv stimuli study_key.txt models README scan_key.txt model_key.txt listing.txt license.txt emptyroom ../metadata/')  # noqa: E501
os.chdir(os.path.join(study_path, 'ds117'))
os.system('rmdir ds117')
os.system('mv ds117_R0.1.1_metadata.tgz archive/')

for i in range(1, 20):
    subject = "sub%03d" % i
    print("processing %s" % subject)
    fname = "ds117_R0.1.1_%s_raw.tgz" % subject
    url = "http://openfmri.s3.amazonaws.com/tarballs/" + fname
    if os.path.isdir(subject):
        continue
    os.system('wget %s' % url)
    os.system('tar xvzf %s' % fname)
    os.system('mv ds117/$subject .')
    os.system('mv $fname archive/')
    os.system('rmdir ds117')

os.chdir(pwd)

if not os.path.isdir(subjects_dir):
    os.mkdir(subjects_dir)
