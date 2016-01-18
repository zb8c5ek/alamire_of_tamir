__author__ = 'Xuanli CHEN'

"""
    PhD Student at VISICS, KU Leuven
    xuanli.chen@esat.kuleuven.be
"""

import music21 as m21

s = m21.stream.Stream()
clef = m21.medren.MensuralClef(sign='C')
# ts = m21.medren.Mensuration(tempus='imperfect', prolation='minor', mode='imperfect', scalingFactor=2)
ts = m21.trecento.notation.Divisione('.o.')
# ts.minimaPerBrevis = 4

s.append(clef)

s.append(ts)

for i in range(8):
    this_note = m21.medren.MensuralNote('A', 'B')
    s.append(this_note)

# ======================== Ligature ==========================

l1 = m21.medren.Ligature(['A4', 'F4', 'G4', 'A4', 'B-4'])
l1.makeOblique(0)
l1.setStem(0, 'down', 'left')
# print([n.fullName for n in l1.notes])

l2 = m21.medren.Ligature(['F4', 'G4', 'A4', 'B-4', 'D5'])
l2.setStem(4, 'down', 'left')
l2.setReverse(4, True)
# print([(n.mensuralType, n.pitch.nameWithOctave) for n in l2.notes])


s.append(l1)

for i in range(8):
    this_note = m21.medren.MensuralNote('F', 'M')
    s.append(this_note)

s.append(l2)

for mn in s:
    if isinstance(mn, m21.medren.GeneralMensuralNote):
        mn.updateDurationFromMensuration(mensuration=ts, surroundingStream=s)
        print mn
        print(mn.duration.quarterLength)


# ===================================================================

p = m21.medren.stream.Part()
m = m21.medren.stream.Measure()
m.append(m21.medren.MensuralNote('G', 'B'))
p.append(m21.trecento.notation.Divisione('.q.'))
p.repeatAppend(m21.medren.MensuralNote('A', 'SB'), 2)
p.append(m21.trecento.notation.Punctus())
p.repeatAppend(m21.medren.MensuralNote('B', 'M'), 4)
p.append(m21.trecento.notation.Punctus())
p.append(m21.medren.MensuralNote('C', 'B'))

for i in range(8):
    this_note = m21.medren.MensuralNote('A', 'SB')
    p.append(this_note)

s = m21.stream.Stream()
s.append(m21.medren.Mensuration(tempus='perfect', prolation='minor'))
s.append(p)

s.append(m)
# t = m21.medren.breakMensuralStreamIntoBrevisLengths(s, printUpdates=True)

# t.show('text')

# ============================= Original Perform ===============================
s = m21.stream.Stream()
s.append(m21.trecento.notation.Divisione('.p.'))
clef = m21.medren.MensuralClef(sign='C')
clef.line = 2
s.append(clef)
# s.append(m21.medren.Mensuration(tempus='imperfect', prolation='minor'))
for i in range(3):
    s.append(m21.medren.MensuralNote('A', 'SB'))
# s.append(m21.trecento.notation.Punctus())
s.append(m21.medren.MensuralNote('B', 'SB'))
s.append(m21.medren.MensuralNote('B', 'SB'))
# s.append(m21.trecento.notation.Punctus())
s.append(m21.medren.MensuralNote('A', 'B'))
for mn in s:
    if isinstance(mn, m21.medren.GeneralMensuralNote):
        mn.updateDurationFromMensuration(surroundingStream=s)
        print(mn.duration.quarterLength)

# =======================================================================

# s = m21.stream.Score()
# p = m21.stream.Part()
# m = m21.stream.Measure()
# s.append(p)
# s.append(m21.medren.GeneralMensuralNote('B'))
# medren.breakMensuralStreamIntoBrevisLengths(s)
s = m21.stream.Score()
p = m21.stream.Part()
# m.append(m21.medren.MensuralNote('G','B'))
# p.append(m21.trecento.notation.Divisione('.q.'))

divisione = m21.trecento.notation.Divisione('o')

p.append(divisione)
p.repeatAppend(m21.medren.MensuralNote('A','SB'),2)
p.append(m21.medren.MensuralNote('C','B'))
# p.append(m21.trecento.notation.Punctus())
p.repeatAppend(m21.medren.MensuralNote('B','M'),4)
# p.append(m21.trecento.notation.Punctus())
p.append(m21.medren.MensuralNote('C','B'))
p.append(m21.medren.MensuralNote('C','B'))
p.append(m21.medren.MensuralNote('C','B'))
p.append(m21.medren.MensuralNote('C','B'))

# s.append(m21.trecento.notation.Divisione('.q.'))
s.append(p)
# s.append(m)

# for mn in s:
#     if isinstance(mn, m21.medren.GeneralMensuralNote):
#         mn.updateDurationFromMensuration(surroundingStream=s)
#         print(mn.duration.quarterLength)
#
# t = m21.medren.breakMensuralStreamIntoBrevisLengths(s, printUpdates = True)

t = m21.trecento.notation.BrevisLengthTranslator(divisione=divisione, BL=s)
t.getKnownLengths()

t.show('text')