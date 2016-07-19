from . import transcribe_script
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

def main(annotation_filename, output_filename=None):
    transcribe_script(annotation_filename=annotation_filename, output_filename=output_filename)
