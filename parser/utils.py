import os

import requests


def download_xlsx_file(url, folder):
    resp = requests.get(url)
    output = open(os.path.join(folder, url.split("/")[-1]), 'wb')
    output.write(resp.content)
    output.close()