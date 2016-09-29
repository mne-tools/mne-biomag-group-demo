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
        ax.plot(f, 10 * np.log10((H * H.conj()).real),
                linewidth=2, zorder=4, label='$f_p$=%0.1f Hz' % f_p)
        xticks = [1, 2, 4, 10, 20, 40, 100, 200, 400]
        ax.set(xlim=xlim, ylim=ylim, xticks=xticks, xlabel='Frequency (Hz)',
               ylabel='Amplitude (dB)')
        ax.set(xticklabels=xticks)
        ax.set_title('MNE default %s ' % label)
    box_off(ax)
    plt.legend(loc='lower right', ncol=1)
plt.tight_layout()
plt.show()
