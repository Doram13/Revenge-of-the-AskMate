import csv

def read_file(file_path):
    with open(file_path, 'r') as csv_file:
        reader = csv.DictReader(csv_file)
        list_of_dicts = [dict(line) for line in reader]
    return list_of_dicts

def append_to_csvfile(file_path, dict_to_append, data_header):
    with open(file_path, 'a') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=data_header)
        writer.writerow(dict_to_append)

def update_file(file_path, updated_dict, data_header):
    with open(file_path, 'w') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=data_header)
        writer.writeheader()
        writer.writerows(updated_dict)


def read_answers():
    return None

def write_answer():
    return None