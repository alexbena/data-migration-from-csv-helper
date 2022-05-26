import csv
import os
import sys
from os import listdir
from os.path import isfile, join

def load_folder_csv_files(files):
    result_dictionary = {}
    for file in files:
        result_dictionary[file] = []
        with open('csv-files' + '/' + file, mode='r') as infile:
            for line in csv.DictReader(infile):
                result_dictionary[file].append(line)
        
    return result_dictionary

def id_search(id, data, primary_key='id'):
    for object in data:
        if object[primary_key] == id:    
            return object
    return None

def generate_csv(data):
    if not os.path.exists('output'):
        os.makedirs('output')
    
    data_columns = []
    for key in data[0].keys():
        data_columns.append(key)
    
    with open('output/output.csv', 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames = data_columns)
        writer.writeheader()
        writer.writerows(data)

def replace_foreign_key_with_attribute(data, foreign_data, foreign_key, attribute):
    for object in data:
        related_object = id_search(object[foreign_key], foreign_data)
        if related_object:
            object[foreign_key] = related_object[attribute]
    return data
    
def main():
    if len(sys.argv) != 5:
        print("Wrong arguments")
        return
    csv_name = sys.argv[1]
    related_csv = sys.argv[2] 
    csv_column = sys.argv[3] 
    related_csv_column = sys.argv[4] 
     
    csv_dictionaries = load_folder_csv_files([csv_name, related_csv])
    updated_dictionary = replace_foreign_key_with_attribute(csv_dictionaries[csv_name], csv_dictionaries[related_csv], csv_column, related_csv_column)
    generate_csv(updated_dictionary)

if __name__ == "__main__":
    main()