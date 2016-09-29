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


###############################################################################
# The defaults in MNE 0.12 are slightly different from the defaults in
# MNE 0.13. We define a convenience function to get the defaults for each
# version. For more detailed information regarding these choices, head over
# to the `filtering tutorial <http://mne-tools.github.io/stable/auto_tutorials/plot_background_filtering.html>`_
# on the MNE website.
def get_filter_defaults(version, filter_type):
    window = 'hann'
    if version == '0.12':
        f_w = 0.5  # Transition bandwidth (Hz)
        filter_dur = 10.  # seconds
    elif version == '0.13':
        if filter_type == 'highpass':
            f_w = min(max(0.25 * f_p, 2.), f_p)  # Hz
        else:
            f_w = min(max(0.25 * f_p, 2.), sfreq / 2. - f_p)  # Hz
        filter_dur = 6.6 / f_w  # sec

    return window, f_w, filter_dur


###############################################################################
# Then, we define a function to design the filters using
# :func:`scipy.signal.firwin2`.
def design_filter(filter_type, f_p, f_w, filter_dur, window):
    if filter_type == 'highpass':
        f_s = f_p - f_w
        freq = [0., f_s, f_p, sfreq / 2.]
        gain = [0., 0., 1., 1.]
    else:
        f_s = f_p + f_w
        freq = [0., f_p, f_s, sfreq / 2.]
        gain = [1., 1., 0., 0.]

    n = int(sfreq * filter_dur)
    n += ~(n % 2)  # Type II filter can't have 0 attenuation at nyq

    h = signal.firwin2(n, freq, gain, nyq=sfreq / 2., window=window)
    return h


###############################################################################
# To choose our filters, we plot the frequency response of the filter (in dB).
# Higher attenuation is good for reducing noise.
def plot_filter_response(ax, h, xlim, label):
    f, H = signal.freqz(h)
    f *= sfreq / (2 * np.pi)
    ax.plot(f, 20 * np.log10(np.abs(H)),
            linewidth=2, zorder=4, label=label)
    ax.set(xlim=xlim, ylim=ylim, xlabel='Frequency (Hz)',
           ylabel='Amplitude (dB)')
    box_off(ax)


###############################################################################
# However, filters can introduce ripples in the time domain. So, we also plot
# the impulse response ``h`` of the filter.
def plot_impulse_response(ax, h, label):
    dur = 10.
    h_plot = np.zeros((int(dur * sfreq), ))
    start = len(h_plot) // 2 - len(h) // 2
    stop = start + len(h)
    h_plot[start:stop] = h
    t = np.arange(len(h_plot)) / sfreq - dur / 2
    ax.plot(t, h_plot, linewidth=2, label=label)
    ax.set(xlim=(-0.1, 0.1), xlabel='Time (s)', ylabel='Amplitude of h')
    ax.legend()
    box_off(ax)


###############################################################################
# Before we start plotting, let us define a simple function to turn off boxes
# in a plot. It takes as argument the axis handle ``ax``.
def box_off(ax):
    """Helper to beautify plot."""
    ax.grid(zorder=0)
    for key in ('top', 'right'):
        ax.spines[key].set_visible(False)


###############################################################################
# Now we plot the frequency response and impulse response for the lowpass
# and highpass filters in MNE versions 0.12 and 0.13.
fig, axes = plt.subplots(2, 2, figsize=(12, 8))

xlim = dict(highpass=[0, 4.], lowpass=[35, 55])
ylim = [-40, 10]  # for dB plots
f_ps = [1., 40.]  # corner frequencies (Hz)
filter_types = ['highpass', 'lowpass']

for ax, f_p, filter_type in zip(axes.T, f_ps, filter_types):

    # MNE old defaults
    window, f_w, filter_dur = get_filter_defaults('0.12', filter_type)
    h = design_filter(filter_type, f_p, f_w, filter_dur, window)
    lbl = 'MNE (0.12)' + ('' if filter_type == 'lowpass' else ' (Used)')
    plot_filter_response(ax[0], h, xlim[filter_type], label=lbl)
    plot_impulse_response(ax[1], h, lbl)

    # MNE new defaults
    window, f_w, filter_dur = get_filter_defaults('0.13', filter_type)
    h = design_filter(filter_type, f_p, f_w, filter_dur, window)
    lbl = 'MNE (0.13)' + ('' if filter_type == 'highpass' else ' (Used)')
    plot_filter_response(ax[0], h, xlim[filter_type], label=lbl)
    plot_impulse_response(ax[1], h, label=lbl)

    # Ideal gain
    freq = [0, f_p, f_p, sfreq / 2.]
    min_gain = 10 ** (ylim[0] / 20)
    if filter_type == "highpass":
        gain = [min_gain, min_gain, 1, 1]
    else:
        gain = [1, 1, min_gain, min_gain]
    ax[0].plot(freq, 20 * np.log10(gain), 'r--', alpha=0.5,
               linewidth=4, zorder=3, label='Ideal')
    ax[0].legend()
    ax[0].set_title(filter_type + " (cutoff %s Hz)" % f_p)

plt.tight_layout()
plt.show()
