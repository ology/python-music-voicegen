import random
from collections import defaultdict
from typing import Callable, List, Dict, Any, Optional

class MusicVoiceGen:
    def __init__(self, pitches=None, intervals=None, possibles=None, weightfn=None,
                 contextfn=None, startfn=None, MAX_CONTEXT=1):
        if pitches is not None and intervals is not None:
            if not isinstance(pitches, list) or not pitches:
                raise ValueError("have no pitches to work with")
            if not isinstance(intervals, list) or not intervals:
                raise ValueError("have no intervals to work with")
            self.pitches = pitches
            self.intervals = intervals
            self.weightfn = weightfn if weightfn else lambda from_, to, interval: 1
            self.possibles = defaultdict(dict)
            allowed_pitches = set(map(int, pitches))
            allowed_intervals = set(map(int, intervals))
            for pitch in allowed_pitches:
                for interval in allowed_intervals:
                    newpitch = pitch + interval
                    if newpitch in allowed_pitches:
                        self.possibles[pitch][newpitch] = self.weightfn(pitch, newpitch, interval)
        elif possibles is not None:
            if not isinstance(possibles, dict):
                raise ValueError("possibles must be dict")
            self.possibles = possibles
            self.pitches = []
            self.intervals = []
        else:
            raise ValueError("need 'pitches' and 'intervals' or 'possibles'")

        self._choices = self._build_choices(self.possibles)
        self._context = []
        self.MAX_CONTEXT = int(MAX_CONTEXT)
        self.contextfn = contextfn if contextfn else lambda choice, mrd, count: (random.choice(mrd), True)
        self.startfn = startfn if startfn else lambda possibles: random.choice(possibles)

    def _build_choices(self, possibles):
        choices = {}
        for fromval, tovals in possibles.items():
            choices[fromval] = []
            weights = []
            for toval, weight in tovals.items():
                choices[fromval].append(toval)
                weights.append(weight)
            choices[str(fromval)] = (choices[fromval], weights)
        return choices

    def clear_context(self):
        self._context = []

    def context(self, context=None):
        if context is None:
            return self._context
        if not isinstance(context, list):
            context = list(context)
        mc = self.MAX_CONTEXT
        if len(context) > mc:
            context = context[-mc:]
        self._context = context
        return self._context

    def rand(self):
        choices = self._choices
        choice = None
        context = self._context
        if not context:
            possibles = list(self.possibles.keys())
            if not possibles:
                raise ValueError("no keys in possibles")
            choice = self.startfn(possibles)
        else:
            count = 1
            for i in range(len(context)):
                key = ".".join(str(x) for x in context[i:])
                if key in choices:
                    items, weights = choices[key]
                    choice, abort = self.contextfn(choice, items, count)
                    if abort:
                        break
                    count += 1
        if choice is None:
            raise ValueError("could not find a choice")
        context.append(choice)
        self.context(context)
        return choice

    def subsets(self, min_, max_, fn: Callable, lst: List[Any]):
        if not isinstance(lst, list):
            lst = list(lst)
        for lo in range(0, len(lst) - min_ + 1):
            for hi in range(lo + min_ - 1, min(lo + max_ - 1, len(lst) - 1) + 1):
                fn(*lst[lo:hi+1])
        return self

    def update(self, possibles: Dict, preserve_pitches=False):
        if not isinstance(possibles, dict):
            raise ValueError("possibles must be dict")
        self.possibles = possibles
        self._choices = self._build_choices(possibles)
        if not preserve_pitches:
            self.pitches = []
            self.intervals = []
        return self
    