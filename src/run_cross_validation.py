import dialogs
import analyse.cross_validation as cv
from analyse.cross_validation import ResultAssessor
import cross_validation_configuration
import logging
from multiprocessing.pool import Pool
from util import time_util
import cProfile, pstats, io

logging.basicConfig(level=logging.INFO)

id_column_name = 'iteration'
positive_class = 'succeeded'
negative_class = 'failed'

file_turns_succeeded        = '../data/turnsSucceeded.csv'
file_turns_failed           = '../data/turnsFailed.csv'

file_best_simulation        = '../data/bestSimulation.csv'
file_worst_simulation       = '../data/worstSimulation.csv'

file_shortest_interaction   = '../data/shortest49Interactions.csv'
file_longest_interaction    = '../data/longest49Interactions.csv'

file_wa_100                 = '../data/WA_60.csv'
file_wa_60                  = '../data/WA_100.csv'


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
    
    positive_reader = dialogs.DialogsReader(positive_data_file)
    positive_dialogs = dialogs.createDialogsDocuments(positive_reader, id_column_name, positive_class)
    print 'Dialogs in positive class: {}'.format( len(positive_dialogs) )
    
    negative_reader = dialogs.DialogsReader(negative_data_file)
    negative_dialogs = dialogs.createDialogsDocuments(negative_reader, id_column_name, negative_class)
    print 'Dialogs in negative: {}'.format( len(negative_dialogs) )
    
    configurations = cross_validation_configuration.getConfigurations();
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
    cross_validator.addDocuments(job.negative_dialogs)
    cross_validator.addDocuments(job.positive_dialogs)
    
    single_results = cross_validator.runCrossValidation()
    
    assessor = ResultAssessor(single_results, positive_class, negative_class, classifier_name, size,  frequency_treshold, criteria)
    
    #profiler.disable()
    #s = io.StringIO()
    #ps = pstats.Stats(profiler, stream = s)
    #ps.dump_stats("classifier.profile")
        
    #return assessor
    return assessor.getResultAnalysis()

    
    
if __name__ == '__main__':

    succees_result      = []
    simulation_result   = []
    length_result       = []
    wa_result           = []
    
    
    print 'Criteria: Turn Success'
    succees_result = validate(file_turns_succeeded, positive_class, file_turns_failed, negative_class, id_column_name, 'task_success')
    
    #print 'Criteria: Quality of Simulation'
    #simulation_result = validate(file_best_simulation, positive_class, file_worst_simulation, negative_class, id_column_name, 'simulation_quality')
    
    #print 'Criteria: Length of Interaction'
    #length_result = validate(file_shortest_interaction, positive_class, file_longest_interaction, negative_class, id_column_name, 'length_of_interaction')
    
    #print 'Criteria: Word Accuracy'
    #wa_result = validate(file_wa_100, positive_class, file_wa_60, negative_class, id_column_name, 'word_accuracy')
    
        
    results = []
    results.extend(succees_result)
    results.extend(length_result)
    results.extend(simulation_result)
    results.extend(wa_result)
    
    result_file_name = time_util.humanReadableTimestamp() + '__results.csv'
    cv.writeResultTableToFile(results, ',', '../results/' + result_file_name)
    