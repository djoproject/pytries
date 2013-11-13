#!/usr/bin/python2.6
# -*- coding: utf-8 -*- 

#Copyright (C) 2012 Jonathan Delvaux <pytries@djoproject.net>

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


from exception import triesException, noValueSetTriesException, pathExistsTriesException, pathNotExistsTriesException
from utils import noneFunc, charInCommons, returnNode

class tries():
    """
    This class provide a complete implementation of the tries stucture
    
    @contact: pytries@djoproject.net
    @version: 1.0
    @licence: GPL v3
    @see: http://en.wikipedia.org/wiki/Trie
    """
    
    def __init__(self, key = "", parent = None, anySuffix = False):
        """
        init a tries node with a key, and maybe a parent
        
        @type key: string
        @param key: the part of the key string stored in the current node
        @type parent: tries
        @param parent: the parent node in the tree
        @type anySuffix: boolean
        @param anySuffix: enable the anysuffix management on this node
        @rtype: tries
        @return: a new instance of tries
        """
        
        self.key       = key
        self.childs    = []
        self.value     = None
        self.valueSet  = False
        self.parent    = parent
        self.anySuffix = anySuffix
    
    
    def setValue(self, value):
        """
        this method allow to set the value stored on this node

        @type value: anything even None
        @param value: the value to store on this node 
        """
        
        self.value = value
        self.valueSet = True
    
    
    def unsetValue(self):
        """
        this method allow to unset the value stored on this node
        """
        
        self.value = None
        self.valueSet = False
    
    
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
            raise noValueSetTriesException("this node does not contain any value")
            
        return self.value
    
    
    def isFinalNode(self):
        """
        this methode identify if the current node is an end node or not

        @rtype: boolean
        @return: True if the current node is an end node, return False otherwise
        """
        
        return len(self.child) == 0
    
    
    def isEmpty(self):
        """
        this methode identifies if the current tries is an empty tree or not
        an empty tree does not store any sub tree

        @rtype: boolean
        @return: True if the current tree does not store any child, False otherwise
        """
        
        return len(self.childs) == 0 and self.value == None
    
    
