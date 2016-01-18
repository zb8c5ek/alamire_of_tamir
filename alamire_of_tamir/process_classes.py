__author__ = 'Xuanli CHEN'

"""
    PhD Student at VISICS, KU Leuven
    xuanli.chen@esat.kuleuven.be
"""

import music21 as m21
import numpy as np
import xml.etree.cElementTree as ET


class NoteAndRest(object):
    """
        Stand for each element in the musical score, e.g. A pitch, rest etc.
        Track: different songs, normally one.
        Channel: different voices. In Alamire, normally four.
    """

    def __init__(self):
        # self.id = None
        self.track = None
        self.channel = None  # Channel is also the part, stands for different players.
        self.volume = None
        self.pitch = None
        self.time = None
        self.duration = None
        self.time_sig = None
        self.clef = None
        self.program = None

    def write_into_file(self, opened_file):
        """
        Output the properties into the opened file
        """
        opened_file.write('\n')
        # opened_file.write('object: %d\n' % self.id)
        opened_file.write('track: %d\n' % self.track)
        opened_file.write('channel: %d\n' % self.channel)
        opened_file.write('volume: %d\n' % self.volume)
        opened_file.write('pitch: %d\n' % self.pitch)
        opened_file.write('time: %d\n' % self.time)
        opened_file.write('duration: %d\n' % self.duration)
        if self.time_sig is not None:
            opened_file.write('time_sig: %d %d\n' % (self.time_sig[0], self.time_sig[1]))
        if self.clef is not None:
            opened_file.write('clef: %s\n' % self.clef)
        if self.program is not None:
            opened_file.write('program: %d\n' % self.program)


class MXLNote(object):
    """
        The note of the score.
    """

    def __init__(self, raw_note=None):

        self.rest = False
        self.dot = 0
        # ======== Pitch Part =======
        self.pitchStep = None  # C, F, G etc.
        self.pitchAlter = None  # Accidentals, Minus for Flat while Positive for Sharp, 0 for Natural
        self.pitchOctave = None  # The position in the Octave ==> The midi transformation could be done by M21.
        # ========    End    ========
        self.duration = None
        self.type = None
        self.stem = None

        if raw_note is not None:
            self.read_from_root(raw_note)

    def read_from_root(self, raw_note):

        for child in raw_note:
            if child.tag == 'rest':
                self.rest = True
            elif child.tag == 'dot':
                self.dot = 1
            elif child.tag == 'pitch':
                for sub_child in child:
                    if sub_child.tag == 'step':
                        self.pitchStep = sub_child.text
                    elif sub_child.tag == 'octave':
                        self.pitchOctave = sub_child.text
                    elif sub_child.tag == 'alter':
                        self.pitchAlter = sub_child.text

            elif child.tag == 'duration':
                self.duration = child.text
            elif child.tag == 'type':
                self.type = child.text
            elif child.tag == 'stem':
                self.stem = child.text

    def write_into_xml(self, root):

        if self.rest:
            ET.SubElement(root, "rest")
        else:
            now_pitch_root = ET.SubElement(root, "pitch")
            ET.SubElement(now_pitch_root, "step").text = self.pitchStep
            ET.SubElement(now_pitch_root, "octave").text = self.pitchOctave
            if self.pitchAlter is not None:
                ET.SubElement(now_pitch_root, "alter").text = self.pitchAlter

        if self.dot > 0:
            ET.SubElement(root, "dot")
        if self.duration is not None:
            ET.SubElement(root, "duration").text = self.duration
        if self.type is not None:
            ET.SubElement(root, "type").text = self.type
        if self.stem is not None:
            ET.SubElement(root, "stem").text = self.type

    def to_m21_object(self):

        if not self.rest:
            new_note = m21.note.Note(self.pitchStep + self.pitchOctave)
            if self.pitchAlter is not None:

                if self.pitchAlter > 0:
                    new_note.accidental = 'sharp'
                elif self.pitchAlter == 0:
                    new_note.accidental = 'natural'
                elif self.pitchAlter < 0:
                    new_note.accidental = 'flat'

                new_note.accidental.alter = np.float(self.pitchAlter)

        else:
            new_note = m21.note.Rest()

        new_note.duration.type = self.type
        new_note.duration.dots = np.int(self.dot)

        return new_note


