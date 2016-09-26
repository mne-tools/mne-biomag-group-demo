.. title:: MNE

.. raw:: html

    <div class="container"><div class="row">
      <div class="col-md-12">
        <div style="text-align:center">
          <a href="http://martinos.org/mne">
            <img src="_static/mne_logo.png" border="0" alt="MNE">
          </a>
        </div>
      </div>

Authors
-------

- `Alexandre Gramfort <http://alexandre.gramfort.net/>`_, Telecom ParisTech
- `Mainak Jas <http://perso.telecom-paristech.fr/~mjas/>`_, Telecom ParisTech
- `Jaakko Leppäkangas <https://github.com/jaeilepp>`_, Telecom ParisTech
- `Denis Engemann <http://www.denis-engemann.de/>`_, INRIA, Parietal Team

Content
-------

The aim of this web site is to demonstrate the use of MNE to process the data from the SPM tutorial
`"Multimodal, Multisubject data fusion" <http://www.fil.ion.ucl.ac.uk/spm/doc/manual.pdf#Chap:data:multi>`_.
The data processed here consists of simultaneous magneto-/electroencephalography (M/EEG) recordings from 19 participants
performing a simple visual recognition task from presentations of famous, unfamiliar and scrambled faces.

We provide the full scripts to analyse the data, going from the files on `OpenfMRI <https://openfmri.org/>`_, to processed data ready to
make publication quality figures at the single subject and at the group level.

The scripts are provided on `mne-biomag-group-demo github repository <https://github.com/mne-tools/mne-biomag-group-demo/>`_

Dataset description
-------------------

This is a mulimodal dataset containing simultaneous M/EEG recordings on 19 healthy subjects.
Subjects were presented with 6 sessions of 10 minutes duration each. In the original study, three subjects
(sub001, sub005, sub016) were excluded from the analysis.

Stimulation details
^^^^^^^^^^^^^^^^^^^
* The start of a trial was indicated with a fixation cross of random duration between 400 to 600 ms
* The face stimuli was superimposed on the fixation cross for a random duration of 800 to 1,000 ms
* Interstimlus interval of 1,700 ms comprised a central white circle
* Two types of stimulation patterns:
  - Immediate: The image was presented consecutively
  - Long: The two images were presented with 5-15 intervening stimuli
  For the purposes of our analysis, we treat these two patterns of stimuli together
* To maintain attention, subjects were asked to judge the symmetry of the image and respond with a keypress

Acquisition details
^^^^^^^^^^^^^^^^^^^
* Sampling frequency : 1100 Hz
* Stimulation triggers: The trigger channel is STI101 with the following event codes:
  - Famous faces: 5 (first), 6 (immediate), and 7 (long)
  - Unfamiliar faces: 13 (first), 14 (immediate), and 15 (long)
  - Scrambled faces: 17 (first), 18 (immediate), and 19 (long)
* Sensors
  - 102 magnetometers
  - 204 planar gradiometers
  - 70 electrodes recorded with a nose reference (Easycap conforming to extended 10-20% system)
* Two sets of bipolar electrodes were used to measure vertical (left eye; EEG062) and
  horizontal electro-oculograms (EEG061). Another set was used to measure ECG (EEG063)
* A fixed 34 ms delay exists between the appearance of a trigger in the trigger channel STI101 and the appearance
  of the stimulus on the screen

What's next?
------------

.. toctree::
    :maxdepth: 2

    /auto_examples/index


**Disclaimer** : The scripts provide very little details on the tools used. We recommend you to visit the `MNE web site <http://martinos.org/mne/>`_ and especially the `tutorials <http://martinos.org/mne/stable/tutorials.html>`_ to learn more.

.. raw:: html

   </div>
