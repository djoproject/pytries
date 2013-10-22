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
    #-change variable name
        #-commandStrings
        #-command
        #-...
        
    #comment everything
    #allow to insert command with other caractere than space between them

from tries import *
from exception import triesException

class multiLevelTries():
    
    def __init__(self):
        "this method init the multiLevelTries with an empty tries root"
        self.levelOneTries = tries()
        self.spaceCaracter = " "
    
    def searchNode(self):
        pass #TODO faire une recherche similaire a celle du tries qui pourra etre reutilisee dans toutes les fonctions du multiTries
    
    #
    # @param stringList : array string
    # @param value : object to store
    #    
    def addEntry(self,stringList, value):
        "this method allows to insert a new string list associated with a value"
        #check stringList
        if stringList == None or type(stringList) != list or len(stringList) < 0:
            raise triesException("need string token to insert a new value, no token found")
        
        #the value node is always stored in the root of a tries
        stringList.append("")
        
        #TODO can store a tries here ?
            #yeah why not, it will create a new functionnal branch in the multiTries
                #except if some information are added later with the node
                    #a value must always be stored at a root node with empty key
        
        #SEARCH a similar String list
        tries_tmp = self.levelOneTries
        for i in range(0,len(stringList)): #for each token of the string list to insert
            tmp = tries_tmp.search(stringList[i])
            
            #is there a value node here ?
            if tmp != None and tmp.isValueSet(): 
                #the value of the node is another tries ?
                if isinstance(tmp.value,tries):  
                    tries_tmp = tmp.value 
                    continue #continue exploring
                    
                else: #there is a value in this node and this is not a tries, can't create a new branch here
                          #this case include the case where the complete inserted path exists
                          #normaly at this point, the inserted path must be the same as the value here
                    
                    #detect inconsistance in the tree
                    if tmp.key != "":
                        pass #TODO
                    
                    #build the path to insert
                    pathToInsert = ""
                    for k in range(0,len(stringList)):
                        pathToInsert += stringList[k]+self.spaceCaracter
                    
                    #raise the exception signaling the existing path
                    raise triesException("The path <"+pathToInsert+"> already exists in the multi tries")
            break
        
        stringList = stringList[:-1]
        #INSERT the new value, stringList[i:] does not exist yet in the tree
        for j in range(i,len(stringList)-1):
            #build the tries structure
            tries_tmp = tries_tmp.insert(stringList[j],tries()).value
        else:
            # ???
            j = len(stringList)-2
        
        #the value is inserted in the root node of an empty tree
        tries_tmp.insert(stringList[j+1],tries()).setValue(value)
    
    #
    #
    #
    def removeEntry(self,commandStrings):
        
        #check commandStrings
        if commandStrings == None or type(commandStrings) != list or len(commandStrings) < 0:
            raise triesException("need string token to find a value, no token found")
        
        #creer un tableau avec tous les tries composant la commande
        tries_tmp = self.levelOneTries
        tries_table = [self.levelOneTries]
        for i in range(0,len(commandStrings)):
            tmp = tries_tmp.searchUniqueFromPrefix(commandStrings[i])
            
            if tmp != None and tmp.value != None:
                if isinstance(tmp.value,tries) :
                    tries_tmp = tmp.value
                    tries_table.append(tries_tmp)
                    continue
                else:
                    if i == len(commandStrings)-1:
                        break
                    
                    raise triesException("the command string doesn't exist")
            else:
                raise triesException("unknown chain in level "+str(i)+" <"+commandStrings[i]+">")
        
        #on retire les elements du bas vers le haut
        for i in range(0,len(tries_table)):
            indice = len(tries_table)-1-i
            
            #le tries ne contient qu'un element?
            if tries_table[indice].countValue() == 1:
                if indice == 0:
                    tries_table[indice].remove(commandStrings[indice])
                else:
                    continue #on propage la suppression au noeud parent
            else:
                #supprimer la cle du tries
                tries_table[indice].remove(commandStrings[indice])
                break
    
    def updateEntry(self, commandStrings, newValue):
        node, args = self.searchEntry(commandStrings)
        node.value = newValue
    
    #
    # 
    # TODO difference avec searchEntryFromMultiplePrefix?
    #
    #def searchEntry(self, commandStrings):
    #    return self.searchEntry(commandStrings)
    
    #
    #
    #
    def searchEntryFromMultiplePrefix(self,commandStrings,returnTriesValue = False):
        #check commandStrings
        if commandStrings == None or type(commandStrings) != list or len(commandStrings) < 0:
            raise triesException("need string token to find a value, no token found")
        
        #search string
        tries_tmp = self.levelOneTries
        for i in range(0,len(commandStrings)):
            tmp = tries_tmp.searchUniqueFromPrefix(commandStrings[i])
            
            if tmp != None and tmp.value != None:
                if isinstance(tmp.value,tries) :
                    tries_tmp = tmp.value
                    continue
                else:
                    return tmp,commandStrings[(i+1):]
            else:
                raise triesException("unknown chain in level "+str(i)+" <"+commandStrings[i]+">")
        
        if not returnTriesValue:
            raise triesException("uncomplete command")
            
        return tries_tmp,[]
    
    def __repr__(self):
        return repr(self.levelOneTries)
        
#
#  ???
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
    
        
















