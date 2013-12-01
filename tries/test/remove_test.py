#!/usr/bin/python2.6
# -*- coding: utf-8 -*-

from tries.tries import tries
import unittest
from tries.test.tries_testunit import ElementaryTest

### test 1 : no child, root
class RemoveTest1(unittest.TestCase, ElementaryTest):
    
    ### called before each test
    def setUp(self):
        self.insertedKey = ["bear"] #test every case in the insert function
        self.t           = tries()
        self.keyValue    = {}
        
        for key in self.insertedKey:
            self.keyValue[key] = self.t.insert(key,key).value
        
        #remove the node 
        self.t.remove("bear")
        del self.insertedKey[0]
        del self.keyValue["bear"]

### test 2 : no child, parent is value node or intermediate node with more than 2 child
class RemoveTest2(unittest.TestCase, ElementaryTest):

    ### called before each test
    def setUp(self):

        self.insertedKey = ["bear","bearor"] #test every case in the insert function
        self.t           = tries()
        self.keyValue    = {}

        for key in self.insertedKey:
            self.keyValue[key] = self.t.insert(key,key).value

        #remove the node
        self.t.remove("bearor")
        del self.insertedKey[1]
        del self.keyValue["bearor"]

### test 3 : no child, parent is an intermerdiate note with 2 child, great parent is root
class RemoveTest3(unittest.TestCase, ElementaryTest):

    ### called before each test
    def setUp(self):

        self.insertedKey = ["be","beard","bearor"] #test every case in the insert function
        self.t           = tries()
        self.keyValue    = {}

        for key in self.insertedKey:
            self.keyValue[key] = self.t.insert(key,key).value

        #remove the node 
        self.t.remove("beard")
        del self.insertedKey[1]
        del self.keyValue["beard"]
        
        
### test 4 : no child, parent is an intermerdiate note with 2 child, great parent is not root
class RemoveTest4(unittest.TestCase, ElementaryTest):

    ### called before each test
    def setUp(self):

        self.insertedKey = ["be","bee","beeard","beearor"] #test every case in the insert function
        self.t           = tries()
        self.keyValue    = {}

        for key in self.insertedKey:
            self.keyValue[key] = self.t.insert(key,key).value

        #remove the node 
        self.t.remove("beeard")
        del self.insertedKey[2]
        del self.keyValue["beeard"]


### test 5 : one child
class RemoveTest5(unittest.TestCase, ElementaryTest):

    ### called before each test
    def setUp(self):

        self.insertedKey = ["be","bear","bearor"] #test every case in the insert function
        self.t           = tries()
        self.keyValue    = {}

        for key in self.insertedKey:
            self.keyValue[key] = self.t.insert(key,key).value

        #remove the node 
        self.t.remove("bear")
        del self.insertedKey[1]
        del self.keyValue["bear"]
        
### test 6 : more than one child
class RemoveTest6(unittest.TestCase, ElementaryTest):

    ### called before each test
    def setUp(self):

        self.insertedKey = ["be","bear","bearor", "beard"] #test every case in the insert function
        self.t           = tries()
        self.keyValue    = {}

        for key in self.insertedKey:
            self.keyValue[key] = self.t.insert(key,key).value

        #remove the node 
        self.t.remove("bear")
        del self.insertedKey[1]
        del self.keyValue["bear"]
      
if __name__ == '__main__':
    unittest.main()