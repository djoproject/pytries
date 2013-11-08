#!/usr/bin/python2.6
# -*- coding: utf-8 -*- 

#Copyright (C) 2012 Jonathan Delvaux <jonathan.delvaux@uclouvain.be>

#This program is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#any later version.

#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#GNU General Public License for more details.

#You should have received a copy of the GNU General Public License
#along with this program. If not, see <http://www.gnu.org/licenses/>.

#TODO
    #-test genericBreadthFirstTraversal
    #-specialize the exception (e.g. pathExistsTriesException, pathNotExistsTriesException)

from exception import triesException
from utils import noneFunc, charInCommons, returnNode

class tries():
    
    #
    # constructor of the class tries
    #
    # @parameter self, the reference of the class object
    # @parameter key, the part of the key string stored in the current node
    # @parameter parent, the parent node in the tree
    # @parameter value, the value stored in the key
    #
    def __init__(self, key = "", parent = None, anySuffix = False):
        "init the node with a key, and maybe a parent and a value"
        #print "{"+key+"}"
        #if key == None or type(key) != str or len(key) == 0:
        # raise triesException("the inserted key must be a string with a length bigger than zero")
        
        self.key       = key
        self.childs    = []
        self.value     = None
        self.valueSet  = False
        self.parent    = parent
        self.anySuffix = anySuffix
    
    
    def setValue(self, value):
        self.value = value
        self.valueSet = True
    
    
    def unsetValue(self):
        self.value = None
        self.valueSet = False
    
    
    def isValueSet(self):
        return self.valueSet
    
    
    def getValue(self):
        if not self.valueSet:
            raise triesException("this node does not contain any value")
            
        return self.value
    
    
    #
    # this methode identify if the current node is an end node or not
    #
    # @return True if the current node is an end node, return False otherwise
    #
    def isFinalNode(self):
        return len(self.child) == 0
    
    
    #
    #
    #
    def isEmpty(self):
        return len(self.childs) == 0 and self.value == None
    
    
