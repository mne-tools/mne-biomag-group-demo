"""
===========================
Plotting the analysis chain
===========================

Run the analysis.
"""
from mne.externals.tempita import Template

with open('template_analysis.py') as f:
    lines = f.readlines()
template = Template(''.join(lines))
for subject in range(1, 20):
    py_str = template.substitute(subject_id=subject)

    with open('plot_analysis_%s.py' % subject, 'w') as f:
        f.write(py_str)
