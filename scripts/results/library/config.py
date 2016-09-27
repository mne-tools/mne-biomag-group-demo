"""
Blabla
======================

blabla
"""

import os

user = os.environ['USER']
if user == 'gramfort':
    study_path = '/tsi/doctorants/data_gramfort/dgw_faces'
    N_JOBS = 8
elif user == 'jleppakangas' or user == 'mjas':
    study_path = '/tsi/doctorants/data_gramfort/dgw_faces'
    N_JOBS = 4
else:
    study_path = os.path.join(os.path.dirname(__file__), '..', '..', '..')
    N_JOBS = 1

subjects_dir = os.path.join(study_path, 'subjects')
meg_dir = os.path.join(study_path, 'MEG')

os.environ["SUBJECTS_DIR"] = subjects_dir

spacing = 'oct6'
mindist = 5
map_subjects = {1: 'subject_01', 2: 'subject_02', 3: 'subject_03',
                4: 'subject_05', 5: 'subject_06', 6: 'subject_08',
                7: 'subject_09', 8: 'subject_10', 9: 'subject_11',
                10: 'subject_12', 11: 'subject_14', 12: 'subject_15',
                13: 'subject_16', 14: 'subject_17', 15: 'subject_18',
                16: 'subject_19', 17: 'subject_23', 18: 'subject_24',
                19: 'subject_25'}

if not os.path.isdir(subjects_dir):
    os.mkdir(subjects_dir)

ctc = os.path.join(os.path.dirname(__file__), 'ct_sparse.fif')
cal = os.path.join(os.path.dirname(__file__), 'sss_cal.dat')

ylim = {'eeg': [-15, 15], 'mag': [-200, 200], 'grad': [-50, 50]}
