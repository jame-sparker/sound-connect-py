""" Instruments class 
"""

instrument_names = ["pulse",
                    "flute",
                    "marimba",
                    "bass",
                    "bass_drum",
                    "crash",
                    "hi_hat_closed",
                    "hi_hat_open",
                    "snare_drum",
                    "bell",
                    "ripple",
                    "zap"]

instrument_display_names =\
 [name.replace("_", " ").title() for name in instrument_names]


notes = ["C","C#","D","D#","E","F","F#","G","G#","A","A#","B"]

allnotes = []

for i in range(3):
    for note in notes:
        allnotes.append(note[:1] + str(i + 3) + note[1:])


def note_to_number(note):
    base = ord(note[0])
    octave = int(note[1])
    is_sharp = len(note) > 2

    return (base - ord('C')) % 7 + (octave - 4) * 7 + (1./2 if is_sharp else 0)