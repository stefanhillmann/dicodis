from common.ngram import export

model = {'a': 4, 'b': 5, 'c': 3}

export.to_csv(model, '/home/stefan/temp/csv_export.csv')

