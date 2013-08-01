# -*- coding: utf-8 -*-
"""
Created on Fri Jun  7 13:41:29 2013

@author: Stefan Hillmann (stefan.hillmann@tu-berlin.de)
"""

import logging
from run_cross_validation import validate
import analyse.cross_validation as cv
from multiprocessing import Manager


logging.basicConfig(level=logging.INFO)

id_column_name = 'iteration'
positive_class = 'succeeded'
negative_class = 'failed'

file_turns_succeeded        = '/home/stefan/workspace/DialogueClassifying/data/turnsSucceeded.csv'
file_turns_failed           = '/home/stefan/workspace/DialogueClassifying/data/turnsFailed.csv'

file_best_simulation        = '/home/stefan/workspace/DialogueClassifying/data/bestSimulation.csv'
file_worst_simulation       = '/home/stefan/workspace/DialogueClassifying/data/worstSimulation.csv'

file_shortest_interaction   = '/home/stefan/workspace/DialogueClassifying/data/shortest49Interactions.csv'
file_longest_interaction    = '/home/stefan/workspace/DialogueClassifying/data/longest49Interactions.csv'

file_wa_100                 = '/home/stefan/workspace/DialogueClassifying/data/WA_60.csv'
file_wa_60                  = '/home/stefan/workspace/DialogueClassifying/data/WA_100.csv'

#succees_result      = []
#length_result       = []
#simulation_result   = []
#wa_result           = []

if __name__ == '__main__':

    manager = Manager()
    results = manager.list()
    
    print 'Criteria: Turn Success'
    succees_result = validate(file_turns_succeeded, positive_class, file_turns_failed, negative_class, id_column_name, results)
    
    #print 'Criteria: Quality of Simulation'
    #validate(file_best_simulation, positive_class, file_worst_simulation, negative_class, id_column_name)
    
    #print 'Criteria: Length of Interaction'
    #length_result = validate(file_shortest_interaction, positive_class, file_longest_interaction, negative_class, id_column_name)
    
    #print 'Criteria: Word Accuracy'
    #wa_result = validate(file_wa_100, positive_class, file_wa_60, negative_class, id_column_name)
    
    #results = []
    #results.extend(succees_result)
    #results.extend(length_result)
    #results.extend(simulation_result)
    #results.extend(wa_result)
    
    cv.writeResultTableToFile(results, ',', '/home/stefan/test_output_2.csv')
