#!/usr/bin/python2.6
# -*- coding: utf-8 -*-

from tries.tries import tries
import unittest
from tries.test.tries_testunit import ElementaryTest

class TraversalTest(unittest.TestCase, ElementaryTest):
    
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
        
        #do the traversal again, an execution of the traversal can't influence a second execution
        self.assertTrue( self.t.genericDepthFirstTraversal(self._traversal, ({},{},0,))[2] == len(self.insertedKey))

    def test_BreadthFirstTraversal(self):
        self.assertTrue( self.t.genericBreadthFirstTraversal(self._traversal, ({},{},0,))[2] == len(self.insertedKey))
        
    def test_traversal_post(self):
        #the number of traversal is equal to the number of node
        self.assertTrue( self.t.genericDepthFirstTraversal(self._traversal, ({},{},0,), False)[2] == len(self.insertedKey))
        
        #do the traversal again, an execution of the traversal can't influence a second execution
        self.assertTrue( self.t.genericDepthFirstTraversal(self._traversal, ({},{},0,), False)[2] == len(self.insertedKey))

if __name__ == '__main__':
    unittest.main()
