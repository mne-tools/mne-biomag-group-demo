:orphan:

.. _processing_scripts:

Processing scripts
==================

.. contents:: Contents
   :local:
   :depth: 2


Setup
-----

.. raw:: html

    <div class="sphx-glr-thumbcontainer" tooltip="This script gives some basic code that can be adapted to fetch data. ">

.. only:: html

    .. figure:: /auto_scripts/images/thumb/sphx_glr_00-fetch_data_thumb.png

        :ref:`sphx_glr_auto_scripts_00-fetch_data.py`

.. raw:: html

    </div>


.. toctree::
   :hidden:

   /auto_scripts/00-fetch_data

.. raw:: html

    <div class="sphx-glr-thumbcontainer" tooltip="This runs Freesurfer recon-all on all subjects and computes the BEM surfaces later used for for...">

.. only:: html

    .. figure:: /auto_scripts/images/thumb/sphx_glr_01-anatomy_thumb.png

        :ref:`sphx_glr_auto_scripts_01-anatomy.py`

.. raw:: html

    </div>

.. toctree::
   :hidden:

   /auto_scripts/01-anatomy


.. raw:: html

    <div class="sphx-glr-thumbcontainer" tooltip="Configuration parameters for the study. This should be in a folder called ``library/`` inside t...">

.. only:: html

    .. figure:: /auto_scripts/library/images/thumb/sphx_glr_config_thumb.png

        :ref:`sphx_glr_auto_scripts_library_config.py`

.. raw:: html

    </div>


.. toctree::
   :hidden:

   /auto_scripts/library/config

.. toctree::
   :hidden:

   /auto_scripts/01-anatomy

.. raw:: html

    <div style='clear:both'></div>

Sensor space
------------

.. raw:: html

    <div class="sphx-glr-thumbcontainer" tooltip="The events are extracted from stimulus channel &#x27;STI101&#x27;. The events are saved to the subject&#x27;s ...">

.. only:: html

    .. figure:: /auto_scripts/images/thumb/sphx_glr_02-extract_events_thumb.png

        :ref:`sphx_glr_auto_scripts_02-extract_events.py`

.. raw:: html

    </div>


.. toctree::
   :hidden:

   /auto_scripts/02-extract_events

.. raw:: html

    <div class="sphx-glr-thumbcontainer" tooltip="The data are Maxwell filtered using tSSS and movement compensation.">

.. only:: html

    .. figure:: /auto_scripts/images/thumb/sphx_glr_03-maxwell_filtering_thumb.png

        :ref:`sphx_glr_auto_scripts_03-maxwell_filtering.py`

.. raw:: html

    </div>


.. toctree::
   :hidden:

   /auto_scripts/03-maxwell_filtering

.. raw:: html

    <div class="sphx-glr-thumbcontainer" tooltip="The data are bandpass filtered (1 - 40 Hz) using linear-phase fir filter with delay compensatio...">

.. only:: html

    .. figure:: /auto_scripts/images/thumb/sphx_glr_04-python_filtering_thumb.png

        :ref:`sphx_glr_auto_scripts_04-python_filtering.py`

.. raw:: html

    </div>


.. toctree::
   :hidden:

   /auto_scripts/04-python_filtering

.. raw:: html

    <div class="sphx-glr-thumbcontainer" tooltip="ICA decomposition using fastICA. ">

.. only:: html

    .. figure:: /auto_scripts/images/thumb/sphx_glr_05-run_ica_thumb.png

        :ref:`sphx_glr_auto_scripts_05-run_ica.py`

.. raw:: html

    </div>


.. toctree::
   :hidden:

   /auto_scripts/05-run_ica

.. raw:: html

    <div class="sphx-glr-thumbcontainer" tooltip="The epochs are constructed by using the events created in script 03. MNE supports hierarchical ...">

.. only:: html

    .. figure:: /auto_scripts/images/thumb/sphx_glr_06-make_epochs_thumb.png

        :ref:`sphx_glr_auto_scripts_06-make_epochs.py`

.. raw:: html

    </div>


.. toctree::
   :hidden:

   /auto_scripts/06-make_epochs

.. raw:: html

    <div class="sphx-glr-thumbcontainer" tooltip="The evoked data sets are created by averaging different categories of epochs. The evoked data i...">

.. only:: html

    .. figure:: /auto_scripts/images/thumb/sphx_glr_07-make_evoked_thumb.png

        :ref:`sphx_glr_auto_scripts_07-make_evoked.py`

.. raw:: html

    </div>


.. toctree::
   :hidden:

   /auto_scripts/07-make_evoked

.. raw:: html

    <div class="sphx-glr-thumbcontainer" tooltip="Covariance matrices are computed and saved. ">

.. only:: html

    .. figure:: /auto_scripts/images/thumb/sphx_glr_08-make_cov_thumb.png

        :ref:`sphx_glr_auto_scripts_08-make_cov.py`

.. raw:: html

    </div>


.. toctree::
   :hidden:

   /auto_scripts/08-make_cov

