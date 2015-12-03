# -*- coding: utf-8 -*-
"""
Created on Thu Jun  6 15:59:01 2013

@author: Stefan Hillmann (stefan.hillmann@tu-berlin.de)
"""

from common.dialog_document.document import Document


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
    if field == "userFields" or field == "sysRep.field":
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
