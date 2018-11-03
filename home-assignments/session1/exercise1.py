import json
from collections import abc
from sys import maxsize
import subprocess

try:
    import yaml
except ModuleNotFoundError:
    subprocess.call(['pip', 'install', 'pyyaml'])
    import yaml


with open("ppl_ages.json", "r") as read_file:
    ppl_ages_dict = json.load(read_file)


sorted_orig_buckets = sorted(ppl_ages_dict["buckets"])


def full_bucket_list_build(sorted_orig_buckets):
    """
    :param sorted_orig_buckets:
    :return: full list of buckets,
             dynamically generated from the buckets list in input json file + considering max age
    """
    tuple_list = []
    for i in range(len(sorted_orig_buckets)):
        if i == 0:
            tuple_list.append((0, sorted_orig_buckets[i]))
            continue
        tuple_list.append((sorted_orig_buckets[i - 1], sorted_orig_buckets[i]))
        if i == len(sorted_orig_buckets) - 1:
            tuple_list.append((sorted_orig_buckets[i], maxsize))
            continue
    return tuple_list


full_bucket_list = full_bucket_list_build(sorted_orig_buckets)


def nested_dict_iter(ppl_ages_dict):
    """
    :param ppl_ages_dict:
    :return: flat dict without nested lists,
             to be able to extract specific oldest age value later on
    """
    for key, value in ppl_ages_dict.items():
        if isinstance(value, abc.Mapping):
            yield from nested_dict_iter(value)
        else:
            yield key, value


flat_ppl_ages_list = list(nested_dict_iter(ppl_ages_dict))  # Define the generator output as list
del flat_ppl_ages_list[len(flat_ppl_ages_list) - 1]  # Remove buckets key as it's not needed in this context


def oldest_person_in_ppl_ages(input_sequence):
    """
    Get oldest person from all people listed in json input file.
    Relevant later on when constructing the yaml output file,
    To show oldest age as part of the key.
    :param input_sequence:
    :return: oldest age in people available in input json file
    """
    if not input_sequence:
        raise ValueError('empty list')
    maximum = input_sequence[0]
    for item in input_sequence:
        # Compare elements by their weight stored
        # in their second element.
        if item[1] > maximum[1]:
            maximum = item
    return maximum


oldest_age = oldest_person_in_ppl_ages(flat_ppl_ages_list)[1]


def dict_iteration(input_dict):
    """
    Go over all people in input json file,
    Divide them to age groups
    :param input_dict:
    :return: Dictionary of group ages and corresponding people in each group
    """
    children = []
    teens = []
    mid_adults = []
    adults = []
    old = []
    for key in input_dict:
        if full_bucket_list[0][0] < input_dict[key] < full_bucket_list[0][1]:
            children.append(key)
        if full_bucket_list[1][0] < input_dict[key] < full_bucket_list[1][1]:
            teens.append(key)
        if full_bucket_list[2][0] < input_dict[key] < full_bucket_list[2][1]:
            mid_adults.append(key)
        if full_bucket_list[3][0] < input_dict[key] < full_bucket_list[3][1]:
            adults.append(key)
        if full_bucket_list[4][0] < input_dict[key] < full_bucket_list[4][1]:
            old.append(key)
    return children, teens, mid_adults, adults, old


ppl_by_ages_groups = (dict_iteration(ppl_ages_dict['ppl_ages']))

output_dict = dict()  # Populate an output dictionary with values from the original dict iteration, with key names
for i in range(5):
    if i < 4:
        output_dict[str(full_bucket_list[i])] = ppl_by_ages_groups[i]
    else:
        last_group_age = str((full_bucket_list[i][0], oldest_age))
        output_dict[last_group_age] = ppl_by_ages_groups[i]

with open('output_data.yml', 'w') as outfile: #
    try:
        yaml.dump(output_dict, outfile, default_flow_style=False)
    except ValueError:
        print('Sorry, can not write to file output_data.yml')
