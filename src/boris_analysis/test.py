import boris_analysis.dialogs as d


docs = d.create_dialogs_documents_from_database("word accuracy 60", "positive")

print(docs[0])
