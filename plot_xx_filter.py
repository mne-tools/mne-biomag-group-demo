"""
Select filters
==============

Here we look at the choice of filters both for low and high
pass.
"""
import numpy as np
from scipy import signal
import matplotlib.pyplot as plt

sfreq = 1100.
ylim = [-40, 10]  # for dB plots
xlim = dict(highpass=[0, 4.], lowpass=[35, 55])


def box_off(ax):
    """Helper to beautify plot."""
    ax.grid(zorder=0)
    for key in ('top', 'right'):
        ax.spines[key].set_visible(False)


def design_filter(label, f_p, transition_band, filter_dur, window):
    if label == 'highpass':
        f_s = f_p - transition_band
        # design the filter
        freq = [0., f_s, f_p, sfreq / 2.]
        gain = [0., 0., 1., 1.]
    else:
        f_s = f_p + transition_band
        # design the filter
        freq = [0., f_p, f_s, sfreq / 2.]
        gain = [1., 1., 0., 0.]

    n = int(sfreq * filter_dur)
    n += ~(n % 2)  # Type II filter can't have 0 attenuation at nyq

    h = signal.firwin2(n, freq, gain, nyq=sfreq / 2., window=window)
    return h


def plot_filter(ax, h, xlim, label):
    # plot freqency response
    f, H = signal.freqz(h)
    f *= sfreq / (2 * np.pi)
    ax.plot(f, 20 * np.log10(np.abs(H)),
            linewidth=2, zorder=4, label=label)
    ax.set(xlim=xlim, ylim=ylim, xlabel='Frequency (Hz)')
    box_off(ax)


fig, axes = plt.subplots(1, 2, sharey=True, figsize=(12, 4))
f_ps = [1., 40.]
labels = ['highpass', 'lowpass']
for ax, f_p, label in zip(axes, f_ps, labels):
    # MNE old defaults
    transition_band = 0.5  # Hz
    filter_dur = 10.  # seconds
    window = 'hann'
    h = design_filter(label, f_p, transition_band, filter_dur, window)
    plot_filter(ax, h, xlim[label],
                label='MNE (0.12)' + ('' if label == 'lowpass' else ' (Used)'))

    # MNE new defaults
    if label == "highpass":
        transition_band = min(max(0.25 * f_p, 2.), f_p)  # Hz
        ideal_gain = [0, 0, 1, 1]
    else:
        transition_band = min(max(0.25 * f_p, 2.), sfreq / 2. - f_p)  # Hz
        ideal_gain = [1, 1, 0, 0]

    filter_dur = 6.6 / transition_band  # sec
    window = 'hamming'
    h = design_filter(label, f_p, transition_band, filter_dur, window)
    plot_filter(ax, h, xlim[label],
                label='MNE (0.13)' + ('' if label == 'highpass' else ' (Used)'))

    ideal_freq = [0, f_p, f_p, sfreq / 2.]
    ideal_gain = np.array(ideal_gain, dtype=float)
    ideal_gain[ideal_gain == 0.] = 10 ** (ylim[0] / 20)
    ax.plot(ideal_freq, 20 * np.log10(ideal_gain), 'r--', alpha=0.5, linewidth=4,
            zorder=3, label='Ideal')
    ax.legend()
    ax.set_title(label + " (cutoff %s Hz)" % f_p)

axes[0].set_ylabel('Amplitude (dB)')
plt.tight_layout()
plt.show()
