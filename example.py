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

#TODO
    #le .value est contre intuitif
        #soit on renvoit un tries object, soit la value
            #si on renvoit la value, comment peut on savoir si la recherche a echoue ?
                #avec une exception ?
                    #pas vraiment un cas d'erreur
                #multiResult ?
                    
    #example du mltries aussi

from tries import tries

t = tries()
t.insert("beor",42)
t.insert("toto",69)

print t.search("t").value #will print 69
print t.search("to").value #will print 69
print t.search("tot").value #will print 69
print t.search("toto").value #will print 69

t.insert("beer",55)

try:
    print t.search("b").value
except Exception as e:
    print e #will print ambiguity, can be beer or bear
    
t.insert("be",78)

print t.search("b").value #will print 78

#but bear and beer are still accessible
print t.search("bee").value #will print 55
print t.search("beer").value #will print 55
print t.search("beo").value #will print 42
print t.search("beor").value #will print 42

if t.search("blabla") == None:
    print "blabla does not exist in the tree"

