import collections
import operator


def sort_by_key(d):
    ordered_dict = collections.OrderedDict( sorted(d.items()) )
    
    return ordered_dict


def sort_by_value(d):
    sorted_d = sorted(d.items(), key=operator.itemgetter(1))

    return sorted_d
