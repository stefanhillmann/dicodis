import collections

def sort_by_key(d):
    ordered_dict = collections.OrderedDict( sorted(d.items()) )
    
    return ordered_dict
