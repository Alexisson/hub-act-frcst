import os

import requests


def download_xlsx_file(url, folder):
    resp = requests.get(url)
    file_path = os.path.join(folder, url.split("/")[-1])
    if not os.path.isfile(file_path):
        with open(file_path, 'wb') as output:
            output.write(resp.content)