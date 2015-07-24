__author__ = 'Stefan Hillmann'

import common.util.names as names

class Document:

    """
    Constructor method
    """
    def __init__(self, true_class, content, dialog_id):

        assert true_class in [names.Class.POSITIVE, names.Class.NEGATIVE]

        self.true_class = true_class
        self.content = content
        self.dialog_id = dialog_id

    def __str__(self):
        return 'Id: ' + self.dialog_id + ', Label: ' + self.true_class + ', Content: ' + ', '.join(self.content)


def sort_documents_by_dialog_id(documents):
    return sorted(documents, key=lambda document: document.dialog_id)