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
    for p in parameter:
        value = exchange[p]
        if value:
            value = value.strip()  # strip leading/tailing spaces
            value = value.lower()  # lower case
            values.append(value)
       
    # add values if there one or several
    if values:
        return values
    else:
        return ''

