#!/usr/bin/python2.6
# -*- coding: utf-8 -*-

import random
import unittest
from tries import tries
from exception import triesException

class TriesTestState(unittest.TestCase):
    
    ### called before each test
    def setUp(self):
        self.insertedKey = ["bear", "be", "bearor", "beer", ""]
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
            #print key + " vs " + value.key + " vs "+node.key
            self.assertTrue( node != None and node.isValueSet() and node.value == key)
            #This condition can be true, because key and value are moved in the insert process of the other nodes  and node == value)

######## if the tree hold only one value, the root child can't have any child

    def test_if1valueOnly1Node(self):
        self.assertTrue(len(self.insertedKey) == 0 or (len(self.insertedKey) == 1 and self.t.isValueSet() and len(self.t.childs) == 0) or len(self.insertedKey) > 1)

####### test traversal
    def _traversal(self, path, node, state, level):
        counter = state[2]+1
        
        
        #each path must appear only once
        self.assertTrue(path not in state[0])
        pathDict = state[0]
        pathDict[path] = True
        
        #each node must appear only once
        self.assertTrue(node not in state[1])
        nodeDict = state[1]
        nodeDict[node] = True
        
        #check path, compare path with path rebuilder
        self.assertTrue( node.getCompleteName() == path )
        
        #check value
        if node.isValueSet():
            #print "value : "+str(node.value) + " vs " + self.keyValue[path]
            self.assertTrue( node.value == self.keyValue[path] )
        
        #check level
        currentLevel = 0
        cur = node.parent
        while cur != None:
            currentLevel += 1
            cur = cur.parent
        self.assertTrue( currentLevel == level)
        
        return (pathDict,nodeDict,counter)

    def test_traversal(self):
        #the number of traversal is equal to the number of node
        self.assertTrue( self.t.genericDepthFirstTraversal(self._traversal, ({},{},0,))[2] == len(self.insertedKey))

if __name__ == '__main__':
    unittest.main()
