import os, csv
def companies_csv_to_dict():
    companies_dict = {}
    symbols_list = []
    filenames = os.listdir('data/companies')
    for file in filenames:
        with open(f'data/companies/{file}') as f:
            for row in csv.reader(f):
                companies_dict[row[0]] = {'company':row[1]}
                symbols_list.append(row[0])
    companies_dict.pop('Symbol')
    return companies_dict, symbols_list[1:]
