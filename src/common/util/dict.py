import collections
import operator


def sort_by_key(d):
    ordered_dict = collections.OrderedDict( sorted(list(d.items())) )
    
    return ordered_dict


def sort_by_value(d):
    sorted_d = sorted(d.items(), key=operator.itemgetter(1))

    return sorted_d


def convert_string_to_integer(d, fields):
    for field in fields:
        d[field] = int(d[field])


def replace_dots_in_keys(d):
    for old_key in d.keys():
        new_key = old_key.replace(".", "_")
        d[new_key] = d.pop(old_key)
