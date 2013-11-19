#!/usr/bin/python2.6
# -*- coding: utf-8 -*- 

#Copyright (C) 2012  Jonathan Delvaux <pytries@djoproject.net>

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

from tries import *
from exception import *


class multiLevelTries(object):
    """
    This class provide a complete implementation of the multi level tries stucture
    
    @contact: pytries@djoproject.net
    @version: 1.0
    @licence: GPL v3
    @see: http://en.wikipedia.org/wiki/Trie
    """
    
    def __init__(self):#, parentMLTries = None):
        """
        this method init the multiLevelTries with an empty tries root
        """
        
        self.localTries = tries() #levelOneTries
        self.valueSet      = False
        self.value         = None
        self.stopTraversal = False
    
    
    def setValue(self,value):
        """
        this method allow to set the value stored on this node
        
        @type value: anything even None
        @param value: the value to store on this node 
        """
        
        self.valueSet = True
        self.value    = value
    
    
    def unsetValue(self):
        """
        this method allow to unset the value stored on this node
        """
        
        self.valueSet = False
        self.value    = None
    
    
    def isValueSet(self):
        """
        this method allow to check if a value is set on this node
        
        @rtype: boolean
        @return: True if there is a value stored on this node, False otherwise
        """
        
        return self.valueSet
    
    
    def getValue(self):
        """
        this method allow to get the value stored on this node
        
        @rtype: anything even None
        @return: the value stored on this
        @raise noValueSetTriesException: if there is no value stored on this node
        """
        
        if not self.valueSet:
            raise noValueSetTriesException("(multiLevelTries) getValue, this node does not contain any value")
            
        return self.value
        
        
