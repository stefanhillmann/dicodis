import configparser
import csv

import pymongo

import boris_analysis.corpora_names as cd
from common.util import persistence
from common.util import dict as du

# read configuration
config = configparser.ConfigParser()
config.read('local_config.ini')

coll_dialogues = persistence.get_collection(persistence.Collection.dialogues)

evaluation_id = config.get('cross_validation', 'evaluation_id')
base_directory = config.get('cross_validation', 'source_directory')


file_turns_succeeded        = base_directory + 'data/turnsSucceeded.csv'
file_turns_failed           = base_directory + 'data/turnsFailed.csv'
file_shortest_interaction   = base_directory + 'data/shortest49Interactions.csv'
file_longest_interaction    = base_directory + 'data/longest49Interactions.csv'
file_wa_100                 = base_directory + 'data/WA_60.csv'
file_wa_60                  = base_directory + 'data/WA_100.csv'
file_judged_bad             = base_directory + 'data/badJudged.csv'
file_judged_good            = base_directory + 'data/goodJudged.csv'
file_best_simulation        = base_directory + 'data/bestSimulation.csv'
file_worst_simulation       = base_directory + 'data/worstSimulation.csv'
file_experiment             = base_directory + 'data/annotatedData_corrected.csv'

file_best_simulation_interaction_parameter = base_directory  + "data/bestSimulationInteractionParameter.csv"
file_worst_simulation_interaction_parameter = base_directory  + "data/worstSimulationInteractionParameter.csv"

corpora_files = {
    cd.SUCCESSFUL: file_turns_succeeded,
    cd.NOT_SUCCESSFUL: file_turns_failed,
    cd.DIALOGUES_SHORT: file_shortest_interaction,
    cd.DIALOGUES_LONG: file_longest_interaction,
    cd.WORD_ACCURACY_100: file_wa_100,
    cd.WORD_ACCURACY_60: file_wa_60,
    cd.USER_JUDGMENT_GOOD: file_judged_good,
    cd.USER_JUDGMENT_BAD: file_judged_bad,
    cd.SIMULATION_GOOD: file_best_simulation,
    cd.SIMULATION_BAD: file_worst_simulation,
    cd.REAL_USER: file_experiment
}

SUCCESS = ["S", "SCs", "SN", "SCu", "SCuCs"]
NO_SUCCESS = ["FS", "FU"]


def get_rows(file_path):
    data_file = open(file_path, 'r')
    data_reader = csv.DictReader(data_file, delimiter=';')

    read_rows = []
    for row in data_reader:
        read_rows.append(row)

    data_file.close()

    return read_rows


def get_task_success(annotation):
    if annotation in SUCCESS:
        return 1
    elif annotation in NO_SUCCESS:
        return 0
    else:
        raise ValueError("Unknown value for task success annotation: '{0}'".format(annotation))


def add_task_success_simulations(corpus):
    if cd.SIMULATION_GOOD == corpus:
        file_parameters = file_best_simulation_interaction_parameter
    elif cd.SIMULATION_BAD == corpus:
        file_parameters = file_worst_simulation_interaction_parameter
    else:
        raise ValueError("Cannot handle corpus '{0}'".format(corpus))

    data_file = open(file_parameters, 'r')
    dialogues_parameters = csv.DictReader(data_file)

    for dp in dialogues_parameters:
        iteration = int(dp["iteration"])  # id of dialogue
        task_success = get_task_success(dp["task success"])  # get dialogue's success

        # set task success for all turns belonging to iteration (a dialogue) in corpora
        update_result = coll_dialogues.update_many(
            {"corpus": corpus.name, "iteration": iteration},
            {"$set": {"task_success": task_success}}
        )

        if update_result.modified_count == 0:
            raise ValueError("No dialogue was updated for corpus {0} and iteration {1} with task success {2}"
                             .format(corpus, iteration, task_success))

    data_file.close()


for corpus in corpora_files.keys():
    print("Corpus: " + str(corpus))
    print("Read rows")
    rows = get_rows(corpora_files[corpus])

    for r in rows:
        du.replace_dots_in_keys(r)
        du.convert_string_to_integer(r, ["iteration", "exchange_no"])
        r.update({"corpus": corpus.name})

    print("Write rows to collection '{0}'".format(coll_dialogues))

    coll_dialogues.insert(rows)

# create index for corpora and iteration
coll_dialogues.create_index([("corpus", pymongo.ASCENDING), ("iteration", pymongo.ASCENDING)])
# create index for iteration
coll_dialogues.create_index([("iteration", pymongo.ASCENDING)])

print("Setting task success for simulation good.")
add_task_success_simulations(cd.SIMULATION_GOOD)

print("Setting task success for simulation bad.")
add_task_success_simulations(cd.SIMULATION_BAD)


persistence.close()

