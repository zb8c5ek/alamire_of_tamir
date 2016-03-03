__author__ = 'Xuanli CHEN'

"""
    PhD Student at VISICS, KU Leuven
    xuanli.chen@esat.kuleuven.be
"""
import music21 as m21


def get_general_text_position(text_position, clef_position=4, clef_sign='F'):
    """
    Compute the position as a Note.
    * C ==> Octave is 4, F ==> Octave is 3
    :return:
    """
    if clef_sign == 'F':
        octave = 3
    elif clef_sign == 'C':
        octave = 4
    else:
        octave = 4

    table = ['C', 'D', 'E', 'F', 'G', 'A', 'B']
    abs_position = int(float(text_position) / 0.5)
    offset = abs_position - clef_position * 2
    offset_note = table.index(clef_sign) + offset

    if offset_note > 6:
        offset_note -= 7
        octave_note = octave + 1
    elif offset_note < 0:
        offset_note += 7
        octave_note = octave - 1
    else:
        octave_note = octave

    # print 'Clef: %s    Position:' % clef_sign, clef_position, 'Text position: %s' % text_position, \
    #     'Result: %s' % table[offset_note] + str(octave_note)

    return table[offset_note] + str(octave_note)


class AnnotationObject(object):
    """
    This the annotation object, aiming to read in the annoatation file/ pre
    """

    def __init__(self):
        self.id = None
        self.bbox = []
        self.comments = None
        self.object_type = None
        self.text_position = None
        self.label_symbol = None
        self.musical_symbol = None
        self.channel = 0
        self.description = None
        self.comment = None

    def get_note_text_position(self, clef_position=4, clef_sign='F'):
        """
        Compute the position as a Note.
        * C ==> Octave is 4, F ==> Octave is 3
        :return:
        """
        if clef_sign == 'F':
            octave = 3
        elif clef_sign == 'C':
            octave = 4
        else:
            octave = 4

        table = ['C', 'D', 'E', 'F', 'G', 'A', 'B']
        abs_position = int(float(self.text_position) / 0.5)
        offset = abs_position - clef_position * 2
        offset_note = table.index(clef_sign) + offset

        if offset_note > 6:
            offset_note -= 7
            octave_note = octave + 1
        elif offset_note < 0:
            offset_note += 7
            octave_note = octave - 1
        else:
            octave_note = octave

        print 'Clef: %s    Position:' % clef_sign, clef_position, 'Text position: %s' % self.text_position, \
            'Result: %s' % table[offset_note] + str(octave_note)

        return table[offset_note] + str(octave_note)

    def get_text_position(self):
        """
        Process the text position
        :return:
        """
        # print 'Context position is: ', self.text_position
        return float(self.text_position)

    def write_into_file(self, opened_file):
        """
        Output the properties into the opened file
        """
        # The format of writing now changed. According the google doc shared by Yu-Hui, now there is 'predicted:'
        opened_file.write('\n')
        opened_file.write('object: %s \n' % self.id)
        opened_file.write('bbox: %s \n' % ",".join(map(str, self.bbox)))
        opened_file.write('object_type: %s \n' % self.object_type)
        opened_file.write('label_symbol: %s \n' % self.label_symbol)
        if self.musical_symbol is not None:
            opened_file.write('musical_symbol: %s \n' % self.musical_symbol)

        if len(self.text_position) == 1:
            opened_file.write('text_position: %s \n' % self.text_position[0])
        elif len(self.text_position) == 2:
            opened_file.write('text_position: %s \n' % ",".join(map(str, self.text_position)))

        if self.comments is not None:
            opened_file.write('comments: %s \n' % self.comments)

        if self.channel is not None:
            opened_file.write('channel: %d \n' % self.channel)

    def parse(self):
        """
            If the 'description' attribute is not None, a parsing is needed to get the value of other fields.
        """

        if 'note' in self.description:

            self.label_symbol = 'note'
            if 'semibreve' in self.description:
                self.musical_symbol = 'semibreve'
            elif 'breve' in self.description:
                self.musical_symbol = 'breve'
            elif 'semiminim' in self.description:
                self.musical_symbol = 'semiminim'
            elif 'minim' in self.description:
                self.musical_symbol = 'minim'
            elif 'longa' in self.description:
                self.musical_symbol = 'longa'
            elif 'maxima' in self.description:
                self.musical_symbol = 'maxima'
            else:
                raise "This string is illegal: %s" % self.description

        elif 'rest' in self.description:

            self.label_symbol = 'rest'
            if 'semibreve' in self.description:
                self.musical_symbol = 'semibreve'
            elif 'breve' in self.description:
                self.musical_symbol = 'breve'
            elif 'semiminim' in self.description:
                self.musical_symbol = 'semiminim'
            elif 'minim' in self.description:
                self.musical_symbol = 'minim'
            elif 'longa' in self.description:
                self.musical_symbol = 'longa'
            elif 'maxima' in self.description:
                self.musical_symbol = 'maxima'
            else:
                raise "This string is illegal: %s" % self.description

        elif 'clef' in self.description:
            c = self.description.split('_')
            self.label_symbol = c[0]
            self.musical_symbol = c[1]

        elif 'time_sig_Imin' in self.description:
            self.label_symbol = 'time_sig'
            # Explain the time signature, now support Imin, Imaj, Pmin, Pmaj, ** Cut property is presently ignored.
            if 'Imin' in self.description:
                self.musical_symbol = ['imperfect', 'minor']
            elif 'Imaj' in self.description:
                self.musical_symbol = ['imperfect', 'major']
            elif 'Pmin' in self.description:
                self.musical_symbol = ['perfect', 'minor']
            elif 'Pmaj' in self.description:
                self.musical_symbol = ['perfect', 'major']

        elif 'key_sig' in self.description:
            if 'flat' in self.description:
                self.label_symbol = 'key_sig'
                self.musical_symbol = 'flat'

        elif 'ligature' in self.description.lower():
            # Ligature Implementation
            self.label_symbol = 'ligature'
            self.musical_symbol = self.description.split('_')[1:]

        # elif 'comment' in self.description.lower():
        #
        #     self.comment =

        else:
            self.label_symbol = self.description
            self.musical_symbol = self.description

    def ligature_imperfect_parse(self, clef_position=4, clef_sign='F'):
        """
        Parsing the ligature and generate a note list.
        @:param
        @:
        """
        # FD
        # print "Ligature Processing!"

        temp = []

        for c in self.musical_symbol:
            if 'OO' in c:
                t = c.index('OO') + 1
                temp.append(c[:t])
                temp.append(c[t:])
            elif 'OpO' in c:
                t = c.index('OpO') + 2
                temp.append(c[:t])
                temp.append(c[t:])
            else:
                temp.append(c)
        # FD
        # print "The temp information is: "
        # for element in temp:
        #     print element
        # print "---------------------"
        # Note text position inside the ligature
        if len(self.text_position) != len(temp):
            raise Exception("Length Check Failure.")
        # else:
        #     print "Length Check Pass!"

        # Beginning upward stem flag
        if temp[0][0] == 'u':
            beginning_upward_flag = True
        else:
            beginning_upward_flag = False

        # Two_note Ligature processing
        if len(temp) == 2:

            # FD
            # print "Category: Length 2 Ligature"

            if beginning_upward_flag:

                # FD
                # print "The text position information are:"
                # print self.text_position[0], self.text_position[1], clef_position, clef_sign
                note_1 = m21.note.Note(get_general_text_position(text_position=self.text_position[0],
                                                                 clef_position=clef_position, clef_sign=clef_sign))
                note_2 = m21.note.Note(get_general_text_position(text_position=self.text_position[1],
                                                                 clef_position=clef_position, clef_sign=clef_sign))

                # # FD
                # print "Note Unable"
                # TODO: Check whether points possible in Two notes ligature * Indenpent point operation funciont?
                # TODO: Check whether downward stems possible with 2 notes ligature
                note_1.duration.type = 'whole'
                note_2.duration.type = 'whole'
                # Add dot support
                if 'p' in temp[0]:
                    note_1.duration.dots = 1
                if 'p' in temp[1]:
                    note_2.duration.dots = 1

                return [note_1, note_2]

            elif ('O' in temp[0]) & ('O' in temp[1]):
                # FD
                # print "In OO class"
                note_1 = m21.note.Note(get_general_text_position(text_position=self.text_position[0],
                                                                 clef_position=clef_position, clef_sign=clef_sign))
                note_2 = m21.note.Note(get_general_text_position(text_position=self.text_position[1],
                                                                 clef_position=clef_position, clef_sign=clef_sign))

                note_1.duration.type = 'longa'
                note_2.duration.type = 'breve'

                # Add dot support
                if 'p' in temp[0]:
                    note_1.duration.dots = 1
                if 'p' in temp[1]:
                    note_2.duration.dots = 1

                return [note_1, note_2]

            else:

                # # FD
                # print "The text position information are:"
                # print self.text_position[0], self.text_position[1]
                if self.text_position[1] > self.text_position[0]:
                    note_1 = m21.note.Note(get_general_text_position(text_position=self.text_position[0],
                                                                     clef_position=clef_position, clef_sign=clef_sign))
                    note_2 = m21.note.Note(get_general_text_position(text_position=self.text_position[1],
                                                                     clef_position=clef_position, clef_sign=clef_sign))

                    note_1.duration.type = 'breve'
                    note_2.duration.type = 'breve'
                    # Add dot support
                    if 'p' in temp[0]:
                        note_1.duration.dots = 1
                    if 'p' in temp[1]:
                        note_2.duration.dots = 1
                    return [note_1, note_2]
                else:
                    note_1 = m21.note.Note(get_general_text_position(text_position=self.text_position[0],
                                                                     clef_position=clef_position, clef_sign=clef_sign))
                    note_2 = m21.note.Note(get_general_text_position(text_position=self.text_position[1],
                                                                     clef_position=clef_position, clef_sign=clef_sign))

                    note_1.duration.type = 'longa'
                    note_2.duration.type = 'longa'
                    # Add dot support
                    if 'p' in temp[0]:
                        note_1.duration.dots = 1
                    if 'p' in temp[1]:
                        note_2.duration.dots = 1
                    return [note_1, note_2]

        # More than 2 notes ligature processing

        out_list = []
        for i in range(len(temp)):
            this_position = self.text_position[i]
            this_symbol = temp[i]
            this_note = m21.note.Note(get_general_text_position(text_position=this_position, clef_position=clef_position
                                                                , clef_sign=clef_sign))
            # Length of the note analysis

            if i == 0:
                # The first note of Ligature
                if beginning_upward_flag:
                    this_note.duration.type = 'whole'
                elif 'O' in this_symbol:
                    this_note.duration.type = 'longa'
                elif self.text_position[1] > self.text_position[0]:
                    this_note.duration.type = 'breve'
                elif self.text_position[1] < self.text_position[0]:
                    this_note.duration.type = 'longa'
                else:
                    raise Exception('This length note case is NOT decleared!')

            elif i == 1:
                # The 2nd note of Ligature
                if beginning_upward_flag:
                    this_note.duration.type = 'whole'
                elif 'd' in this_symbol:
                    this_note.duration.type = 'longa'
                else:
                    this_note.duration.type = 'breve'

            elif i == len(temp):
                # The last note of Ligature
                if self.text_position[-1] > self.text_position[-2]:
                    this_note.duration.type = 'breve'
                elif self.text_position[-1] < self.text_position[-2]:
                    this_note.duration.type = 'longa'
                elif 'd' in this_symbol:
                    this_note.duration.type = 'longa'
                else:
                    raise Exception('This case is NOT covered yet. Please trace back!')

            else:
                # Anynote in the middle of the Ligature
                if 'd' in this_symbol:
                    this_note.duration.type = 'longa'
                else:
                    this_note.duration.type = 'breve'

            # TODO: In perfect sense how to handle Point

            if 'p' in this_symbol:
                this_note.duration.dots = 1
            out_list.append(this_note)

        return out_list


