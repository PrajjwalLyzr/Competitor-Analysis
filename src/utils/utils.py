import os
import shutil
import re



def create_folder(folder_name, report_folder_name, agent_file ):
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