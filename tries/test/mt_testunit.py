#!/usr/bin/python2.6
# -*- coding: utf-8 -*-

import unittest
from multiLevelTries import multiLevelTries
from exception import pathExistsTriesException, triesException

def buildList(minSize, maxSize, charset):
    ret = []
    for l in range(minSize, maxSize+1):
        index = [0] * l
        
        for c in range(len(charset)**l):
            #build string
            s = ""
            divisor = 1
            for i in range(l):
                s = charset[index[i]] + s
        
            ret.append(s)
            #incremente
            index[0] += 1
            for i in range(len(index)):
                if(index[i] == len(charset)):
                    index[i] = 0
                    if i+1 < len(index):
                        index[i+1] += 1

    return ret

def buildMultiList(minSize, maxSize, listOrigin):
    ret = []
    for l in range(minSize, maxSize+1):
        index = [0] * l
        
        for c in range(len(listOrigin)**l):
            #build string
            s = []
            divisor = 1
            for i in range(l):
                s.append(listOrigin[index[i]])
        
            ret.append(s)
            #incremente
            index[0] += 1
            for i in range(len(index)):
                if(index[i] == len(listOrigin)):
                    index[i] = 0
                    if i+1 < len(index):
                        index[i+1] += 1

    return ret
    
class TraversalTest(unittest.TestCase):
    
    def setUp(self):
        self.mlt = multiLevelTries()
        toInsert = buildMultiList(1,3,buildList(1,3,["a","b"]))
        self.keyValue = {}
        
        for v in toInsert:
            tv = tuple(v)
            string = "".join(v)
            self.keyValue[tv] = string
            self.mlt.insert(tv,string)        
    
    #every inserted stringList are in the tree
    def test_everyKeyInTheTree(self):
        for k,v in self.keyValue.iteritems():
            self.assertTrue( self.mlt.search(k) == v)
    
    
    def _inner_test_everyValueCorrespondToAKey(self, path, node, state, level):
        if node.isValueSet():
            local_mltries = node.value
            
            newState = []
            newState.extend(state)
            newState.append(node.getCompleteName())
            
            if local_mltries.isValueSet():
                self.assertTrue( tuple(newState) in self.keyValue and self.keyValue[tuple(newState)] == local_mltries.value )
            
            
            local_mltries.localTries.genericDepthFirstTraversal(self._inner_test_everyValueCorrespondToAKey, newState)
            
        return state
            
    #a path in the tree comme from a stringList
    def test_everyValueCorrespondToAKey(self):
        self.mlt.localTries.genericDepthFirstTraversal(self._inner_test_everyValueCorrespondToAKey, [])
    
    #can't insert an existing path
    def test_insertExistingValue(self):
        self.assertRaises(pathExistsTriesException, self.mlt.insert,["a"],"a")
    
    #search a non existing path
    def test_tryToSearchANonExistingPath(self):
        self.assertRaises(triesException,self.mlt.search,["z"])
    
    #TODO test both TRAVERSAL
        #test stopTraversal
            #how ?
                #set some node at stopTraversal
                    #every layer 2, example of layer 2 [aa, aa]
                    #so we test the setStopTraveral
                
    
    def _inner_test_traversal(self, currentPath, node, traversalState, level):
        #check if it the path has already been met
        self.assertTrue(tuple(currentPath) not in traversalState[0])
        traversalState[0][tuple(currentPath)] = True
        
        #check if the node MLTries has been already met
        self.assertTrue(node.value not in traversalState[1])
        traversalState[1][node.value] = True
        
        #incremente the value node count
        newCount = traversalState[2]
        if node.isValueSet():
            #check if the key/value pair exists, and so if the path is correct
            self.assertTrue( tuple(currentPath) in self.keyValue and self.keyValue[tuple(currentPath)] == node.value )
        
            newCount += 1
        
        #check level
        self.assertTrue(len(currentPath) == level+1)
                    
        return (traversalState[0],traversalState[1],newCount,)
    
    def test_preOrderTraversal(self):
        self.assertTrue( self.mlt.genericDepthFirstTraversal(self._inner_test_traversal,({},{},0,), True)[2] == len(self.keyValue.keys())

        #do the traversal again, an execution of the traversal can't influence a second execution
        self.assertTrue( self.mlt.genericDepthFirstTraversal(self._inner_test_traversal,({},{},0,), True)[2] == len(self.keyValue.keys())

    def test_postOrderTraversal(self):
        self.assertTrue( self.mlt.genericDepthFirstTraversal(self._inner_test_traversal,({},{},0,), False)[2] == len(self.keyValue.keys())

        #do the traversal again, an execution of the traversal can't influence a second execution
        self.assertTrue( self.mlt.genericDepthFirstTraversal(self._inner_test_traversal,({},{},0,), False)[2] == len(self.keyValue.keys())

        
    def test_BreadthFirstTraversal(self):
        self.assertTrue( genericBreadthFirstTraversal(self._inner_test_traversal,({},{},0,))[2] == len(self.keyValue.keys())
            
    #test buildDictionnary
        #prblm with the traversal, no node explored...
    def test_buildDictWithoutPrefix(self):
        dico = self.mlt.buildDictionnary()
        self.assertTrue( len(dico) == len(self.keyValue))
        
        for k,v in dico.iteritems():
            print k,v
            self.assertTrue(k in self.keyValue and self.keyValue[k] == v)

    def test_buildDictWithPrefix(self):
        pass #TODO
            #TODO which prefix ?
                #random ? nop
                #every layer one prefix
                #then layer two
                
        #TODO compute and check the number of value to print
        #TODO check if the prefix is always correct
    
    #test update process
        #changer toutes les valeurs et vérifier que c'est bon
    def test_update(self):
        newKeyVal = {}
        for k,v in self.keyValue.iteritems():
            newVal = "plop"+v
            self.mlt.update(k, newVal)
            newKeyVal[k] = newVal
    
        for k,v in newKeyVal.iteritems():
            self.assertTrue( self.mlt.search(k) == v)
        
        
    #test the remove operation
        #remove all
    def test_removeAll(self):
        for k,v in self.keyValue.iteritems():
            self.mlt.remove(k)
            
        self.test_everyKeyInTheTree()
        self.test_everyValueCorrespondToAKey()
    
    def test_removeIntermediateNodeWithValue():
        pass #TODO remove value stored at intermediate node
    
    def test_removeIntermediateNodeWithoutValue():
        pass #TODO
    
    def test_removeEndValue():
        pass #TODO remove end value
        
    
if __name__ == '__main__':
    unittest.main()
