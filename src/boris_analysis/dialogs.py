# -*- coding: utf-8 -*-
"""
Created on Thu Jun  6 15:59:01 2013

@author: Stefan Hillmann (stefan.hillmann@tu-berlin.de)
"""

from common.dialog_document.document import Document
import common.util.persistence as persistence
import configparser


# read configuration
config = configparser.ConfigParser()
config.read('local_config.ini')

if config.has_section('database') and config.has_section('dialogue_database'):
    host = config.get('database', 'host')
    port = config.getint('database', 'port')
    dialogue_db = config.get('dialogue_database', 'dialogues_db_name')
    dialogue_collection = config.get('dialogue_database', 'dialogues_collection')
else:
    print("Could not load configuration.")

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
    conn = persistence.DbManager(host, port, dialogue_db).get_connection()
    dialogues = conn[dialogue_collection]
    iteration_ids = dialogues.find({"corpus": corpus}).distinct("iteration")

    dialogs_documents = []
    for iteration in iteration_ids:
        dialogue_rows = dialogues.find({"corpus": corpus, "iteration": iteration})

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

    dialog_id = iteration + "_" + corpus.replace(" ", "_")
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
