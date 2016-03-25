from script_translation import script_transcription


def transcribe_script(annotation_filename, output_filename=None):
    print "This is version 0.12"
    script_transcription(annotation_filename, output_filename)
