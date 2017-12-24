Group analysis with MNE
=======================

The code contains the [MNE](http://martinos.org/mne/) contribution to the [Biomag 2016](http://www.biomag2016.org/) satellite meeting

["How to perform MEG group analysis with free academic software"](http://www.biomag2016.org/satellite_meetings2.php)

Results of our analysis is presented [here](http://mne-tools.github.io/mne-biomag-group-demo/)

Steps to replicate
------------------

First, clone the repository using git::

	$ git clone https://github.com/mne-tools/mne-biomag-group-demo.git

Then go to the directory `mne-biomag-group-demo` and check out the tag `v0.1` using the command::

	$ git checkout tags/v0.1

This ensures that you use the same code which was used to produce the results in the paper.

Next, make sure your system is properly configured. You should have the following
installed::

	Python packages: numpy, scipy, matplotlib, scikit-learn, pysurfer, mayavi, mne-python, sphinx_gallery
	Anatomy: freesurfer

Then, go to the `scripts/processing` folder and do::

	$ make check

If should check that your system is properly configured. It tests that you have
`mne` installed as well as `freesurfer`. It also recommends you set the
OMP_NUM_THREADS environment variable. This limits the number CPUs used by
linear algebra routines.

If you don't get any error you can do::

	$ make all

This will fetch the data from openfmri, then run freesurfer on all subjects
and then do the analysis with MNE. The full analysis may take up to a week
if running on a 16 GB workstation with a single process.

You may want to edit the file `scripts/processing/library/config.py` 
to specify the number of subjects you can to run in parallel (N_JOBS). Note that
using more `N_JOBS` will increase the memory requirements as the data will be
copied across parallel processes.

Once this is done, you can go in the folder `scripts/doc` where you can
type::

	$ make html

This will build the website with all the results (takes around a few hours).

Authors
-------

- [Mainak Jas](http://perso.telecom-paristech.fr/~mjas/), Telecom ParisTech
- [Eric Larson](http://larsoner.com), University of Washington ILABS
- [Denis Engemann](http://denis-engemann.de), Neurospin, CEA/INSERM, UNICOG Team
- Jaakko Leppäkangas, Telecom ParisTech
- [Samu Taulu](http://ilabs.washington.edu/institute-faculty/bio/i-labs-samu-taulu-dsc), University of Washington, ILABS
- [Matti Hämäläinen](https://www.martinos.org/user/5923), Martinos Center, MGH, Harvard Medical School
- [Alexandre Gramfort](http://alexandre.gramfort.net), Telecom ParisTech

Abstract (of the satellite meeting)
-----------------------------------
<details>
<summary>Free academic toolboxes have gained increasing prominence in MEG analysis as a means to disseminate cutting edge </summary>
<p>methods, share best practices between different research groups and pool resources for developing essential tools for the MEG community. In the recent years large and vibrant research communities have emerged around several of these toolboxes. Teaching events are regularly held around the world where the basics of each toolbox are explained by its respective developers and experienced power users. There are, however, two knowledge gaps that our BIOMAG satellite symposium aims to address. Firstly, most teaching examples only show analysis of a single ‘typical best’ subject whereas most real MEG studies involve analysis of group data. It is then left to the researchers in the field to figure out for themselves how to make the transition and obtain significant group results. Secondly, we are not familiar with any examples of fully analyzing the same group dataset with different academic toolboxes to assess the degree of agreement in scientific conclusions and compare strengths and weaknesses of various analysis methods and their independent implementations. Our workshop is organised by the lead developers of six most popular free academic MEG toolboxes (in alphabetic order): Brainstorm, EEGLAB, FieldTrip, MNE, NUTMEG, and SPM. Ahead of the workshop the research team for each toolbox will analyze the same group MEG/EEG dataset. This dataset containing evoked responses to face stimuli was acquired by Richard Henson and Daniel Wakeman, who won a special award at BIOMAG2010 to make it freely available to the community. All the raw data are available at https://openfmri.org/dataset/ds000117/.

Detailed instructions for each toolbox will be made available online including analysis scripts and figures of results. All analyses will show a full pipeline from the raw data to detailed publication quality results. Researchers who are interested in using the respective toolbox will then be able to reproduce the analysis in their lab and port it to their own data.

At the workshop each group will briefly introduce their software and present the key results from their analysis. This will be followed by a panel discussion and questions from the audience.

Following the event we plan to integrate the suggestions and questions from the workshop audience and to publish the analyses details as part of a special research topic in Frontiers in Neuroscience, section Brain Imaging Methods so that the proposed best practices will be endorsed by peer review and become citable in future publications. Other research groups will be invited to contribute to the research topic as long as they present detailed descriptions of analyses of group data that are freely available online and make it possible for others to fully reproduce their analysis and results.

We hope that this proposal will lead to creation of invaluable resource for the whole MEG community and the workshop will contribute to establishment of good practice and promoting consistent and reproducible analyses approaches. The event will also showcase all the toolboxes and will be of interest to beginners in the field with basic background in MEG who contemplate the most suitable analysis approach and software for their study as well as to experienced researchers who would like to get up to date with the latest methodological developments.
</p>
</details>
