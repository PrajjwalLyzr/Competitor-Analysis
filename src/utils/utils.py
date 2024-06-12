import os
import shutil
import re
import json


def create_folder(folder_name, report_folder_name, agent_file):
    if os.path.exists(folder_name):
        shutil.rmtree(folder_name)

    os.makedirs(folder_name)

    if os.path.exists(report_folder_name):
        shutil.rmtree(report_folder_name)

    os.makedirs(report_folder_name)

    if os.path.exists(agent_file):
        os.remove(agent_file)


def remove_www(url):
    if url.startswith("www."):
        return url[4:]
    return url


def format_key(title):
    # Remove non-alphanumeric characters and convert to lowercase
    key = re.sub(r"\W+", "_", title).lower()
    return key


def convert_field_name_advanced(field_name):
    field_name = field_name.lower()
    field_name = re.sub(r"[^a-z0-9]", "_", field_name)
    field_name = re.sub(r"__+", "_", field_name)
    field_name = field_name.strip("_")
    return field_name



def parse_json_output(json_object):
    try:
        data_dict = json.loads(json_object.replace("'", '"'))
        return data_dict
    except json.JSONDecodeError:
        return {}