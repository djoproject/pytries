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
    
    #build advanced search function 
        #like the advanced search of tries
        #goal : solve the call command with args, the args are not in the tree
    
    #check how the intermediate node are managed
        #insert (especialy this one)
        #remove
    
from tries import *
from exception import triesException

class multiLevelTries(object):
    
    def __init__(self, parentMLTries = None):
        "this method init the multiLevelTries with an empty tries root"
        self.localTries = tries() #levelOneTries
        self.parentMLTries = parentMLTries
        self.valueSet      = False
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
        if stringList == None or type(stringList) != list or len(stringList) < 0:
            raise triesException("need string token to insert a new value, no token found")
        
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
                MLTries_tmp = MLTries_tmp.localTries.search(stringList[i])
            else:
                MLTries_tmp = MLTries_tmp.localTries.searchUniqueFromPrefix(stringList[i]) #allow partial but non ambigous result
            
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
            raise triesException("Insert, the path <"+" ".join(stringList)+"> already exists in the multi tries")
        
        #determine where the string list must be insert, searchNode always return at least one value in existingPath
            #in the worst case, it contains [(stringList[0], self, None)]
        currentMLTriesWhereInsert = existingPath[-1][1] #the token is not found in the last MLTries
        
        #insert the path
        for i in range(len(existingPath)-1, len(stringList)): #from the first index of a non common string to the end of the list
            currentMLTriesWhereInsert = currentMLTriesWhereInsert.localTries.insert(stringList[i],multiLevelTries(currentMLTriesWhereInsert), anyStringEnable[i]).value

        #set the value and its args
        currentMLTriesWhereInsert.setValue(value)
        node.stopTraversal = stopTraversalAtThisNode

    #
    #
    #
    def remove(self, stringList):
        #search for a similar existing stringList in the tree (we want a perfect match)
        existingPath, existing, existingValue = self.searchNode(stringList, True)
        
        #raise an exception if the path does not exist
        if not existing:
            raise triesException("Remove, The path <"+" ".join(stringList)+"> does not exist in the multi tries")
        
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
            raise triesException("Update, The path <"+" ".join(stringList)+"> does not exist in the multi tries")
        
        #set the new value (the last node of the path contains a tries with an empty key tries, this node have to be updated)
        existingPath[-1][2].setValue(newValue)
    

    #
    #
    #
    def search(self,stringList, strict = False) :
        #search for a similar existing stringList in the tree (partial result are accepted)
        existingPath, existing, existingValue = self.searchNode(stringList, strict)
        
        #return the value found
        if existing:
            return existingValue
        
        if strict:
            raise triesException("(multiLevelTries) search, The path <"+" ".join(stringList)+"> does not exist in the multi tries")
        
        #error managing
        if len(existingPath) -1 == len(stringList):
            raise triesException("Search, string list is uncomplete")
        
        raise triesException("Search, unknown string in level "+str(len(existingPath))+" <"+existingPath[-1][0]+">")
    
    def advancedSearch(self, stringList):
        
        #return more information about the search
            #how many token have been found
                #and so, how many token have been not found
            #the value on the last find value
            #the path found (with the token used)
            #the remaining tokens
            #... ?
        
        pass #TODO


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
            raise triesException("(multiLevelTries) setStopTraversal, The path <"+" ".join(stringList)+"> does not exist in the multi tries")
    
        #update state
        existingPath[-1][2].stopTraversal = state
    
    #
    #
    #
    def __repr__(self):
        return repr(self.levelOneTries)
    
    
### TODO ### TODO ### TODO ### TODO ### TODO ### TODO ### TODO ### TODO ### TODO ### convert into the new MLTries design
    #
    # TODO refactor
    # TODO execute on every node, not only the value node
    #
    def genericDepthFirstTraversal(self,executeOnNode, initState = None, preOrder = True, ignoreStopTraversal = False):
        current        = self.levelOneTries
        currentPath    = [""]
        traversalState = initState
        level          = 0
         
        while current != None:
            #print "current", level, len(currentPath),current
            ### traverse the node ###
            if "traversed" not in current.__dict__.keys():
                currentPath[level] += current.key
                if preOrder and current.isValueSet() and current.value.isValueSet():
                    traversalState = executeOnNode(currentPath, current.value, traversalState, level)
                        
                current.traversed = True
            
            ### identify next node to explore ###
            #is there some child to explore
            if len(current.childs) > 0:
                #does the exploration already start ?
                if "traversal_index" not in current.__dict__.keys():
                    current.traversal_index = 0
                
                #is there still child to explore ,
                if current.traversal_index < len(current.childs):
                    current.traversal_index += 1
                    current = current.childs[current.traversal_index -1]
                    continue
                
                #no more need the index
                del current.traversal_index
                #level -= 1
            
            #TODO after or before the child visit ?
            if current.isValueSet() and current.value.nextTries != None and (ignoreStopTraversal or not current.value.stopTraversal):
                if "MTParent" in current.value.nextTries.__dict__.keys():
                    #print "del goto down"
                    del current.value.nextTries.MTParent
                else:
                    #print "goto down ", len(currentPath)
                    level += 1
                    currentPath.append("")
                    current.value.nextTries.MTParent = current
                    current = current.value.nextTries
                    continue
            
            #post order traversal
            if not preOrder and current.isValueSet() and current.value.isValueSet():
                traversalState = executeOnNode(currentPath, current, traversalState, level)
            
            #remove the key string of the current node from the path
            if len(current.key) > 0:
                currentPath[level] = currentPath[level][:-len(current.key)]
            
            #back to the parent
            del current.traversed
            
            #go up in the multilevel tries
            if current.parent == None and "MTParent" in current.__dict__.keys():
                #print "goto up", len(currentPath)
                level -= 1
                oldCurrent = current
                currentPath = currentPath[:-1]
                current = current.MTParent
                #del oldCurrent.MTParent
                continue
                    
            current = current.parent
        return traversalState

### TODO ### TODO ### TODO ### TODO ### TODO ### TODO ### TODO ### TODO ### TODO ### convert into the new MLTries design
    

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
    def buildDictionnary(self, stringList = [], ignoreStopTraversal):
        #find the starting node if needed
        startingPoint = self
        if len(stringList) > 0:
            existingPath, existing, existingValue = self.searchNode(stringList, True)

            #raise an exception if the path does not exist
            if not existing:
                raise triesException("(multiLevelTries) buildDictionnary, The path <"+" ".join(stringList)+"> does not exist in the multi tries")
        
            startingPoint = existingPath[-1][2]
        
        #start the search TODO at the starting node
        return startingPoint.genericDepthFirstTraversal(startingPoint._inner_buildDictionnary, {}, True, ignoreStopTraversal)

    

    
    



