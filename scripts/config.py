import os

if os.environ['USER'] == 'gramfort':
    study_path = '/tsi/doctorants/data_gramfort/dgw_faces'
    N_JOBS = 8
else:
    study_path = os.path.join(os.path.dirname(__file__), '..')
    N_JOBS = 1

subjects_dir = os.path.join(study_path, 'subjects')
meg_dir = os.path.join(study_path, 'MEG')

os.environ["SUBJECTS_DIR"] = subjects_dir

spacing = 'oct6'
mindist = 5

if not os.path.isdir(subjects_dir):
    os.mkdir(subjects_dir)