class MXLMeasure(object):
    """
        The measure of the score.
    """

    def __init__(self):
        self.number = None
        self.divisions = 10080  # Quarter
        self.keyFifths = None


class MXLPart:
    """
        The part of the score.
    """

    def __init__(self, part_root=None):
        """
            The part_root should be processed by ET first.
        """

        # self.root = part_root
        self.name = 'NoPartName'
        self.scoreInstrumentID = None
        self.scoreInstrumentName = 'NoInstrumentName'
        self.midiInstrumentID = None
        self.midiChannel = None
        self.midiProgram = None
        # ===== From 1st Measure =====
        self.keyFifths = None
        self.keyMode = None

        self.timeBeats = None
        self.timeBeatType = None

        self.clefSign = None
        self.clefLine = None
        # =====  End ======

        self.content = []

        if part_root is not None:
            self.read_from_root(part_root)

    def read_from_root(self, part_root):
        """
            Get the notes information from self.root
            * Assume the key, time signature and clef information are contained in the first measure of this Part.
        """

        measure = part_root[0]
        for child in measure:
            # print child.tag

            if child.tag == 'attributes':
                for deeper_child in child:
                    if deeper_child.tag == 'key':
                        for sub_child in deeper_child:
                            if sub_child.tag == 'fifths':
                                self.keyFifths = sub_child.text
                            elif sub_child.tag == 'mode':
                                self.keyMode = sub_child.text
                    elif deeper_child.tag == 'time':
                        for sub_child in deeper_child:
                            if sub_child.tag == 'beats':
                                self.timeBeats = sub_child.text
                            elif sub_child.tag == 'beat-type':
                                self.timeBeatType = sub_child.text
                    elif deeper_child.tag == 'clef':
                        for sub_child in deeper_child:
                            if sub_child.tag == 'sign':
                                self.clefSign = sub_child.text
                            elif sub_child.tag == 'line':
                                self.clefLine = sub_child.text

        for measure in part_root:
            for child in measure:
                # print child.tag
                if child.tag == 'note':
                    now_note = MXLNote(child)
                    self.content.append(now_note)

    def to_m21_object(self):

        new_part = m21.stream.Part()

        key = m21.key.KeySignature(np.int(self.keyFifths), self.keyMode)
        time_signature = m21.meter.TimeSignature(self.timeBeats + '/' + self.timeBeatType)
        clef = m21.clef.Clef()
        clef.line = self.clefLine
        clef.sign = self.clefSign

        new_part.append(key)
        new_part.append(time_signature)
        new_part.append(clef)

        for note in self.content:
            new_part.append(note.to_m21_object())

        return new_part

    def write_into_xml(self, root):

        # Generate the first Measure so that The reading regular could Maintain.
        measure_root = ET.SubElement(root, "measure", number="1")
        # ================== Attributes Information ==================
        attribute_root = ET.SubElement(measure_root, "attributes")

        key_root = ET.SubElement(attribute_root, "key")
        ET.SubElement(key_root, "fifths").text = self.keyFifths
        ET.SubElement(key_root, "mode").text = self.keyMode

        time_root = ET.SubElement(attribute_root, "time")
        ET.SubElement(time_root, "beats").text = self.timeBeats
        ET.SubElement(time_root, "beat-type").text = self.timeBeatType

        clef_root = ET.SubElement(attribute_root, "clef")
        ET.SubElement(clef_root, "sign").text = self.clefSign
        ET.SubElement(clef_root, "line").text = self.clefLine
        # ========================== End =============================

        for note in self.content:
            now_note_root = ET.SubElement(measure_root, "note")
            note.write_into_xml(now_note_root)


