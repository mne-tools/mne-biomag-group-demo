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
    study_path = os.path.join(op.dirname("__file__"), '..', '..', '..')
    N_JOBS = 1

subjects_dir = os.path.join(study_path, 'subjects')
meg_dir = os.path.join(study_path, 'MEG')

os.environ["SUBJECTS_DIR"] = subjects_dir

if not os.path.isdir(subjects_dir):
    os.mkdir(subjects_dir)
