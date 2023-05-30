# -*- coding: utf-8 -*-

class Automata:
    def __init__(self, alphabet, pattern):
        self.numstates = len(pattern) + 1
        self.alphabet = alphabet
        self.transitionTable = {}
        self.buildTransitionTable(pattern)
        self.final_state = self.numstates - 1
        self.pattern = pattern

    def buildTransitionTable(self, pattern):
        for q in range(self.numstates):
            for a in self.alphabet:
                prefix = pattern[:q] + a
                self.transitionTable[(q, a)] = self.overlap(prefix, pattern)

    def printAutomata(self):
        print("States:", self.numstates)
        print("Alphabet:", self.alphabet)
        print("Transition table:")
        for k in self.transitionTable.keys():
            print(k[0], ",", k[1], " -> ", self.transitionTable[k])

    def nextState(self, current, symbol):
        while current > 0 and symbol != self.pattern[current - 1]:
            current = self.transitionTable[(current, symbol)]
            if symbol == self.pattern[current - 1]:
                current += 1
            else:
                current = 0
        return current

    def applySeq(self, seq):
        q = 0
        res = [q]
        for c in seq:
            q = self.nextState(q, c)
            res.append(q)
        if res[-1] == self.final_state:
            res.pop()
        return res

    def occurrencesPattern(self, text):
        res = []
        count = 0
        for state in self.applySeq(text):
            if state == self.final_state:
                res.append(count - len(self.pattern) + 1)
            count += 1
        return res

    def overlap(self, s1, s2):
        maxov = min(len(s1), len(s2))
        for i in range(maxov, 0, -1):
            if s1[-i:] == s2[:i]:
                return i
        return 0

from unittest import TestCase
from Automata import Automata

class TestAutomata(TestCase):
    def test_types(self):
        auto = Automata("AC", "ACA")
        self.assertRaises(TypeError, auto.check_pattern_alphabet, "phge")
        self.assertRaises(TypeError, auto.check_pattern_alphabet, True)
        self.assertRaises(TypeError, auto.check_pattern_alphabet, 1654)
        self.assertRaises(TypeError, auto.check_pattern_alphabet, "AC", "BBB")
        self.assertRaises(TypeError, auto.check_pattern_alphabet, "AC", 2134)
        self.assertRaises(TypeError, auto.check_pattern_alphabet, 1234, "ACA")

