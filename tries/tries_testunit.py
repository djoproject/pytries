#!/usr/bin/python2.6
# -*- coding: utf-8 -*-

import random
import unittest
from tries import tries
from exception import triesException

#ELEMENTARY TREE PROPERTIES (all this properties must always be verified to get a valid tree)
class ElementaryTest(object):
    
#1 INSERT
    #1.1 every inserted key are in the tree
    def test_EveryInsertedKeyMustBeInTree(self):
        for key,value in self.keyValue.iteritems():
            node = self.t.search(key)
            #print key + " vs " + value.key + " vs "+node.key
            self.assertTrue( node != None and node.isValueSet() and node.value == key)
            #This condition can be true, because key and value are moved in the insert process of the other nodes  and node == value)
            
    #1.2 each key appears only once, no redundant path
        #TODO
        
    #1.3 every value node come from the insertion of a key
        #TODO
    
    #1.4 the value of a node corresponds to the path string of the insertion
        #TODO
        
    #1.5 if the tree hold only one value, the root child can't have any child
    def test_if1valueOnly1Node(self):
        self.assertTrue(len(self.insertedKey) == 0 or (len(self.insertedKey) == 1 and self.t.isValueSet() and len(self.t.childs) == 0) or len(self.insertedKey) > 1)
        
#2 CHILD (end node = no child)
    #2.1 an intermediate node without value must have more than 1 child (or its existence is useless)
    def test_No1childInNonValueIntermediateNode(self):
        self._inner_No1childInNonValueIntermediateNode(self.t)
    
    def _inner_No1childInNonValueIntermediateNode(self, node):
        if not node.isValueSet() and node.parent != None:
            self.assertTrue( len(node.childs) > 1)
            
        for c in node.childs:
            self._inner_No1childInNonValueIntermediateNode(c)
            
    #2.2 every end node are value node, except an empty root
        #TODO

#3 KEY STRING
    #3.1 only the root node can have the empty string as key
    def test_OnlyRootCanHaveEmptyString(self):
        self._inner_OnlyRootCanHaveEmptyString(self.t)
    
    def _inner_OnlyRootCanHaveEmptyString(self, node):
        if node.parent != None:
            self.assertTrue( node.key != None and node.key != "")

        for c in node.childs:
            self._inner_No1childInNonValueIntermediateNode(c)
    
    #3.2 every no root node must have a key length of more than 0
        #TODO

#4. PARENT
    #4.1 a child node must have its parent in the variable parent
        #TODO
        
    #4.2 there is always only one root
        #TODO
        
    #4.3 no cycle is allowed
        #TODO

class TriesTestState(unittest.TestCase, ElementaryTest):
    
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
