"""
Created on Tue Jul 23 09:09:30 2015

@author: Stefan Hillmann (stefan.hillmann@tu-berlin.de)
"""

from common.util import time_util
from common.ngram import model_generator as mg
from common.dialog_document.dialog_reader import DialogsReader
from common.util.names import Class
import common.util.persistence as pe
import dialogs


base_directory = '/home/stefan/git/DialogueClassifying/'

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

criteria_to_file = {
    'turns_succeeded': file_turns_succeeded,
    'turns_failed': file_turns_failed,
    'best_simulation': file_best_simulation,
    'worst_simulation': file_worst_simulation,
    'shortest_interaction': file_shortest_interaction,
    'longest_interaction': file_longest_interaction,
    'wa_100': file_wa_100,
    'wa_60': file_wa_60,
    "judged_bad": file_judged_bad,
    "judged_good": file_judged_good,
    'all_dialogs': file_experiment
}


# Load die dialogues for each criteria and count them
id_column_name = 'iteration'
count = dict()
for criteria in criteria_to_file.keys():
    file_name = criteria_to_file[criteria]
    print 'Processing criteria {0} from file {1}'.format(criteria, file_name)
    dialog_reader = DialogsReader(file_name)

    documents = dialogs.create_dialogs_documents(dialog_reader, id_column_name, Class.POSITIVE)
    count[criteria] = len(documents)

for c in count:
    print 'Dialogues for criteria {0}: {1}'.format( c, count[c] )




