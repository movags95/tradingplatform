import os, csv
def companies_csv_to_symbols_list():
    symbols = []
    filenames = os.listdir('data/companies')
    for file in filenames:
        with open(f'data/companies/{file}') as f:
            for row in csv.reader(f):
                symbols.append(row[0])
    
    return symbols