########### MAJOR FUNCTION (remove/update/insert) #######################################################################################################################################################
    
    
    def _transferNodeContent(self,otherTries):
        self.key += otherTries.key
        
        self.childs = otherTries.childs
        for c in otherTries.childs:
            c.parent = self
        
        self.anySuffix  = otherTries.anySuffix
        self.value    = otherTries.value
        self.valueSet = otherTries.valueSet
    
    
    def remove(self, key):
        """
        this method removes a key string and its value from the tree

        @type key: string
        @param key: the key of the path to remove
        @exception pathNotExistsTriesException: if no node exists with the specified key
        """

        #search the specific node
        Node = self.searchNode(key,returnNode)
        
        #the node must exist and be a value node
        if Node == None or not Node.isValueSet():
		    raise pathNotExistsTriesException("key not found")
        
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
                        """parent.key      = parent.key + sibbling.key 
                        parent.childs   = sibbling.childs
                        #update childs
                        for c in sibbling.childs:
                            c.parent = parent
                        
                        parent.value    = sibbling.value
                        parent.valueSet = sibbling.valueSet"""
                        
                        #the root become the sibling
                        parent._transferNodeContent(sibbling)
                        
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
            """#concat key
            child = Node.childs[0]
            Node.key    = Node.key + child.key
            
            #merge node
            Node.setValue(child.value)
            Node.childs = child.childs
            #update childs
            for c in child.childs:
                c.parent = Node"""
            
            #merge node
            Node._transferNodeContent(Node.childs[0])
            
            """#del the child
            child.unsetValue()
            del child"""
            
        ### Case 3 : More than one Child ###
            #if there is several child, the current node is the biggest common prefix of these nodes
            #so the node must just become an non value intermediate node
        else:
            Node.unsetValue()                
    
    
    def update(self, key, newValue):
        """
        this method updates the value of the node corresponding to the key
        
        @type key: string
        @param key: the key of the path to update
        @type newValue: anything even None
        @param newValue: the value to change in the node corresponding of the key path
        @rtype: tries
        @return: the updated node
        @raise pathNotExistsTriesException: if no node exists with the specified key
        """
        
        Node = self.searchNode(key,returnNode)
        if Node != None and Node.isValueSet():
            Node.value = newValue
            return Node
            
        raise pathNotExistsTriesException("key not found")
    
    
    def insert(self,key, value, anySuffix = False):
        """
        this method inserts a new couple key/value in the tree
        
        @type key: string
        @param key: the key of the path to insert
        @type value: anything even None
        @param value: the value to store on this path
        @type anySuffix: boolean
        @param anySuffix: enable the anysuffix management on this path
        @rtype: tries
        @return: the inserted node
        @raise pathExistsTriesException: if the path has already been inserted into the tree
        """
        
        #CASE 1 : perfect match
        def exact(Node,key):
            #if the current node is a value node, can't insert the new value
            if Node.isValueSet(): #is it a value node?
                raise pathExistsTriesException("the inserted key already exists")
            
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
    
    
    def searchNode(self,prefix,exactResult,partialResult = noneFunc, noMatchChild = noneFunc, falseResult = noneFunc, anySuffixAllowed = False):
        """
        generic search method, this method allow to retrieve any kind of result from the tree with the parameter methods
        
        @type prefix: string
        @param prefix: the prefix path to find in the tree
        @type exactResult: function(currentNode,prefix)
        @param exactResult: this function is called when a perfect path match exists in the tree
        @type partialResult: function(currentNode,prefix,count,totalCount)
        @param partialResult: this function is called when a partial node is found in the tree.  So there is no other sibling node with the same prefix
        @type noMatchChild: function(currentNode,prefix,totalCount)
        @param noMatchChild: this function is called when there is no corresping child in a node of the path to finish the search
        @type falseResult: function(currentNode,prefix,count,totalCount)
        @param falseResult: this function is called when there is an existing node with a similar prefix but with a different suffix
        @type anySuffixAllowed: boolean
        @param anySuffixAllowed: allow to disable the special stuff any suffix to make a strict search on the tree
        @rtype: anything
        @return: the returned result is the result of one of the four called method
        @raise triesException if the prefix is not a string type
        """
        
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
    
    
    def search(self,key):
        """
        This search looks for a perfect key match and return a value node or an non value node
        
        @type key: string
        @param key: the string path to find
        @rtype: Tries or None
        @return: a perfect match value Node or None
        @raise triesException if the prefix is not a string type
        """
        
        Node = self.searchNode(key,returnNode)
        if Node != None and Node.isValueSet():
            return Node
        return None
    

    def searchUniqueFromPrefix(self,prefix):
        """
        this function looks for a complete path corresponding to the prefix string given
        
        @type prefix: string
        @param prefix: the prefix to search in the tree
        @rtype: tries
        @return: a value node
        @raise triesException if the prefix is not a string or if the string does not correspond to a complete path
        """
        
        Node = self.searchNode(prefix,returnNode,returnNode)
        if Node != None:
            if Node.isValueSet():
                return Node
            else:
                #ambiguous result, raise
                raise triesException("the prefix <"+str(prefix)+"> corresponds to multiple node")
        
        #no match in the tree
        return None
    
    
    def advancedSearch(self, prefix):
        """
        This function build an advanced result
        
        @type prefix: string
        @param prefix: the prefix of the key to search in the tree
        @rtype: triesSearchResult
        @return: an advanced result object, see its documentation to get more details
        """
        
        result = triesSearchResult()
        return self.searchNode(prefix, result._perfect, result._partial, result._noChild, result._false)
    
    
############ TRAVERSAL FUNCTION #####################################################################################################################################################################
    
    def genericDepthFirstTraversal(self,executeOnNode, initState = None, preOrder = True):
        """
        This function executes a depth first traversal on the tries.  
        
        @type executeOnNode: function(currentPath, current, traversalState, level)
        @param executeOnNode: the function that will be call on every (included no value node) tries node
        @type initState: anything
        @param initState: this is the initial value of the traversal state
        @type preOrder: boolean
        @param preOrder: True means preorder, False means postorder
        @rtype: anything
        @return: the last state
        @attention: this graph works with node colouring, so the variable traversed and traversal_index can't be used outside of this function
        """
        
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
    
    
    def genericBreadthFirstTraversal(self, executeOnNode, initState = None):
        """
        This function executes a breadth first traversal on the tries.  
        
        @type executeOnNode: function(currentPath, current, traversalState, level)
        @param executeOnNode: the function that will be call on every (included no value node) tries node
        @type initState: anything
        @param initState: this is the initial value of the traversal state
        @rtype: anything
        @return: the last state
        @see: http://en.wikipedia.org/wiki/Breadth-first_search
        """
        
        level          = 0
        Queue          = [(self,level,self.key)]
        traversalState = initState
        currentPath    = ""
        
        while len(Queue) > 0:
            #dequeu current node
            current, level, currentPath = Queue.pop(0)
            
            #enqueue node child
            for c in current.childs:
                Queue.append( (c,level+1, currentPath+c.key) )
            
            #execute user function
            traversalState = executeOnNode(currentPath, current, traversalState, level)
    
        return traversalState
    
