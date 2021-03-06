import configparser
import logging
from multiprocessing.pool import Pool

import common.util.persistence as db
from boris_analysis import cross_validation_configuration, dialogs
from common.analyse import cross_validation as cv
from common.analyse.cross_validation import ResultAssessor
from common.dialog_document.dialog_reader import DialogsReader
from common.util import time_util
from common.util.names import Class
import common.util.persistence as pe

logging.basicConfig(level=logging.WARNING)


# read configuration
config = configparser.ConfigParser()
config.read('local_config.ini')

doc_result_collection = config.get('collections', 'doc_result')

evaluation_id = config.get('cross_validation', 'evaluation_id')
base_directory = config.get('cross_validation', 'source_directory')

id_column_name = 'iteration'


file_turns_succeeded        = base_directory + 'data/turnsSucceeded.csv'
file_turns_failed           = base_directory + 'data/turnsFailed.csv'

file_best_simulation        = base_directory + 'data/bestSimulation.csv'
file_worst_simulation       = base_directory + 'data/worstSimulation.csv'

file_shortest_interaction   = base_directory + 'data/shortest49Interactions.csv'
file_longest_interaction    = base_directory + 'data/longest49Interactions.csv'

file_wa_100                 = base_directory + 'data/WA_60.csv'
file_wa_60                  = base_directory + 'data/WA_100.csv'

file_judged_bad             = base_directory + 'data/badJudged.csv'
file_judged_good            = base_directory + 'data/goodJudged.csv'


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
        

def is_job_already_done(criteria, configuration, no_of_dialogs):
    doc_res = pe.get_collection(pe.Collection.doc_result)
    r = doc_res.find({'evaluation_id': evaluation_id, 'criteria': criteria, 'n_gram_size': configuration.size,
                            'classifier_name': configuration.classifier, 'frequency_threshold': configuration.frequency_threshold,
                            'smoothing_value': configuration.smoothing_value})
    count = r.count()
    is_done = count == no_of_dialogs

    if not is_done and count > 0:
        print('Results not valid for criteria: {0} and configuration: {1}'.format(criteria, configuration))
        assert count == 0  # emergency hold

    return is_done


def validate(positive_data_file, positive_class, negative_data_file, negative_class, id_column_name, criteria):
    
    positive_reader = DialogsReader(positive_data_file)
    positive_dialogs = dialogs.create_dialogs_documents(positive_reader, id_column_name, positive_class)
    print('Dialogs in positive class: {}'.format( len(positive_dialogs) ))
    
    negative_reader = DialogsReader(negative_data_file)
    negative_dialogs = dialogs.create_dialogs_documents(negative_reader, id_column_name, negative_class)
    print('Dialogs in negative class: {}'.format( len(negative_dialogs) ))

    configurations = cross_validation_configuration.getConfigurations()

    jobs = []
    job_number = 0
    for configuration in configurations:
        if is_job_already_done(criteria, configuration, len(positive_dialogs) + len(negative_dialogs)):
            print('Already done! (criteria: {0}, configuration: {1}'.format(criteria, configuration))
        else:
            job_number += 1
            job = Job(configuration, positive_dialogs, negative_dialogs, positive_class,
                      negative_class, criteria, job_number)
            jobs.append(job)

    print('{} to be executed.'.format( len(jobs) ))
    pool = Pool(processes=cross_validation_configuration.validation_processes)
    results = pool.map(run_validation, jobs)
    print('All jobs finished.')
    
    return results
    

