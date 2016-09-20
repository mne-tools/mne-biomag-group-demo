"""
===========================
Plotting the analysis chain
===========================

Run the analysis.
"""
import os.path as op

from mne.externals.tempita import Template

with open(op.join(op.dirname(__file__), 'template_analysis.py')) as f:
    lines = f.readlines()
template = Template(unicode(''.join(lines)))
for subject in range(1, 20):
    py_str = template.substitute(subject_id=subject)

    with open(op.join(op.dirname(__file__),
              'plot_analysis_%s.py' % subject), 'w') as f:
        f.write(py_str)
