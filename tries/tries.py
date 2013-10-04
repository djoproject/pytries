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

from exception import triesException
from utils import noneFunc, charInCommons

class tries():
    
    #
    # constructor of the class tries
    #
    # @parameter self, the reference of the class object
    # @parameter key, the part of the key string stored in the current node
    # @parameter parent, the parent node in the tree
    # @parameter value, the value stored in the key
    #
    def __init__(self, key, parent = None, value = None):
        "init the node with a key, and maybe a parent and a value"
        #print "{"+key+"}"
        #if key == None or type(key) != str or len(key) == 0:
        # raise triesException("the inserted key must be a string with a length bigger than zero")
        
        self.key = key
        self.childs = []
        self.value = value
        self.parent = parent

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
        if Node == None or Node.value == None:
		    raise triesException("key not found")

        ### Case 1 : No Child ###
        if len(Node.childs) == 0:
            ## Case 1.1 : root node ##
            if Node.parent == None:
                Node.key = ""
                Node.value = None
            ## Case 1.2 : no root node ##
            else:
                #remove node from parent list
                Node.parent.childs.remove(Node)

                #is the parent a non value intermediate node ?
                parent = Node.parent
                if parent.value == None and len(parent.childs) == 1:
                    
                    #concat the parent key with the node key
                    parent.childs[0].key = parent.key + parent.childs[0].key

                    #the parent is the root ?
                    if parent.parent == None:
                        parent.key = ""
                    else:
                        #add the child in the great parent
                        parent.parent.childs.remove(parent)
                        parent.parent.childs.append(parent.childs[0])
                        parent.childs[0].parent = parent.parent
                        
                        #remove the intermediate parent node
                        del parent
                        
                #remove the node
                del Node
                
        ### Case 2 : One Child ###
            #the current node become its child and its child disappear
            #there is no different process to do if the node is root
        elif len(Node.childs) == 1:
            #concat key
            Node.key    = Node.key + Node.childs[0].key
            
            #merge node
            Node.value  = Node.childs[0].value
            Node.childs = Node.childs[0].childs
            
            #TODO del the child
                
        ### Case 3 : More than one Child ###
        else:
            if Node.parent == None:
                pass  #TODO
            else:
                pass  #TODO
                
        ####################################################################################

        #CAS 1 : suppression de la racine
            #TODO euuhh, pas convaincu de la gestion de ce cas...
                #le root devrait etre recalcule avec la plus grande racine commune
                    #juste s'il y a un unique intermediate child, pas d'autre cas possible normalement
        if Node.parent == None:
            if len(Node.key) > 0:
                for child in Node.childs:
                    child.key = Node.key + child.key
                    
                Node.key = ""
            Node.value = None
        
        #CAS 2 : only one child
        elif len(Node.childs) == 1:
            Node.childs[0].key = Node.key + Node.childs[0].key
            Node.parent.childs.remove(Node)
            Node.parent.childs.append(Node.childs[0])
            Node.childs[0].parent = Node.parent
            del Node
        
        #CAS 3 : more than one child
            #TODO meme chose qu'au CAS 1
        elif len(Node.childs) > 1:
            Node.value = None
        
        #CAS 4 : final node
        else: #len(Node.childs) == 0
            Node.parent.childs.remove(Node)

            #cas limite, a t'on un parent no value Node desequilibre?
            parent = Node.parent
            if parent.value == None and len(parent.childs) == 1:
                
                parent.childs[0].key = parent.key + parent.childs[0].key

                #on est a la racine?
                if parent.parent == None:
                    parent.key = ""
                else:
                    parent.parent.childs.remove(parent)
                    parent.parent.childs.append(parent.childs[0])
                    parent.childs[0].parent = parent.parent
                    del parent
            del Node

    #
    # update the value of the node corresponding to the key
    #
    # @param key, the key of the final node to update
    # @param newValue, the value to change in the node corresponding of the key
    # @return the updated node
    #
    def update(self, key, newValue):
        Node = self.searchNode(key,returnNode)
        if Node != None and Node.value != None:
            Node.value = newValue
            return Node
            
        raise triesException("key not found")

    #
    # insert a new couple key/value in the tree
    #
    # @return the inserted node
    # @exception triesException if insertion failed
    #
    def insert(self,key, value):
        
        if value == None:
            raise triesException("the inserted value can't be none") #TODO why not
        
        #CASE 1 : perfect match
        def exact(Node,key):
            #if the current node is a value node, can't insert the new value
            if Node.value != None : #is it a value node?
                raise triesException("the inserted key already exists")

            return Node
        
        #CASE 2  : partial match, the key is a prefix of another key
        def partial(Node,key,count,totalCount):
            #split the key string of the old node and create a new value node with the existing value
            tempTries = tries(Node.key[count:], Node, Node.value)
            
            #the new node become the parent of the existing childs
            tempTries.childs = Node.childs
            
            #update the parent field of the childs
            for child in tempTries.childs:
                child.parent = tempTries
            
            #TODO to check, is this line usefull ? because the value is already transfered in the constructor method
            tempTries.value = Node.value
            
            #update the key of the old node
            Node.key = Node.key[:count]

            #the only child of the old node is the new node
            Node.childs = [tempTries]
            
            #return the old node, it will contain the new value
            return Node

        #CASE 3 :
        def noMatchChild(Node,key,totalCount):
            newNode = tries(key[totalCount:],Node)
            Node.childs.append(newNode)
            return newNode
        
        #CASE 4 : 
        def false(Node,key,count,totalCount):
            tempTries = tries(Node.key[count:], Node, Node.value)
            tempTries.childs = Node.childs
            
            for child in tempTries.childs:
                child.parent = tempTries
            
            tempTries.value = Node.value
            
            Node.key = Node.key[:count]
            
            #creation du nouveau noeud
            newTries = tries(key[totalCount:], Node)
        
            #mise a jour du noeud courant, non value node, devient un noeud pivot
            Node.childs = [tempTries,newTries]
            Node.value = None
            
            return newTries
        
        #assign the value
        Node = self.searchNode(key,exact,partial,noMatchChild,false)
        Node.value = value
        
        #return the node
        return Node

