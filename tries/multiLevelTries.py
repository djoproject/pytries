#!/usr/bin/python2.6
# -*- coding: utf-8 -*- 

#Copyright (C) 2012  Jonathan Delvaux <djo938@gmail.com>

#This program is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#any later version.

#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.

#You should have received a copy of the GNU General Public License
#along with this program.  If not, see <http://www.gnu.org/licenses/>.

#TODO  
    #comment everything
        #IN PROGRESS
    
    #pourquoi ne pas pouvoir stocker une chqine vide ?
    
from tries import *
from exception import triesException,pathExistsTriesException, pathNotExistsTriesException

class multiLevelTries(object):
    
    def __init__(self, parentMLTries = None):
        "this method init the multiLevelTries with an empty tries root"
        self.localTries = tries() #levelOneTries
        self.parentMLTries = parentMLTries #TODO a quoi sert cette variable si elle ne sert pas dans le traversal ?
        self.valueSet      = False
        self.value         = None
        self.stopTraversal = False
    
    
    def setValue(self,value):
        self.valueSet = True
        self.value    = value
    
    
    def unsetValue(self):
        self.valueSet = False
        self.value    = None
    
    
    def isValueSet(self):
        return self.valueSet
    
    
    #
    # @parameter stringList is the list of string token to find in the multiTries
    # @parameter onlyPerfectMatch is a boolean to limit the search to the perfect match result, if it is set to false, the partial result will be allowed
    # @return the number of matching token, 
    #
    def searchNode(self, stringList, onlyPerfectMatch=True):
        #check string list
        if stringList == None or not hasattr(stringList, '__iter__') or len(stringList) < 0:
            raise triesException("(multiLevelTries) searchNode, need string token to search a value, no token found")
        
        #SEARCH a similar String list
        parentMLTries_tmp = None
        MLTries_tmp       = self
        triesLinked       = [] #list to store the result
        foundValue        = False #did we find the result ?
        value             = None #result match ?
        for i in range(0,len(stringList)): #for each token of the string list to insert
            #test if stringList[i] is a string
            if type(stringList[i]) != str:
                raise triesException("(multiLevelTries) searchNode, try to search a non string value : <"+str(stringList[i])+">")
            
            #search the string[i] in the current tries
            parentMLTries_tmp = MLTries_tmp
            if onlyPerfectMatch:
                tmp = MLTries_tmp.localTries.search(stringList[i])
            else:
                tmp = MLTries_tmp.localTries.searchUniqueFromPrefix(stringList[i]) #allow partial but non ambigous result
            
            if tmp != None:
                MLTries_tmp = tmp.value
            else:
                MLTries_tmp = None
            
            #store the result (string token, the MLTries parent, and the MLTries child or None if not found)
            triesLinked.append( (stringList[i],parentMLTries_tmp, MLTries_tmp,) )

            #is there a match ?
            if MLTries_tmp != None:
                #every string had been consumed ?
                if i == len(stringList)-1:
                    return triesLinked, MLTries_tmp.valueSet, MLTries_tmp.value
                
                #continue to explore, there are still string tokens and tries to explore 
                continue
            #no more tries to explore, we stop the search
            break
        #at this point, we found a result or the path does not exist in the tree
        return triesLinked, False, None
    
    
    
    #
    #
    # @param stringList : array string
    # @param value : object to store
    #
    def insert(self, stringList, value, stopTraversalAtThisNode = False, anyStringSuffix="*"):
        #identify anyString
        anyStringEnable = [False] * len(stringList)
        if len(anyStringSuffix) > 0:
            for i in range(len(stringList)):
                if stringList[i].endswith(anyStringSuffix):
                    anyStringEnable[i] = True
        
        #search for a similar existing stringList in the tree (we want a perfect match)
        existingPath, existing, existingValue = self.searchNode(stringList, True)
        
        #raise an exception if the path exist
        if existing:
            raise pathExistsTriesException("(multiLevelTries) insert, the path <"+" ".join(stringList)+"> already exists in the multi tries")
        
        #manage the case where we want to insert into an empty intermediate node
        if existingPath[-1][2] == None:
            #determine where the string list must be insert, searchNode always return at least one value in existingPath
                #in the worst case, it contains [(stringList[0], self, None)]
            currentMLTriesWhereInsert = existingPath[-1][1] #the token is not found in the last MLTries
            
            #insert the path
            for i in range(len(existingPath)-1, len(stringList)): #from the first index of a non common string to the end of the list
                currentMLTriesWhereInsert = currentMLTriesWhereInsert.localTries.insert(stringList[i],multiLevelTries(currentMLTriesWhereInsert), anyStringEnable[i]).value
        else: #existingPath[-1][2] is different of None, so the complete path has been found, but the last node has no value
            currentMLTriesWhereInsert = existingPath[-1][2]

        #set the value and its args
        currentMLTriesWhereInsert.setValue(value)
        currentMLTriesWhereInsert.stopTraversal = stopTraversalAtThisNode

    #
    #
    #
    def remove(self, stringList):
        #search for a similar existing stringList in the tree (we want a perfect match)
        existingPath, existing, existingValue = self.searchNode(stringList, True)
        
        #raise an exception if the path does not exist
        if not existing:
            raise pathNotExistsTriesException("(multiLevelTries) remove, The path <"+" ".join(stringList)+"> does not exist in the multi tries")
        
        #unset value
        existingPath[-1][2].unsetValue()
        
        #remove the node from bottom up
        for i in range(0,len(existingPath)):
            #next node index to remove
            index = len(existingPath) - 1 - i
            
            #child to remove can't have value or child in the tries
            if existingPath[index][2].isValueSet() or not existingPath[index][2].localTries.isEmpty():
                break
            
            #remove the value stored
            existingPath[index][1].remove(existingPath[index][0])
    
    

    #
    #
    #
    def update(self, stringList, newValue):
        existingPath, existing, existingValue = self.searchNode(stringList, True)
        
        #raise an exception if the path does not exist
        if not existing:
            raise pathNotExistsTriesException("(multiLevelTries) update, The path <"+" ".join(stringList)+"> does not exist in the multi tries")
        
        #set the new value (the last node of the path contains a tries with an empty key tries, this node have to be updated)
        existingPath[-1][2].setValue(newValue)
    

    #
    #
    #
    def search(self,stringList, onlyPerfectMatch = False) :
        #search for a similar existing stringList in the tree (partial result are accepted)
        existingPath, existing, existingValue = self.searchNode(stringList, onlyPerfectMatch)
        
        #return the value found
        if existing:
            return existingValue
        
        if onlyPerfectMatch:
            raise pathNotExistsTriesException("(multiLevelTries) search, The path <"+" ".join(stringList)+"> does not exist in the multi tries")
        
        #error management
        if len(existingPath) -1 == len(stringList):
            raise triesException("(multiLevelTries) search, string list is uncomplete")
        
        raise triesException("(multiLevelTries) search, unknown string in level "+str(len(existingPath))+" <"+existingPath[-1][0]+">")
    

    def advancedSearch(self, stringList, onlyPerfectMatch=True):
        #make the search and fill a result object
        existingPath, existing, existingValue = self.searchNode(stringList, onlyPerfectMatch)
        return multiLevelTriesSearchResult(stringList, existingPath, existing, existingValue, onlyPerfectMatch)


    #
    #
    #
    def setStopTraversal(self, stringList, state):
        #test state
        if type(state) != bool:
            raise triesException("(multiLevelTries) setStopTraversal, try to set a non boolean value to the stop traversal state")
        
        #look after the string
        existingPath, existing, existingValue = self.searchNode(stringList, True)
        if not existing:
            raise pathExistsTriesException("(multiLevelTries) setStopTraversal, The path <"+" ".join(stringList)+"> does not exist in the multi tries")
    
        #update state
        existingPath[-1][2].stopTraversal = state
    

    #
    #
    #
    def __repr__(self):
        return repr(self.localTries)
    
    
    def exploreNextTries(self, level, currentPath, current):
        currentPath.append("")
        current.value.localTries.MTParent = current
        return level+1, current.value.localTries
    