########### MAJOR FUNCTION (insert/remove/update) #######################################################################################################################################################
    
    
    def insert(self, stringList, value, stopTraversalAtThisNode = False, anyStringSuffix="*"):
        """
        This method inserts a new path in the tree.  
        
        @type stringList: string list
        @param stringList: the new path to insert
        @type value: anything even None
        @param value: the value associates to the path
        @type stopTraversalAtThisNode: boolean
        @param stopTraversalAtThisNode: set the stop traversal on this node to avoid a traversal on its childs
        @type anyStringSuffix: string
        @param anyStringSuffix: set the anystring string, to disable it, set an ampty string
        @rtype: multiLevelTries
        @return: the new multiLevelTries node
        @raise pathExistsTriesException: if a value is already associated with this string path
        """
        
        #identify anyString
        anyStringEnable = [False] * len(stringList)
        if len(anyStringSuffix) > 0:
            for i in range(len(stringList)):
                if stringList[i].endswith(anyStringSuffix):
                    anyStringEnable[i] = True
        
        #search for a similar existing stringList in the tree (we want a perfect match)
        searchResult = self.searchNode(stringList, True)
        
        #raise an exception if the path exist
        if searchResult.isValueFound():
            raise pathExistsTriesException("(multiLevelTries) insert, the path <"+" ".join(stringList)+"> already exists in the multi tries")
        
        #manage the case where we want to insert into an empty intermediate node
        if not searchResult.isPathFound():
            #determine where the string list must be insert, searchNode always return at least one value in existingPath
                #in the worst case, it contains [(stringList[0], self, None)]
            currentMLTriesWhereInsert = searchResult.existingPath[-1][1] #the token is not found in the last MLTries
            
            #insert the path
            for i in range(len(searchResult.existingPath)-1, len(stringList)): #from the first index of a non common string to the end of the list
                #currentMLTriesWhereInsert = currentMLTriesWhereInsert.localTries.insert(stringList[i],multiLevelTries(currentMLTriesWhereInsert), anyStringEnable[i]).value
                currentMLTriesWhereInsert = currentMLTriesWhereInsert.localTries.insert(stringList[i],multiLevelTries(), anyStringEnable[i]).value
        else: #searchResult.existingPath[-1][2] is different of None, so the complete path has been found, but the last node has no value
            currentMLTriesWhereInsert = searchResult.getMltFound()
        
        #set the value and its args
        currentMLTriesWhereInsert.setValue(value)
        currentMLTriesWhereInsert.stopTraversal = stopTraversalAtThisNode
        
        return currentMLTriesWhereInsert
    
    
    def _remove(self, searchResult):
        #unset value
        searchResult.getMltFound().unsetValue()
        
        #remove the node from bottom up
        for i in range(0,len(searchResult.existingPath)):
            #next node index to remove
            index = len(searchResult.existingPath) - 1 - i
            
            #child to remove can't have value or child in the tries
            if searchResult.existingPath[index][2].isValueSet() or not searchResult.existingPath[index][2].localTries.isEmpty():
                break
            
            #remove the value stored
            if searchResult.existingPath[index][1] == None:
                break
            
            searchResult.existingPath[index][1].localTries.remove(searchResult.existingPath[index][0])
            
            
        #no value is return, because in the other function, the mltries is returned, but here the mltries could still have a place into the tree structure
        #so it is not a good idea to return an element of this structure
    
    
    def removeBranch(self,stringList):
        """
        This function remove an entire branch of the tree without any check about the child into this branch.
        The string path must be associated to a value node or a no value node
        
        @type stringList: string list
        @param stringList: the string path to remove in the multi level tries
        """
                
        #find the node
        searchResult = self.searchNode(stringList, True)
        
        if not searchResult.isPathFound():
            raise pathNotExistsTriesException("(multiLevelTries) removeBranch, The branch <"+" ".join(stringList)+"> does not exist in the multi tries")
        
        #reset the tries
        searchResult.getMltFound().localTries = tries()
        
        #use the generic part of remove
        self._remove(searchResult)
    
    
    def remove(self, stringList):
        """
        This function remove a path from the multi level tries.  This method only removed path with a value on it.
        The path must only be associated to a value node
        
        @type stringList: string list
        @param stringList: the string path to remove in the multi level tries
        @raise pathNotExistsTriesException: if the there is no value associated to the path
        """
        
        #search for a similar existing stringList in the tree (we want a perfect match)
        searchResult = self.searchNode(stringList, True)
        
        #raise an exception if the path does not exist
        if not searchResult.isValueFound():
            raise pathNotExistsTriesException("(multiLevelTries) remove, The path <"+" ".join(stringList)+"> is not found or not associated to a value")
        
        self._remove(searchResult)
        
        
    def update(self, stringList, newValue):
        """
        This method update the value of an existing path
        
        @type stringList: string list
        @param stringList: the existing path to update
        @type newValue: anything even None
        @param newValue: the new value of the path
        @rtype: multiLevelTries
        @return: the updated multiLevelTries node
        """
        
        searchResult = self.searchNode(stringList, True)
        
        #raise an exception if the path does not exist
        if not searchResult.isValueFound():
            raise pathNotExistsTriesException("(multiLevelTries) update, The path <"+" ".join(stringList)+"> is not found or not associated to a value")
        
        #set the new value (the last node of the path contains a tries with an empty key tries, this node have to be updated)
        existingMlt = searchResult.getMltFound()
        existingMlt.setValue(newValue)
        return existingMlt
    
    def move(self, oldStringList, newStringList, anyStringSuffix="*"):
        """
        This function move a value from an old path to a new one.
        The old path is removed except if the new one already exists.
        
        @type oldStringList: string list
        @param oldStringList: the old path to remove
        @type newStringList: string list
        @param newStringList: the new path to insert
        @type anyStringSuffix: string
        @param anyStringSuffix: set the anystring string for the new string list, to disable it, set an ampty string
        @rtype: multiLevelTries
        @return: the new multiLevelTries node inserted on the new string list path
        @raise pathExistsTriesException: if a value is already associated with the new path
        """
        
        #looking for the previous path
        searchResult = self.searchNode(oldStringList, True)
        
        #raise an exception if the path does not exist
        if not searchResult.isValueFound():
            raise pathNotExistsTriesException("(multiLevelTries) move, The path <"+" ".join(oldStringList)+"> is not found or not associated to a value")
        
        existingMlt = searchResult.getMltFound()
        existingValue = existingMlt.value
        
        #insert the new one
        newNode = self.insert(newStringList, existingValue,existingMlt.stopTraversal,anyStringSuffix)
        
        #remove the old
        self.remove(oldStringList)
        
        return newNode
        
