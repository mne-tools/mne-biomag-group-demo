import os

study_path = '/tsi/doctorants/data_gramfort/dgw_faces'

subjects_dir = os.path.join(study_path, 'subjects')
meg_dir = os.path.join(study_path, 'MEG')

os.environ["SUBJECTS_DIR"] = subjects_dir

spacing = 'oct6'

if not os.path.isdir(subjects_dir):
    os.mkdir(subjects_dir)
