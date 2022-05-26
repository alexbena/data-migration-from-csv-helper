import csv
import os
from os import listdir
from os.path import isfile, join

def load_folder_csv_files(folder):
    result_dictionary = {}
    folder_files = [f for f in listdir(folder) if isfile(join(folder, f))]
    for file in folder_files:
        result_dictionary[file] = []
        with open(folder + '/' + file, mode='r') as infile:
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
    csv_dictionaries = load_folder_csv_files('csv-files')
    updated_dictionary = replace_foreign_key_with_attribute(csv_dictionaries['inmuebles_inmueble.csv'], csv_dictionaries['clientes_cliente.csv'], 'propietario_id', 'nombre')
    generate_csv(updated_dictionary)

if __name__ == "__main__":
    main()