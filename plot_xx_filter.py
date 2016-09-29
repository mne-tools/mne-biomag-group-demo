"""
Select filters
==============

Here we look at the choice of filters
"""
import numpy as np
from scipy import signal
import matplotlib.pyplot as plt

sfreq = 1100.
ylim = [-60, 10]  # for dB plots
xlim = [0, 5.]


def box_off(ax):
    """Helper to beautify plot."""
    ax.grid(zorder=0)
    for key in ('top', 'right'):
        ax.spines[key].set_visible(False)


fig, axes = plt.subplots(1, 2, sharex=True, sharey=True, figsize=(12, 6))
labels = ['v0.12', 'v0.13']
for ax, label in zip(axes, labels):
    for f_p in [1, 1.5, 2.5]:  # passband corner frequency
        if label == 'v0.12':
            transition_band = 0.5
            filter_dur = 10
            window = 'hann'
        elif label == 'v0.13':
            transition_band = np.minimum(np.maximum(0.25 * f_p, 2.), f_p)
            filter_dur = 6.6 / transition_band  # sec
            window = 'hamming'

        f_s = f_p - transition_band
        n = int(sfreq * filter_dur)
        n += ~(n % 2)  # Type II filter can't have 0 attenuation at nyq

        # design the filter
        freq = [0., f_s, f_p, sfreq / 2.]
        gain = [0., 0., 1., 1.]
        h = signal.firwin2(n, freq, gain, nyq=sfreq / 2., window=window)

        # plot freqency response
        f, H = signal.freqz(h)
        f *= sfreq / (2 * np.pi)
        ax.plot(f, 20 * np.log10(np.abs(H)),
                linewidth=2, zorder=4, label='$f_p$=%0.1f Hz' % f_p)
        ax.set(xlim=xlim, ylim=ylim, xlabel='Frequency (Hz)')
        ax.set_title('MNE default %s ' % label)
    box_off(ax)
    plt.legend(loc='lower right', ncol=1)
axes[0].set_ylabel('Amplitude (dB)')
plt.tight_layout()
plt.show()