############ SEARCH FUNCTION #########################################################################################################################################################################
    
    
    def searchNode(self, stringList, onlyPerfectMatch=True):
        """
        This function is a the kernel part of the research algorithm of the multi level tries.
        Indeed, thes result are a stack of the different state of the research process.
        This function allow to make a lot of search operation on the mltries.
        
        @type stringList: list of string
        @param stringList: stringList is the list of string token to find in the multiTries
        @type onlyPerfectMatch: boolean
        @param onlyPerfectMatch: onlyPerfectMatch is a boolean to limit the search to the perfect match result, if it is set to false, the partial result will be allowed
        @rtype: list of tuple(string,multiLevelTries,multiLevelTries,tries),boolean, anything
        @return: the returned value is a tuple of 3 elements, the first one is a list of tuple representing the status of each research step, 
                                                              the second one is a boolean to indicate if there is a value match
        The tuple of the list is composed of the token string used at this step, the mltries used to make the search, the mltries found in the search and the tries where the value found is stored
        @raise triesException: if invalid argument
        @raise ambiguousPathExceptionWithLevel: if onlyPerfectMatch is set to False and there is an ambiguous result inside a inner tries search
        """
        
        #print "searchNode <"+str(stringList)+">"
        #check string list
        if stringList == None or not hasattr(stringList, '__iter__'):
            raise triesException("(multiLevelTries) searchNode, need string token to search a value, no token found")
        
        #manage empty path
        if len(stringList) == 0:
            return multiLevelTriesSearchResult(stringList, [(None,None, self, None)], onlyPerfectMatch)
        
        #SEARCH a similar String list
        parentMLTries_tmp = None
        MLTries_tmp       = self
        triesLinked       = [] #list to store the result
        foundValue        = False #did we find the result ?
        #value             = None #result match ?
        for i in range(0,len(stringList)): #for each token of the string list to insert
            #test if stringList[i] is a string
            if type(stringList[i]) != str:
                raise triesException("(multiLevelTries) searchNode, try to search a non string value : <"+str(stringList[i])+">")
            
            #search the string[i] in the current tries
            parentMLTries_tmp = MLTries_tmp
            if onlyPerfectMatch:
                tmp = MLTries_tmp.localTries.searchPerfect(stringList[i])
            else:
                try:
                    tmp = MLTries_tmp.localTries.search(stringList[i]) #allow partial but non ambigous result
                except ambiguousPathException as ape:
                    triesLinked.append( (stringList[i],parentMLTries_tmp, None, None) )
                    raise ambiguousPathExceptionWithLevel(ape.value+" at level "+str(i),i,multiLevelTriesSearchResult(stringList,triesLinked, onlyPerfectMatch, True))
                
            if tmp != None:
                MLTries_tmp = tmp.value
            else:
                MLTries_tmp = None
                
            #store the result (string token, the MLTries parent, and the MLTries child or None if not found)
            triesLinked.append( (stringList[i],parentMLTries_tmp, MLTries_tmp, tmp) )
            
            #is there a match ?
            if MLTries_tmp != None:
                #every string had been consumed ?
                if i == len(stringList)-1:
                    return multiLevelTriesSearchResult(stringList,triesLinked, onlyPerfectMatch)
                
                #continue to explore, there are still string tokens and tries to explore 
                continue
            #no more tries to explore, we stop the search
            break
        #at this point, we found a result or the path does not exist in the tree
        return multiLevelTriesSearchResult(stringList,triesLinked, onlyPerfectMatch)    
    
    
    def search(self,stringList, onlyPerfectMatch = False) :
        """
        This function is the simpliest way to make a search in the multi level tries.
        The result will be the value of the path.  And if the path did not exist, an exception will be raised
        
        @type stringList: string list
        @param stringList: the path to find in the tree
        @type onlyPerfectMatch: boolean
        @param onlyPerfectMatch: if this param is set to True, only the perfect matching will be accepted in the search algorithm
        @rtype: multiLevelTries or None
        @return: if there is a value corresponding to the path, return the mltries that contains this value. Otherwise return None
        @raise ambiguousPathExceptionWithLevel: if onlyPerfectMatch is set to False and there is an ambiguous result inside a inner tries search
        """
        
        #search for a similar existing stringList in the tree (partial result are accepted)
        searchResult = self.searchNode(stringList, onlyPerfectMatch)
        
        #return the value found
        if searchResult.isValueFound():
            return searchResult.getMltFound()
            
        return None
    
    
    def advancedSearch(self, stringList, onlyPerfectMatch=True):
        """
        This function does not do any particular processing on the search result.  
        But a special object is returned to explored the result of the search on many ways.
        
        @type stringList: string list
        @param stringList: the path to find in the tree
        @type onlyPerfectMatch: boolean
        @param onlyPerfectMatch: if this param is set to True, only the perfect matching will be accepted in the search algorithm
        @rtype: multiLevelTriesSearchResult
        @return: the details result of the search inside an instance of multiLevelTriesSearchResult
        @raise ambiguousPathExceptionWithLevel: if onlyPerfectMatch is set to False and there is an ambiguous result inside a inner tries search
        """
        
        #make the search and fill a result object
        try:
            return self.searchNode(stringList, onlyPerfectMatch)
        except ambiguousPathExceptionWithLevel as apewl:
            return apewl.searchStack
    
    