def run_validation(job):
    #profiler = cProfile.Profile()
    #profiler.enable()
        
    size                = job.configuration.size
    classifier_name     = job.configuration.classifier
    frequency_threshold  = job.configuration.frequency_threshold
    smoothing_value     = job.configuration.smoothing_value
    criteria            = job.criteria
    
    print('Executing job: {0} for criteria {1} with configuration: {2}'.format(job.job_number, criteria, job.configuration))
        
    cross_validator = cv.CrossValidator(classifier_name, size, frequency_threshold, smoothing_value)
    cross_validator.add_documents(job.negative_dialogs)
    cross_validator.add_documents(job.positive_dialogs)
    
    single_results = cross_validator.run_cross_validation()
    db.write_evaluation_results_to_database(evaluation_id, single_results, size, classifier_name, frequency_threshold,
                                            smoothing_value, criteria)

    assessor = ResultAssessor(single_results, Class.POSITIVE, Class.NEGATIVE,
                              classifier_name, size, frequency_threshold, criteria,
                              smoothing_value)
    
    return assessor.getResultAnalysis()






if __name__ == '__main__':
    
    logging.info("Cross validation starts.")

    success_successful_result   = []
    success_failed_result       = []
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
    
    
    print('Criteria: Turn Success')
    print('Successful?')
    success_successful_result = validate(file_turns_succeeded, Class.POSITIVE, file_turns_failed, Class.NEGATIVE, id_column_name, 'task_successful')
    print('Failed?')
    success_failed_result = validate(file_turns_failed, Class.POSITIVE, file_turns_succeeded, Class.NEGATIVE, id_column_name, 'task_failed')

    print('Criteria: User Judgment')
    print('Good')
    judged_good_result = validate(file_judged_good, Class.POSITIVE, file_judged_bad, Class.NEGATIVE, id_column_name, 'juged_good')
    print('Bad')
    judged_bad_result = validate(file_judged_bad, Class.POSITIVE, file_judged_good, Class.NEGATIVE, id_column_name, 'juged_bad')
        
    print('Criteria: Quality of Simulation')
    print('Best simulation?')
    simulation_best_result = validate(file_best_simulation, Class.POSITIVE, file_worst_simulation, Class.NEGATIVE, id_column_name, 'simulation_quality_best')
    print('Worst simulation?')
    simulation_worst_result = validate(file_worst_simulation, Class.POSITIVE, file_best_simulation, Class.NEGATIVE, id_column_name, 'simulation_quality_worst')
    
    print('Criteria: Length of Interaction')
    print('Short interaction?')
    length_short_result = validate(file_shortest_interaction, Class.POSITIVE, file_longest_interaction, Class.NEGATIVE, id_column_name, 'short_interactions')
    print('Long interaction')
    length_long_result = validate(file_longest_interaction, Class.POSITIVE, file_shortest_interaction, Class.NEGATIVE, id_column_name, 'long_interactions')
    
    print('Criteria: Word Accuracy')
    print('Word accuracy is 100?')
    wa_100_result = validate(file_wa_100, Class.POSITIVE, file_wa_60, Class.NEGATIVE, id_column_name, 'word_accuracy_100')
    print('Word accuracy is 60?')
    wa_60_result = validate(file_wa_60, Class.POSITIVE, file_wa_100, Class.NEGATIVE, id_column_name, 'word_accuracy_60')
    
    print('Criteria: Dialogue Source')
    print('simulated dialogues?')
    sim_result = validate(file_best_simulation, Class.POSITIVE, file_experiment, Class.NEGATIVE, id_column_name, 'simulated')
    print('real dialogues? ')
    real_result = validate(file_experiment, Class.POSITIVE, file_best_simulation, Class.NEGATIVE, id_column_name, 'real')

    print('Criteria: Dialogue Source')
    print('simulated dialogues?')
    sim_result = validate(file_worst_simulation, Class.POSITIVE, file_experiment, Class.NEGATIVE, id_column_name, 'simulated_worst_vs_real')
    print('real dialogues? ')
    real_result = validate(file_experiment, Class.POSITIVE, file_worst_simulation, Class.NEGATIVE, id_column_name, 'real_vs_simulated_worst')
    
        
    results = []
    results.extend(success_successful_result)
    results.extend(success_failed_result)
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

