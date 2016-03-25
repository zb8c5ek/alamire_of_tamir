from . import transcribe_script


def main(annotation_filename, output_filename=None):
    transcribe_script(annotation_filename=annotation_filename, output_filename=output_filename)
