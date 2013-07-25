# -*- coding: utf-8 -*-
"""
Created on Thu Jun  6 15:59:01 2013

@author: Stefan Hillmann (stefan.hillmann@tu-berlin.de)
"""

import csv
import util.list as lu


def createDialogDocument(id_column, system_parameter, user_parameter, dialog, dialogLabel):
    content = []
        
    for exchange in dialog:
        """System Turn"""
        system_values = createSubDocument(exchange, system_parameter)
        if system_values:
            content.append( ",".join(system_values) )
        
        """User Turn"""
        user_values = createSubDocument(exchange, user_parameter)  
        if user_values:
            content.append( ",".join(user_values) )
    
    dialog_id = dialog[0][id_column]
    document = Document(dialogLabel, content, dialog_id)
    
    return document


def createSubDocument(exchange, parameter):
    values = [] 
    for p in parameter:
        value = exchange[p]
        if value:
            value = value.strip() # strip leading/tailing spaces
            value = value.lower() # lower case
            values.append(value)
       
    # add values if there one or several
    if values:
        return values
    else:
        return ''
        
def sortDocumentsByDialogId(documents):
    return sorted(documents, key=lambda document: document.dialog_id)


class DialogsReader:
    
    """
    Constructor method.
    """    
    def __init__(self, filename):
        dataFile = open(filename, 'r')
        dataReader = csv.DictReader(dataFile, delimiter=';')
        
        self.data = []
        for row in dataReader:
            self.data.append(row)
            
        dataFile.close()
        
            
    def getRows(self, column, value):
        
        filtered_rows = []
        for row in self.data:
            if row[column] == value:
                filtered_rows.append(row)
        return filtered_rows
        
    def getValues(self, column_name):
        values = []
        for row in self.data:
            values.append(row[column_name])
            
        return values
        
    def getUniqueValues(self, column_name):
        values = self.getValues(column_name)
        return lu.uniqueValues(values)

class Document:

    """
    Constructor method
    """
    def __init__(self, label, content, dialog_id):
        self.label = label
        self.content = content
        self.dialog_id = dialog_id
        
    def __str__(self):
        return 'Id: ' + self.dialog_id + ', Label: ' + self.label + ', Content: '+ ', '.join(self.content)
        