#!/usr/bin/python2.6
# -*- coding: utf-8 -*-

from tries.tries import tries
import unittest
from tries.test.tries_testunit import ElementaryTest

class SearchTest(unittest.TestCase, ElementaryTest):
    
    ### called before each test
    def setUp(self):
        
        self.insertedKey = ["bear", "be", "bearor", "beer", ""] #test every case in the insert function
        #bear        (insert in empty tree)
        #    be      (partial match)
        #    bearor  (no match child)
        #    beer    (false result)
        self.t           = tries()
        self.keyValue    = {}
        
        for key in self.insertedKey:
            self.keyValue[key] = self.t.insert(key,key).value


    def test_ExactResult(self):
        self.assertTrue(self.t.searchNode("beer",lambda *a:0, lambda *a:1, lambda *a:2, lambda *a:3 ) == 0)
        
    def test_PartialResult(self):
        self.assertTrue(self.t.searchNode("bee",lambda *a:0, lambda *a:1, lambda *a:2, lambda *a:3 ) == 1)
        
    def test_noMatchChild(self):
        self.assertTrue(self.t.searchNode("bet",lambda *a:0, lambda *a:1, lambda *a:2, lambda *a:3 ) == 2)
        
    def test_falseResult(self):
        self.assertTrue(self.t.searchNode("beet",lambda *a:0, lambda *a:1, lambda *a:2, lambda *a:3 ) == 3)
        
if __name__ == '__main__':
    unittest.main()