### TODO ### TODO ### TODO ### TODO ### TODO ### TODO ### TODO ### TODO ### TODO ### convert into the new MLTries design    
    #
    # cas de figure qui merde, un noeud qui contient un mltries et des childs
    #   en preOrder
    #   ça risque de boucler, tester
    #
    def genericDepthFirstTraversal(self,executeOnNode, initState = None, preOrder = True, ignoreStopTraversal = False):
        current        = self.localTries
        currentPath    = [""]
        traversalState = initState
        level          = 0
         
        while current != None:
            #print "currentPath",currentPath
            #print "current", level, len(currentPath),current
        ### traverse the node ###
            if "traversed" not in current.__dict__.keys():
                currentPath[level] += current.key
                if preOrder and current.isValueSet():
                    traversalState = executeOnNode(currentPath, current.value, traversalState, level)
                        
                current.traversed = True
            #print "1"
            if preOrder:
                #explore next level tries
                if current.isValueSet() and not current.value.localTries.isEmpty() and (ignoreStopTraversal or not current.value.stopTraversal):
                    if "MTParent" in current.value.localTries.__dict__.keys():
                        #print "del goto down"
                        del current.value.localTries.MTParent
                    else:
                        #print "goto down ", len(currentPath)
                        level, current = self.exploreNextTries(level, currentPath, current)
                        #print "continue to bottom level (1)", str(current)
                        continue
            #print "2"
        ### identify next node to explore ###
            if len(current.childs) > 0: #is there some child to explore ?
                #does the exploration already start ?
                if "traversal_index" not in current.__dict__.keys():
                    current.traversal_index = 0
                
                #is there still child to explore ,
                if current.traversal_index < len(current.childs):
                    current.traversal_index += 1
                    current = current.childs[current.traversal_index -1]
                    #print "continue to next child", str(current)
                    continue
                
                #no more need the index
                del current.traversal_index
            #print "3"                
            #post order traversal
            if not preOrder and current.isValueSet():
                #print "plop"
                #explore next level tries
                if not current.value.localTries.isEmpty() and (ignoreStopTraversal or not current.value.stopTraversal):
                    if "MTParent" in current.value.localTries.__dict__.keys():
                        del current.value.localTries.MTParent
                    else:
                        level, current = self.exploreNextTries(level, currentPath, current)
                        #print "continue to bottom level (2)", str(current)
                        continue
                        
                traversalState = executeOnNode(currentPath, current.value, traversalState, level)
            #print "4"
            #remove the key string of the current node from the path
            if len(current.key) > 0:
                currentPath[level] = currentPath[level][:-len(current.key)]
            
            #back to the parent
            del current.traversed
            #print "5"
            #go up in the multilevel tries
            #if current.isValueSet():
            #    print "check 5, ",current.parent, current.isValueSet(), current.value.parentMLTries
            #    print current.parent == None, current.isValueSet(), current.value.parentMLTries != None
            #else:
            #    print "check 5, ",current.parent, current.isValueSet()
            #    print current.parent == None, current.isValueSet()
            #print "instance tries ?",isinstance(current, tries)
            #print "parent none ?", current.parent == None
            #print "is value set ?", current.isValueSet()
            
            if current.parent == None and hasattr(current,"MTParent") and current.MTParent: # current.isValueSet() and current.value.parentMLTries != None:
                #print "goto up", len(currentPath)
                level -= 1
                oldCurrent = current
                currentPath = currentPath[:-1]
                current = current.MTParent #current.value.parentMLTries
                #print "####### continue to parent", str(current)
                continue
                    
            current = current.parent
            #print "6"
        ### return the final state
        return traversalState
    
