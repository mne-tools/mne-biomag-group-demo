.. -*- coding: utf-8 -*-

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

- `Mainak Jas <http://perso.telecom-paristech.fr/~mjas/>`_, Telecom ParisTech
- `Eric Larson <http://larsoner.com>`_, University of Washington, ILABS
- `Denis Engemann <http://www.denis-engemann.de/>`_, Neurospin, CEA/INSERM, UNICOG Team
- `Jaakko Leppäkangas <https://github.com/jaeilepp>`_, Telecom ParisTech
- `Samu Taulu <http://ilabs.washington.edu/institute-faculty/bio/i-labs-samu-taulu-dsc>`_, University of Washington, ILABS
- `Matti Hämäläinen <https://www.martinos.org/user/5923>`_, Martinos Center, MGH, Harvard Medical School
- `Alexandre Gramfort <http://alexandre.gramfort.net/>`_, Telecom ParisTech

Slides of presentation at Biomag 2016 Conf.
-------------------------------------------

`Link to presented slides <http://www.slideshare.net/agramfort/mne-group-analysis-presentation-biomag-2016-conf>`_

Content
-------

The aim of this web site is to demonstrate the use of MNE to process the data from the SPM tutorial
`"Multimodal, Multisubject data fusion" <http://www.fil.ion.ucl.ac.uk/spm/doc/manual.pdf#Chap:data:multi>`_.
The data processed here consists of simultaneous magneto-/electroencephalography (M/EEG) recordings from 19 participants
performing a simple visual recognition task from presentations of famous, unfamiliar and scrambled faces.

We provide the full scripts to analyse the data, going from the files on OpenfMRI_, to processed data ready to
make publication quality figures at the single subject and at the group level.

The scripts are provided on `mne-biomag-group-demo github repository <https://github.com/mne-tools/mne-biomag-group-demo/>`_

The original dataset analysis is available `here <https://www.ncbi.nlm.nih.gov/pubmed/25977808>`_.

The code contains the `MNE <http://martinos.org/mne/>`_ contribution to the `Biomag 2016 <http://www.biomag2016.org/>`_ satellite meeting `"How to perform MEG group analysis with free academic software" <http://www.biomag2016.org/satellite_meetings2.php>`_

Abstract (of the satellite meeting)
-----------------------------------

Free academic toolboxes have gained increasing prominence in MEG analysis as a means to disseminate cutting edge methods, share best practices between different research groups and pool resources for developing essential tools for the MEG community. In the recent years large and vibrant research communities have emerged around several of these toolboxes. Teaching events are regularly held around the world where the basics of each toolbox are explained by its respective developers and experienced power users. There are, however, two knowledge gaps that our BIOMAG satellite symposium aims to address. Firstly, most teaching examples only show analysis of a single ‘typical best’ subject whereas most real MEG studies involve analysis of group data. It is then left to the researchers in the field to figure out for themselves how to make the transition and obtain significant group results. Secondly, we are not familiar with any examples of fully analyzing the same group dataset with different academic toolboxes to assess the degree of agreement in scientific conclusions and compare strengths and weaknesses of various analysis methods and their independent implementations. Our workshop is organised by the lead developers of six most popular free academic MEG toolboxes (in alphabetic order): Brainstorm, EEGLAB, FieldTrip, MNE, NUTMEG, and SPM. Ahead of the workshop the research team for each toolbox will analyze the same group MEG/EEG dataset. This dataset containing evoked responses to face stimuli was acquired by Richard Henson and Daniel Wakeman, who won a special award at BIOMAG2010 to make it freely available to the community. All the raw data are available on OpenFMRI_.

Detailed instructions for each toolbox will be made available online including analysis scripts and figures of results. All analyses will show a full pipeline from the raw data to detailed publication quality results. Researchers who are interested in using the respective toolbox will then be able to reproduce the analysis in their lab and port it to their own data.

At the workshop each group will briefly introduce their software and present the key results from their analysis. This will be followed by a panel discussion and questions from the audience.

Following the event we plan to integrate the suggestions and questions from the workshop audience and to publish the analyses details as part of a special research topic in Frontiers in Neuroscience, section Brain Imaging Methods so that the proposed best practices will be endorsed by peer review and become citable in future publications. Other research groups will be invited to contribute to the research topic as long as they present detailed descriptions of analyses of group data that are freely available online and make it possible for others to fully reproduce their analysis and results.

We hope that this proposal will lead to creation of invaluable resource for the whole MEG community and the workshop will contribute to establishment of good practice and promoting consistent and reproducible analyses approaches. The event will also showcase all the toolboxes and will be of interest to beginners in the field with basic background in MEG who contemplate the most suitable analysis approach and software for their study as well as to experienced researchers who would like to get up to date with the latest methodological developments.

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

  * Immediate: The image was presented consecutively
  * Long: The two images were presented with 5-15 intervening stimuli
* For the purposes of our analysis, we treat these two stimulation patterns of stimuli together
* To maintain attention, subjects were asked to judge the symmetry of the image and respond with a keypress

Acquisition details
^^^^^^^^^^^^^^^^^^^
* Sampling frequency : 1100 Hz
* Stimulation triggers: The trigger channel is STI101 with the following event codes:

  * Famous faces: 5 (first), 6 (immediate), and 7 (long)
  * Unfamiliar faces: 13 (first), 14 (immediate), and 15 (long)
  * Scrambled faces: 17 (first), 18 (immediate), and 19 (long)
* Sensors

  * 102 magnetometers
  * 204 planar gradiometers
  * 70 electrodes recorded with a nose reference (Easycap conforming to extended 10-20% system)
* Two sets of bipolar electrodes were used to measure vertical (left eye; EEG062) and
  horizontal electro-oculograms (EEG061). Another set was used to measure ECG (EEG063)
* A fixed 34 ms delay exists between the appearance of a trigger in the trigger channel STI101 and the appearance
  of the stimulus on the screen

What's next?
------------

Take a look at our scripts and results

* :doc:`auto_scripts/index`
* :doc:`auto_examples/index`

**Disclaimer** : The scripts provide very little details on the tools used. We recommend you to visit the `MNE web site <http://martinos.org/mne/>`_ and especially the `tutorials <http://martinos.org/mne/stable/tutorials.html>`_ to learn more.

.. raw:: html

   </div>

.. _OpenFMRI: https://openfmri.org/dataset/ds000117/
