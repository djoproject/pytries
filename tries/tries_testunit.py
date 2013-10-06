#!/usr/bin/python2.6
# -*- coding: utf-8 -*-

import random
import unittest
from tries import tries

class TriesTestState(unittest.TestCase):
    def setUp(self):
        self.insertedKey = []
        self.t           = tries()
        
    def test_No1childInNonValueIntermediateNode(self):
        pass
        
    def test_OnlyRootCanHaveEmptyString(self):
        pass
        
    def test_EveryInsertedKeyMustBeInTree(self):
        for key in self.insertedKey:
            self.assertTrue( self.t.search(key) != None )

class TestSequenceFunctions(unittest.TestCase):

    def setUp(self):
        self.seq = range(10)

    def test_shuffle(self):
        # make sure the shuffled sequence does not lose any elements
        random.shuffle(self.seq)
        self.seq.sort()
        self.assertEqual(self.seq, range(10))

        # should raise an exception for an immutable sequence
        self.assertRaises(TypeError, random.shuffle, (1,2,3))

    def test_choice(self):
        element = random.choice(self.seq)
        self.assertTrue(element in self.seq)

    def plop_sample(self):
        with self.assertRaises(ValueError):
            random.sample(self.seq, 20)
        for element in random.sample(self.seq, 5):
            self.assertTrue(element in self.seq)

if __name__ == '__main__':
    unittest.main()