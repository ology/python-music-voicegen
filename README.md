# Music VoiceGen

Musical Voice Generation

Python based on https://metacpan.org/dist/Music-VoiceGen by Jeremy Mates (gemini://thrig.me)

## DESCRIPTION

This module offers the ability to generate a voice (a series of notes or melody) using only certain pitches and intervals, or otherwise a custom set of possible choices (via a hash of hashes) that a given pitch (an integer) will move to some other pitch. The design suits choral work, where leaps of a tritone or similar must be forbidden, and the range of pitches confined to a certain ambitus. With suitable input this module could be made to produce more chromatic lines over larger ranges.

## SYNOPSIS
```python
from music_voicegen import MusicVoiceGen

voice = MusicVoiceGen(
    pitches=[60,62,64,65,67,69],
    intervals=[-4,-3,-2,-1,1,2,3,4]
)
voice.context(context=[60]) # start at middle c
voices = [ voice.rand() for _ in range(8) ]
```

Please see [the original documentation](https://metacpan.org/pod/Music::VoiceGen) for detailed usage.

## AUTHOR

thrig - Jeremy Mates (jmates at cpan.org)
