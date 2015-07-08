__author__ = 'Stefan Hillmann'


class Document:

    """
    Constructor method
    """
    def __init__(self, label, content, dialog_id):
        self.label = label
        self.content = content
        self.dialog_id = dialog_id

    def __str__(self):
        return 'Id: ' + self.dialog_id + ', Label: ' + self.label + ', Content: ' + ', '.join(self.content)


def sort_documents_by_dialog_id(documents):
    return sorted(documents, key=lambda document: document.dialog_id)