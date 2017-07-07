import matplotlib.pyplot as plt
import os.path as op

import mne
from library.config import meg_dir, set_matplotlib_defaults

subject = 'sub004'

plt.style.use('seaborn-white')
set_matplotlib_defaults(plt)

raw_fname = op.join(meg_dir, subject,
                    'run_01_filt_sss_highpass-1Hz_raw.fif')
raw = mne.io.read_raw_fif(raw_fname, preload=True)
rank_meg = raw.pick_types(eeg=False).estimate_rank()

evo_fname = op.join(meg_dir, subject, '%s_highpass-1Hz_ave.fif' % subject)
evoked = mne.read_evokeds(evo_fname)

famous_evo, scrambled_evo, unfamiliar_evo, contrast_evo, faces_evo = evoked
cov = mne.read_cov(op.join(meg_dir, subject,
                   '%s_highpass-1Hz-cov.fif' % subject))
fig = mne.viz.evoked._plot_evoked_white(contrast_evo.pick_types(eeg=False),
                                        cov,
                                        rank={'meg': rank_meg})
# fig = contrast_evo.copy().pick_types(eeg=False).plot_white(cov)
axes = fig.axes
axes[0].set_ylabel('Whitened data (A.U.)')
axes[1].set_title('')
axes[1].set_ylabel('Global Field Power')
# axes[1].legend_.remove()
fig.set_size_inches(8, 6, forward=True)
plt.tight_layout()
fig.savefig('plot_white.pdf', bbox_to_inches='tight')
