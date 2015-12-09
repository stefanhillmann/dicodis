import pandas as pd
import collections
import random
import time
import common.util.dict as du

print("Create keys")
keys = list(range(10000))
random.shuffle(keys)

print("Create values")
values = list(range(10000))
random.shuffle(values)

print("Create dict")
d = dict(zip(keys, values))
print("Create ordered dict")
od = collections.OrderedDict(d)
print('Create Series')
s = pd.Series(d)

trials = 100

print("Sort ordered dict {0} times".format(trials))
# sort ordered dict
start_od = time.time()
for n in range(1, trials):
    od_sorted = du.sort_by_value(od)
end_od = time.time()

# sort series
print("Sort series {0} times".format(trials))
start_s = time.time()
for n in range(1, trials):
    s_sorted = s.sort_values(inplace=False)
end_s = time.time()

print('Time for OrderedDict: {0} seconds'.format(end_od - start_od))
print('Time for Series: {0} seconds'.format(end_s - start_s))
