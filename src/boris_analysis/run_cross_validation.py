import logging
from multiprocessing.pool import Pool

import common.dialog_document.dialog_reader
from common.analyse import cross_validation as cv
from common.analyse.cross_validation import ResultAssessor
from boris_analysis import cross_validation_configuration, dialogs
from common.util import time_util
from common.util.names import Class
import pymongo
from pymongo import MongoClient

logging.basicConfig(level=logging.WARNING)

id_column_name = 'iteration'
data_directory = '/home/stefan/git/DialogueClassifying/data/'

file_turns_succeeded        = data_directory + 'turnsSucceeded.csv'
file_turns_failed           = data_directory + 'turnsFailed.csv'

file_best_simulation        = data_directory + 'bestSimulation.csv'
file_worst_simulation       = data_directory + 'worstSimulation.csv'

file_shortest_interaction   = data_directory + 'shortest49Interactions.csv'
file_longest_interaction    = data_directory + 'longest49Interactions.csv'

file_wa_100                 = data_directory + 'WA_60.csv'
file_wa_60                  = data_directory + 'WA_100.csv'


class Job:
    def __init__(self, configuration, positive_dialogs, negative_dialogs, positive_class,
                 negative_class, criteria, job_number):
        self.configuration      = configuration
        self.positive_dialogs   = positive_dialogs
        self.negative_dialogs   = negative_dialogs
        self.positive_class     = positive_class
        self.negative_class     = negative_class
        self.configuration      = configuration
        self.criteria           = criteria
        self.job_number         = job_number
        

def validate(positive_data_file, positive_class, negative_data_file, negative_class, id_column_name, criteria):
    
    positive_reader = common.dialog_document.dialog_reader.DialogsReader(positive_data_file)
    positive_dialogs = dialogs.create_dialogs_documents(positive_reader, id_column_name, positive_class)
    print 'Dialogs in positive class: {}'.format( len(positive_dialogs) )
    
    negative_reader = common.dialog_document.dialog_reader.DialogsReader(negative_data_file)
    negative_dialogs = dialogs.create_dialogs_documents(negative_reader, id_column_name, negative_class)
    print 'Dialogs in negative: {}'.format( len(negative_dialogs) )
    
    configurations = cross_validation_configuration.getConfigurations()
    jobs = []
    job_number = 0
    for configuration in configurations:
        job_number += 1
        job = Job(configuration, positive_dialogs, negative_dialogs, positive_class, 
                  negative_class, criteria, job_number)
        jobs.append(job)
        
        
    print '{} to be executed.'.format( len(jobs) )
    pool = Pool(processes = cross_validation_configuration.validation_processes)
    results = pool.map(run_validation, jobs)
    print 'All jobs finished.'
    
    return results
    

def run_validation(job):
    print 'Executing job: {}'.format(job.job_number)
    #profiler = cProfile.Profile()
    #profiler.enable()
    
    
    
    size                = job.configuration.size
    classifier_name     = job.configuration.classifier
    frequency_treshold  = job.configuration.frequency_threshold
    criteria            = job.criteria
        
    cross_validator = cv.CrossValidator(classifier_name, size, frequency_treshold)
    cross_validator.add_documents(job.negative_dialogs)
    cross_validator.add_documents(job.positive_dialogs)
    
    single_results = cross_validator.run_cross_validation()


    assessor = ResultAssessor(single_results, Class.POSITIVE, Class.NEGATIVE, classifier_name, size,
                              frequency_treshold, criteria)

    
    #profiler.disable()
    #s = io.StringIO()
    #ps = pstats.Stats(profiler, stream = s)
    #ps.dump_stats("classifier.profile")
        
    #return assessor
    return assessor.getResultAnalysis()

    
    
if __name__ == '__main__':
    
    logging.info("Cross validation starts.")

    succees_successful_result   = []
    succees_failed_result       = []
    simulation_best_result      = []
    simulation_worst_result     = []
    length_short_result         = []
    length_long_result          = []
    wa_100_result               = []
    wa_60_result                = []
    
    
    print 'Criteria: Turn Success'
    print 'Successful?'
    succees_successful_result = validate(file_turns_succeeded, Class.POSITIVE, file_turns_failed,
                                         Class.NEGATIVE, id_column_name, 'task_successful')
    print 'Failed?'
    succees_failed_result = validate(file_turns_failed, Class.POSITIVE, file_turns_succeeded,
                                     Class.NEGATIVE, id_column_name, 'task_failed')
    
    #print 'Criteria: Quality of Simulation'
    #print 'Best simulation?'
    #simulation_best_result = validate(file_best_simulation, positive_class, file_worst_simulation, negative_class, id_column_name, 'simulation_quality_best')
    #print 'Worst simulation?'
    #simulation_worst_result = validate(file_worst_simulation, positive_class, file_best_simulation, negative_class, id_column_name, 'simulation_quality_worst')
    
    #print 'Criteria: Length of Interaction'
    #print 'Short interaction?'
    #length_short_result = validate(file_shortest_interaction, positive_class, file_longest_interaction, negative_class, id_column_name, 'short_interactions')
    #print 'Long interaction'
    #length_long_result = validate(file_longest_interaction, positive_class, file_shortest_interaction, negative_class, id_column_name, 'long_interactions')
    
    #print 'Criteria: Word Accuracy'
    #print 'Word accuracy is 100?'
    #wa_100_result = validate(file_wa_100, positive_class, file_wa_60, negative_class, id_column_name, 'word_accuracy_100')
    #print 'Word accuracy is 60?'
    #wa_60_result = validate(file_wa_60, positive_class, file_wa_100, negative_class, id_column_name, 'word_accuracy_60')
    
        
    results = []
    results.extend(succees_successful_result)
    results.extend(succees_failed_result)
    results.extend(length_short_result)
    results.extend(length_long_result)
    results.extend(simulation_best_result)
    results.extend(simulation_worst_result)
    results.extend(wa_100_result)
    results.extend(wa_60_result)
    
    result_file_name = time_util.human_readable_timestamp() + '__results.csv'
    cv.write_result_table_to_file(results, ';', '../results/' + result_file_name)
    