############ TRAVERSAL FUNCTION #####################################################################################################################################################################
    
    def setStopTraversal(self, stringList, state):
        """
        This methode set the boolean StropTraversal on the node corresponding to the stringList.
        
        @type stringList: string list
        @param stringList: the string path where to set the StopTraversal
        @type state: boolean
        @param state: the new StropTraversal state
        @rtype: multiLevelTries
        @return: the updated node
        @raise triesException: if the new state is not a valid boolean
        @raise pathNotExistsTriesException: if the path does not exist
        """
                
        #test state
        if type(state) != bool:
            raise triesException("(multiLevelTries) setStopTraversal, try to set a non boolean value to the stop traversal state")
        
        #look after the string
        searchResult = self.searchNode(stringList, True)
        #if not searchResult.isValueFound():
        #    raise pathNotExistsTriesException("(multiLevelTries) setStopTraversal, The path <"+" ".join(stringList)+"> does not exist in the multi tries")
        
        #check if a node (value or not) exist on this path
        if not searchResult.isPathFound(): #len(existingPath) < len(stringList) or 
            raise pathNotExistsTriesException("(multiLevelTries) setStopTraversal, The path <"+" ".join(stringList)+"> does not exist in the multi tries")
        
        #update state
        searchResult.getMltFound().stopTraversal = state
        return searchResult.getMltFound()
    
    
    #def _traversalWithPrefix(self, currentPath, current, level):
    def _traversalWithPrefix(self, path, node, state, level):
        prefixPath, subMeth, innerState = state
        
        #build complete path
        newPath = prefixPath[:]
        newPath.extend(path)
    
        #call submethod
        newState = subMeth(newPath, node, innerState, level)
        
        #return state
        return prefixPath,subMeth,newState
    
    
    def _exploreNextTries(self, level, currentPath, current):
        currentPath.append("")
        current.value.localTries.MTParent = current
        return level+1, current.value.localTries
    
    def genericDepthFirstTraversal(self,executeOnNode, initState = None, preOrder = True, ignoreStopTraversal = False, onlyPerfectMatch=True, prefix=(), includePrexix=False):
        """
        This function executes a depth first traversal on the multi level tries.
        
        @type executeOnNode: function(currentPath, current, traversalState, level)
        @param executeOnNode: the function that will be call on every (included no value node) tries node
        @type initState: anything
        @param initState: this is the initial value of the traversal state
        @type preOrder: boolean
        @param preOrder: True means preorder, False means postorder
        @type ignoreStopTraversal: boolean
        @param ignoreStopTraversal: if set to True, the exploration process will stop on the node with stopTraversal set to True
        @type onlyPerfectMatch: boolean
        @param onlyPerfectMatch: if this param is set to True, only the perfect matching will be accepted in the search algorithm
        @type prefix: string list
        @param prefix: the list of the prefix to traverse, only the node corresponding to the prefix and its child will be explored
        @type includePrexix: boolean
        @param includePrexix: if set to True, the prefix will be included in the path given to the method executeOnNode, if False, only the path from the prefix will be given
        @rtype: anything
        @return: the last state
        @raise pathNotExistsTriesException: if prefix is set to an unexistant path in the tree
        @raise ambiguousPathExceptionWithLevel: if onlyPerfectMatch is set to False and there is an ambiguous result inside a inner tries search
        @attention: this graph works with node colouring, so the variable traversed and traversal_index can't be used outside of this function
        """
        
        current        = self.localTries #current is always a tries, never a mltries
        currentPath    = [""]            #string list of the current path
        traversalState = initState       #the evolution of the state variable
        level          = 1               #the level of the current node
        methToExecute  = executeOnNode   #
        originMltNode  = self            #
        
        #manage traversal with prefix
        if len(prefix) > 0:
            #search for the node
            searchResult = self.searchNode(prefix, onlyPerfectMatch)
            
            #path exist ?
            if not searchResult.isPathFound(): #len(existingPath) < len(prefix) or 
                raise pathNotExistsTriesException("(multiLevelTries) genericDepthFirstTraversal, The path <"+" ".join(prefix)+"> does not exist in the multi tries")
            
            originMltNode = searchResult.getMltFound()
            
            #include the prefix ?
            if includePrexix:
                traversalState = (searchResult.getFoundCompletePath(),executeOnNode,initState,)
                methToExecute  = originMltNode._traversalWithPrefix
        
        #explore empty path preOrder
        if preOrder:
            traversalState = methToExecute([], self, traversalState, 0)
         
        while current != None:
            #print currentPath, current
        ### traverse the node AND pre order process ###
            if "traversed" not in current.__dict__.keys(): #execute this statement only once
                currentPath[level-1] += current.key #update the current part of the key path
                current.traversed = True #set the node as traversed ONCE
                
                #pre order processing
                if preOrder and current.isValueSet():
                    #traverse the node
                    traversalState = methToExecute(currentPath, current.value, traversalState, level)
                    
                    #traverse the tries store in the node
                    if not current.value.localTries.isEmpty() and (ignoreStopTraversal or not current.value.stopTraversal):
                        level, current = originMltNode._exploreNextTries(level, currentPath, current)
                        continue
            else:
                #remove the reference about the traversal
                if preOrder and current.isValueSet() and "MTParent" in current.value.localTries.__dict__.keys():
                    del current.value.localTries.MTParent
            
        ### child process ###
            #explore only if there is more than one child AND no post order traversal in progress
                #because if there is a postorder traversal, the childs have been already explored
            
            if len(current.childs) > 0 and (preOrder or (not current.isValueSet() or "MTParent" not in current.value.localTries.__dict__.keys())  ): #is there some child to explore ?
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
        ### post order process ###
            #post order traversal
            if not preOrder and current.isValueSet():
                #explore next level tries
                if not current.value.localTries.isEmpty() and (ignoreStopTraversal or not current.value.stopTraversal):
                    if "MTParent" in current.value.localTries.__dict__.keys():
                        del current.value.localTries.MTParent
                    else:
                        level, current = originMltNode._exploreNextTries(level, currentPath, current)
                        continue
                        
                traversalState = methToExecute(currentPath, current.value, traversalState, level)
        ### end of the node process ###
            #remove the key string of the current node from the path
            if len(current.key) > 0:
                currentPath[level-1] = currentPath[level-1][:-len(current.key)]
            
            #back to the parent
            del current.traversed
            
            #if we are at the tries root, test if there is a parent Multi Level Tries, and go up if necessary
            if current.parent == None and hasattr(current,"MTParent") and current.MTParent:
                level -= 1
                oldCurrent = current
                currentPath = currentPath[:-1]
                current = current.MTParent
                continue
            
            current = current.parent
        
        #explore empty path postOrder
        if not preOrder:
            return methToExecute([], originMltNode, traversalState, 0)
        
        ### return the final state
        return traversalState

    def genericBreadthFirstTraversal(self, executeOnNode, initState = None, ignoreStopTraversal = False, onlyPerfectMatch=True, prefix=(), includePrexix=False): 
        """
        This function executes a breadth first traversal on the multi level tries.
        
        @type executeOnNode: function(currentPath, current, traversalState, level)
        @param executeOnNode: the function that will be call on every (included no value node) multi level tries node
        @type initState: anything
        @param initState: this is the initial value of the traversal state
        @type ignoreStopTraversal: boolean
        @param ignoreStopTraversal: if set to True, the exploration process will stop on the node with stopTraversal set to True
        @type onlyPerfectMatch: boolean
        @param onlyPerfectMatch: if this param is set to True, only the perfect matching will be accepted in the search algorithm
        @type prefix: string list
        @param prefix: the list of the prefix to traverse, only the node corresponding to the prefix and its child will be explored
        @type includePrexix: boolean
        @param includePrexix: if set to True, the prefix will be included in the path given to the method executeOnNode, if False, only the path from the prefix will be given
        @rtype: anything
        @return: the last state
        @raise pathNotExistsTriesException: if prefix is set to an unexistant path in the tree
        @raise ambiguousPathExceptionWithLevel: if onlyPerfectMatch is set to False and there is an ambiguous result inside a inner tries search
        @see: http://en.wikipedia.org/wiki/Breadth-first_search
        """
        
        startingNode = self
        traversalState = initState
        if len(prefix) > 0:
            #search for the node
            searchResult = self.searchNode(prefix, onlyPerfectMatch)
            
            #path exist ?
            if not searchResult.isPathFound(): #len(existingPath) < len(prefix) or 
                raise pathNotExistsTriesException("(multiLevelTries) genericBreadthFirstTraversal, The path <"+" ".join(prefix)+"> does not exist in the multi tries")
            
            startingNode = searchResult.getMltFound()
            
            #include the prefix ?
            if includePrexix:
                traversalState = (searchResult.getFoundCompletePath(),executeOnNode,initState,)


        Queue          = []
        #init the Queue with every key value of the first level tries
        #keyValue = self.localTries.getKeyValue()
        #for k,v in keyValue.iteritems():
        #    Queue.append( (v, 0, [k],))
        Queue.append( (startingNode, 0, [],))
        
        #read the queue
        while len(Queue) > 0:
            #dequeu current node
            current, level, currentPath = Queue.pop(0)
            
            #add every child in the Queue
            if not current.localTries.isEmpty() and (ignoreStopTraversal or not current.stopTraversal):
                keyValue = current.localTries.getKeyValue()
                
                for k,v in keyValue.iteritems():
                    newPath = currentPath[:]
                    newPath.append(k)
                    Queue.append( (v, level+1, newPath,))       
            
            #read value node with value
            traversalState = executeOnNode(currentPath, current, traversalState, level)
        return traversalState
    
    
