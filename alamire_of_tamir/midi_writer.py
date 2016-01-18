__author__ = 'Xuanli CHEN'

"""
    PhD Student at VISICS, KU Leuven
    xuanli.chen@esat.kuleuven.be
"""

from midiutil.MidiFile import MIDIFile


class MidiObject(object):
    """
        Stand for each element in the musical score, e.g. A pitch, rest etc.
        Track: different songs, normally one.
        Channel: different voices. In Alamire, normally four.
    """

    def __init__(self):
        self.id = None
        self.track = None
        self.channel = None
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
        opened_file.write('object: %d\n' % self.id)
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


class MidiFile(object):
    """
        A whole MIDI file.
    """

    def __init__(self):
        self.contents = []
        self.tempo = 120
        self.time_sig = [0, 0]
        self.clef = None
        self.nr_track = 1
        self.nr_channel = 4

    def read_file(self, filename):
        """
        Read the MIDI related file information from file.
        :param filename: Input filename
        :return: None
        """
        with open(filename) as f:
            d = f.readlines()

        try:
            self.tempo = int(d[0].split()[1])

            if len(d[1].split()[1:]) != 2:
                raise ValueError
            else:
                self.time_sig = map(int, d[1].split()[1:])

            self.clef = d[2].split()[1:]
            self.nr_channel = int(d[3].split()[-1])
            self.nr_track = int(d[4].split()[-1])

        except (IndexError, ValueError):
            print 'The Input File is Illegal.'

        count_line = 5
        count_object = 0
        while count_line < len(d):
            now_line = d[count_line]
            # print now_line
            if 'object: ' in now_line:
                count_object += 1
                self.contents.append(MidiObject())
                self.contents[count_object-1].id = int(now_line.split()[-1])
                print self.contents[count_object-1].id
            elif 'track: ' in now_line:
                self.contents[count_object-1].track = int(now_line.split()[-1])
            elif 'channel: ' in now_line:
                self.contents[count_object-1].channel = int(now_line.split()[-1])
            elif 'volume: ' in now_line:
                self.contents[count_object-1].volume = int(now_line.split()[-1].split())
            elif 'pitch: ' in now_line:
                self.contents[count_object-1].pitch = int(now_line.split()[-1])
            elif 'time: ' in now_line:
                self.contents[count_object-1].time = int(now_line.split()[-1])
            elif 'duration: ' in now_line:
                self.contents[count_object-1].duration = int(now_line.split()[-1])

            count_line += 1

    def write_file(self, filename):
        """
        Write the MIDI related file information to a file.
        :param filename: Output filename
        :return: None
        """

        with open(filename) as f:

            f.write('tempo: %d\n' % self.tempo)
            f.write('time_sig: %d %d\n' % (self.time_sig[0], self.time_sig[1]))
            f.write('clef: %s\n' % self.clef)
            f.write('nr_channel: %d\n' % self.nr_channel)
            f.write('nr_track: %d\n' % self.nr_track)

            for temp_object in self.contents:

                temp_object.write_into_file(f)

        print 'The Contents Writing Accomplished ==> %s \n' % filename