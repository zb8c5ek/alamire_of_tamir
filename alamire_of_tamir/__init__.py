__author__ = 'Xuanli Chen'
"""
Xuanli Chen
PhD student at PSI-VISICS, KU Leuven
Supervisor: Prof. Luc Van Gool
Focus Domain: Machine Learning, Music, Computer Vision
Email: xuanli.chen@esat.kuleuven.be

Address:
Kasteelpark Arenberg 10 - bus 2441
B-3001 Heverlee
Belgium

Group website: http://www.esat.kuleuven.be/psi/visics
LinkedIn: https://be.linkedin.com/in/xuanlichen
"""
from script_translation import script_transcription


def transcribe_script(annotation_filename, output_filename=None):
    print "This is version 0.12"
    script_transcription(annotation_filename, output_filename)
