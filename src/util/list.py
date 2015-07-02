# -*- coding: utf-8 -*-
"""
Created on Fri Jun  7 11:13:50 2013

@author: Stefan Hillmann (stefan.hillmann@tu-berlin.de)
"""

"""
Collects unique items from a list.

Example: If l = [1 1 2 3 3], then uniqueValues(l) returns [1 2 3].

Parameter:
    l: list of items to searched for unique items.
"""
def uniqueValues(l):
    unique_values_set = set(l)
    unique_values = list(unique_values_set)
    
    return unique_values
    
"""
Collects unique items from a list of items. The unique property of an item
is defined by a particular field of that item

Parameter:
    l: list of items to searched for unique items.
    field_name: name the field in each item, that will be used for the search.
    In other words, an item is compared to the other items by the value of the
    field with the name field_name.
"""
def uniqueObjectValues(l, field_name):
    unique_values = []
    for obj in l:
        value = getattr(obj, field_name)
        if not value in unique_values:
            unique_values.append(value)
            
    return unique_values

"""
Collects all items form a list of items. The items are selected by a particular
value in a particular field.

Parameter:
    l: list of items
    field_name: Name of field inside an item that will be used for the compartment.
    field_value: Each item with value field_value in field field_name is added to
    the result list.
"""    
def filterByFieldValue(l, field_name, field_value):
    filtered_objects = []
    
    for obj in l:
        value = getattr(obj, field_name)
        if value == field_value:
            filtered_objects.append(obj)
            
    return filtered_objects