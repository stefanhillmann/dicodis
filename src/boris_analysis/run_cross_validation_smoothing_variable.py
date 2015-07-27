import logging
from multiprocessing.pool import Pool

from common.analyse import cross_validation as cv
from common.analyse.cross_validation import ResultAssessor
from boris_analysis import cross_validation_configuration, dialogs
from common.util import time_util
from common.dialog_document.dialog_reader import DialogsReader
from common.util.persistence import EvaluationResult
import common.util.persistence as db
from common.util.names import Class

logging.basicConfig(level=logging.WARNING)

# evaluation_id = time_util.shorter_human_readable_timestamp()
evaluation_id = '2015_07_24__15_55'
host = 'localhost'
port = 27017
database = 'classification_cross_validation'

id_column_name = 'iteration'

base_directory = '/home/stefan/git/DialogueClassifying/'

file_turns_succeeded        = base_directory + 'data/turnsSucceeded.csv'
file_turns_failed           = base_directory + 'data/turnsFailed.csv'

file_best_simulation        = base_directory + 'data/bestSimulation.csv'
file_worst_simulation       = base_directory + 'data/worstSimulation.csv'

file_shortest_interaction   = base_directory + 'data/shortest49Interactions.csv'
file_longest_interaction    = base_directory + 'data/longest49Interactions.csv'

file_wa_100                 = base_directory + 'data/WA_60.csv'
file_wa_60                  = base_directory + 'data/WA_100.csv'

file_experiment             = base_directory + 'data/annotatedData_corrected.csv'


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
    
    positive_reader = DialogsReader(positive_data_file)
    positive_dialogs = dialogs.create_dialogs_documents(positive_reader, id_column_name, positive_class)
    print 'Dialogs in positive class: {}'.format( len(positive_dialogs) )
    
    negative_reader = DialogsReader(negative_data_file)
    negative_dialogs = dialogs.create_dialogs_documents(negative_reader, id_column_name, negative_class)
    print 'Dialogs in negative class: {}'.format( len(negative_dialogs) )
    
    configurations = cross_validation_configuration.getConfigurations()
    jobs = []
    job_number = 0
    for configuration in configurations:
        job_number += 1
        job = Job(configuration, positive_dialogs, negative_dialogs, positive_class, 
                  negative_class, criteria, job_number)
        jobs.append(job)
        
    print '{} to be executed.'.format( len(jobs) )
    pool = Pool(processes=cross_validation_configuration.validation_processes)
    results = pool.map(run_validation, jobs)
    print 'All jobs finished.'
    
    return results
    

def run_validation(job):
    #profiler = cProfile.Profile()
    #profiler.enable()
        
    size                = job.configuration.size
    classifier_name     = job.configuration.classifier
    frequency_threshold  = job.configuration.frequency_threshold
    smoothing_value     = job.configuration.smoothing_value
    criteria            = job.criteria
    
    print 'Executing job: {} with configuration: {}'.format(job.job_number, job.configuration)
        
    cross_validator = cv.CrossValidator(classifier_name, size, frequency_threshold, smoothing_value)
    cross_validator.add_documents(job.negative_dialogs)
    cross_validator.add_documents(job.positive_dialogs)
    
    single_results = cross_validator.run_cross_validation()
    db.write_results_to_database(single_results, size, classifier_name, frequency_threshold, smoothing_value, criteria)

    assessor = ResultAssessor(single_results, Class.POSITIVE, Class.NEGATIVE,
                              classifier_name, size, frequency_threshold, criteria,
                              smoothing_value)
    
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
    judged_good_result          = []
    judged_bad_result           = []
    sim_result                  = []
    real_result                 = []
    
    
    #print 'Criteria: Turn Success'
    #print 'Successful?'
    #succees_successful_result = validate(file_turns_succeeded, Class.POSITIVE, file_turns_failed, Class.NEGATIVE, id_column_name, 'task_successful')
    #print 'Failed?'
    #succees_failed_result = validate(file_turns_failed, Class.POSITIVE, file_turns_succeeded, Class.NEGATIVE, id_column_name, 'task_failed')

    #print 'Criteria: User Judgment'
    #print 'Good'
    #judged_good_result = validate(file_judged_good, positive_class, file_judged_bad, negative_class, id_column_name, 'juged_good')
    #print 'Bad' 
    #judged_bad_result = validate(file_judged_bad, positive_class, file_judged_good, negative_class, id_column_name, 'juged_bad')
        
    #print 'Criteria: Quality of Simulation'
    #print 'Best simulation?'
    #simulation_best_result = validate(file_best_simulation, positive_class, file_worst_simulation, negative_class, id_column_name, 'simulation_quality_best')
    #print 'Worst simulation?'
    #simulation_worst_result = validate(file_worst_simulation, positive_class, file_best_simulation, negative_class, id_column_name, 'simulation_quality_worst')
    
    #print 'Criteria: Length of Interaction'
    #print 'Short interaction?'
    #length_short_result = validate(file_shortest_interaction, Class.POSITIVE, file_longest_interaction, Class.NEGATIVE, id_column_name, 'short_interactions')
    #print 'Long interaction'
    #length_long_result = validate(file_longest_interaction, positive_class, file_shortest_interaction, negative_class, id_column_name, 'long_interactions')
    
    #print 'Criteria: Word Accuracy'
    #print 'Word accuracy is 100?'
    #wa_100_result = validate(file_wa_100, Class.POSITIVE, file_wa_60, Class.NEGATIVE, id_column_name, 'word_accuracy_100')
    print 'Word accuracy is 60?'
    wa_60_result = validate(file_wa_60, Class.POSITIVE, file_wa_100, Class.NEGATIVE, id_column_name, 'word_accuracy_60')
    
    # print 'Criteria: Dialogue Source'
    # print 'simulated dialogues?'
    # sim_result = validate(file_best_simulation, positive_class, file_experiment, negative_class, id_column_name, 'simulated')
    # print 'real dialogues? '
    # real_result = validate(file_experiment, positive_class, file_best_simulation, negative_class, id_column_name, 'real')
    
        
    results = []
    results.extend(succees_successful_result)
    results.extend(succees_failed_result)
    results.extend(judged_good_result)
    results.extend(judged_bad_result)
    results.extend(length_short_result)
    results.extend(length_long_result)
    results.extend(simulation_best_result)
    results.extend(simulation_worst_result)
    results.extend(wa_100_result)
    results.extend(wa_60_result)
    results.extend(sim_result)
    results.extend(real_result)
    
    
    
    result_file_name = time_util.human_readable_timestamp() + '__results.csv'
    cv.write_result_table_to_file(results, ';', base_directory + 'results/' + result_file_name)