############ SEARCH FUNCTION #########################################################################################################################################################################

    #
    # @return any kind of node
    #
    def search(self,key):
        return self.searchNode(key,returnNode)
    
    #
    # @return a value node
    #
    def searchUniqueFromPrefix(self,prefix):        
        node = self.searchNode(prefix,returnNode,returnNode)
        if Node.value != None:
            return Node
            
        #if the current node has a None value, it's an intermediate node with at most two children
        raise triesException("the prefix <"+str(prefix)+"> corresponds to multiple node")
    
    #
    #
    #
    def searchNode(self,prefix,exactResult,partialResult = noneFunc, noMatchChild = noneFunc, falseResult = noneFunc):
        #must be a valid string
        if prefix == None or type(prefix) != str or len(prefix) == 0:
            raise triesException("the searched key must be a string with a length bigger than zero")
        
        currentNode = self
        currentPrefix = prefix
        totalCount = 0
        while True:
            #count the common char with this node key
            count = charInCommons(currentNode.key, currentPrefix)
            totalCount += count

            #the current key node is completly used
            if count == len(currentNode.key):
                #valide string and end node
                if len(currentPrefix) == count:
                    return exactResult(currentNode,prefix) # bear = bear #perfect concordance, prefix is equal to a prefix in the tree
                    
                #else count < len(self.key):
                        
                currentPrefix = currentPrefix[len(currentNode.key):]
                for child in currentNode.childs:
                    if child.canPropagate(currentPrefix):
                        currentNode = child
                        break
                else:
                    return noMatchChild(currentNode,prefix,totalCount) # bearor > bear
                
            else: #count < len(self.key)
            
                if len(currentPrefix) == count:
                    return partialResult(currentNode,prefix,count,totalCount) # be < bear #partial match, prefix is a part of a prefix in the tree
                
                return falseResult(currentNode,prefix,count,totalCount) # bee != bear
            
############ MISC FUNCTION #########################################################################################################################################################################
    #
    # @return a dictionnary with all the key/value or None if there is no result
    #
    def getKeyListFromPrefix(self,prefix):
        def exact(Node,prefix):
            return Node.getAllPossibilities()
            
        def partial(Node,prefix,count,totalCount):
            return Node.getAllPossibilities()
            
        return self.searchNode(prefix,exact,partial)

    #
    # build a dictionnary (key + value) with all the combinatories possible from this node
    #
    # TODO convert en non recursif
    #
    # @return a set of string
    #
    def getAllPossibilities(self, dico = {}):
        dico[self.getCompleteName()] = self.value
        
        for child in self.childs:
            child.getAllPossibilities(dico)
            
        return dico
    
    #
    # this methode compute the bigger number of child of all the current node childs
    #
    # @return an integer bigger or equal to zero
    #
    def getMaxChildCount(self):
        m = len(self.childs)
        
        if self.value != None:
            m += 1
        
        for child in self.childs:
            m = max(m,child.getMaxChildCount)

        return m
    
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
    def canPropagate(self, key):
        return len(self.key) == 0 or len(key) == 0 or self.key[0] == key[0]

    #
    # TODO convert en non recursif
    #
    def traversal(self,level = 0):
        s = ""
        for i in range(0,level):
            s+= " "

        s = s+"{"+self.key+"}"
        s += repr(self)

        for child in self.childs :
            s += "\n" + child.traversal(level+1)

        return s
        
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
        
    #
    #
    #
    def isEmptyTries(self):
        return len(self.childs) == 0 and self.value == None
    
    def countValue(self):
        if self.value != None:
            count = 1
        else:
            count = 0
        
        for c in self.childs:
            count += c.countValue()
            
        return count

############ __ FUNCTION __ #########################################################################################################################################################################

    #
    #
    #
    def __repr__(self):
        
        if self.value == None:
            if self.parent == None:
                return "none node (key = \""+self.key+"\", completeName = "+self.getCompleteName()+", parent = None, child count = "+str(len(self.childs))+")"
            else:
                return "none node (key = \""+self.key+"\", completeName = "+self.getCompleteName()+", parent = \""+self.parent.key+"\", child count = "+str(len(self.childs))+")"
        else:
            if self.parent == None:
                return "tries node (key = \""+self.key+"\", value = \""+str(self.value)+"\", completeName = "+self.getCompleteName()+", parent = None, child count = "+str(len(self.childs))+")"
            else:
                return "tries node (key = \""+self.key+"\", value = \""+str(self.value)+"\", completeName = "+self.getCompleteName()+", parent = \""+self.parent.key+"\", child count = "+str(len(self.childs))+")"


    #TODO faire les equals, hash, etc..
        
        