class MXLScore(object):
    """
        This class is to represent the Score file.
    """

    def __init__(self, root_score):

        self.parts = []
        self.title = 'Test'
        self.composer = 'Alamire'
        self.otl = 'Flemish Chord'
        if root_score is not None:
            for child in root_score:
                # print 'Score==> %s' % child.tag
                if child.tag == 'part':
                    # print child.tag
                    new_part = MXLPart(child)
                    self.parts.append(new_part)
                    # print '======================'

    def to_m21_object(self):

        new_score = m21.stream.Stream()
        new_meta = m21.metadata.Metadata()
        new_meta.title = self.title
        new_meta.composer = self.composer
        new_meta.otl = self.otl
        new_score.insert(new_meta)
        for child in self.parts:
            # print 'Score==>', child.tag
            # new_score.append(child.to_m21_object())
            # print '=================='
            new_score.insert(0, child.to_m21_object())

        return new_score

    def write_into_xml(self, out_filename):

        root = ET.Element("score-partwise")
        work = ET.SubElement(root, "work")
        ET.SubElement(work, "work-title").text = self.title
        identification = ET.SubElement(root, "identification")
        ET.SubElement(identification, "creator", type="composer").text = self.composer

        count = 0

        for part in self.parts:
            count += 1
            now_part_root = ET.SubElement(root, "part", id="P" + str(count))
            part.write_into_xml(now_part_root)

        tree = ET.ElementTree(root)
        tree.write(out_filename)


class MXLFile(object):
    """
        This class aims to dealing with the whole file of MXL.
    """

    def __init__(self):
        self.head = '<?xml version="1.0" encoding="utf-8"?>\n'
        self.docType = "<!DOCTYPE score-partwise PUBLIC\n'-//Recordare//DTD MusicXML 2.0 Partwise//EN'\n'http://www.musi" \
                       "cxml.org/dtds/partwise.dtd'\nGenerated by: Xuanli Chen, VISICS, ESAT, KU Leuven\nEmail: " \
                       "xuanli.chen@esat.kuleuven.be>"
        self.workTitle = 'NoWorkTitle'
        self.movementTitle = 'NoMovementTitle'
        self.composer = 'Anonymous'
        self.scalingMillimeters = 7
        self.scalingTenths = 40

        self.partGroupNumber = 1  # Check the number of parts first.
        self.partGroupType = "start"
        self.partGroupSymbol = "bracket"
        self.partGroupBarline = "yes"

        self.partList = []


# ====================================== Mensural Notation Development Below ========================================

