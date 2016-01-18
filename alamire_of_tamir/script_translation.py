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

from read_write_init import *

filename = '/Users/Xuanli-iMac/Develop/alamire/data/B-BrusSG_9424_frontcover_forTranscription.annotation'
output_filename = '/Users/Xuanli-iMac/Develop/alamire/data/B-BrusSG_9424_frontcover_transcripted.xml'

ann = AnnotationPage()
ann.read_annotation_file(filename)
s = ann.process_modern()

s.write('xml', output_filename)
