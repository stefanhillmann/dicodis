import configparser
import logging
import time
import traceback
from multiprocessing import Pool, Manager

from common.util import persistence
from boris_analysis import cross_validation_configuration_manual, dialogs
from boris_analysis.corpora_names import CorporaNames as cns
from common.analyse import cross_validation as cv
from common.util.names import Class

logging.basicConfig(level=logging.WARNING)


# read configuration
config = configparser.ConfigParser()
config.read('local_config.ini')

time_format = "%d-%m-%Y %H:%M:%S"
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


# Job Monitoring
m = Manager()
q = m.Queue()


class Chorpora:
    def __init__(self, positive_data_file, positive_class, negative_data_file, negative_class, id_column_name, criteria):
        self.positive_data_file = positive_data_file
        self.positive_class = positive_class
        self.negative_data_file = negative_data_file
        self.negative_class = negative_class
        self.id_column_name = id_column_name
        self.criteria = criteria


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
    coll_documents = persistence.get_collection(persistence.Collection.doc_result)
    r = coll_documents.find({'evaluation_id': evaluation_id, 'criteria': criteria, 'n_gram_size': configuration.size,
                             'classifier_name': configuration.classifier,
                             'frequency_threshold': configuration.frequency_threshold,
                             'smoothing_value': configuration.smoothing_value})
    count = r.count()
    is_done = count == no_of_dialogs

    if not is_done and count > 0:
        raise ValueError("Results not valid for criteria '{0}' and configuration '{1}'"
                         "Number of dialogues is {2}, but there {3} results in the database".format(criteria,
                                                                                                    configuration,
                                                                                                    no_of_dialogs,
                                                                                                    count))
    return is_done


def validate(corpora_to_be_used):
    configurations = cross_validation_configuration_manual.getConfigurations()
    jobs = []
    job_number = 0

    print("Generate Jobs...")
    for cor in corpora_to_be_used:
    
        # positive_reader = DialogsReader(cor.positive_data_file)
        positive_dialogs = dialogs.create_dialogs_documents_from_database(cor.positive_data_file, cor.positive_class)
        print('Dialogs in positive class: {}'.format( len(positive_dialogs) ))

        # negative_reader = DialogsReader(cor.negative_data_file)
        negative_dialogs = dialogs.create_dialogs_documents_from_database(cor.negative_data_file, cor.negative_class)
        print('Dialogs in negative class: {}'.format( len(negative_dialogs) ))

        for configuration in configurations:
            print('Generate job: criteria: {0}, configuration: {1}'.format(cor.criteria, configuration))
            job_number += 1
            job = Job(configuration, positive_dialogs, negative_dialogs, cor.positive_class,
                      cor.negative_class, cor.criteria, job_number)
            jobs.append(job)

    n_jobs = len(jobs)
    print('{0} Jobs to be executed.'.format( n_jobs ))

    # close exiting database client/connections before forking
    persistence.reset()

    jobs_start = time.time()
    if config.getboolean('cross_validation', 'single_process'):
        for single_job in jobs:
            run_validation(single_job)
    else:
        pool = Pool(processes=cross_validation_configuration_manual.validation_processes)
        result = pool.map_async(run_validation, jobs)

        # monitor loop
        last_size = 1
        while True:
            if result.ready():
                break
            else:
                size = q.qsize()
                if size > last_size:
                    print("{0} of {1} jobs done.".format(size, n_jobs))
                    last_size = size
            time.sleep(1)
    jobs_end = time.time()

    print('All jobs finished.')
    print('Execution time for all jobs: {0} seconds.'.format(jobs_end - jobs_start))

    
def run_validation(job):
    try:
        size                = job.configuration.size
        classifier_name     = job.configuration.classifier
        frequency_threshold  = job.configuration.frequency_threshold
        smoothing_value     = job.configuration.smoothing_value
        criteria            = job.criteria

        if is_job_already_done(job.criteria, job.configuration, len(job.positive_dialogs) + len(job.negative_dialogs)):
            print('Already done! (criteria: {0}, configuration: {1})'.format(criteria, job.configuration))
        else:
            print("{3}: Starting job: {0} for criteria {1} with configuration: {2}"
                  .format(job.job_number, criteria, job.configuration, time.strftime(time_format)))

            cross_validator = cv.CrossValidator(classifier_name, size, frequency_threshold, smoothing_value)
            cross_validator.add_documents(job.negative_dialogs)
            cross_validator.add_documents(job.positive_dialogs)

            single_results = cross_validator.run_cross_validation()
            persistence.write_evaluation_results_to_database(evaluation_id, single_results, size, classifier_name,
                                                             frequency_threshold, smoothing_value, criteria)

        q.put(1)  # put an element on the queue, just to count finished jobs
        print("{0}: Finished job: {1}.".format(time.strftime(time_format), job.job_number))
    except Exception as e:
        print("Caught exception in worker thread (job: {0}):".format(job))

        # This prints the type, value, and stack trace of the
        # current exception being handled.
        traceback.print_exc()

        print()
        raise e

if __name__ == '__main__':
    
    logging.info("Cross validation starts.")

    corpora = [
        Chorpora(cns.SUCCESSFUL, Class.POSITIVE, cns.NOT_SUCCESSFUL, Class.NEGATIVE, id_column_name, 'task success'),
        Chorpora(cns.USER_JUDGMENT_GOOD, Class.POSITIVE, cns.USER_JUDGMENT_BAD, Class.NEGATIVE, id_column_name, 'user judgement'),
        Chorpora(cns.SIMULATION_GOOD, Class.POSITIVE, cns.SIMULATION_BAD, Class.NEGATIVE, id_column_name, 'simulation quality'),
        Chorpora(cns.DIALOGUES_SHORT, Class.POSITIVE, cns.DIALOGUES_LONG, Class.NEGATIVE, id_column_name, 'dialogue length'),
        Chorpora(cns.WORD_ACCURACY_100, Class.POSITIVE, cns.WORD_ACCURACY_60, Class.NEGATIVE, id_column_name, 'word accuracy '),
        Chorpora(cns.SIMULATION_GOOD, Class.POSITIVE, cns.REAL_USER, Class.NEGATIVE, id_column_name, 'sim. good vs real'),
        Chorpora(cns.SIMULATION_BAD, Class.POSITIVE, cns.REAL_USER, Class.NEGATIVE, id_column_name, 'sim. bad vs real')
    ]

    validate(corpora)