############ MISC FUNCTION #########################################################################################################################################################################
    
    
    def __repr__(self):
        """
        This methods return the representation of the tries stored on this mltries node
        
        @rtype: string
        @return: 
        """
        
        return repr(self.localTries)
    
    
    def _inner_buildDictionnary(self, path, node, state, level):
        if not node.isValueSet():
            return state
        
        state[tuple(path)] = node.value
        return state

    
    def buildDictionnary(self, stringList = (), ignoreStopTraversal=False, addPrexix= False, onlyPerfectMatch=True):
        """
        This function built a dictionnary with every path/value existing in the tree.  
        
        @type stringList: string list
        @param stringList: the argument allows to build only a subset of the tree, set the prefix of the wanted paths
        @type ignoreStopTraversal: boolean
        @param ignoreStopTraversal: if set to True, the exploration process will stop on the node with stopTraversal set to True
        @type addPrexix: boolean
        @param addPrexix: if set to True, the prefix set in stringList will be concat to every path
        @type onlyPerfectMatch: boolean
        @param onlyPerfectMatch: if this param is set to True, only the perfect matching will be accepted in the search algorithm
        @rtype: dictionary
        @return: a dictionnary with every path/value existing in the tree
        @raise ambiguousPathExceptionWithLevel: if onlyPerfectMatch is set to False and there is an ambiguous result inside a inner tries search
        """
        
        return self.genericDepthFirstTraversal(self._inner_buildDictionnary, {}, True, ignoreStopTraversal,onlyPerfectMatch, stringList, addPrexix)
        #return self.genericBreadthFirstTraversal(self._inner_buildDictionnary, {}, ignoreStopTraversal,onlyPerfectMatch, stringList, addPrexix)


