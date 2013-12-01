#!/usr/bin/python2.6
# -*- coding: utf-8 -*-

import unittest
from tries.tries import tries
from tries.test.tries_testunit import ElementaryTest
from tries.exception import triesException

class InsertTest(unittest.TestCase, ElementaryTest):
    
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
    
    ######### try to insert an existing key
    def test_insertExistingKey(self):
        self.assertRaises(triesException, self.t.insert,"beer","beer")
        
if __name__ == '__main__':
    unittest.main()
