#!/usr/bin/python2.6
# -*- coding: utf-8 -*-

import random
import unittest
from tries import tries

class TriesTestState(unittest.TestCase):
    
    ### called before each test
    def setUp(self):
        self.insertedKey = ["bear", "be", "bearor", "beer", ""]
        self.t           = tries()
        self.keyValue    = {}
        
        for key in self.insertedKey:
            self.keyValue[key] = self.t.insert(key,key)

######### print just the tree
    def test_traversal_value(self):
        print ""
        print self.t.traversal()
        print ""

######### an intermediate node without value can't have less than 2 childs

    def test_No1childInNonValueIntermediateNode(self):
        self._inner_No1childInNonValueIntermediateNode(self.t)
    
    def _inner_No1childInNonValueIntermediateNode(self, node):
        if not node.isValueSet() and node.parent != None:
            self.assertTrue( len(node.childs) > 1)
            
        for c in node.childs:
            self._inner_No1childInNonValueIntermediateNode(c)
    
######### only the root can have an empty string as key

    def test_OnlyRootCanHaveEmptyString(self):
        self._inner_OnlyRootCanHaveEmptyString(self.t)
    
    def _inner_OnlyRootCanHaveEmptyString(self, node):
        if node.parent != None:
            self.assertTrue( node.key != None and node.key != "")

        for c in node.childs:
            self._inner_No1childInNonValueIntermediateNode(c)

######### every inserted key must be in the tree with 
        
    def test_EveryInsertedKeyMustBeInTree(self):
        for key,value in self.keyValue.iteritems():
            node = self.t.search(key)
            print key + " vs " + value.key + " vs "+node.key
            self.assertTrue( node != None and node.isValueSet() and node.value == key)#TODO  and node == value)

######## if the tree hold only one value, the root child can't have any child

    def test_if1valueOnly1Node(self):
        self.assertTrue(len(self.insertedKey) == 0 or (len(self.insertedKey) == 1 and self.t.isValueSet() and len(self.t.childs) == 0) or len(self.insertedKey) > 1)

####### test traversal
    def _traversal(self, path, node, state, level):
        state += 1
        return state
        
        pass #TODO try to test each value

    def test_traversal(self):
        self.assertTrue( self.t.genericDepthFirstTraversal(self._traversal, 0) == len(self.insertedKey))

if __name__ == '__main__':
    unittest.main()