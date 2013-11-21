#!/usr/bin/python2.6
# -*- coding: utf-8 -*-

import unittest
from tries import multiLevelTries
from tries.tries import triesSearchResult
from tries.exception import *


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
    
class mltriesTest(unittest.TestCase):
    
    def setUp(self):
        self.mlt           = multiLevelTries()
        self.mltlist       = buildList(1,3,["a","b"])
        self.numberOfLevel = 3
        toInsert           = buildMultiList(1,self.numberOfLevel,self.mltlist)
        self.keyValue      = {}
        
        for v in toInsert:
            tv = tuple(v)
            string = "".join(v)
            self.keyValue[tv] = string
            self.mlt.insert(tv,string)        

### basics

    #every inserted stringList are in the tree
    """def test_everyKeyInTheTree(self):
        for k,v in self.keyValue.iteritems():
            mlt = self.mlt.search(k)
            if mlt == None:
                print "missing key <",k,">"
            self.assertTrue(mlt != None and mlt.value == v)
    
    
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
        #self.assertRaises(triesException,self.mlt.search,["z"])
        self.assertTrue(self.mlt.search(["z"]) == None)

### traversal

    def _inner_test_traversal(self, currentPath, node, traversalState, level):
        #check if it the path has already been met
        self.assertTrue(tuple(currentPath) not in traversalState[0])
        traversalState[0][tuple(currentPath)] = True
        
        #check if the node MLTries has been already met
        self.assertTrue(node not in traversalState[1])
        traversalState[1][node] = True
        
        #incremente the value node count
        newCount = traversalState[2]
        if node.isValueSet():
            
            #check if the key/value pair exists, and so if the path is correct
            self.assertTrue( tuple(currentPath) in self.keyValue and self.keyValue[tuple(currentPath)] == node.value )
        
            newCount += 1
        
        #check level
        self.assertTrue(len(currentPath) == level)
                    
        return (traversalState[0],traversalState[1],newCount,)

    def test_preOrderTraversal(self):
        last_state = self.mlt.genericDepthFirstTraversal(self._inner_test_traversal,({},{},0,), True)
        self.assertTrue( last_state[2] == len(self.keyValue.keys()))

        #do the traversal again, an execution of the traversal can't influence a second execution
        self.assertTrue( self.mlt.genericDepthFirstTraversal(self._inner_test_traversal,({},{},0,), True)[2] == len(self.keyValue.keys()))


    def test_postOrderTraversal(self):
        self.assertTrue( self.mlt.genericDepthFirstTraversal(self._inner_test_traversal,({},{},0,), False)[2] == len(self.keyValue.keys()))

        #do the traversal again, an execution of the traversal can't influence a second execution
        self.assertTrue( self.mlt.genericDepthFirstTraversal(self._inner_test_traversal,({},{},0,), False)[2] == len(self.keyValue.keys()))

    def test_BreadthFirstTraversal(self):
        self.assertTrue( self.mlt.genericBreadthFirstTraversal(self._inner_test_traversal,({},{},0,))[2] == len(self.keyValue.keys()))

    def test_preOrderTraversalWithStopTraversalLayer1(self):
        #update stopTraversal on node
        for key in self.mltlist:
            self.mlt.setStopTraversal((key,),True)        
            
        self.assertTrue( self.mlt.genericDepthFirstTraversal(self._inner_test_traversal,({},{},0,), True)[2] == len(self.mltlist))

        #do the traversal again, an execution of the traversal can't influence a second execution
        self.assertTrue( self.mlt.genericDepthFirstTraversal(self._inner_test_traversal,({},{},0,), True)[2] == len(self.mltlist))


    def test_postOrderTraversalWithStopTraversalLayer1(self):
        #update stopTraversal on node
        for key in self.mltlist:
            self.mlt.setStopTraversal((key,),True)  
        
        self.assertTrue( self.mlt.genericDepthFirstTraversal(self._inner_test_traversal,({},{},0,), False)[2] == len(self.mltlist))

        #do the traversal again, an execution of the traversal can't influence a second execution
        self.assertTrue( self.mlt.genericDepthFirstTraversal(self._inner_test_traversal,({},{},0,), False)[2] == len(self.mltlist))

    def test_BreadthFirstTraversalWithStopTraversalLayer1(self):
        #update stopTraversal on node
        for key in self.mltlist:
            self.mlt.setStopTraversal((key,),True)  
        
        self.assertTrue( self.mlt.genericBreadthFirstTraversal(self._inner_test_traversal,({},{},0,))[2] == len(self.mltlist))

    def test_preOrderTraversalWithStopTraversalLayer2(self):
        #update stopTraversal on node
        for key1 in self.mltlist:
            for key2 in self.mltlist:
                self.mlt.setStopTraversal((key1,key2,),True)

        self.assertTrue( self.mlt.genericDepthFirstTraversal(self._inner_test_traversal,({},{},0,), True)[2] == (len(self.mltlist)**2 + len(self.mltlist)))

        #do the traversal again, an execution of the traversal can't influence a second execution
        self.assertTrue( self.mlt.genericDepthFirstTraversal(self._inner_test_traversal,({},{},0,), True)[2] == (len(self.mltlist)**2 + len(self.mltlist)))


    def test_postOrderTraversalWithStopTraversalLayer2(self):
        #update stopTraversal on node
        for key1 in self.mltlist:
            for key2 in self.mltlist:
                self.mlt.setStopTraversal((key1,key2,),True)  
        
        self.assertTrue( self.mlt.genericDepthFirstTraversal(self._inner_test_traversal,({},{},0,), False)[2] == (len(self.mltlist)**2 + len(self.mltlist)))

        #do the traversal again, an execution of the traversal can't influence a second execution
        self.assertTrue( self.mlt.genericDepthFirstTraversal(self._inner_test_traversal,({},{},0,), False)[2] == (len(self.mltlist)**2 + len(self.mltlist)))

    def test_BreadthFirstTraversalWithStopTraversalLayer2(self):
        #update stopTraversal on node
        for key1 in self.mltlist:
            for key2 in self.mltlist:
                self.mlt.setStopTraversal((key1,key2,),True)  
        
        state = self.mlt.genericBreadthFirstTraversal(self._inner_test_traversal,({},{},0,))
        self.assertTrue( state[2] == (len(self.mltlist)**2 + len(self.mltlist)))


#### test buildDictionnary
        #prblm with the traversal, no node explored...
    def test_buildDictWithoutPrefix(self):
        dico = self.mlt.buildDictionnary()
        self.assertTrue( len(dico) == len(self.keyValue))
        
        for k,v in dico.iteritems():
            self.assertTrue(k in self.keyValue and self.keyValue[k] == v)

    def test_buildDictWithPrefix(self):
        expectedValueCount = len(self.mltlist)**2 + len(self.mltlist) + 1
        
        #one key prefix
        for key in self.mltlist:
            dico = self.mlt.buildDictionnary( (key,) , False, True)
            #print key, len(dico), expectedValueCount
            
            #i = 0
            #for k,v in dico.iteritems():
            #    print i, k
            #    i+=1
            
            self.assertTrue( len(dico) == expectedValueCount)

            for k,v in dico.iteritems():
                self.assertTrue(len(k) > 0 and k[0] == key)
                self.assertTrue(k in self.keyValue and self.keyValue[k] == v)
        
        expectedValueCount = len(self.mltlist) + 1
        #two key prefix
        for key1 in self.mltlist:
            for key2 in self.mltlist:
                dico = self.mlt.buildDictionnary( (key1,key2,) , False, True)
                #print len(dico), expectedValueCount
                self.assertTrue( len(dico) == expectedValueCount)
                
                for k,v in dico.iteritems():
                    self.assertTrue(len(k) > 1 and k[0] == key1 and k[1] == key2)
                    self.assertTrue(k in self.keyValue and self.keyValue[k] == v)

    def test_buildDictWithPrefixNotIncludedInTheResult(self):
        expectedValueCount = len(self.mltlist)**2 + len(self.mltlist) + 1
        
        #one key prefix
        for key in self.mltlist:
            dico = self.mlt.buildDictionnary( (key,) , False, False)
            #print key, len(dico), expectedValueCount
            self.assertTrue( len(dico) == expectedValueCount)
            
            for k,v in dico.iteritems():
                #self.assertTrue(len(k) > 0 and k[0] == key)
                keys = [key]
                keys.extend(k)
                keys = tuple(keys)
                self.assertTrue(keys in self.keyValue and self.keyValue[keys] == v)
        
        expectedValueCount = len(self.mltlist) + 1
        #two key prefix
        for key1 in self.mltlist:
            for key2 in self.mltlist:
                dico = self.mlt.buildDictionnary( (key1,key2,) , False, False)
                self.assertTrue( len(dico) == expectedValueCount)
                
                for k,v in dico.iteritems():
                    keys = [key1, key2]
                    keys.extend(k)
                    #self.assertTrue(len(k) > 1 and k[0] == key1 and k[1] == key2)
                    keys = tuple(keys)
                    self.assertTrue(keys in self.keyValue and self.keyValue[keys] == v)

#### update

    #test update process
        #changer toutes les valeurs et vérifier que c'est bon
    def test_update(self):
        newKeyVal = {}
        for k,v in self.keyValue.iteritems():
            newVal = "plop"+v
            self.mlt.update(k, newVal)
            newKeyVal[k] = newVal
    
        for k,v in newKeyVal.iteritems():
            mlt = self.mlt.search(k)
            self.assertTrue(mlt != None and mlt.value == v)
            #self.assertTrue( self.mlt.search(k) == v)


#### remove test
        
    #test the remove operation
        #remove all
    def test_removeAll(self):
        for k,v in self.keyValue.iteritems():
            self.mlt.remove(k)
            
        self.keyValue = {}
        self.test_everyKeyInTheTree()
        self.test_everyValueCorrespondToAKey()


    def test_removeIntermediateNodeWithValueLevel1(self):
        for key1 in self.mltlist:
            self.mlt.remove( (key1,) )
            del self.keyValue[(key1,)]
            
        self.test_everyKeyInTheTree()
        self.test_everyValueCorrespondToAKey()

    
    def test_removeIntermediateNodeWithValueLevel2(self):
        for key1 in self.mltlist:
            for key2 in self.mltlist:
                self.mlt.remove( (key1,key2,) )
                del self.keyValue[(key1,key2,)]
                
        self.test_everyKeyInTheTree()
        self.test_everyValueCorrespondToAKey()
    
    def test_removeIntermediateNodeWithValueLevel1and2(self):
        for key1 in self.mltlist:
            self.mlt.remove( (key1,) )
            del self.keyValue[(key1,)]
            for key2 in self.mltlist:
                self.mlt.remove( (key1,key2,) )
                del self.keyValue[(key1,key2,)]

        self.test_everyKeyInTheTree()
        self.test_everyValueCorrespondToAKey()
        
    def test_removeEndValue(self):
        for key1 in self.mltlist:
            for key2 in self.mltlist:
                for key3 in self.mltlist:
                    self.mlt.remove( (key1,key2,key3,) )
                    del self.keyValue[(key1,key2,key3,)]
        self.test_everyKeyInTheTree()
        self.test_everyValueCorrespondToAKey()
        
    def test_removeIntermediateNodeWithoutValue(self):
        #remove every intermediate node
        for key1 in self.mltlist:
            self.mlt.remove( (key1,) )
            del self.keyValue[(key1,)]
            for key2 in self.mltlist:
                self.mlt.remove( (key1,key2) )
                del self.keyValue[(key1,key2,)]
        
        #try to remove them againje suis en train de tester.  J
        for key1 in self.mltlist:
            self.assertRaises(pathNotExistsTriesException,self.mlt.remove, (key1,))
            for key2 in self.mltlist:
                self.assertRaises(pathNotExistsTriesException,self.mlt.remove, (key1,key2,))
        
        #check the tree
        self.test_everyKeyInTheTree()
        self.test_everyValueCorrespondToAKey()

#empty path

    def test_insertEmptyPathAlone(self):
        mlt = multiLevelTries()
        mlt.insert([],"empty path")
        mltnode = mlt.search()
        self.assertTrue(mltnode != None and mltnode.value == "empty path")
        
    def test_insertEmptyPathNotAlone(self):
        #self.mlt = multiLevelTries()
        self.mlt.insert([],"empty path")
        mltnode = self.mlt.search()
        self.assertTrue(mltnode != None and mltnode.value == "empty path")
    
        #check the tree
        self.test_everyKeyInTheTree()
        self.test_everyValueCorrespondToAKey()
    
    def test_insertExistingEmptyPathAlone(self):
        mlt = multiLevelTries()
        mlt.insert([],"empty path")
        self.assertRaises(pathExistsTriesException, mlt.insert,[],"plop")
        
    def test_insertExistingEmptyPathNotAlone(self):
        #self.mlt = multiLevelTries()
        self.mlt.insert([],"empty path")
        self.assertRaises(pathExistsTriesException, self.mlt.insert,[],"plop")
        
        #check the tree
        self.test_everyKeyInTheTree()
        self.test_everyValueCorrespondToAKey()
    
    def test_removeEmptyPathAlone(self):
        mlt = multiLevelTries()
        mlt.insert([],"empty path")
        mlt.remove()
        mltnode = mlt.search()
        self.assertTrue(mltnode == None)
        
    def test_removeEmptyPathNotAlone(self):
        #self.mlt = multiLevelTries()
        self.mlt.insert([],"empty path")
        self.mlt.remove()
        mltnode = self.mlt.search()
        self.assertTrue(mltnode == None)
        
        #check the tree
        self.test_everyKeyInTheTree()
        self.test_everyValueCorrespondToAKey()
        
    def test_updateEmptyPathAlone(self):
        mlt = multiLevelTries()
        mlt.insert([],"empty path")
        mltnode = mlt.search()
        mlt.update((), "plop")
        self.assertTrue(mltnode != None and mltnode.value == "plop")
        
    def test_updateEmptyPathNotAlone(self):
        #self.mlt = multiLevelTries()
        self.mlt.insert([],"empty path")
        mltnode = self.mlt.search()
        self.mlt.update((), "plop")
        self.assertTrue(mltnode != None and mltnode.value == "plop")
        
        #check the tree
        self.test_everyKeyInTheTree()
        self.test_everyValueCorrespondToAKey()

    

### remove branch
    #remove branch with an empty tree, empty list or random path
        #remove branch in level 0 (empty list), level 1, level 2, ...
        
    def test_removeBranchEmptyPath(self):
        self.mlt.removeBranch()
        self.assertTrue(self.mlt.isEmpty())
        
    def test_removeBranchLevel1(self):
        self.mlt.removeBranch(["a"])
        
        #remove from dict every key that starts with "a"
        newDico = {}
        for k,v in self.keyValue.iteritems():
            if len(k) > 0 and k[0] == "a":
                continue
            newDico[k] = v
        self.keyValue = newDico
        
        #check the tree
        self.test_everyKeyInTheTree()
        self.test_everyValueCorrespondToAKey()
        
    def test_removeBranchLevel1(self):
        self.mlt.removeBranch(["a", "a"])
        
        #remove from dict every key that starts with "a","a"
        newDico = {}
        for k,v in self.keyValue.iteritems():
            if len(k) > 1 and k[0] == "a" and k[1] == "a":
                continue
            newDico[k] = v
        self.keyValue = newDico
        
        #check the tree
        self.test_everyKeyInTheTree()
        self.test_everyValueCorrespondToAKey()"""