### END  XXX ### XXX ### XXX ### XXX ### XXX ### XXX ### XXX ### XXX ### XXX ### convert into the new MLTries design
    
    
    #
    #
    #    
    def genericBreadthFirstTraversal(self, executeOnNode, initState = None, ignoreStopTraversal = False): 
        Queue          = []
        traversalState = initState
        
        #init the Queue with every key value of the first level tries
        keyValue = self.localTries.getKeyValue()
        for k,v in keyValue.iteritems():
            Queue.append(v, 0, [k])
        
        #read the queue
        while len(Queue) > 0:
            #dequeu current node
            current, level, currentPath = Queue.popleft()
            
            #add every child in the Queue
            if not current.localTries.isEmpty() and (ignoreStopTraversal or not current.stopTraversal):
                keyValue = current.localTries.getKeyValue()
                
                for k,v in keyValue.iteritems():
                    newPath = currentPath[:]
                    newPath.append(k)
                    Queue.append(v, level+1, newPath)       
            
            #read value node with value
            traversalState = executeOnNode(currentPath, current, traversalState, level)
    

    def _inner_buildDictionnary(self, path, node, state, level):
        state[path] = node.value
    
    
    #
    # return a dictionnary of every key/value in the tree
    #
    # TODO add an option to store the complete path inside the dictionary
    #     concat the stringList with the key
    #     not exaclty, get the complete path from the tries
    #
    def buildDictionnary(self, stringList = [], ignoreStopTraversal=False, addPrexix= False):
        #find the starting node if needed
        startingPoint = self
        prefix = []
        if len(stringList) > 0:
            existingPath, existing, existingValue = self.searchNode(stringList, True)
            
            #raise an exception if the path does not exist
            if not existing:
                raise pathNotExistsTriesException("(multiLevelTries) buildDictionnary, The path <"+" ".join(stringList)+"> does not exist in the multi tries")
            
            startingPoint = existingPath[-1][2]
            
            #build prefix
            if addPrexix:
                pass #TODO need the tries that contains the mltries, but not directly available, need to modify the searchNode function
        
        #start the search
        return startingPoint.genericDepthFirstTraversal(startingPoint._inner_buildDictionnary, {}, True, ignoreStopTraversal)
    
    

