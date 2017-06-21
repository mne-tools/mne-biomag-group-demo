"""
Create BEM surfaces
===================

Create BEM surfaces using watershed algorithm.
"""

import mne

from library.config import subjects_dir

for subject_id in range(1, 20):  # subject 019 left out
    subject = "sub%03d" % subject_id
    mne.bem.make_flash_bem(subject, subjects_dir=subjects_dir, overwrite=True,
                           show=False)
