import csv

def read_file(file_path):
    with open(file_path, 'r') as f:
        reader = csv.DictReader(f)
        list_of_dicts = [dict(line) for line in reader]
    return list_of_dicts

def write_question():
    return None


def read_answers():
    return None

def write_answer():
    return None