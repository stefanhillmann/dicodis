# -*- coding: utf-8 -*-
"""
Created on Thu Jun  6 13:55:08 2013

@author: Stefan Hillmann (stefan.hillmann@tu-berlin.de)
"""

import numpy as np

def compute_probabilities(frequencies):
    probabilities = np.array([])
    n = sum(frequencies)
    
    for f in frequencies:
        probabilities = np.append(probabilities, float(f)/n)
        
    return probabilities
