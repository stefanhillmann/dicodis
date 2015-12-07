import configparser
import common.util.persistence as db
import pymongo
from boris_analysis.corpora_names import CorporaNames as CN
import csv

# read configuration
config = configparser.ConfigParser()
config.read('local_config.ini')

host = config.get('database', 'host')
port = config.getint('database', 'port')
database = config.get('dialogue_database', 'dialogues_db_name')
dialogues_collection = config.get('dialogue_database', 'dialogues_collection')

dbm = db.DbManager(host, port, database)
db_connection = dbm.get_connection()
dialogues = db_connection[dialogues_collection]

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

corpora_names = {
    CN.SUCCESSFUL: file_turns_succeeded,
    CN.NOT_SUCCESSFUL: file_turns_failed,
    CN.DIALOGUES_SHORT: file_shortest_interaction,
    CN.DIALOGUES_LONG: file_longest_interaction,
    CN.WORD_ACCURACY_100: file_wa_100,
    CN.WORD_ACCURACY_60: file_wa_60,
    CN.USER_JUDGMENT_GOOD: file_judged_good,
    CN.USER_JUDGMENT_BAD: file_judged_bad,
    CN.SIMULATION_GOOD: file_best_simulation,
    CN.SIMULATION_BAD: file_worst_simulation,
    CN.REAL_USER: file_experiment
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


def replace_dots_in_keys(d):
    for old_key in d.keys():
        new_key = old_key.replace(".", "_")
        d[new_key] = d.pop(old_key)

    return d


def get_task_success(annotation):
    if annotation in SUCCESS:
        return 1
    elif annotation in NO_SUCCESS:
        return 0
    else:
        raise ValueError("Unknown value for task success annotation: '{0}'".format(annotation))


def add_task_success_simulations(corpous_name):
    if CN.SIMULATION_GOOD == corpous_name:
        file_parameters = file_best_simulation_interaction_parameter
    elif CN.SIMULATION_BAD == corpous_name:
        file_parameters = file_worst_simulation_interaction_parameter
    else:
        raise ValueError("Cannot handle corpus '{0}'".format(corpous_name))

    data_file = open(file_parameters, 'r')
    dialogues_parameters = csv.DictReader(data_file)

    for dp in dialogues_parameters:
        iteration = dp["iteration"]  # id of dialogue
        task_success = get_task_success(dp["task success"])  # get dialogue's success

        # set task success for all turns belonging to iteration (a dialogue) in corpora
        dialogues.update_many(
            {"corpus": corpous_name, "iteration": iteration},
            {"$set": {"task_success": task_success}}
        )

    data_file.close()


for corpus in corpora_names.keys():
    print("Corpus: " + corpus)
    print("Read rows")
    rows = get_rows(corpora_names[corpus])

    for r in rows:
        replace_dots_in_keys(r)
        r.update({"corpus": corpus})

    print("Write rows to collection '{0} in database '{1}.".format(database, dialogues_collection))

    dialogues.insert(rows)

# create index for corpora and iteration
dialogues.create_index([("corpus", pymongo.ASCENDING), ("iteration", pymongo.ASCENDING)])
# create index for iteration
dialogues.create_index([("iteration", pymongo.ASCENDING)])

print("Setting task success for simulation good.")
add_task_success_simulations(CN.SIMULATION_GOOD)

print("Setting task success for simulation bad.")
add_task_success_simulations(CN.SIMULATION_BAD)


dbm.close()