class MensuralPart:
    """
        The mensural part of the score.
    """

    def __init__(self, part_root=None):
        """
            The part_root should be processed by ET first.
        """

        # self.root = part_root
        self.name = 'NoPartName'
        self.scoreInstrumentID = None
        self.scoreInstrumentName = 'NoInstrumentName'
        self.midiInstrumentID = None
        self.midiChannel = None
        self.midiProgram = None
        # ===== From 1st Measure =====
        self.keyFifths = None
        self.keyMode = None

        self.timeBeats = None
        self.timeBeatType = None

        self.clefSign = None
        self.clefLine = None
        # =====  End ======

        self.content = []

        if part_root is not None:
            self.read_from_root(part_root)

    def read_from_root(self, part_root):
        """
            Get the notes information from self.root
            * Assume the key, time signature and clef information are contained in the first measure of this Part.
        """

        measure = part_root[0]
        for child in measure:
            # print child.tag

            if child.tag == 'attributes':
                for deeper_child in child:
                    if deeper_child.tag == 'key':
                        for sub_child in deeper_child:
                            if sub_child.tag == 'fifths':
                                self.keyFifths = sub_child.text
                            elif sub_child.tag == 'mode':
                                self.keyMode = sub_child.text
                    elif deeper_child.tag == 'time':
                        for sub_child in deeper_child:
                            if sub_child.tag == 'beats':
                                self.timeBeats = sub_child.text
                            elif sub_child.tag == 'beat-type':
                                self.timeBeatType = sub_child.text
                    elif deeper_child.tag == 'clef':
                        for sub_child in deeper_child:
                            if sub_child.tag == 'sign':
                                self.clefSign = sub_child.text
                            elif sub_child.tag == 'line':
                                self.clefLine = sub_child.text

        for measure in part_root:
            for child in measure:
                # print child.tag
                if child.tag == 'note':
                    now_note = MensuralNote(child)
                    self.content.append(now_note)

    def to_m21_object(self):

        new_part = m21.stream.Part()

        key = m21.key.KeySignature(np.int(self.keyFifths), self.keyMode)
        time_signature = m21.meter.TimeSignature(self.timeBeats + '/' + self.timeBeatType)
        clef = m21.clef.Clef()
        clef.line = self.clefLine
        clef.sign = self.clefSign

        new_part.append(key)
        new_part.append(time_signature)
        new_part.append(clef)

        for note in self.content:
            new_part.append(note.to_m21_object())

        return new_part


class MensuralNote(object):
    """
        The mensural note of the score.
    """

    def __init__(self, raw_note=None):

        self.rest = False
        self.dot = 0
        # ======== Pitch Part =======
        self.pitchStep = None  # C, F, G etc.
        self.pitchAlter = None  # Accidentals, Minus for Flat while Positive for Sharp, 0 for Natural
        self.pitchOctave = None  # The position in the Octave ==> The midi transformation could be done by M21.
        # ========    End    ========
        self.duration = None
        self.type = None
        self.stem = None

        if raw_note is not None:
            self.read_from_root(raw_note)

    def read_from_root(self, raw_note):

        for child in raw_note:
            if child.tag == 'rest':
                self.rest = True
            elif child.tag == 'dot':
                self.dot = 1
            elif child.tag == 'pitch':
                for sub_child in child:
                    if sub_child.tag == 'step':
                        self.pitchStep = sub_child.text
                    elif sub_child.tag == 'octave':
                        self.pitchOctave = sub_child.text
                    elif sub_child.tag == 'alter':
                        self.pitchAlter = sub_child.text

            elif child.tag == 'duration':
                self.duration = child.text
            elif child.tag == 'type':
                self.type = child.text
            elif child.tag == 'stem':
                self.stem = child.text

    def write_into_xml(self, root):

        if self.rest:
            ET.SubElement(root, "rest")
        else:
            now_pitch_root = ET.SubElement(root, "pitch")
            ET.SubElement(now_pitch_root, "step").text = self.pitchStep
            ET.SubElement(now_pitch_root, "octave").text = self.pitchOctave
            if self.pitchAlter is not None:
                ET.SubElement(now_pitch_root, "alter").text = self.pitchAlter

        if self.dot > 0:
            ET.SubElement(root, "dot")
        if self.duration is not None:
            ET.SubElement(root, "duration").text = self.duration
        if self.type is not None:
            ET.SubElement(root, "type").text = self.type
        if self.stem is not None:
            ET.SubElement(root, "stem").text = self.type

    def to_m21_object(self):

        if not self.rest:
            new_note = m21.note.Note(self.pitchStep + self.pitchOctave)
            if self.pitchAlter is not None:

                if self.pitchAlter > 0:
                    new_note.accidental = 'sharp'
                elif self.pitchAlter == 0:
                    new_note.accidental = 'natural'
                elif self.pitchAlter < 0:
                    new_note.accidental = 'flat'

                new_note.accidental.alter = np.float(self.pitchAlter)

        else:
            new_note = m21.note.Rest()

        new_note.duration.type = self.type
        new_note.duration.dots = np.int(self.dot)

        return new_note