### TODO test advanced search (how to test every case ? no, only specific case)
    #on level 0, level 1, level 2, ...
      
    #TODO XXX case 0 : empty path (found/not found)
    
     
    #case 1 : path not found
    def test_AdvancedSearchCaseNoMatch(self):
        ### level 1
        searchResult = self.mlt.advancedSearch(("k",))
        
        self.assertTrue(not searchResult.isPathFound())
        self.assertTrue(not searchResult.isValueFound())
        #self.assertTrue(searchResult.getMltFound() ) #assert if result
        self.assertRaises(pathNotExistsTriesException, searchResult.getMltFound) #assert if exception
        #self.assertTrue(searchResult.getValue()) #assert if result
        self.assertRaises(noValueSetTriesException, searchResult.getValue) #assert if exception
        self.assertTrue( len(searchResult.getFoundTokenList()) == 0)
        self.assertTrue(len(searchResult.getFoundCompletePath()) == 0)
        self.assertTrue( len(searchResult.getNotFoundTokenList()) == 1 )
        self.assertTrue(searchResult.getTokenFoundCount() == 0)
        self.assertTrue(searchResult.getTokenNotFoundCount() == 1) 
        self.assertTrue(searchResult.getTotalTokenCount() == 1)
        self.assertTrue(searchResult.getTokenUsed() == 1)
        self.assertTrue(searchResult.getTokenNotUsed() == 0)
        self.assertTrue(not searchResult.isAvalueOnTheLastTokenFound())
        #self.assertTrue(searchResult.getLastTokenFoundValue()) #assert if result
        self.assertRaises(noValueSetTriesException, searchResult.getLastTokenFoundValue) #assert if exception
        #self.assertTrue(searchResult.isAllTokenHasBeenConsumed()) 
        self.assertTrue(not searchResult.isLastExploredTriesEmpty())
        self.assertTrue(searchResult.isTokenNotFoundInLastTries())
        self.assertTrue(not searchResult.isPathCorrespondsToNonValueNode())
        self.assertTrue(searchResult.isPerfectSearchSet())
        self.assertTrue(not searchResult.isAmbiguous())
        #self.assertTrue(searchResult.getAdvancedTriesResult(tokenIndex))
        for i in range(0,searchResult.getTokenUsed()):
            astries =  searchResult.getAdvancedTriesResult(i)
            self.assertTrue(astries != None)
            self.assertTrue(isinstance(astries, triesSearchResult))
            self.assertTrue(astries.isNoMatchChild())
        
        self.assertRaises(triesException,searchResult.getAdvancedTriesResult,searchResult.getTokenUsed())
        
        astries = searchResult.getAdvancedTriesResultForLastTokenExplored()
        self.assertTrue(astries != None)
        self.assertTrue(isinstance(astries, triesSearchResult))
        self.assertTrue(astries.isNoMatchChild())
        
        
        ### level 2
        searchResult = self.mlt.advancedSearch(("a","k",))
        
        self.assertTrue(not searchResult.isPathFound())
        self.assertTrue(not searchResult.isValueFound())
        #self.assertTrue(searchResult.getMltFound() ) #assert if result
        self.assertRaises(pathNotExistsTriesException, searchResult.getMltFound) #assert if exception
        #self.assertTrue(searchResult.getValue()) #assert if result
        self.assertRaises(noValueSetTriesException, searchResult.getValue) #assert if exception
        self.assertTrue( len(searchResult.getFoundTokenList()) == 1)
        self.assertTrue(len(searchResult.getFoundCompletePath()) == 1)
        self.assertTrue( len(searchResult.getNotFoundTokenList()) == 1 )
        self.assertTrue(searchResult.getTokenFoundCount() == 1)
        self.assertTrue(searchResult.getTokenNotFoundCount() == 1) 
        self.assertTrue(searchResult.getTotalTokenCount() == 2)
        self.assertTrue(searchResult.getTokenUsed() == 2)
        self.assertTrue(searchResult.getTokenNotUsed() == 0)
        self.assertTrue(searchResult.isAvalueOnTheLastTokenFound())
        self.assertTrue(searchResult.getLastTokenFoundValue() == "a") #assert if result
        #self.assertRaises(noValueSetTriesException, searchResult.getLastTokenFoundValue) #assert if exception
        #self.assertTrue(searchResult.isAllTokenHasBeenConsumed()) 
        self.assertTrue(not searchResult.isLastExploredTriesEmpty())
        self.assertTrue(searchResult.isTokenNotFoundInLastTries())
        self.assertTrue(not searchResult.isPathCorrespondsToNonValueNode())
        self.assertTrue(searchResult.isPerfectSearchSet())
        self.assertTrue(not searchResult.isAmbiguous())
        #self.assertTrue(searchResult.getAdvancedTriesResult(tokenIndex))
        for i in range(0,searchResult.getTokenUsed()):
            astries =  searchResult.getAdvancedTriesResult(i)
            self.assertTrue(astries != None)
            self.assertTrue(isinstance(astries, triesSearchResult))
            if i == searchResult.getTokenUsed()-1:
                self.assertTrue(astries.isNoMatchChild())
            else:
                self.assertTrue(astries.isMatch())
        
        self.assertRaises(triesException,searchResult.getAdvancedTriesResult,searchResult.getTokenUsed())
        
        astries = searchResult.getAdvancedTriesResultForLastTokenExplored()
        self.assertTrue(astries != None)
        self.assertTrue(isinstance(astries, triesSearchResult))
        self.assertTrue(astries.isNoMatchChild())
        
        #level 3
        searchResult = self.mlt.advancedSearch(("a","b","k",))
        
        self.assertTrue(not searchResult.isPathFound())
        self.assertTrue(not searchResult.isValueFound())
        #self.assertTrue(searchResult.getMltFound() ) #assert if result
        self.assertRaises(pathNotExistsTriesException, searchResult.getMltFound) #assert if exception
        #self.assertTrue(searchResult.getValue()) #assert if result
        self.assertRaises(noValueSetTriesException, searchResult.getValue) #assert if exception
        self.assertTrue( len(searchResult.getFoundTokenList()) == 2)
        self.assertTrue(len(searchResult.getFoundCompletePath()) == 2)
        self.assertTrue( len(searchResult.getNotFoundTokenList()) == 1 )
        self.assertTrue(searchResult.getTokenFoundCount() == 2)
        self.assertTrue(searchResult.getTokenNotFoundCount() == 1) 
        self.assertTrue(searchResult.getTotalTokenCount() == 3)
        self.assertTrue(searchResult.getTokenUsed() == 3)
        self.assertTrue(searchResult.getTokenNotUsed() == 0)
        self.assertTrue(searchResult.isAvalueOnTheLastTokenFound())
        print searchResult.getLastTokenFoundValue()
        self.assertTrue(searchResult.getLastTokenFoundValue() == "ab") #assert if result
        #self.assertRaises(noValueSetTriesException, searchResult.getLastTokenFoundValue) #assert if exception
        #self.assertTrue(searchResult.isAllTokenHasBeenConsumed()) 
        self.assertTrue(not searchResult.isLastExploredTriesEmpty())
        self.assertTrue(searchResult.isTokenNotFoundInLastTries())
        self.assertTrue(not searchResult.isPathCorrespondsToNonValueNode())
        self.assertTrue(searchResult.isPerfectSearchSet())
        self.assertTrue(not searchResult.isAmbiguous())
        #self.assertTrue(searchResult.getAdvancedTriesResult(tokenIndex))
        for i in range(0,searchResult.getTokenUsed()):
            astries =  searchResult.getAdvancedTriesResult(i)
            self.assertTrue(astries != None)
            self.assertTrue(isinstance(astries, triesSearchResult))
            if i == searchResult.getTokenUsed()-1:
                self.assertTrue(astries.isNoMatchChild())
            else:
                self.assertTrue(astries.isMatch())
        
        self.assertRaises(triesException,searchResult.getAdvancedTriesResult,searchResult.getTokenUsed())
        
        astries = searchResult.getAdvancedTriesResultForLastTokenExplored()
        self.assertTrue(astries != None)
        self.assertTrue(isinstance(astries, triesSearchResult))
        self.assertTrue(astries.isNoMatchChild())
