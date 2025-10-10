import random
from music21 import converter, corpus, note, stream
# if author:
import sys
sys.path.append('./src')
from music_voicegen.music_voicegen import MusicVoiceGen
# else:
from music_voicegen import MusicVoiceGen

# song = converter.parse('/Users/gene/Music/MIDI/lichens_g_major.mid')
song = corpus.parse('bwv66.6')

max = sys.argv[1] if len(sys.argv) > 1 else 16 # maximum notes in the result phrase

transition = {}
prev = None # network item
last = None # network transition item
total = 0 # total number of notes
pitches = []

# gather the transitions
for n in song.flatten().notes:
    if type(n) == note.Note:
        pitches.append(n.pitch.midi)
        if prev:
            if last:
                key = (prev.name, last.name)
                if key in transition:
                    if n.name in transition[key]:
                        transition[key][n.name] += 1
                    else:
                        transition[key][n.name] = 1
                else:
                    transition[key] = {n.name: 1}
                prev = last
                total += 1
            last = n
        else:
            prev = n

pitches = list(set(pitches)) # uniqify

# probability for each transition
for k,v in transition.items():
    for i,j in v.items():
        transition[k][i] = j / total

# # transition probability score
score = stream.Stream()

key = list(transition.keys())[0]
keys = [' '.join(i) for i in list(transition.keys())]

voice = MusicVoiceGen(
    pitches=pitches,
    intervals=[-7,-5,-4,-3,-2,-1,1,2,3,4,5,7]
)
# voice.context(context=[60]) # start at middle c

# build the score
for _ in range(max):
    if key in transition:
        draw = voice.rand()
        n = note.Note(draw)
        score.append(n)
        key = (key[1], n.name)
    else:
        print(key)
        # score.append(note.Rest())
        draw = random.choice(keys)
        key = tuple(draw.split())

score.show('midi')