class multiLevelTriesSearchResult(object):
    def __init__(self, stringList, existingPath, existing, existingValue, onlyPerfectMatch):
        self.stringList    = stringList
        self.existingPath  = existingPath
        self.existing      = existing
        self.existingValue = existingValue
        self.tokenFoundCount        = len(existingPath)
        
        #special case, the last token searched is in the existingPath but if it is not found, it does not count as a existing part of the path
        if not self.existing and existingPath[-1][2] == None:
            self.tokenFoundCount -= 1
        
        self.tokenNotFound = len(stringList) - self.tokenFoundCount
    
    def getFoundToken(self):
        return spaceChar.join(stringList[:self.tokenFoundCount])
    
    def getNotFoundToken(self):
        return spaceChar.join(stringList[:self.tokenFoundCount])
    
    def getTokenFoundCount(self):
        return self.tokenFoundCount
    
    def getTokenNotFoundCount(self):
        return self.tokenNotFound
    
    def getTotalTokenCount(self):
        return len(stringList)
    
    def isValueFound(self):
        return self.existing
    
    def getValue(self):
        if not self.existing:
            raise triesException("(multiLevelTriesSearchResult) getLastTokenFoundValue, no value found on this path")
        
        return self.existingValue
    
    def isAvalueOnTheLastTokenFound(self):
        return self.tokenFoundCount > 0 and existingPath[self.tokenFoundCount-1][2] != None and existingPath[self.tokenFoundCount-1][2].isValueSet()
    
    def getLastTokenFoundValue(self):
        if not self.isAvalueOnTheLastTokenFound():
            raise triesException("(multiLevelTriesSearchResult) getLastTokenFoundValue, no value on the last token found")
        
        return existingPath[self.tokenFoundCount-1][1].value
    
    def isAllTokenHasBeenConsumed(self):
        return len(self.stringList) == self.tokenFoundCount
    
    ### not found reason
    
    #
    # there are still token to use but no more tries
    #    occurs when the last explored tries is empty
    #
    def isLastExploredTriesEmpty(self):
        return existingPath[-1][1].localTries.isEmpty()
    
    #
    # the last token searched was not found in the 
    #    occurs when last explored tries is not empty
    #
    def isTokenNotFoundInLastTries(self):
        return existingPath[-1][2] == None and not self.existing 
    #
    # the path has been completly found be there is no value attached to this path
    #
    def isPathCorrespondsToNonValueNode(self):
        return self.existingPath[-1][2] != None and not self.existing
        #return self.pathExistButNoValue
    


