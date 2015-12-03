import csv
import ConfigParser
import common.util.persistence as db

# read configuration
config = ConfigParser.ConfigParser()
config.read('local_config.ini')

host = config.get('database', 'host')
port = config.getint('database', 'port')
database = config.get('dialogue_database', 'dialogues_db_name')
dialogues_collection = config.get('dialogue_database', 'dialogues_collection')

dbm = db.DbManager(host, port, database)

evaluation_id = config.get('cross_validation', 'evaluation_id')
base_directory = config.get('cross_validation', 'source_directory')

file_best_simulation        = base_directory + 'data/bestSimulation.csv'
file_worst_simulation       = base_directory + 'data/worstSimulation.csv'
file_experiment             = base_directory + 'data/annotatedData_corrected.csv'

corpora_names = {
    'simulation good': file_best_simulation,
    'simulation bad': file_worst_simulation,
    'real user': file_experiment
}


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


for corpora in corpora_names.keys():
    print "Corpora: " + corpora
    print "Read rows"
    rows = get_rows(corpora_names[corpora])

    rows = map(lambda r: replace_dots_in_keys(r), rows)
    map(lambda r: r.update({"corpora": corpora}), rows)  # add corpora name to each row

    print "Write rows to collection '{0} in database '{1}.".format(database, dialogues_collection)
    db = dbm.get_connection()
    dialogues = db[dialogues_collection]
    dialogues.insert(rows)
    dbm.close()

