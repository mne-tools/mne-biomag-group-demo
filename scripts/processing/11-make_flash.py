"""
Create BEM surfaces
===================

Create BEM surfaces using flash images.
"""

import mne

from library.config import subjects_dir

exclude = [1, 5, 16]  # Excluded subjects

for subject_id in range(1, 19):

    if subject_id in exclude:
        continue
    subject = "sub%03d" % subject_id
    mne.bem.make_flash_bem(subject, subjects_dir=subjects_dir, overwrite=True,
                           show=False)