class multiLevelTriesSearchResult(object):
    """
    This provide an advanced multi level tries result object
    
    @contact: pytries@djoproject.net
    @version: 1.0
    @licence: GPL v3
    """
        
    def __init__(self, stringList, existingPath, onlyPerfectMatch, ambiguous = False):
        """
        This method is the constructor of the multi level tries search result.
        Its arguments are every value extracted from the search algorithm
        
        @type stringList: list of string
        @param stringList: the list of string explored in the tree
        @type existingPath: list of tuple(string, multiLevelTries, multiLevelTries, tries)
        @param existingPath: it is the stack of every exploration step of the search process, see searchNode function in multiLevelTries
        @type onlyPerfectMatch: boolean
        @param onlyPerfectMatch: this boolean is set to True if it was set to true during the search call, False otherwise
        @type ambiguous: boolean
        @param ambiguous: this boolean is set to True if the search algorithm found an ambiguous result, False otherwise
        @rtype: multiLevelTriesSearchResult
        @return: an instance of multiLevelTriesSearchResult
        """
        
        self.stringList   = stringList
        self.existingPath = existingPath
        self.tokenFoundCount  = len(self.existingPath)
        self.onlyPerfectMatch = onlyPerfectMatch
        self.ambiguous        = ambiguous
        
        #special case, the last token searched is in the existingPath but if it is not found, it does not count as a existing part of the path
        if not self.isPathFound():
            self.tokenFoundCount -= 1
        
        self.tokenNotFound = len(self.stringList) - self.tokenFoundCount
    
    
    def isPathFound(self):
        """
        This method returns True if the search process has found a path corresponding to the string list
        
        @rtype: boolean
        @return: True if the search process has found a path, False otherwise
        """
        
        return self.existingPath[-1][2] != None
    
    
    def isValueFound(self):
        """
        This method returns True if a value corresponds to the explored path.
        
        @rtype: boolean
        @return: True if a value corresponds to the explored path, False otherwise
        """
        
        #return (len(stringList) == 0 and existingPath[0][1].valueSet) or (len(stringList) > 0 and existingPath[-1][2] != None and existingPath[-1][2].valueSet)
        return self.existingPath[-1][2] != None and self.existingPath[-1][2].valueSet


    def getMltFound(self):
        """
        This method return the multi level tries node corresponding to the path
        
        @rtype: multiLevelTries
        @return: the multi level tries node corresponding to the path
        @raise pathNotExistsTriesException: if there is no multi level tries node corresponding to the path
        """
        
        if not self.isValueFound() and not self.isPathFound():
            raise pathNotExistsTriesException("(multiLevelTriesSearchResult) getMltFound, No match on the path <"+" ".join(self.stringList)+">")
            
        return self.existingPath[-1][2]
        
    def getValue(self):
        """
        This method returns the value stored in the multi level tries node corresponding to the explored path if exists, otherwise an exception is raised
        
        @rtype: anything
        @return: the value corresponding to the explored path
        @raise noValueSetTriesException: if no value are stored on the explored path
        """
        
        
        if not self.isValueFound(self):
            raise noValueSetTriesException("(multiLevelTriesSearchResult) getValue, no value found on this path")
        
        return self.existingPath[-1][2].value
    
    def getFoundToken(self):
        """
        This method returns a list with the tokens found
        
        @rtype: string list
        @return: the list of tokens found
        """
        
        return self.stringList[:self.tokenFoundCount]
    
    
    def getFoundCompletePath(self):
        """
        This method convert any prefix into the original stringList into the complete string stored in the tree
        
        @rtype: string list
        @return: the list of the complete path of each token in the original string list
        """
        
        ret = []
        for string, parentMLT, valueMLT, triesNode in self.existingPath:
            if triesNode == None:
                break
        
            ret.append(triesNode.getCompleteName)
        
        return ret
    
    
    def getNotFoundToken(self):
        """
        This method returns a list with the tokens not found
        
        @rtype: string list
        @return: the list of tokens not found
        """
        
        return self.stringList[:self.tokenFoundCount]
    
    
    def getTokenFoundCount(self):
        """
        This methode returns the count of the token found in the mltries.
        
        @rtype: integer
        @return: the count of the token found
        """
        
        return self.tokenFoundCount
    
    
    def getTokenNotFoundCount(self):
        """
        This methode returns the count of the token not found in the mltries.
        
        @rtype: integer
        @return: the count of the token not found
        """
        
        return self.tokenNotFound
    
    
    def getTotalTokenCount(self):
        """
        This method returns the count of token in the searched path
        
        @rtype: integer
        @return: the count of token in the searched path
        """
        
        return len(self.stringList)
    
    
    def getTokenUsed(self):
        """
        This method returns the number of token used in the search process.
        This is different of the token found in the tree.
        
        @rtype: integer
        @return: the number of token used in the search process
        """
        
        return len(self.existingPath)
    

    def getTokenNotUsed(self):
        """
        This method returns the number of token not used in the search process. 
        If the returned value is bigger than 0, the search process has not find a value
        
        @rtype: integer
        @return: the number of token not used in the search process
        """
        
        return len(self.stringList) - len(self.existingPath) 
    
    
    def isAvalueOnTheLastTokenFound(self):
        """
        This methode returns True if there is a value stored on the last token found, otherwise the method return False
        
        @rtype: boolean
        @return: True if a value exists on the last token found, False otherwise
        """
        
        return self.tokenFoundCount > 0 and self.existingPath[self.tokenFoundCount-1][2] != None and self.existingPath[self.tokenFoundCount-1][2].isValueSet()
    
    
    def getLastTokenFoundValue(self):
        """
        This methode returns the value of the last token found.
        If there is no token found or no value on the last token, an exception is raised.
        
        @rtype: multiLevelTries
        @return: the last token found
        @raise triesException: if there is no token found
        """
        
        if not self.isAvalueOnTheLastTokenFound():
            raise noValueSetTriesException("(multiLevelTriesSearchResult) getLastTokenFoundValue, no value on the last token found")
        
        return self.existingPath[self.tokenFoundCount-1][1].value
    
    
    def isAllTokenHasBeenConsumed(self):
        """
        This method returns True if every token have been found into the mltries.  
        This not means there is a match, maybe the node found does not contain any value.
        
        @rtype: boolean
        @return: True if every tokens have been found into the tree, False otherwise
        """
        
        return len(self.stringList) == self.tokenFoundCount
    
    
    ### not found reason
    
    #
    # there are still token to use but no more tries
    #    occurs when the last explored tries is empty
    #
    def isLastExploredTriesEmpty(self):
        """
        This method returns True if the last explored tries was empty. 
        
        @rtype: boolean
        @return: True is if the last explored tries was empty, False otherwise
        """
        
        return self.existingPath[-1][1].localTries.isEmpty()
    

    #
    # the last token searched was not found in the 
    #    occurs when last explored tries is not empty
    #
    def isTokenNotFoundInLastTries(self):
        """
        This method returns True if the last string token searched was not found.  
        The last token searched is different of the last token of the string list
        
        @rtype: boolean
        @return: True if the last token searched was not found, False otherwise
        """
        
        return not self.isPathFound()# and not self.existing
    

    #
    # the path has been completly found be there is no value attached to this path
    #
    def isPathCorrespondsToNonValueNode(self):
        """
        This method returns True if the searched path exists in the mltries but there is no value stored in the last node
        
        @rtype: boolean
        @return: True if the path exists and there is no value in the last node, False otherwise
        """
        
        return self.isPathFound() and not self.isValueFound()
        #return self.pathExistButNoValue
    
    
    def isPerfectSearchSet(self):
        """
        This method return True is the search was started with the boolean PerfectSearch set to True, otherwise it returns False
        
        @rtype: boolean
        @return: True is PerfectSearch was set during the search, False otherwise
        """
        
        return self.onlyPerfectMatch
    
    
    def isAmbiguous(self):
        """
        This method returns True if the searched path has several possibilities into the tree, False otherwise
        
        @rtype: boolean
        @return: True if the result has produced an ambiguous result, False otherwise
        """
        return self.ambiguous
    
    
    def getAdvancedTriesResult(self, tokenIndex):
        """
        This method returns the advanced result of any used token into its corresponding tries.
        This method does not work with empty path.  
        
        @type tokenIndex: integer
        @param tokenIndex: the index of the token to retrieve
        @rtype: triesSearchResult
        @return: the search result corresponding to specified used token
        @raise triesException: if the search was made with a n empty string or if tokenIndex is invalid
        """
        
        #is empty path?
        if len(self.stringList) == 0:
            raise triesException("(multiLevelTriesSearchResult) getAdvancedTriesResult, need at least one string token, there is no token on empty path")
        
        #index is valid ?
        if len(self.existingPath) < tokenIndex or tokenIndex < 0:
            if self.getTokenUsed() > 1:
                raise triesException("(multiLevelTriesSearchResult) getAdvancedTriesResult, invalid index, the available index are [0-"+str(self.getTokenUsed()-1)+"]")
            else:
                raise triesException("(multiLevelTriesSearchResult) getAdvancedTriesResult, invalid index, the only available index is 0")
        
        #create advanced tries result
        advancedTriesResult = self.existingPath[tokenIndex][1].localTries.advancedSearch(self.existingPath[tokenIndex][0])
        
        #return the whole result
        return advancedTriesResult
    
    
    def getAdvancedTriesResultForLastTokenExplored(self):
        """
        This method returns the advanced result of the last used token into its corresponding tries.
        This method does not work with empty path.  
        
        @rtype: triesSearchResult
        @return: the search result corresponding to the last used token
        """
        
        return self.getAdvancedTriesResult(len(self.existingPath) - 1)
    

