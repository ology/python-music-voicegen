from VoiceGen import MusicVoiceGen

gen = MusicVoiceGen(
    pitches=[60, 62, 64, 65, 67, 69, 71, 72],
    intervals=[-3, -2, -1, 1, 2, 3]
)

v = gen.rand()
print(v)