import csv

def toCSV(ngram_model, file_path):
    with open(file_path, 'w') as f:
        csv_writer = csv.writer(f, delimiter=';')
               
        # writer header
        csv_writer.writerow( ['n-gram', 'frequency'] )
        
        #append data (the n-gram-model) to csv file
        # writerows of DictWriter needs a _list_ of dictionaries
        for k in ngram_model:
            row = [k, str(ngram_model[k])]
            csv_writer.writerow(row)
        