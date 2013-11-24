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
    
    #make advanced search test
        #case perfect :
    def test_advancedResultPerfect(self):
        result = self.t.advancedSearch("beer")
        
        self.assertTrue(result.getPrefix() == "beer")
        self.assertTrue(result.getNode().getCompleteName() == "beer")
        self.assertTrue(result.getTotalCharFoundCount() > 0)
        self.assertTrue(result.getCharFoundOnLastExploredNodeCount() > 0)
        self.assertTrue(result.isPerfectMatch())
        self.assertTrue(not result.isPartialMatch())
        self.assertTrue(result.isMatch())
        self.assertTrue(not result.isNoMatchChild())
        self.assertTrue(not result.isFalseResult())
        self.assertTrue(result.getNode() != None)
        self.assertTrue(result.getPreviousNode()!= None)
        self.assertTrue(not result.isAmbiguous())
        
        #case partial :
    def test_advancedResultPartial(self):
        result = self.t.advancedSearch("bee")
        
        self.assertTrue(result.getPrefix() == "bee")
        self.assertTrue(result.getNode().getCompleteName() == "beer")
        self.assertTrue(result.getTotalCharFoundCount() > 0)
        self.assertTrue(result.getCharFoundOnLastExploredNodeCount() > 0)
        self.assertTrue(not result.isPerfectMatch())
        self.assertTrue(result.isPartialMatch())
        self.assertTrue(result.isMatch())
        self.assertTrue(not result.isNoMatchChild())
        self.assertTrue(not result.isFalseResult())
        self.assertTrue(result.getNode() != None)
        self.assertTrue(result.getPreviousNode()!= None)
        self.assertTrue(not result.isAmbiguous())
        #case false :
    def test_advancedResultFalse(self):
        result = self.t.advancedSearch("ba")
        
        self.assertTrue(result.getPrefix() == "ba")
        self.assertTrue(result.getTotalCharFoundCount() == 1)
        self.assertTrue(result.getCharFoundOnLastExploredNodeCount() == 1)
        self.assertTrue(not result.isPerfectMatch())
        self.assertTrue(not result.isPartialMatch())
        self.assertTrue(not result.isMatch())
        self.assertTrue(not result.isNoMatchChild())
        self.assertTrue(result.isFalseResult())
        self.assertTrue(result.getNode() == None)
        self.assertTrue(result.getPreviousNode()!= None)
        self.assertTrue(not result.isAmbiguous())
    
    #case no child :
    def test_advancedResultNoChild(self):
        result = self.t.advancedSearch("beb")
        
        self.assertTrue(result.getPrefix() == "beb")
        self.assertTrue(result.getTotalCharFoundCount() == 2)
        self.assertTrue(result.getCharFoundOnLastExploredNodeCount() == 2)
        self.assertTrue(not result.isPerfectMatch())
        self.assertTrue(not result.isPartialMatch())
        self.assertTrue(not result.isMatch())
        self.assertTrue(result.isNoMatchChild())
        self.assertTrue(not result.isFalseResult())
        self.assertTrue(result.getNode() == None)
        self.assertTrue(result.getPreviousNode()!= None)
        self.assertTrue(not result.isAmbiguous())
        
    #case ambiguous :   
    def test_advancedResultNoChild(self):
        result = self.t.advancedSearch("be")
        self.t.remove("be")
        
        self.assertTrue(result.getPrefix() == "be")
        self.assertTrue(result.getTotalCharFoundCount() == 2)
        self.assertTrue(result.getCharFoundOnLastExploredNodeCount() == 2)
        self.assertTrue(result.isPerfectMatch())
        self.assertTrue(not result.isPartialMatch())
        self.assertTrue(result.isMatch())
        self.assertTrue(not result.isNoMatchChild())
        self.assertTrue(not result.isFalseResult())
        self.assertTrue(result.getNode() != None)
        self.assertTrue(result.getPreviousNode()!= None)
        self.assertTrue(result.isAmbiguous())
        
if __name__ == '__main__':
    unittest.main()
