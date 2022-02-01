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

def append_value_to_key(dict_obj, key, value):
    # Check if key exist in dict or not
    if key in dict_obj:
        # Key exist in dict.
        # Check if type of value of key is list or not
        if not isinstance(dict_obj[key], list):
            # If type is not list then make it list
            dict_obj[key] = [dict_obj[key]]
        # Append the value in list
        dict_obj[key].append(value)
    else:
        # As key is not in dict,
        # so, add key-value pair
        dict_obj[key] = [value]

