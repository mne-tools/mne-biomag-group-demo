"""
===========================
Plotting the analysis chain
===========================

Run the analysis.
"""
import codecs
import os.path as op

from mne.externals.tempita import Template

with codecs.open(op.join(op.dirname(__file__), 'template_analysis.py'),
                 'r', 'utf-8') as f:
    lines = f.readlines()
template = Template(u''.join(lines))
for subject in range(1, 20):
    py_str = template.substitute(subject_id='%02d' % subject)
    out_fname = op.join(op.dirname(__file__), '..', '..',
                        'results', 'single_subject_analysis',
                        'plot_analysis_%02d.py' % subject)
    with codecs.open(out_fname, 'w', 'utf-8') as f:
        f.write(py_str)