"""    
    #case 1 : path found but no value
    def test_AdvancedSearchCasePathMatch(self):
        pass #TODO
    
    #case 3 : ambiguous found
    def test_AdvancedSearchCaseAmbiguous(self):
        pass #TODO
    
    #case 4 : found
    def test_AdvancedSearchCaseFound(self):
        pass #TODO

### test move, from a unexisten to an existent, from an existent to an unexistent, from existent to existent, ...
    #from level 0 to level 1
    def test_moveFrom0to1(self):
        mlt = multiLevelTries()
        mlt.insert((),"a")
        
        #try to move to an existent place (destination unexistant)
        mlt.insert(("b",),"a")
        self.assertRaises(pathExistsTriesException, mlt.move,(),("b",))
        
        #try to move from a unexistent place (source empty)
        self.assertRaises(pathNotExistsTriesException, mlt.move,("c",),())
        
        mlt.move((),("a",))
        
        mltnode = mlt.search()
        self.assertTrue(mltnode == None)
        
        mltnode = mlt.search(("a",))
        self.assertTrue(mltnode != None and mltnode.value == "a")

    #from level 1 to level 0
    def test_moveFrom1to0(self):
        mlt = multiLevelTries()
        mlt.insert(("a",),"a")
        mlt.move(("a",), ())
        
        mltnode = mlt.search(("a",))
        self.assertTrue(mltnode == None)
        
        mltnode = mlt.search()
        self.assertTrue(mltnode != None and mltnode.value == "a")
    
    #from level 2 to level 1
    def test_moveFrom1to2(self):
        mlt = multiLevelTries()
        mlt.insert(("a",),"a")
        mlt.move(("a",), ("a","a",))
        
        mltnode = mlt.search(("a",))
        self.assertTrue(mltnode == None)
        
        mltnode = mlt.search(("a","a",))
        self.assertTrue(mltnode != None and mltnode.value == "a")
    
    #from level 2 to level 1
    def test_moveFrom2to1(self):
        mlt = multiLevelTries()
        mlt.insert(("a","a",),"a")
        mlt.move(("a","a",), ("a",))
        
        mltnode = mlt.search(("a","a",))
        self.assertTrue(mltnode == None)
        
        mltnode = mlt.search(("a",))
        self.assertTrue(mltnode != None and mltnode.value == "a")
    
    #from level 0 to level 2
    def test_moveFrom0to2(self):
        mlt = multiLevelTries()
        mlt.insert((),"a")
        mlt.move((),("a","a",))
        
        mltnode = mlt.search()
        self.assertTrue(mltnode == None)
        
        mltnode = mlt.search(("a","a",))
        self.assertTrue(mltnode != None and mltnode.value == "a")

    #from level 2 to level 0
    def test_moveFrom2to0(self):
        mlt = multiLevelTries()
        mlt.insert(("a","a",),"a")
        mlt.move(("a","a",), ())
        
        mltnode = mlt.search(("a","a",))
        self.assertTrue(mltnode == None)
        
        mltnode = mlt.search()
        self.assertTrue(mltnode != None and mltnode.value == "a")

    #... (no need to go to level 3"""



#TEST LIST TODO
    #produce an ambiguousPathExceptionWithLevel in a search (any search that call SearchNode)
        #with the method search()
        
    #setStopTraversal on an empty node of level 0 (empty list), level 1, level 2, ...
        #and try both traversals
        
    #test traversal with prefix(not empty) included or not included at level 0 (empty list),1, 2,... (depth and breadth)

if __name__ == '__main__':
    unittest.main()
