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

def noneFunc(*args):
    return None

def returnNode(Node,prefix, *args):
    return Node

def charInCommons(char1, char2):
    common = 0
    for i in range(0,min(len(char1),len(char2))):
        if char1[i] != char2[i]:
            break
        common += 1
    
    return common
