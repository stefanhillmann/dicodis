# -*- coding: utf-8 -*-
"""
Created on Thu Jun  6 15:59:01 2013

@author: Stefan Hillmann (stefan.hillmann@tu-berlin.de)
"""

from common.dialog_document.document import Document
from boris_analysis.corpora_names import CorpusData
import common.util.persistence as persistence
import configparser
import pymongo
import boris_analysis.corpora_names as cd
import math


# read configuration
config = configparser.ConfigParser()
config.read('local_config.ini')


def create_dialog_document(id_column, system_parameter, user_parameter, dialog, dialog_label):
    content = []
        
    for exchange in dialog:
        """System Turn"""
        system_values = create_sub_document(exchange, system_parameter)
        if system_values:
            content.append( ",".join(system_values) )
        
        """User Turn"""
        user_values = create_sub_document(exchange, user_parameter)
        if user_values:
            content.append( ",".join(user_values) )
    
    dialog_id = dialog[0][id_column]
    document = Document(dialog_label, content, dialog_id)
    
    return document


def create_dialogs_documents(dialog_reader, id_column_name, class_name):
    iterations_ids = dialog_reader.get_unique_values(id_column_name)
    
    dialogs_documents = []
    for iteration_id in iterations_ids:
        dialog_rows = dialog_reader.get_rows(id_column_name, iteration_id)
        dialog_document = create_dialog_document(id_column_name,
        ['sysSA', 'sysRep.field'], ['userSA', 'userFields'], dialog_rows, class_name)
        
        dialogs_documents.append(dialog_document)
        
    return dialogs_documents


def create_dialogs_documents_from_database(corpus, class_name):
    if type(corpus) != cd.CorpusData:
        raise TypeError("Parameter 'corpus' has to be 'CorpusData' but is '{0}'.".format(type(corpus)))

    iteration_ids = []
    _corpus = None
    if corpus.is_static:
        iteration_ids = get_iteration_ids_for_static_corpus(corpus)
        _corpus = corpus
    else:
        iteration_ids = get_iteration_ids_for_dynamic_corpus(corpus)
        _corpus = get_static_base_corpus_for_dynamic_corpus(corpus)

    return create_documents_by_iteration_ids(class_name, _corpus, iteration_ids)


def get_iteration_ids_for_static_corpus(corpus):
    dialogues = persistence.get_collection(persistence.Collection.dialogues)
    iteration_ids = dialogues.find({"corpus": corpus.name}).distinct("iteration")
    return iteration_ids


def get_static_base_corpus_for_dynamic_corpus(dynamic_corpus):

    if dynamic_corpus == cd.GOOD_SIMULATION_SUB_SET_SAMPLE\
            or dynamic_corpus == cd.GOOD_SIMULATION_NOT_SUCCESSFUL\
            or dynamic_corpus == cd.GOOD_SIMULATION_SUCCESSFUL:
        return cd.SIMULATION_GOOD
    else:
        raise ValueError("Cannot determine base corpus for dynamic corpus '{0}'".format(str(dynamic_corpus)))


def get_iteration_ids_for_dynamic_corpus(corpus_data):
    if corpus_data == cd.GOOD_SIMULATION_SUCCESSFUL:
        return get_iteration_ids_for_good_simulation_by_success(1)
    elif corpus_data == cd.GOOD_SIMULATION_NOT_SUCCESSFUL:
        return get_iteration_ids_for_good_simulation_by_success(0)
    elif corpus_data == cd.GOOD_SIMULATION_SUB_SET_SAMPLE:
        return get_iteration_ids_for_good_simulation_sub_set_sample(corpus_data)
    else:
        raise ValueError("No implementation to get iterations for dynamic corpus {0}".format(str(corpus_data)))


def get_iteration_ids_for_good_simulation_by_success(success):
    dialogues = persistence.get_collection(persistence.Collection.dialogues)
    query = {"corpus": cd.SIMULATION_GOOD.name, "task_success": success}
    iteration_ids = dialogues.find(query).distinct("iteration")
    return iteration_ids


