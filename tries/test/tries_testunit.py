#!/usr/bin/python2.6
# -*- coding: utf-8 -*-

import unittest
from tries.tries import tries
from tries.exception import triesException

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
    def test_noRedundantPath(self):
        self._inner_test_noRedundantPath(self.t)
    
    def _inner_test_noRedundantPath(self, node):
        #two childs can't begin with the same letter
        for i in range(0,len(node.childs)):
            for j in range(i+1,len(node.childs)):
                self.assertTrue(node.childs[i].key[0] != node.childs[j].key[0])
        
        for c in node.childs:
            self._inner_test_aValueNodeHadBeenInserted(c)
        
    #1.3 every value node come from the insertion of a key
    #1.4 the value of a node corresponds to the path string of the insertion
    def test_aValueNodeHadBeenInserted(self):
        self._inner_test_aValueNodeHadBeenInserted(self.t)
        
    def _inner_test_aValueNodeHadBeenInserted(self,node):
        cpath = node.getCompleteName()
        self.assertTrue(not node.isValueSet() or (node.isValueSet() and cpath in self.keyValue and node.value == self.keyValue[cpath]) )
        
        for c in node.childs:
            self._inner_test_aValueNodeHadBeenInserted(c)
        
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
    def test_everyEndNodeAreValueNode(self):
        for c in self.t.childs:
            self._inner_test_everyEndNodeAreValueNode(c)
        
    def _inner_test_everyEndNodeAreValueNode(self, node):
        self.assertTrue(len(node.childs) > 0 or (len(node.childs) == 0 and node.isValueSet()) )
        
        for c in node.childs:
            self._inner_test_everyEndNodeAreValueNode(c)
    
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
    def test_keyStringBiggerThanOne(self):
        for c in self.t.childs:
            self._inner_test_keyStringBiggerThanOne(c)
    
    def _inner_test_keyStringBiggerThanOne(self,node):
        self.assertTrue(len(node.key) > 0)
        
        for c in node.childs:
            self._inner_test_keyStringBiggerThanOne(c)
    
#4. PARENT
    #4.1 a child node must have its parent in the variable parent    
    def test_node_linked_to_its_parent(self):
        self._inner_test_node_linked_to_its_parent(self.t, None)
        
    def _inner_test_node_linked_to_its_parent(self, node, parent):
        self.assertTrue( node.parent == parent)
        
        for c in node.childs:
            self._inner_test_node_linked_to_its_parent(c, node)
    
    #4.2 there is always only one root
    def test_onlyOneRoot(self):
        self.assertTrue( self.t.parent == None)
        
        for c in self.t.childs:
            self._inner_test_onlyOneRoot(c)
    
    def _inner_test_onlyOneRoot(self, node):
        self.assertTrue( node.parent != None)
        self.assertIsInstance(node.parent, tries)
        
        for c in node.childs:
            self._inner_test_onlyOneRoot(c)
    
    #4.3 no cycle is allowed
    def test_noCycle(self):
        self._inner_test_noCycle(self.t)
    
    def _inner_test_noCycle(self,node):
        self.assertTrue("nocycle" not in node.__dict__.keys())
        node.nocycle = True
        
        for c in node.childs:
            self._inner_test_noCycle(c)

    ######### print just the tree
    #def test_traversal_value(self):
    #    print ""
    #    print self.t.traversal()
    #    print ""

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

if __name__ == '__main__':
    unittest.main()
