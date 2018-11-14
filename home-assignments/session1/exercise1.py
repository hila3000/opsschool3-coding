#!/usr/bin/python3

import json
import operator
from json.decoder import JSONDecodeError
from sys import argv
import subprocess

try:
    import yaml
except ModuleNotFoundError:
    subprocess.call(['pip', 'install', 'pyyaml'])
    import yaml


def get_dict_from_json(json_file):
    try:
        with open(json_file, "r") as read_file:
            ppl_ages_dict = json.load(read_file)
            return ppl_ages_dict
    except JSONDecodeError:
        print("The input file isn't parsed correctly")
    except FileNotFoundError:
        print("File", argv[1], "Not Found")


def full_bucket_list_build(sorted_orig_buckets, oldest_age):
    ages_ranges = []
    for i in range(len(sorted_orig_buckets)):
        if i == 0:
            ages_ranges.append((0, sorted_orig_buckets[i]))
            continue
        ages_ranges.append((sorted_orig_buckets[i - 1], sorted_orig_buckets[i]))
        if i == len(sorted_orig_buckets) - 1:
            ages_ranges.append((sorted_orig_buckets[i], oldest_age))
            continue
    return ages_ranges


def group_people_by_ages(input_dict, full_bucket_list):
    """
    Go over all people in input json file,
    Divide them to age groups
    :return: Dictionary of ppl by ages groups
    """
    ages_groups = {}
    for bucket in full_bucket_list:
        bucket_key = "%d-%d" % (bucket[0], bucket[1])
        ages_groups[bucket_key] = []
        for key in input_dict:
            if bucket[0] <= input_dict[key] < bucket[1]:
                ages_groups[bucket_key].append(key)
                continue
    return ages_groups


def write_to_file(ppl_by_ages_groups):
    with open('output_data.yml', 'w') as outfile:  # Dumps the output dictionary to yaml file
        try:
            yaml.dump(ppl_by_ages_groups, outfile, default_flow_style=False)
        except ValueError:
            print('Sorry, can not write to file output_data.yml')


def main():
    if len(argv) == 2:  # Script will run only if one input file was provided
        ppl_ages_dict = get_dict_from_json(argv[1])
        if not ppl_ages_dict:
            return -1
        sorted_orig_buckets = sorted(ppl_ages_dict["buckets"])
        ppl_dict = ppl_ages_dict["ppl_ages"]
        oldest_age = max(ppl_dict.items(), key=operator.itemgetter(1))[1]
        full_bucket_list = full_bucket_list_build(sorted_orig_buckets, oldest_age)
        ppl_by_ages_groups = (group_people_by_ages(ppl_ages_dict["ppl_ages"], full_bucket_list))
        write_to_file(ppl_by_ages_groups)
    else:
        print('USAGE: python exercise1.py <JSON_PATH>')


if __name__ == "__main__":
    main()