# -*- coding: utf-8 -*-
"""
Created on Tue Jun 18 15:15:47 2013

@author: Stefan Hillmann (stefan.hillmann@tu-berlin.de)
"""

class Foo:
    
    def __init__(self, name):
        self.name = name
        
        
foo = Foo('name_foo')
bar = Foo('name_bar')

val = getattr(foo, 'name')
print val