.. raw:: html

    <div class="sphx-glr-thumbcontainer" tooltip="The epoched data is transformed to time-frequency domain using morlet wavelets. Faces and scram...">

.. only:: html

    .. figure:: /auto_scripts/images/thumb/sphx_glr_09-time_frequency_thumb.png

        :ref:`sphx_glr_auto_scripts_09-time_frequency.py`

.. raw:: html

    </div>


.. toctree::
   :hidden:

   /auto_scripts/09-time_frequency

.. raw:: html

    <div class="sphx-glr-thumbcontainer" tooltip="A sliding estimator fits a logistic legression model for every time point. In this example, we ...">

.. only:: html

    .. figure:: /auto_scripts/images/thumb/sphx_glr_10-sliding_estimator_thumb.png

        :ref:`sphx_glr_auto_scripts_10-sliding_estimator.py`

.. raw:: html

    </div>


.. toctree::
   :hidden:

   /auto_scripts/10-sliding_estimator

.. raw:: html

    <div class="sphx-glr-thumbcontainer" tooltip="The EEG-channel data are averaged for group averages. ">

.. only:: html

    .. figure:: /auto_scripts/images/thumb/sphx_glr_11-group_average_sensors_thumb.png

        :ref:`sphx_glr_auto_scripts_11-group_average_sensors.py`

.. raw:: html

    </div>


.. toctree::
   :hidden:

   /auto_scripts/11-group_average_sensors

.. raw:: html

    <div class="sphx-glr-thumbcontainer" tooltip="Calculate forward solution for MEG channels. ">

.. only:: html

    .. figure:: /auto_scripts/images/thumb/sphx_glr_12-make_forward_thumb.png

        :ref:`sphx_glr_auto_scripts_12-make_forward.py`

.. raw:: html

    </div>

.. raw:: html

    <div style='clear:both'></div>

Source space
------------

.. toctree::
   :hidden:

   /auto_scripts/12-make_forward

.. raw:: html

    <div class="sphx-glr-thumbcontainer" tooltip="Compute inverse solution for each evoked data set. ">

.. only:: html

    .. figure:: /auto_scripts/images/thumb/sphx_glr_13-make_inverse_thumb.png

        :ref:`sphx_glr_auto_scripts_13-make_inverse.py`

.. raw:: html

    </div>


.. toctree::
   :hidden:

   /auto_scripts/13-make_inverse

.. raw:: html

    <div class="sphx-glr-thumbcontainer" tooltip="Source estimates are morphed to the ``fsaverage`` brain. ">

.. only:: html

    .. figure:: /auto_scripts/images/thumb/sphx_glr_14-group_average_source_thumb.png

        :ref:`sphx_glr_auto_scripts_14-group_average_source.py`

.. raw:: html

    </div>


.. toctree::
   :hidden:

   /auto_scripts/14-group_average_source

.. raw:: html

    <div class="sphx-glr-thumbcontainer" tooltip="Compute LCMV beamformer. ">

.. only:: html

    .. figure:: /auto_scripts/images/thumb/sphx_glr_15-lcmv_beamformer_thumb.png

        :ref:`sphx_glr_auto_scripts_15-lcmv_beamformer.py`

.. raw:: html

    </div>


.. toctree::
   :hidden:

   /auto_scripts/15-lcmv_beamformer

.. raw:: html

    <div class="sphx-glr-thumbcontainer" tooltip="Source estimates are computed for contrast between faces and scrambled and morphed to average b...">

.. only:: html

    .. figure:: /auto_scripts/images/thumb/sphx_glr_16-group_average_lcmv_thumb.png

        :ref:`sphx_glr_auto_scripts_16-group_average_lcmv.py`

.. raw:: html

    </div>


.. toctree::
   :hidden:

   /auto_scripts/16-group_average_lcmv

.. raw:: html

    <div class="sphx-glr-thumbcontainer" tooltip="Builds an html report containing all the relevant analysis plots. ">

.. only:: html

    .. figure:: /auto_scripts/images/thumb/sphx_glr_99-make_reports_thumb.png

        :ref:`sphx_glr_auto_scripts_99-make_reports.py`

.. raw:: html

    </div>


.. toctree::
   :hidden:

   /auto_scripts/99-make_reports


.. raw:: html

    <div style='clear:both'></div>



.. only :: html

 .. container:: sphx-glr-footer


  .. container:: sphx-glr-download

    :download:`Download all examples in Python source code: auto_scripts_python.zip <//mnt/bakraid/larsoner/mne-biomag-group-demo/mne-biomag-group-demo/scripts/doc/auto_scripts/auto_scripts_python.zip>`



  .. container:: sphx-glr-download

    :download:`Download all examples in Jupyter notebooks: auto_scripts_jupyter.zip <//mnt/bakraid/larsoner/mne-biomag-group-demo/mne-biomag-group-demo/scripts/doc/auto_scripts/auto_scripts_jupyter.zip>`


.. only:: html

 .. rst-class:: sphx-glr-signature

    `Gallery generated by Sphinx-Gallery <https://sphinx-gallery.readthedocs.io>`_
