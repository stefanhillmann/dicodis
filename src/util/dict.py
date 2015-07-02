import collections

def sortByKey(d):
    ordered_dict = collections.OrderedDict( sorted(d.items()) )
    
    return ordered_dict
