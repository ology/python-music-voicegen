from music_voicegen.music_voicegen import MusicVoiceGen
import unittest

class TestMusicVoiceGen(unittest.TestCase):
    def setUp(self):
        # You would import your MusicVoiceGen class here
        # from music.voicegen import MusicVoiceGen
        pass

    def test_no_params_set(self):
        with self.assertRaises(ValueError):
            MusicVoiceGen()

    def test_pitches_and_intervals(self):
        vg = MusicVoiceGen(pitches=[1,2,3], intervals=[1,2,3,4])
        self.assertIsInstance(vg, MusicVoiceGen)
        self.assertEqual(vg.pitches, [1,2,3])
        self.assertEqual(vg.intervals, [1,2,3,4])
        self.assertEqual(vg.possibles, {1: {2: 1, 3: 1}, 2: {3: 1}})

        vg.update({'cat': {'cat': 1}}, preserve_pitches=True)
        self.assertEqual(vg.possibles, {'cat': {'cat': 1}})
        self.assertEqual(vg.pitches, [1,2,3])
        self.assertEqual(vg.intervals, [1,2,3,4])

        vg.update({'dog': {'dog': 1}})
        self.assertEqual(vg.pitches, [])
        self.assertEqual(vg.intervals, [])

    def test_possibles_only(self):
        ovg = MusicVoiceGen(possibles={1: {2: 1, 3: 1}, 2: {3: 1}})
        self.assertEqual(ovg.pitches, [])
        self.assertEqual(ovg.intervals, [])
        self.assertEqual(ovg.possibles, {1: {2: 1, 3: 1}, 2: {3: 1}})

    def test_custom_weighting(self):
        def weightfn(pitch_from, pitch_to, interval):
            return 7 if interval < 0 else 5
        wvg = MusicVoiceGen(pitches=[1,2,3], intervals=[1,-1], weightfn=weightfn)
        self.assertEqual(wvg.possibles, {
            1: {2: 5},
            2: {3: 5, 1: 7},
            3: {2: 7}
        })

    def test_default_context(self):
        cvg = MusicVoiceGen(possibles={1: {1: 1}})
        self.assertEqual(cvg.context(), [])
        cvg.rand()
        self.assertEqual(cvg.context(), [1])
        cvg.rand()
        self.assertEqual(cvg.context(), [1])
        cvg.rand()
        self.assertEqual(cvg.context(), [1])

    def test_deterministic_cycle(self):
        cycle = [0,1,2]
        got = []
        bvg = MusicVoiceGen(MAX_CONTEXT=3, possibles={
            0: {1: 5},
            1: {2: 5},
            2: {0: 5}
        })
        got.append(bvg.rand())
        self.assertIn(got[0], cycle)
        self.assertEqual(bvg.context(), got)
        got.append(bvg.rand())
        self.assertEqual(got[1], (got[0]+1)%3)
        self.assertEqual(bvg.context(), got)
        got.append(bvg.rand())
        self.assertEqual(got[2], (got[0]+2)%3)
        self.assertEqual(bvg.context(), got)
        got.append(bvg.rand())
        self.assertEqual(got[3], (got[0]+3)%3)
        self.assertEqual(bvg.context(), got[1:4])
        got.append(bvg.rand())
        self.assertEqual(got[4], (got[0]+4)%3)
        self.assertEqual(bvg.context(), got[2:5])

    def test_context_with_depth(self):
        voice = MusicVoiceGen(MAX_CONTEXT=3, possibles={
            60: {65: 1},
            "60.65": {67: 1},
            65: {-1: 1},
            "60.65.67": {65: 1}
        })
        voice.context(context=[60])
        pitches = []
        i = 10
        while i > 0:
            pitches.append(voice.rand())
            if pitches[-1] == -1:
                break
            i -= 1
        self.assertEqual(pitches, [65, 67, 65, -1])

    def test_startfn_and_contextfn(self):
        def startfn(foo):
            raise Exception("what does this little red button do?")
        fvg = MusicVoiceGen(pitches=list(range(1,101)), intervals=[-1], MAX_CONTEXT=8, startfn=startfn)
        with self.assertRaises(Exception) as cm:
            fvg.rand()
        self.assertIn("what does this little red button do?", str(cm.exception))

        fvg.startfn = lambda foo: 42
        self.assertEqual(fvg.rand(), 42)

        def contextfn(choice, mrd, count):
            return 9 + count, 0
        fvg.contextfn = contextfn
        fvg.context(context=[9])
        fvg.update({
            "9": {42: 1},
            "9.10": {42: 1},
            "10": {42: 1},
            "9.10.11": {42: 1},
            "10.11": {42: 1},
            "11": {42: 1}
        })
        self.assertEqual(fvg.rand(), 10)
        self.assertEqual(fvg.rand(), 11)
        self.assertEqual(fvg.rand(), 12)

    def test_subsets(self):
        svg = MusicVoiceGen(possibles={1: {1: 1}})
        subsets = []
        def cb(*args):
            subsets.append(list(args))
        svg.subsets(2, 4, cb, [65, 67, 69, 60, 62])
        self.assertEqual(subsets, [
            [65, 67], [65, 67, 69], [65, 67, 69, 60], [67, 69],
            [67, 69, 60], [67, 69, 60, 62], [69, 60], [69, 60, 62], [60, 62]
        ])

if __name__ == '__main__':
    unittest.main()
