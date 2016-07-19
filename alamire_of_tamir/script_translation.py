import os
from read_write_init import *
"""
Xuanli Chen
PhD student at PSI-VISICS, KU Leuven
Supervisor: Prof. Luc Van Gool
Research Domain: Computer Vision, Machine Learning
Address:
Kasteelpark Arenberg 10 - bus 2441
B-3001 Heverlee
Belgium
Group website: http://www.esat.kuleuven.be/psi/visics
LinkedIn: https://be.linkedin.com/in/xuanlichen
"""

def script_transcription(
        annotation_file='/users/visics/xchen/project_Alamire/alamire/dots_test.annotation',
        out_file=None):
    if out_file is None:
        stem, ext = os.path.splitext(annotation_file)
        out_file = stem + 'translated.xml'

    ann = AnnotationPage()
    ann.read_annotation_file(annotation_file)
    s = ann.process_modern()

    s.write('xml', out_file)
    print "File Translation Accomplished! Results saved in: %s " % out_file
