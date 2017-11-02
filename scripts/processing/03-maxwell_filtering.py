"""
===================================
03. Maxwell filter using MNE-python
===================================

The data are Maxwell filtered using tSSS and movement compensation.

Using tSSS with a short duration can be used as an alternative to highpass
filtering. Here we will use the default (10 sec) and a short window (1 sec).

It is critical to mark bad channels before Maxwell
filtering. Here for consistency we exploit the MaxFilter log files for
determining the bad channels.

The data are also lowpass filtered at 40 Hz using linear-phase FIR filter with
delay compensation. The transition bandwidth is automatically defined. See
`Background information on filtering <http://mne-tools.github.io/dev/auto_tutorials/plot_background_filtering.html>`_
for more. The filtered data are saved to separate files to the subject's'MEG'
directory.
"""  # noqa: E501

import os
import os.path as op
from warnings import warn

import numpy as np

import mne

from library.config import study_path, meg_dir, N_JOBS, cal, ctc, l_freq


def run_maxwell_filter(subject_id):
    subject = "sub%03d" % subject_id
    print("processing subject: %s" % subject)
    sss_fname_out = op.join(meg_dir, subject, 'run_%02d_filt_tsss_%d_raw.fif')

    raw_fname_in = op.join(study_path, 'ds117', subject, 'MEG',
                           'run_%02d_raw.fif')
    sss_fname_in = op.join(study_path, 'ds117', subject, 'MEG',
                           'run_%02d_sss.fif')

    # To match their processing, transform to the head position of the 4th run
    info = mne.io.read_info(sss_fname_in % 4)
    destination = info['dev_head_t']
    # Get the origin they used
    origin = info['proc_history'][0]['max_info']['sss_info']['origin']

    for run in range(1, 7):
        raw_in = raw_fname_in % run
        try:
            raw = mne.io.read_raw_fif(raw_in)
        except AttributeError:
            # Some files on openfmri are corrupted and cannot be read.
            warn('Could not read file %s. '
                 'Skipping run %s from subject %s.' % (raw_in, run, subject))
            continue
        print('  Run %s' % (run,))

        raw.set_channel_types({
            'EEG061': 'eog',
            'EEG062': 'eog',
            'EEG063': 'ecg',
            'EEG064': 'misc'
        })  # EEG064 free floating el.
        raw.rename_channels({
            'EEG061': 'EOG061',
            'EEG062': 'EOG062',
            'EEG063': 'ECG063'
        })
        raw.fix_mag_coil_types()

        # Read bad channels from the MaxFilter log.
        with open(
                op.join(study_path, 'ds117', subject, 'MEG',
                        'run_%02d_sss_log.txt' % run)) as fid:
            for line in fid:
                if line.startswith('Static bad channels'):
                    chs = line.split(':')[-1].split()
                    bads = ['MEG%04d' % int(ch) for ch in chs]
                    break
        raw.info['bads'] += bads

        # Get the head positions from the existing SSS file.
        # Usually this can be done by saving to a text file with MaxFilter
        # instead, and reading with :func:`mne.chpi.read_head_pos`.
        raw_sss = mne.io.read_raw_fif(sss_fname_in % run, verbose='error')
        chpi_picks = mne.pick_types(raw_sss.info, meg=False, chpi=True)
        assert len(chpi_picks) == 9
        head_pos, t = raw_sss[chpi_picks]
        # Add first_samp.
        t = t + raw_sss.first_samp / raw_sss.info['sfreq']
        # The head positions in the FIF file are all zero for invalid positions
        # so let's remove them, and then concatenate our times.
        mask = (head_pos != 0).any(axis=0)
        head_pos = np.concatenate((t[np.newaxis], head_pos)).T[mask]
        # In this dataset due to old MaxFilter (2.2.10), data are uniformly
        # sampled at 1 Hz, so we save some processing time in
        # maxwell_filter by downsampling.
        skip = int(round(raw_sss.info['sfreq']))
        head_pos = head_pos[::skip]
        del raw_sss

        for st_duration in (10, 1):
            print('    st_duration=%d' % (st_duration,))
            raw_sss = mne.preprocessing.maxwell_filter(
                raw, calibration=cal, cross_talk=ctc, st_duration=st_duration,
                origin=origin, destination=destination, head_pos=head_pos)

            raw_out = sss_fname_out % (run, st_duration)

            # Here we only low-pass MEG (assuming MaxFilter has high-passed
            # the data already), but we still need to band-pass EEG:
            picks_meg = mne.pick_types(raw.info, meg=True, exclude=())
            raw_sss.filter(
                None, 40, l_trans_bandwidth='auto', h_trans_bandwidth='auto',
                filter_length='auto', phase='zero', fir_window='hamming',
                fir_design='firwin', n_jobs=N_JOBS, picks=picks_meg)
            picks_eeg = mne.pick_types(raw.info, eeg=True, exclude=())
            raw_sss.filter(
                l_freq, 40, l_trans_bandwidth='auto', h_trans_bandwidth='auto',
                filter_length='auto', phase='zero', fir_window='hamming',
                fir_design='firwin', n_jobs=N_JOBS, picks=picks_eeg)
            # High-pass EOG to get reasonable thresholds in autoreject
            picks_eog = mne.pick_types(raw.info, meg=False, eog=True)
            raw_sss.filter(
                l_freq, None, picks=picks_eog, l_trans_bandwidth='auto',
                filter_length='auto', phase='zero', fir_window='hann',
                fir_design='firwin')
            raw_sss.save(raw_out, overwrite=True)


run_maxwell_filter(subject_id=3)  # Only for sub003
