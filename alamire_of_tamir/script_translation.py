import os

from read_write_init import *


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