########### MAJOR FUNCTION (remove/update/insert) #######################################################################################################################################################
    
    #
    # method to remove a key string and its value from the tree
    # 
    # @param key, the key of the node to remove
    # @exception triesException if no node exists with the specified key
    #
    def remove(self, key):
        "remove a node with a specific key in the tree"
        #search the specific node
        Node = self.searchNode(key,returnNode)
        
        #the node must exist and be a value node
        if Node == None or not Node.isValueSet():
		    raise triesException("key not found")
        
        ### Case 1 : No Child ###
        if len(Node.childs) == 0:
            ## Case 1.1 : root node ##
            if Node.parent == None:
                Node.key = ""
                Node.unsetValue()
            ## Case 1.2 : no root node ##
            else:
                #remove node from parent list
                Node.parent.childs.remove(Node)
                
                #special Case, the parent node must be balanced
                #is the parent a non value intermediate node ?
                parent = Node.parent
                if not parent.isValueSet() and len(parent.childs) == 1:
                    #concat the parent key with the sibbling node key
                    sibbling = parent.childs[0]
                    
                    #the parent is the root ?
                    if parent.parent == None:
                        #the root become the sibling
                        parent.key      = parent.key + sibbling.key 
                        parent.childs   = sibbling.childs
                        #update childs
                        for c in sibbling.childs:
                            c.parent = parent
                        
                        parent.value    = sibbling.value
                        parent.valueSet = sibbling.valueSet
                    else:
                        #merge the intermediate node with the sibling node
                        sibbling.key = parent.key + sibbling.key
                        #add the child in the great parent
                        parent.parent.childs.remove(parent)
                        parent.parent.childs.append(sibbling)
                        sibbling.parent = parent.parent
                        
                        #remove the intermediate parent node
                        del parent
                        
                #remove the node
                del Node
        
        ### Case 2 : One Child ###
            #the current node become its child and its child disappear
            #there is no different process to do if the node is root
        elif len(Node.childs) == 1:
            #concat key
            child = Node.childs[0]
            Node.key    = Node.key + child.key
            
            #merge node
            Node.setValue(child.value)
            Node.childs = child.childs
            #update childs
            for c in child.childs:
                c.parent = Node
            
            #del the child
            child.unsetValue()
            del child
            
        ### Case 3 : More than one Child ###
            #if there is several child, the current node is the biggest common prefix of these nodes
            #so the node must just become an non value intermediate node
        else:
            Node.unsetValue()                
    
    
    #
    # update the value of the node corresponding to the key
    #
    # @param key, the key of the final node to update
    # @param newValue, the value to change in the node corresponding of the key
    # @return the updated node
    #
    def update(self, key, newValue):
        Node = self.searchNode(key,returnNode)
        if Node != None and Node.isValueSet():
            Node.value = newValue
            return Node
            
        raise triesException("key not found")
    
    
    #
    # insert a new couple key/value in the tree
    #
    # @return the inserted node
    # @exception triesException if insertion failed
    #
    def insert(self,key, value, anySuffix = False):
        #CASE 1 : perfect match
        def exact(Node,key):
            #if the current node is a value node, can't insert the new value
            if Node.isValueSet(): #is it a value node?
                raise triesException("the inserted key already exists")
            
            return Node
        
        #CASE 2 : a node has a path string similar to the prefix of the key searched
        def noMatchChild(Node,key,totalCount):
            #Special Case 1 : manage the root case (first inserted node)
                #the root become the node, otherwise classical threatment
            if not Node.isValueSet() and Node.parent == None and len(Node.childs) == 0: #empty tree ?
                Node.key = key
                return Node

            #create a simple node with the non common part of the key
            newNode = tries(key[totalCount:],Node)

            #append the new node to the parent
            Node.childs.append(newNode)
            return newNode
        
        #CASE 3  : partial match, the key is a prefix of an existing path string
        def partial(Node,key,count,totalCount):
            #split the key string of the old node and create a new value node with the existing value
            tempTries = tries(Node.key[count:], Node)
            tempTries.setValue(Node.value)
            Node.unsetValue()
            
            #the new node become the parent of the existing childs
            tempTries.childs = Node.childs
            
            #update the parent field of the childs
            for child in tempTries.childs:
                child.parent = tempTries
            
            #update the key of the old node
            Node.key = Node.key[:count]
            
            #the only child of the old node is the new node
            Node.childs = [tempTries]
            
            #return the old node, it will contain the new value
            return Node
        
        #CASE 4 : the suffix of the searched key is not include in any existing string path
        def false(Node,key,count,totalCount):                            
            #create an intermediate node
            tempTries = tries(Node.key[count:], Node)
            tempTries.setValue(Node.value)
            
            #transfert the child of the previous node to the new intermediate node
            tempTries.childs = Node.childs
            
            #update child parent
            for child in tempTries.childs:
                child.parent = tempTries
            
            #update the original node key
            Node.key = Node.key[:count]
            
            #create a new node
            newTries = tries(key[totalCount:], Node)
            
            #mise a jour du noeud courant, non value node, devient un noeud pivot
            Node.childs = [tempTries,newTries]
            Node.unsetValue()
            
            return newTries
        
        #assign the value
        Node = self.searchNode(key,exact,partial,noMatchChild,false)
        Node.setValue(value)
        Node.anySuffix = anySuffix
        
        #return the node
        return Node
    
    
