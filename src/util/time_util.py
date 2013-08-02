import time

"""
Creates and returns a human readable timestamp string.
Example: At 2 August, 2013 at 04:23:05 pm the method returns:
2013_08_02__16_23_05 
"""
def humanReadableTimestamp():
    
    return time.strftime('%Y_%m_%d__%H_%M_%S')

