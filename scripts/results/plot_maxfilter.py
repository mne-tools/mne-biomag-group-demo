"""
Maxwell filtering
=================

Demonstrates maxwell filtering for one run (sub001, run01) using MNE-python.
"""

import os.path as op

import mne
from mne import Epochs
from mne.preprocessing import maxwell_filter

from library.config import study_path, cal, ctc

event_ids = [5, 6, 7]  # Famous faces

subject = "sub001"

raw_fname_in = op.join(study_path, 'ds117', subject, 'MEG', 'run_01_raw.fif')
sss_fname_in = op.join(study_path, 'ds117', subject, 'MEG', 'run_01_sss.fif')

###############################################################################
# First the filtered raw data.
raw = mne.io.read_raw_fif(raw_fname_in, preload=True)

raw.info['bads'] = ['MEG1031', 'MEG1111']  # set bads
picks = mne.pick_types(raw.info, meg=True, exclude='bads')
raw.filter(1, 40, fir_window='hann', l_trans_bandwidth=0.5, phase='zero',
           h_trans_bandwidth='auto', filter_length='10s')

events = mne.find_events(raw, stim_channel='STI101', consecutive='increasing',
                         mask=4352, mask_type='not_and', min_duration=0.003,
                         verbose=True)
evoked_before = Epochs(raw, events, event_id=event_ids, picks=picks).average()

###############################################################################
# Then Maxfiltered and tSSS'd data.
raw = mne.io.read_raw_fif(raw_fname_in, preload=True)
raw_sss = mne.io.read_raw_fif(sss_fname_in, preload=True)
raw.info['bads'] = ['MEG1031', 'MEG1111']
raw_sss.info['bads'] = ['MEG1031', 'MEG1111']

raw = maxwell_filter(raw, calibration=cal, cross_talk=ctc, st_duration=5.)

raw.filter(1, 40, fir_window='hann', l_trans_bandwidth=0.5, phase='zero',
           h_trans_bandwidth='auto', filter_length='10s')
raw_sss.filter(1, 40, fir_window='hann', l_trans_bandwidth=0.5, phase='zero',
               h_trans_bandwidth='auto', filter_length='10s')

evoked_after = Epochs(raw, events, event_id=event_ids, picks=picks).average()
evoked_sss = Epochs(raw_sss, events, event_id=event_ids, picks=picks).average()

###############################################################################
# Plotting
evoked_before.plot(spatial_colors=True,
                   titles={'grad': 'Gradiometers before SSS',
                           'mag': 'Magnetometers before SSS'})
evoked_after.plot(spatial_colors=True,
                  titles={'grad': 'tSSS gradiometers',
                          'mag': 'tSSS magnetometers'})
evoked_sss.plot(spatial_colors=True,
                titles={'grad': 'Maxfilter (tm) gradiometers',
                        'mag': 'Maxfilter (tm) magnetometers'})
