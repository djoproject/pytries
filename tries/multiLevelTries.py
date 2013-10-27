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
            
    #traversal
        #TODO
            #manage the stop traversal
            
        #how to make breadth first traversal ?
            #TODO
        
from tries import *
from exception import triesException

class multiLevelNode(object):
    def __init__(self):
        self.nextTries     = tries()
        self.value         = None
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


class multiLevelTries(object):
    
    def __init__(self):
        "this method init the multiLevelTries with an empty tries root"
        self.levelOneTries = tries()
    
    #
    # @parameter stringList is the list of string token to find in the multiTries
    # @parameter onlyPerfectMatch is a boolean to limit the search to the perfect match result, if it is set to false, the partial result will be allowed
    # @return the number of matching token, 
    #
    def searchNode(self, stringList, onlyPerfectMatch=True):
        if stringList == None or type(stringList) != list or len(stringList) < 0:
            raise triesException("need string token to insert a new value, no token found")
        
        #because the value inserted is always stored in the root of a tries, we need to add an empty string
        #stringList = stringList[:] #clone the stringList before to update it, because an update here can have an impact outside the function
        #stringList.append("")
        
        #SEARCH a similar String list
        tries_tmp      = self.levelOneTries #current tries where make the search (at init, it is the first level)
        triesLinked    = [] #list to store the result
        foundValue     = False #did we find the result ?
        value          = None #result match ?
        for i in range(0,len(stringList)): #for each token of the string list to insert
            #TODO test if stringList[i] is a string
            
            #search the string[i] in the current tries
            if onlyPerfectMatch:
                tmp = tries_tmp.search(stringList[i])
            else:
                tmp = tries_tmp.searchUniqueFromPrefix(stringList[i]) #allow partial but non ambigous result
            
            #store the result (token, in which tries the token had been found, the value associated to the token)
            triesLinked.append( (stringList[i], tries_tmp, tmp,) )
            #print stringList[i], tries_tmp, tmp
            #print
            #is there a value node here ?
            if tmp != None and tmp.isValueSet():
                if i == len(stringList)-1: #every string had been consumed
                    foundValue  = tmp.value.valueSet
                    value       = tmp.value.value        
                elif tmp.value.nextTries != None: #look for another sub level to explore
                    tries_tmp = tmp.value.nextTries
                    continue
                            
            #at this point, we found a result or the path does not exist in the tree
            return triesLinked, foundValue, value
    
    
    #
    #
    # @param stringList : array string
    # @param value : object to store
    #
    def insert(self, stringList, value, anyStringSuffix="*"):
        #manage anyString
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
        
        #determine where the string list must be insert, searchNode always stores at least one value in existingPath
        currentTreeWhereInsert = existingPath[-1][1]
        
        #insert the path
        #print stringList
        for i in range(len(existingPath)-1, len(stringList)): #from the first index of a non common string to the end of the list
            if i == len(stringList)-1:
                node = currentTreeWhereInsert.insert(stringList[i], multiLevelNode(), anyStringEnable[i]).value
                node.setValue(value)
                return node
            else:
                currentTreeWhereInsert = currentTreeWhereInsert.insert(stringList[i],multiLevelNode(), anyStringEnable[i]).value.nextTries
        
    

    #
    #
    #
    def remove(self, stringList):
        #search for a similar existing stringList in the tree (we want a perfect match)
        existingPath, existing, existingValue = self.searchNode(stringList, True)
        
        #raise an exception if the path does not exist
        if not existing:
            raise triesException("Remove, The path <"+" ".join(stringList)+"> does not exist in the multi tries")
        
        #remove the node from bottom up
        for i in range(0,len(existingPath)):
            #next node index to remove
            index = len(existingPath) - 1 - i
            
            #remove the value stored
            existingPath[index][1].remove(existingPath[index][0])
            
            #tree is empty ?
            if not existingPath[index][1].isEmpty():
                break
    
    
    #
    #
    #
    def update(self, stringList, newValue):
        existingPath, existing, existingValue = self.searchNode(stringList, True)
        
        #raise an exception if the path does not exist
        if not existing:
            raise triesException("Update, The path <"+" ".join(stringList)+"> does not exist in the multi tries")
        
        #set the new value (the last node of the path contains a tries with an empty key tries, this node have to be updated)
        #existingPath[-1][1].value.setValue(newValue)
        #print existingPath[-1]
        #print existing
        #print existingValue
        existingPath[-1][2].value.setValue(newValue)
    

    #
    #
    #
    def search(self,stringList) :
        #search for a similar existing stringList in the tree (partial result are accepted)
        existingPath, existing, existingValue = self.searchNode(stringList, False)
        
        #return the value found
        if existing:
            return existingValue
        
        #error managing
        if len(existingPath) -1 == len(stringList):
            raise triesException("Search, string list is uncomplete")
        
        raise triesException("Search, unknown string in level "+str(len(existingPath))+" <"+existingPath[-1][0]+">")
    
    
    #
    #
    #
    def __repr__(self):
        return repr(self.levelOneTries)
    
    
    
    #
    #
    #
    def genericDepthFirstTraversal(self,executeOnNode, initState = None, preOrder = True):
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
            if current.isValueSet() and current.value.nextTries != None:
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
    

    #
    #
    #    
    def genericBreadthFirstTraversal(self): 
        #init a queue
        level          = 0 #TODO don't forget to update
        Queue          = [(self,level,self.key)]
        traversalState = initState
        currentPath    = [""] #TODO don't forget to update
        
        #TODO get every value node from this level and add it in the queue
            #voir misc functon dans tries
            
        #read the queue
        while len(Queue) > 0:
            #dequeu current node
            current, level, currentPath = Queue.popleft()
            
            #TODO add next level node in the queue
                #TODO update level (+1) and currentPath (concat)
            #Queue.append( (c,level+1, path+c.key) )
            
            #read value node with value
            if current.isValueSet() and current.value.isValueSet():
                traversalState = executeOnNode(currentPath, current, traversalState, level)

#
# cree un dictionnaitre de toutes les combinaisons cle/valeur existants
# cette fonction n'a pas vraiment sa place ici :/
# et elle doit être réecrite en + 
# TODO possible to do it with traversal function
#  
def buildDictionnary(current,stringStack = []):
    ret = {}
    #print current.key
    #print current.childs
    if current.value != None:
        if isinstance(current.value,tries):
            stringStack.append(current.getCompleteName())
            ret.update(buildDictionnary(current.value,stringStack))
            stringStack.pop()
        else:
            key = ""
            for s in stringStack:
                key += s+" "
            #print key
            key += current.getCompleteName()
            #print key
            ret[key] = current.value
            
    for child in current.childs:
        #print child.key
        ret.update(buildDictionnary(child))
            
    return ret
    
        



