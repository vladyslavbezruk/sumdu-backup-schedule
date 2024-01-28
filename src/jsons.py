import requests
from src import files

requests.packages.urllib3.disable_warnings()
requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS += ':HIGH:!DH:!aNULL'
try:
    requests.packages.urllib3.contrib.pyopenssl.util.ssl_.DEFAULT_CIPHERS += ':HIGH:!DH:!aNULL'
except AttributeError:
    pass

def load_json(path):
    data = files.load_file(path)

    return data

def save_json(data, path):
    files.save_file(data, path)

def download_json(url):
    data = requests.get(url, verify=False)

    return data.json()