############ MISC FUNCTION #########################################################################################################################################################################
    
    def _listEveryCompletePath(self, path, node, state, level):
        if node.isValueSet():
            state.append(path)
        
        return state
    
    
    def getKeyList(self, prefix=""):
        """
        This method build a list with every key stored in this tries
        
        @type prefix: string or None
        @param prefix: the prefix of the key needed, default is an empty string
        @rtype: list
        @return: a list with every existing key pair in this tries
        """
        
        starting_point = self
        if prefix != "":
            starting_point = self.searchNode(prefix,returnNode,returnNode)

            #if invalid result (noMatchChild or falseResult), there is no bigger path
            if starting_point == None:
                return []
        
        return starting_point.genericDepthFirstTraversal(self._listEveryCompletePath, [])
    
    
    def _listEveryCompletePathAndValue(self, path, node, state, level):
        if node.isValueSet():
            state[path] = node.value
        
        return state
    
    
    def getKeyValue(self, prefix=""):
        """
        This method build a dictionary with every key/value pair stored in this tries
        
        @type prefix: string or None
        @param prefix: the prefix of the key needed, default is an empty string
        @rtype: dictionary
        @return: a dictionary with every existing key/value pair in this tries
        """
        starting_point = self
        if prefix != "":
            starting_point = self.searchNode(prefix,returnNode,returnNode)
            
            #if invalid result (noMatchChild or falseResult), there is no bigger path
            if starting_point == None:
                return {}
        
        return starting_point.genericDepthFirstTraversal(self._listEveryCompletePathAndValue, {})
    
    
#################
    
    def _getMaxChildCount(self, path, node, state, level):
        if len(node.child) > state:
            return len(node.child)
        return state
    
    
    def getMaxChildCount(self):
        """
        this methode compute the bigger number of child of all the current node childs
        
        @rtype: integer
        @return: the bigger number of child existing for every node in the tries
        """
        
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
    
    
    def traversal(self,level = 0):
        """
        This method allows to print a text representation of current tries structure
        
        @type level: integer
        @param level: the limit of level to print, 0 means no limit
        """
        
        return self.genericDepthFirstTraversal(self._traversal, "")
    
    
#################
    
    def _countValue(self, path, node, state, level):
        if node.isValueSet():
            state += 1
        return state
    
    
    def countValue(self):
        """
        This method computes the number of value stored below this node.  If a value is stored on the current node, the value is counted.
        
        @rtype: integer
        @return: the number of value store below and in this node
        """
        
        return self.genericDepthFirstTraversal(self._countValue, 0)
    

    
#################
    
    def getCompleteName(self):
        """
        This method build the complete path of the current node.  Every parent node will be traversed to get their part of the path
        @rtype: string
        @return: the complete path of the current node
        """
        
        node = self
        s = ""

        while node != None:
            s = node.key + s
            node = node.parent

        return s
    
    
############ __ FUNCTION __ #########################################################################################################################################################################
    
    
    def __repr__(self):
        """
        This method return a representation of the current tries node
        
        @rtype: string
        @return: the string representation of the object
        """
        
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
    """
    This provide an advanced result object
    
    @contact: pytries@djoproject.net
    @version: 1.0
    @licence: GPL v3
    """

    def __init__(self):
        """
        this method init a triesSearchResult object
        """
        
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
        """
        This method return True if the searched result is a perfect match, False otherwise
        
        @rtype: boolean
        @return: True if there is a perfect match, False otherwise
        """
        
        return self.perfectMatch
    
    def isPartialMatch(self):
        """
        This method return True if the searched result is a partial match, False otherwise
        
        @rtype: boolean
        @return: True if there is a partial match, False otherwise
        """
        return self.partialMatch
    
    def isMatch(self):
        """
        This method return True if the searched result is a match (perfect or partial), False otherwise
        
        @rtype: boolean
        @return: True if there is a partial or pefect match, False otherwise
        """
        
        return self.perfectMatch or self.partialMatch
    
    def isNoMatchChild(self):
        """
        This method return True if the searched result is a no match child, False otherwise
        
        @rtype: boolean
        @return: True if the searched result is a no match child, False otherwise
        """
        
        return self.noMatchChild
        
    def isFalseResult(self):
        """
        This method return True if the searched result is a false result, False otherwise
        
        @rtype: boolean
        @return: True if the searched result is a false result, False otherwise
        """
        
        return self.falseResult
    
    def getNode(self):
        """
        This method return the found node if there is one, None otherwise
        
        @rtype: tries or None
        @return: the node found if there is a found node
        """
        
        return self.resultNode
        
    def getPreviousNode(self):
        """
        This method return the last explored node in the search process if there is no match, otherwise it returns the parent node of the found node.  In the worst case, the returned value is the root node
        
        @rtype: tries
        @return: the last node explored or the node just before the found node
        """
        
        return self.previousNode
    

