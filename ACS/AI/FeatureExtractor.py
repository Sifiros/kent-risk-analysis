#!/usr/local/bin/python3
import json
import plac

def print_results(nbr_data, feature_dic):
    print('{} datas recoverd on a total of {}'.format(len(feature_dic), nbr_data))

    for entry in feature_dic:
        print('{} : {}'.format(entry, feature_dic[entry]))

def extract_data(feature_name, raw_data):
    key_list = []
    feature_dic = {}

    data = raw_data['data']
    for key in data:
        key_list.append(key)
    for key in key_list:
        unit_data = data[key]
        for unit_key in unit_data:
            if unit_key == feature_name:
                feature_dic[key] = unit_data[unit_key]

    print_results(len(key_list), feature_dic)


def open_json(path):
    with open(path) as json_file:  
        data = json.load(json_file)
        return data

def main(feature_name="", json_path=""):
    data = open_json(json_path)
    extract_data(feature_name, data)

if __name__ == "__main__":
    plac.call(main)