def get_iteration_ids_for_good_simulation_sub_set_sample(corpus_data):
    """
    Samples a number iteration ids (dialogues) from the good simulation.
     The ratio between successful/not successful dialogues will be preserved.
    :param corpus_data:
    :return:
    """
    # get number of successful/not successful dialogues
    count_success = len(get_iteration_ids_for_good_simulation_by_success(1))
    count_no_success = len(get_iteration_ids_for_good_simulation_by_success(0))

    # the total number of sampled dialogues is equal to the number of unsuccessful dialogues
    goal_count = count_no_success
    k = (count_success + count_no_success) / goal_count  # get ratio between origin count and goal count
    sample_count_success = math.floor(count_success / k)
    sample_count_no_success = math.floor(count_no_success / k)

    # In order to get always the same dialogues, but have some kind of random, we get the ordered list of
    # iteration_ids and select the first n ones. This works under the assumption that the dialogues are independent
    # from the order in which they were generated.
    success_iterations = get_iteration_ids_for_good_simulation_by_success(1)
    success_iterations.sort()
    no_success_iterations = get_iteration_ids_for_good_simulation_by_success(0)
    no_success_iterations.sort()

    iterations = list()
    iterations.extend(success_iterations[0:sample_count_success])  # sampled iterations of successful dialogues
    iterations.extend(no_success_iterations[0:sample_count_no_success])  # sampled iterations of unsuccessful dialogues

    return iterations


def create_documents_by_iteration_ids(class_name, corpus, iteration_ids):

    if type(corpus) != CorpusData:
        raise TypeError("Parameter 'corpus' has to be from type CorpusData but is '{0}'".format(type(corpus)))

    if len(iteration_ids) == 0:
        raise ValueError("Cannot create documents for zero (0) iteration_ids, as the resulting dialogue document will"
                         " have no content (turns).")

    dialogs_documents = []
    dialogues = persistence.get_collection(persistence.Collection.dialogues)
    for iteration in iteration_ids:
        # get dialogue turns in correct order
        dialogue_rows = dialogues.find({"corpus": corpus.name, "iteration": iteration}) \
            .sort('exchange_no', pymongo.ASCENDING)

        if dialogue_rows.count() == 0:
            raise ValueError("Found no content (turns) for dialogue with iteration = {0} in corpus {1}."
                             .format(iteration, str(corpus)))

        dialog_document = create_dialog_document_from_database(dialogue_rows, class_name, corpus, iteration)

        dialogs_documents.append(dialog_document)
    return dialogs_documents


def create_dialog_document_from_database(dialogue, dialogue_label, corpus, iteration):
    content = []

    for exchange in dialogue:
        """System Turn"""
        system_values = create_sub_document(exchange, ['sysSA', 'sysRep_field'])
        if system_values:
            content.append( ",".join(system_values) )

        """User Turn"""
        user_values = create_sub_document(exchange, ['userSA', 'userFields'])
        if user_values:
            content.append( ",".join(user_values) )

    dialog_id = str(iteration) + "_" + corpus.name.replace(" ", "_")
    document = Document(dialogue_label, content, dialog_id)

    return document


def create_sub_document(exchange, parameter):
    values = []

    sa = parameter[0]
    field = parameter[1]

    is_explicit_confirmation_request_by_system = False

    if sa == "userSA" or sa == "sysSA":
        value = normalize_speech_act_name(exchange[sa])
        if value != "":
            values.append(value)
            if sa == "sysSA" and value == "explicit_confirmation":
                is_explicit_confirmation_request_by_system = True
    else:
        raise ValueError("Unknown parameter!", sa)

    # process field value
    if field == "userFields" or field == "sysRep_field":
        value = normalize_field_values(exchange[field])
        if value != "":
            values.append(value)
        elif is_explicit_confirmation_request_by_system:
            # repair wrong annotation in data and set field to "logical" if we handle a explicit confirmation request
            # from the system
            values.append("logical")
    else:
        raise ValueError("Unknown parameter!", field)

    return values


def normalize_speech_act_name(name):

    _name = name.strip()  # strip leading/tailing spaces
    _name = _name.lower()  # lower case

    norm_names = {
        "accept": "accept",
        "accept provide": "accept_provide",
        "affirm": "accept",
        "affirm provide": "affirm_provide",
        "negate": "negate",
        "neglect": "negate",
        "provide": "provide",
        "hangup": "hang_up",
        "inform": "provide",
        "bye": "bye",
        "explconfirm": "explicit_confirmation",
        "explicitconfirmation": "explicit_confirmation",
        "indicatevalues": "indicate_values",
        "indicatevalue": "indicate_values",
        "indicatevalues1": "indicate_values_1",
        "indicatevaluesone": "indicate_values_1",
        "indicatevalues2": "indicate_values_2",
        "informandoffermore": "inform_and_offer_more",
        "offermodification": "offer_modification",
        "offerrefinement": "offer_refinement",
        "repetitionrequest": "repetition_request",
        "request": "request",
        "empty": "",
        "": ""
    }

    norm_name = norm_names[_name]

    return norm_name


def normalize_field_values(values):
    _values = values.strip()  # strip leading/tailing spaces
    _values = _values.lower()  # lower case

    # split and sort values
    split_values = _values.split()
    sort_values = sorted(split_values)

    sorted_values = " ".join(sort_values)  # create new string with values separated by a space character

    return sorted_values