############ SEARCH FUNCTION #########################################################################################################################################################################
    
    #
    # generic search method, this method allow to retrieve any kind of result from the tree with the parameter methods
    # 
    # @parameter prefix
    # @parameter exactResult(currentNode,prefix), the node corresponding to the perfect match and the complete path to find in the tree
    # @parameter partialResult(currentNode,prefix,count,totalCount), the node corresponding to the partial match, the prefix path to find, the count of common caracter with the current node, and the total count of common caracters
    # @parameter noMatchChild(currentNode,prefix,totalCount), the last explored node, the prefix to find in the tree, and the total count of common caracters
    # @parameter falseResult(currentNode,prefix,count,totalCount), same as partialResult
    # @parameter anySuffixAllowed, allow to disable the special stuff any suffix to make a strict search on the tree
    # @return
    # @exception triesException if the prefix is not a string type
    #
    def searchNode(self,prefix,exactResult,partialResult = noneFunc, noMatchChild = noneFunc, falseResult = noneFunc, anySuffixAllowed = False):
        #must be a valid string
        if prefix == None or type(prefix) != str:# or len(prefix) == 0:
            raise triesException("the searched key must be a string")# with a length bigger than zero")
        
        currentNode   = self   #The starting point of the search is the current node
        currentPrefix = prefix #The prefix to find in the tree
        totalCount    = 0      #The common caracter total count in the whole tree
        while True:
            #count the common caracter with the current node key
            count       = charInCommons(currentNode.key, currentPrefix)
            
            #increment the total counter
            totalCount += count
        
            #the current key node is completly common
            if len(currentNode.key) == count:
                #valide string and end node
                if len(currentPrefix) == count:
                    return exactResult(currentNode,prefix) # bear = bear #perfect concordance, prefix is equal to a prefix in the tree
                
                #reduction of the prefix to find                    
                currentPrefix = currentPrefix[len(currentNode.key):]
                
                #find a child candidate to continue the search
                for child in currentNode.childs:
                    if child.key[0] == currentPrefix[0]: #len(child.key) == 0 or len(currentPrefix) == 0 or child.key[0] == currentPrefix[0] #child.canPropagate(currentPrefix):
                        currentNode = child
                        break
                else:
                    if anySuffixAllowed and self.anySuffix:
                        return exactResult(currentNode,prefix)
                
                    #no child found to continue the search
                    return noMatchChild(currentNode,prefix,totalCount) # bearor > bear
                    
            #the current node is partialy or not common at all
            else: #count < len(self.key)
                #the searched prefix is completly used, so it is a partial result
                if len(currentPrefix) == count:
                    return partialResult(currentNode,prefix,count,totalCount) # be < bear #partial match, prefix is a part of a prefix in the tree
            
                #the searched prefix has a unknown suffix in the tree
                return falseResult(currentNode,prefix,count,totalCount) # bee != bear
    
    
    #
    # This search looks for a perfect key match and return a value node or an non value node
    #
    # @parameter key, the string path to find
    # @return a perfect match value Node or None
    # @exception triesException if the prefix is not a string type
    #
    def search(self,key):
        Node = self.searchNode(key,returnNode)
        if Node != None and Node.isValueSet():
            return Node
        return None
    

    #
    # this function looks for a complete path corresponding to the prefix string given
    #
    # @parameter prefix, the prefix to search in the tree
    # @return a value node
    # @exception triesException if the prefix is not a string or if the string does not correspond to a complete path
    #
    def searchUniqueFromPrefix(self,prefix):
        Node = self.searchNode(prefix,returnNode,returnNode)
        if Node != None:
            if Node.isValueSet():
                return Node
            else:
                #ambiguous result, raise
                raise triesException("the prefix <"+str(prefix)+"> corresponds to multiple node")
        
        #no match in the tree
        return None
    
    
    #
    #
    #
    def advancedSearch(self, prefix):
        result = triesSearchResult()
        return self.searchNode(prefix, result._perfect, result._partial, result._noChild, result._false)
    
    
############ TRAVERSAL FUNCTION #####################################################################################################################################################################
    #
    # start a traversal over all the node of the tree starting from the current node included
    #
    # WARNING, this graph works with node colouring, so the variable traversed and traversal_index can't be used outside of this function
    #
    def genericDepthFirstTraversal(self,executeOnNode, initState = None, preOrder = True):
        current        = self
        currentPath    = ""
        traversalState = initState
        level          = 0
         
        while current != None: 
            ### traverse the node ###
            if "traversed" not in current.__dict__.keys():
                currentPath += current.key
                if preOrder:
                    traversalState = executeOnNode(currentPath, current, traversalState, level)                
                current.traversed = True
            
            ### identify next node to explore ###
            #is there some child to explore
            if len(current.childs) > 0:
                #does the exploration already start ?
                if "traversal_index" not in current.__dict__.keys():
                    level += 1
                    current.traversal_index = 0
                
                #is there still child to explore ,
                if current.traversal_index < len(current.childs):
                    current.traversal_index += 1
                    current = current.childs[current.traversal_index -1]
                    continue
                
                #no more need the index
                del current.traversal_index
                level -= 1
                
            #post order traversal
            if not preOrder:
                traversalState = executeOnNode(currentPath, current, traversalState, level)
            
            #remove the key string of the current node from the path
            if len(current.key) > 0:
                currentPath = currentPath[:-len(current.key)]
            
            #back to the parent
            del current.traversed
            current = current.parent
        
        return traversalState
    
    
    #
    # http://en.wikipedia.org/wiki/Breadth-first_search
    #
    def genericBreadthFirstTraversal(self, executeOnNode, initState = None):
        level          = 0
        Queue          = [(self,level,self.key)]
        traversalState = initState
        currentPath    = ""
        
        while len(Queue) > 0:
            #dequeu current node
            current, level, currentPath = Queue.popleft()
            
            #enqueue node child
            while c in current.childs:
                Queue.append( (c,level+1, path+c.key) )
            
            #execute user function
            traversalState = executeOnNode(currentPath, current, traversalState, level)
    
    
    
