# -*- coding: utf-8 -*-
"""
Created on Thu Jun  6 13:30:45 2013

@author: Stefan Hillmann (stefan.hillmann@tu-berlin.de)
"""

def naiveSmoothing(frequencies, v=0.5):
    """
    Adds a specific value v to each frequency.
    
    
    Parameters:
        frequencies -- a vector of n-gram frequencies
        
        v -- value to be added to each frequence (default 0.5)
        
    Example:
        >>> freq = [1, 1, 2]
        >>> res = naiveSmoothing(freq, 0.5)
        >>> print res
        [ 1.5  1.5  2.5]
        
    """
    return frequencies + v