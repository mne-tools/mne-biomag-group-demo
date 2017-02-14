"""
===========
Config file
===========

Configuration parameters for the study. Place them in a folder called
``library/`` inside the ``results/`` and ``processing/`` folders.
"""

import os

###############################################################################
# Let's set the path where the data is downloaded and stored.

user = os.environ['USER']
if user == 'gramfort':
    study_path = '/tsi/doctorants/data_gramfort/dgw_faces'
    N_JOBS = 8
elif user == 'mjas':
    study_path = '/tsi/doctorants/data_gramfort/dgw_faces'
    N_JOBS = 4
elif user == 'jleppakangas':
    study_path = '/tsi/doctorants/data_gramfort/dgw_faces'
    N_JOBS = 8
elif user == 'alex':
    study_path = '/Users/alex/work/data/mne-biomag-group-demo/'
    N_JOBS = 1
else:
    study_path = os.path.join(os.path.dirname(__file__), '..', '..', '..')
    N_JOBS = 1

###############################################################################
# The ``subjects_dir`` and ``meg_dir`` for reading anatomical and MEG files.

subjects_dir = os.path.join(study_path, 'subjects')
meg_dir = os.path.join(study_path, 'MEG')

os.environ["SUBJECTS_DIR"] = subjects_dir

spacing = 'oct5'
mindist = 5

###############################################################################
# Some mapping betwen filenames for bad sensors and subjects

map_subjects = {1: 'subject_01', 2: 'subject_02', 3: 'subject_03',
                4: 'subject_05', 5: 'subject_06', 6: 'subject_08',
                7: 'subject_09', 8: 'subject_10', 9: 'subject_11',
                10: 'subject_12', 11: 'subject_14', 12: 'subject_15',
                13: 'subject_16', 14: 'subject_17', 15: 'subject_18',
                16: 'subject_19', 17: 'subject_23', 18: 'subject_24',
                19: 'subject_25'}

if not os.path.isdir(subjects_dir):
    os.mkdir(subjects_dir)

###############################################################################
# The `cross talk file <https://github.com/mne-tools/mne-biomag-group-demo/blob/master/scripts/results/library/ct_sparse.fif>`_
# and `calibration file <https://github.com/mne-tools/mne-biomag-group-demo/blob/master/scripts/results/library/sss_cal.dat>`_
# are placed in the same folder.

ctc = os.path.join(os.path.dirname(__file__), '..', '..', 'results', 'library',
                   'ct_sparse.fif')
cal = os.path.join(os.path.dirname(__file__), '..', '..', 'results', 'library',
                   'sss_cal.dat')

ylim = {'eeg': [-10, 10], 'mag': [-300, 300], 'grad': [-80, 80]}