############ MISC FUNCTION #########################################################################################################################################################################
    
    #
    #
    #
    def _listEveryCompletePath(self, path, node, state, level):
        if node.isValueSet():
            state.append(path)
        
        return state
    
    
    #
    #
    #
    def getKeyList(self):
        return self.genericDepthFirstTraversal(self._listEveryCompletePath, [])
    
    
    #
    # @return a dictionnary with all the key or an empty list if no result
    #
    def getKeyListFromPrefix(self,prefix):
        starting_point = self.searchNode(prefix,returnNode,returnNode)
        
        #if invalid result (noMatchChild or falseResult), there is no bigger path
        if starting_point == None:
            return []
        
        return starting_point.genericDepthFirstTraversal(self._listEveryCompletePath, [])
    
    #
    #
    #
    def _listEveryCompletePathAndValue(self, path, node, state, level):
        if node.isValueSet():
            state[path] = node.value
        
        return state
    
    #
    #
    #
    def getKeyValue(self):
        return self.genericDepthFirstTraversal(self._listEveryCompletePathAndValue, {})
    
    
    #
    #
    #    
    def getKeyValueFromPrefix(self, prefix):
        starting_point = self.searchNode(prefix,returnNode,returnNode)
        
        #if invalid result (noMatchChild or falseResult), there is no bigger path
        if starting_point == None:
            return []
        
        return starting_point.genericDepthFirstTraversal(self._listEveryCompletePathAndValue, {})
    
    
#################
    
    def _getMaxChildCount(self, path, node, state, level):
        if len(node.child) > state:
            return len(node.child)
        return state
    
    
    #
    # this methode compute the bigger number of child of all the current node childs
    # @return an integer bigger or equal to zero
    #
    def getMaxChildCount(self):
        return self.genericDepthFirstTraversal(self._getMaxChildCount, 0)
    
    
#################
    
    def _traversal(self, path, node, state, level):
        s = ""
        for i in range(0,level):
            s+= " "
        
        s += "{"+node.key+"}"
        s += repr(node)
        
        if level == 0:
            state += s
        else:
            state += "\n" + s
        
        return state
    
    
    #
    #
    #
    def traversal(self,level = 0):
        return self.genericDepthFirstTraversal(self._traversal, "")
    
    
#################
    
    def _countValue(self, path, node, state, level):
        if node.isValueSet():
            state += 1
        return state
    
    
    #
    # 
    #
    def countValue(self):
        return self.genericDepthFirstTraversal(self._countValue, 0)
    

    
#################
    
    #
    #
    #
    def getCompleteName(self):
        node = self
        s = ""

        while node != None:
            s = node.key + s
            node = node.parent

        return s
    
    
############ __ FUNCTION __ #########################################################################################################################################################################
    
    #
    #
    #
    def __repr__(self):
        if self.value == None:
            if self.parent == None:
                return "none node (key = \""+self.key+"\", completeName = "+self.getCompleteName()+", parent = None, child count = "+str(len(self.childs))+", valueSet = "+str(self.valueSet)+")"
            else:
                return "none node (key = \""+self.key+"\", completeName = "+self.getCompleteName()+", parent = \""+self.parent.key+"\", child count = "+str(len(self.childs))+", valueSet = "+str(self.valueSet)+")"
        else:
            if self.parent == None:
                return "tries node (key = \""+self.key+"\", value = \""+str(self.value)+"\", completeName = "+self.getCompleteName()+", parent = None, child count = "+str(len(self.childs))+", valueSet = "+str(self.valueSet)+")"
            else:
                return "tries node (key = \""+self.key+"\", value = \""+str(self.value)+"\", completeName = "+self.getCompleteName()+", parent = \""+self.parent.key+"\", child count = "+str(len(self.childs))+", valueSet = "+str(self.valueSet)+")"
    

class triesSearchResult(object):
    def __init__(self):
        self.resultNode   = None #perfect or partial match
        self.previousNode = None #noMatchNode, falseNode, partial
    
        self.perfectMatch = False
        self.partialMatch = False
        self.noMatchChild = False
        self.falseResult  = False
    
    def _perfect(node, prefix):
        self.perfectMatch = True
        self.resultNode   = node
        self.previousNode = node.parent
        
    def _partial(node, prefix, count, totalCount):
        self.partialMatch = True
        self.resultNode   = node
        self.previousNode = node.parent
        
    def _noChild(node,prefix,count,totalCount):
        self.noMatchChild = True
        self.previousNode = node
    
    def _false(node,prefix,count,totalCount):
        self.falseResult = True
        self.previousNode = node
    
    ########
    
    def isPerfectMatch(self):
        return self.perfectMatch
    
    def isPartialMatch(self):
        return self.partialMatch
    
    def isMatch(self):
        return self.perfectMatch or self.partialMatch
    
    def isNoMatchNode(self):
        return self.noMatchNode
        
    def isFalseResult(self):
        return self.falseResult
    
    def getNode(self):
        return self.resultNode
        
    def getPreviousNode(self):
        return self.previousNode
    

