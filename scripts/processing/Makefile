PYTHON = python

nohighpass:
	$(PYTHON) 02-python_filtering.py
	$(PYTHON) 04-run_ica.py
	$(PYTHON) 05-make_epochs.py
	$(PYTHON) 06-make_evoked.py

preproc:
	$(PYTHON) 02-maxwell_filtering.py
	$(PYTHON) 02-python_filtering.py
	$(PYTHON) 03-run_extract_events.py
	$(PYTHON) 04-run_ica.py
	$(PYTHON) 05-make_epochs.py
	$(PYTHON) 06-make_evoked.py
	$(PYTHON) 07-time_frequency.py
	$(PYTHON) 08-run_time_decoding.py
	$(PYTHON) 09-group_average_sensors.py
	$(PYTHON) 11-make_watershed.py
	$(PYTHON) 12-make_forward.py
	$(PYTHON) 13-make_inverse.py
	$(PYTHON) 14-group_average_source.py

profile:
	mprof run 02-python_filtering.py
	mprof plot -o python_filtering
	mprof run 03-run_extract_events.py
	mprof plot -o extract_events
	mprof run 04-run_ica.py
	mprof plot -o run_ica
	mprof run 05-make_epochs.py
	mprof plot -o make_epochs
	mprof run 06-make_evoked.py
	mprof plot -o make_evoked
	mprof run 07-time_frequency.py
	mprof plot -o time_frequency
	mprof run 08-run_time_decoding.py
	mprof plot -o run_time_decoding
	mprof run 09-group_average_sensors.py
	mprof plot -o group_average_sensors
	mprof run 11-make_watershed.py
	mprof plot -o make_watershed
	mprof run 12-make_forward.py
	mprof plot -o make_forward
	mprof run 13-make_inverse.py
	mprof plot -o make_inverse
	mprof run 14-group_average_source.py
	mprof plot -o group_average_source