class AnnotationPage(object):
    """
    Contain the information of the whole .annotation file
    """

    def __init__(self):

        self.head = None
        self.image_name = None
        self.contents = []
        self.stream = None

    def read_annotation_file(self, filename):
        """
        Read the annotation file information into class.
        :param filename:
        :return:
        """
        with open(filename) as f:
            d = f.readlines()

        self.head = d[0]
        self.image_name = d[1]

        count_line = 2
        count_object = 0
        while count_line < len(d):
            now_line = d[count_line]
            # print now_line
            if 'object: ' in now_line:
                count_object += 1
                self.contents.append(AnnotationObject())
                self.contents[count_object - 1].id = int(now_line.split()[-1])
                # print self.contents[count_object-1].id
            elif 'bbox: ' in now_line:
                self.contents[count_object - 1].bbox = now_line.split(',')
                self.contents[count_object - 1].bbox[0] = self.contents[count_object - 1].bbox[0].split()[-1]
                self.contents[count_object - 1].bbox = map(float, self.contents[count_object - 1].bbox)
            elif 'comments: ' in now_line:
                self.contents[count_object - 1].comments = now_line.split()[-1]
            elif 'object_type: ' in now_line:
                self.contents[count_object - 1].object_type = now_line.split()[-1]
            elif 'text_position: ' in now_line:
                # self.contents[count_object - 1].text_position = now_line.split()[-1].split(',')
                # WARNING: The new file format don't use ',' in numbers anymore.
                now_str = now_line.split()[-1]
                # print now_str
                if '_' in now_str:
                    self.contents[count_object - 1].text_position = map(float, now_str.split('_'))
                else:
                    self.contents[count_object - 1].text_position = str(float(now_str))
            elif 'label_symbol: ' in now_line:
                self.contents[count_object - 1].label_symbol = now_line.split()[-1]
            elif 'musical_symbol: ' in now_line:
                self.contents[count_object - 1].musical_symbol = now_line.split()[-1]
            elif 'channel' in now_line:
                self.contents[count_object - 1].channel = int(now_line.split()[-1])
            elif 'predicted' in now_line:
                # if 'ligature' in now_line.lower():
                self.contents[count_object - 1].description = now_line.split()[-1]
                self.contents[count_object - 1].parse()
            elif 'predict' in now_line:
                # if 'ligature' in now_line.lower():
                self.contents[count_object - 1].description = now_line.split()[-1]
                self.contents[count_object - 1].parse()

            count_line += 1
            # print count_line, ' out of ', len(d)

        print 'File Loaded and Parsed: %s' % filename

    def write_annotation_file(self, filename):
        """
        Write the annotation inside class instance into a file.
        :param filename: The output file to save the annotation information.
        :return:
        """

        f = open(filename, 'wb')
        f.write(self.head + '\n')
        f.write(self.image_name + '\n')
        for temp_object in self.contents:
            temp_object.write_into_file(f)

        f.close()
        print 'All the contents are saved into %s.' % filename

    def class_statistics(self):
        """
        Count the classes inside the page and list them out.
        :return: None
        """

        list_cls = []
        amount_cls = []

        for element in self.contents:

            now_label = element.label_symbol

            if now_label in list_cls:

                amount_cls[list_cls.index(now_label)] += 1

            else:

                list_cls.append(now_label)
                amount_cls.append(0)

        for i in range(len(list_cls)):
            print list_cls[i], ' :%d ' % amount_cls[i]

        note_list = []
        amount_note = []

        for element in self.contents:
            if element.label_symbol == 'note':

                if element.musical_symbol in note_list:
                    amount_note[note_list.index(element.musical_symbol)] += 1
                else:
                    note_list.append(element.musical_symbol)
                    amount_note.append(0)

        if len(note_list) > 0:
            print '=============== Notes ================'
            for i in range(len(note_list)):
                print note_list[i], ' :%d' % amount_note[i]

    def available_channel_check(self):
        """
        Check which channels are available in this annotation file.
        :return:
        """

        channel_list = []
        for x in self.contents:
            if x.channel not in channel_list:
                channel_list.append(x.channel)

        channel_list.sort()

        return channel_list

    def process_modern(self, channel_chosen=None):

        """
        Transform the annotation file into music21 objects in modern notations.
        :param channel_chosen: A list in which chosen channels were specified
        :return:
        """
        if channel_chosen is None:
            channel_chosen = self.available_channel_check()

        s = m21.stream.Stream()
        print "Now Processing. Do NOT Worry. I am fast ;-)"
        #
        # print 'The total number of elements are: %d' % len(self.contents), \
        #     ' ,distributed in %d channels.' % len(channel_chosen)

        accidental_list = []

        for now_channel in channel_chosen:

            now_part = m21.stream.Part()
            last_note = None
            # accidental_list = ['B']
            now_clef = m21.clef.Clef()
            now_clef.line = 4
            now_clef.sign = 'F'
            # TODO: accidental_list updating
            for x in self.contents:
                if x.channel == now_channel:

                    try:
                        if x.label_symbol == 'clef':

                            now_clef = m21.clef.Clef()
                            now_clef.sign = x.musical_symbol.upper()
                            now_clef.line = int(x.get_text_position())
                            now_part.append(now_clef)
                            print "Clef Change:"
                            print now_clef.line, now_clef.sign, "in Channel: ", now_channel
                        elif x.label_symbol == 'key_sig':

                            now_key = 0
                            if x.musical_symbol == 'flat':
                                now_key = m21.key.KeySignature(-1)
                            elif x.musical_symbol == 'sharp':
                                now_key = m21.key.KeySignature(1)

                            now_part.append(now_key)

                        elif x.label_symbol == 'time_sig':

                            now_timesig = m21.meter.TimeSignature('4/2')
                            if x.musical_symbol[0] == 'imperfect':
                                if x.musical_symbol[1] == 'minor':
                                    now_timesig = m21.meter.TimeSignature('4/2')
                                elif x.musical_symbol[1] == 'major':
                                    now_timesig = m21.meter.TimeSignature('6/2')
                            if x.musical_symbol[0] == 'perfect':
                                if x.musical_symbol[1] == 'minor':
                                    now_timesig = m21.meter.TimeSignature('6/2')
                                elif x.musical_symbol[1] == 'major':
                                    now_timesig = m21.meter.TimeSignature('9/2')

                            now_part.insert(0, now_timesig)

                        elif x.label_symbol == 'note':

                            if x.musical_symbol == 'breve':
                                # now_note = m21.note.Note(table[x.get_text_position()], 'B')
                                # now_note.pitch.octave = x.get_text_position
                                now_note = m21.note.Note(
                                    x.get_note_text_position(clef_position=now_clef.line, clef_sign=now_clef.sign))
                                if now_note.name in accidental_list:
                                    now_note.accidental = -1
                                now_note.duration.type = 'breve'
                                now_part.append(now_note)
                            elif x.musical_symbol == 'semibreve':
                                now_note = m21.note.Note(
                                    x.get_note_text_position(clef_position=now_clef.line, clef_sign=now_clef.sign))
                                if now_note.name in accidental_list:
                                    now_note.accidental = -1
                                now_note.duration.type = 'whole'
                                now_part.append(now_note)
                            elif x.musical_symbol == 'minim':
                                now_note = m21.note.Note(
                                    x.get_note_text_position(clef_position=now_clef.line, clef_sign=now_clef.sign))
                                if now_note.name in accidental_list:
                                    now_note.accidental = -1
                                now_note.duration.type = 'half'
                                now_part.append(now_note)
                            elif x.musical_symbol == 'semiminim':
                                now_note = m21.note.Note(
                                    x.get_note_text_position(clef_position=now_clef.line, clef_sign=now_clef.sign))
                                if now_note.name in accidental_list:
                                    now_note.accidental = -1
                                now_note.duration.type = 'quarter'
                                now_part.append(now_note)
                            elif x.musical_symbol == 'fusa':
                                now_note = m21.note.Note(
                                    x.get_note_text_position(clef_position=now_clef.line, clef_sign=now_clef.sign))
                                if now_note.name in accidental_list:
                                    now_note.accidental = -1
                                now_note.duration.type = 'eighth'
                                now_part.append(now_note)
                            elif x.musical_symbol == 'longa':
                                now_note = m21.note.Note(
                                    x.get_note_text_position(clef_position=now_clef.line, clef_sign=now_clef.sign))
                                if now_note.name in accidental_list:
                                    now_note.accidental = -1
                                now_note.duration.type = 'longa'
                                now_part.append(now_note)
                            elif x.musical_symbol == 'maxima':
                                now_note = m21.note.Note(
                                    x.get_note_text_position(clef_position=now_clef.line, clef_sign=now_clef.sign))
                                if now_note.name in accidental_list:
                                    now_note.accidental = -1
                                now_note.duration.type = 'maxima'
                                now_part.append(now_note)

                            # if x.get_note_text_position(clef_position=4, clef_sign='F') == 'B3':

                            last_note = now_note

                        elif x.label_symbol == 'rest':

                            if x.musical_symbol == 'breve':
                                # now_note = m21.note.Note(table[x.get_text_position()], 'B')
                                # now_note.pitch.octave = x.get_text_position
                                now_rest = m21.note.Rest()
                                now_rest.duration.type = 'breve'
                                now_part.append(now_rest)
                            elif x.musical_symbol == 'semibreve':
                                now_rest = m21.note.Rest()
                                now_rest.duration.type = 'whole'
                                now_part.append(now_rest)
                            elif x.musical_symbol == 'minim':
                                now_rest = m21.note.Rest()
                                now_rest.duration.type = 'half'
                                now_part.append(now_rest)
                            elif x.musical_symbol == 'semiminim':
                                now_rest = m21.note.Rest()
                                now_rest.duration.type = 'quarter'
                                now_part.append(now_rest)
                            elif x.musical_symbol == 'fusa':
                                now_rest = m21.note.Rest()
                                now_rest.duration.type = 'eighth'
                                now_part.append(now_rest)
                            elif x.musical_symbol == 'longa':
                                now_rest = m21.note.Rest()
                                now_rest.duration.type = 'longa'
                                now_part.append(now_rest)
                            elif x.musical_symbol == 'maxima':
                                now_rest = m21.note.Rest()
                                now_rest.duration.rest = 'maxima'
                                now_part.append(now_rest)
                        #
                        elif x.label_symbol == 'point':
                            # Add this point to previous added symbol

                            # for i in range(1, len(now_part) + 1):
                            # now_part[-1].duration.dots += 1
                            # print 'Dot happened!', last_note, last_note.duration
                            # last_note.duration.dots += 1
                            # print 'After dot duration: ', last_note.duration
                            del now_part[-1]
                            last_note.duration.dots += 1
                            now_part.append(last_note)

                        elif x.label_symbol.lower() == 'Ligature'.lower():
                            # print 'Ligature detected!'
                            nl = x.ligature_imperfect_parse(clef_position=now_clef.line, clef_sign=now_clef.sign)
                            for temp_note in nl:
                                now_part.append(temp_note)

                    except:
                        print "=================Exception Raised======================="
                        print "Description: %s" % x.description
                        print "Text Position: %s" % x.text_position

            # s.append(now_part)
            s.insert(0, now_part)
        return s

    ## This function is replaced by the function process_modern, which is above. ##
    ## The reason to keep it is in case m21 implemented the menrural library. ##
    # def processing(self, channel=None, updateLength=True):
    #     """
    #     Transform the annotation file into music21 objects.
    #     :return: None
    #     """
    #     if channel is None:
    #         channel = range(1, 5)
    #
    #     s = m21.stream.Stream()
    #     part = m21.stream.Part()
    #     # TODO: Remove FAKED ones
    #     # s.append(m21.medren.MensuralClef('C'))
    #     # time_sig = m21.trecento.notation.Divisione('.o.')
    #     # time_sig = m21.medren.Mensuration(tempus='imperfect', prolation='minor')
    #     # s.append(time_sig)
    #
    #     # clef = True
    #     # ts = True
    #
    #     undo_list = []
    #     undo_amount = []
    #     print 'The total number of elements are: %d' % len(self.contents)
    #     for element in self.contents:
    #         if int(element.channel) in channel:
    #             try:
    #                 if element.label_symbol == 'clef':
    #
    #                     # now_clef = m21.medren.MensuralClef(sign=element.musical_symbol.upper())
    #                     now_clef = m21.clef.Clef()
    #                     # TODO: Determine the line of context!
    #                     now_clef.sign = element.musical_symbol.upper()
    #                     now_clef.line = int(element.get_text_position())
    #                     part.append(now_clef)
    #
    #                 elif element.label_symbol == 'time_sig':
    #
    #                     # time_sig = m21.medren.Mensuration(tempus=element.musical_symbol[0],
    #                     #                                   prolation=element.musical_symbol[1])
    #                     time_sig = m21.meter.TimeSignature('9/4')
    #                     part.append(time_sig)
    #
    #                 elif element.label_symbol == 'note':
    #                     # TODO: Calculate the octave and steps! Add Maxima, Longa, Fusa
    #                     table = ['C', 'D', 'E', 'F', 'A', 'B', 'C', 'D', 'E', 'F']
    #
    #                     # if element.get_text_position() <= 0:
    #                     # continue
    #
    #                     # print 'position: %d' % element.get_text_position()
    #
    #                     if element.musical_symbol == 'breve':
    #                         now_note = m21.medren.MensuralNote(table[element.get_text_position()], 'B')
    #                         part.append(now_note)
    #                     elif element.musical_symbol == 'semibreve':
    #                         now_note = m21.medren.MensuralNote(table[element.get_text_position()], 'SB')
    #                         part.append(now_note)
    #                     elif element.musical_symbol == 'minim':
    #                         now_note = m21.medren.MensuralNote(table[element.get_text_position()], 'M')
    #                         part.append(now_note)
    #                     elif element.musical_symbol == 'semiminim':
    #                         now_note = m21.medren.MensuralNote(table[element.get_text_position()], 'SM')
    #                         part.append(now_note)
    #                     elif element.musical_symbol == 'longa':
    #                         now_note = m21.medren.MensuralNote(table[element.get_text_position()], 'L')
    #                         part.append(now_note)
    #                     elif element.musical_symbol == 'maxima':
    #                         now_note = m21.medren.MensuralNote(table[element.get_text_position()], 'Mx')
    #                         part.append(now_note)
    #
    #                 elif element.label_symbol == 'rest':
    #
    #                     if element.musical_symbol == 'breve':
    #                         now_note = m21.medren.MensuralRest('B')
    #                         part.append(now_note)
    #                     elif element.musical_symbol == 'semibreve':
    #                         now_note = m21.medren.MensuralRest('SB')
    #                         part.append(now_note)
    #                     elif element.musical_symbol == 'minim':
    #                         now_note = m21.medren.MensuralRest('M')
    #                         part.append(now_note)
    #                     elif element.musical_symbol == 'semiminim':
    #                         now_note = m21.medren.MensuralRest('SM')
    #                         part.append(now_note)
    #                     elif element.musical_symbol == 'longa':
    #                         now_note = m21.medren.MensuralRest('L')
    #                         part.append(now_note)
    #                     elif element.musical_symbol == 'maxima':
    #                         now_note = m21.medren.MensuralRest('Mx')
    #                         part.append(now_note)
    #
    #                 elif element.label_symbol in undo_list:
    #                     undo_amount[undo_list.index(element.label_symbol)] += 1
    #                 else:
    #                     undo_list.append(element.label_symbol)
    #                     undo_amount.append(0)
    #
    #             except:
    #                 print "=================Exception Raised======================="
    #                 print "Description: %s" % element.description
    #                 print "Text Position: %s" % element.text_position
    #
    #     # ============= Print Unprocessed Elements ===============
    #     print '=================== Following Elements Are Not Processed ===================='
    #     for i in range(len(undo_list)):
    #         print undo_list[i], ' : ', undo_amount[i]
    #
    #     # s.append(part)
    #     s_bk = part
    #
    #     print '============================='
    #     print 'After processing, the amount of instances are: %d ' % len(part)
    #
    #     # s = m21.medren.breakMensuralStreamIntoBrevisLengths(s)
    #     for x in part:
    #
    #         if isinstance(x, m21.medren.GeneralMensuralNote):
    #             # print 'Now instance: ', x
    #             try:
    #                 # x.updateDurationFromMensuration(mensuration=time_sig, surroundingStream=s)
    #                 if x.mensuralType == 'semibrevis':
    #                     x.duration.quarterLength = 1
    #                 elif x.mensuralType == 'brevis':
    #                     x.duration.quarterLength = 2
    #                 elif x.mensuralType == 'longa':
    #                     x.duration.quarterLength = 4
    #                 elif x.mensuralType == 'maxima':
    #                     x.duration.quarterLength = 8
    #                 elif x.mensuralType == 'minima':
    #                     x.duration.quarterLength = 0.5
    #                 elif x.mensuralType == 'semiminima':
    #                     x.duration.quarterLength = 0.25
    #
    #                 print(x.duration.quarterLength)
    #                 x.updateDurationFromMensuration(mensuration=time_sig, surroundingStream=part)
    #                 print 'After update: ', x.duration.quarterLength
    #             except ValueError, x.duration.quarterLength:
    #                 print '========= Exception ==========='
    #                 print 'The type is: %s' % x.mensuralType
    #                 print 'The quarterLength is: %s' % x.duration.quarterLength
    #
    #                 # del x
    #                 # x.updateDurationFromMensuration(surroundingStream=s)
    #
    #     s.append(part)
    #     self.stream = s
    #
    #     return s

    def update_length(self):

        s = self.stream
        for x in s:
            if isinstance(x, m21.medren.GeneralMensuralNote):
                # print x
                # x.updateDurationFromMensuration(surroundingStream=s)
                # print(x.duration.quarterLength)
                if x.mensuralTYpe == 'semibrevis':
                    x.duration.quarterLength = 1
                elif x.mensuralType == 'brevis':
                    x.duration.quarterLength = 2
                elif x.mensuralType == 'longa':
                    x.duration.quarterLength = 4
                elif x.mensuralType == 'maxima':
                    x.duration.quarterLength = 8
                elif x.mensuralType == 'minima':
                    x.duration.quarterLength = 0.5
                elif x.mensuralType == 'semiminima':
                    x.duration.quarterLength = 0.25

        self.stream = s

        return s


def local_ligature_data_collection(folder = "/users/visics/xchen/project_Alamire/transcriptionData" ):
    pass

