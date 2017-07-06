import matplotlib.pyplot as plt
import os.path as op

import mne
from library.config import meg_dir, set_matplotlib_defaults

subject = 'sub001'

plt.style.use('seaborn-white')
set_matplotlib_defaults(plt)

evo_fname = op.join(meg_dir, subject, '%s-ave.fif' % subject)
evoked = mne.read_evokeds(evo_fname)

famous_evo, scrambled_evo, unfamiliar_evo, contrast_evo, faces_evo = evoked
cov = mne.read_cov(op.join(meg_dir, subject, '%s-cov.fif' % subject))
fig = faces_evo.copy().pick_types(eeg=False).plot_white(cov)
axes = fig.axes
axes[0].set_ylabel('Whitened data (A.U.)')
axes[1].set_title('')
axes[1].legend_.remove()
fig.set_size_inches(8, 6, forward=True)
plt.tight_layout()
fig.savefig('plot_white.pdf', bbox_to_inches='tight')

