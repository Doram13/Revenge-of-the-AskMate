def get_readable_date(list_of_dict):
    for dict in list_of_dict:
        dict['submission_time'] = str(dict['submission_time'])[:16]
    return list_of_dict


def get_first_five_dictionary(list_of_dict):
    return list_of_dict[:5]