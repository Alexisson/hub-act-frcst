import os
from pathlib import Path

import requests
from bs4 import BeautifulSoup

from parser.cfg import FOLDER, BASE_URL
from parser.utils import download_xlsx_file

if not Path(FOLDER).is_dir():
    Path(FOLDER).mkdir(parents=True)
if not Path(os.path.join(FOLDER, "credits_msp")).is_dir():
    Path(os.path.join(FOLDER, "credits_msp")).mkdir(parents=True)

files_list = ["All_Borrowers_info", "New_loans_sme_by_activity", "Debt_sme", "A_Debt_corp_by_activity",
              "Debt_sme_by_activity", "Funds_clients"]
files_list_stats = ["statbs", "obs"]
url_for_parse = "https://cbr.ru/statistics/bank_sector/sors/"
url_for_stats = "https://cbr.ru/statistics/bank_sector/review/"


def get_soup(url_for_parse):
    page = requests.get(url_for_parse)
    return BeautifulSoup(page.text, "html.parser")


soup = get_soup(url_for_parse)


# Статистические таблицы к бюллетеню «Кредитование субъектов малого и среднего предпринимательства»
def download_all_credits_msp(soup, base_url, folder):
    file_urls = []
    a_tags = soup.find_all('a', href=lambda href: href and "stat_bulletin_lending" in href and ".xlsx" in href)
    for a in a_tags:
        file_urls.append(a['href'])

    for url in file_urls:
        download_xlsx_file(base_url + url, os.path.join(folder, "credits_msp"))
        print(f"File downloaded:{url.split('/')[-1]}")


# A_Debt_corp_by_activity
def download_files_from_href(soup, base_url, files_list):
    for file in files_list:
        a_tags = soup.find_all('a', href=lambda href: href and (file in href) and (
                "branches" not in href) and ".xlsx" in href)
        for a in a_tags:
            if not Path(os.path.join(FOLDER, file)).is_dir():
                Path(os.path.join(FOLDER, file)).mkdir(parents=True)
            download_xlsx_file(base_url + a['href'], os.path.join(FOLDER, file))
            print(f"File downloaded:{a['href'].split('/')[-1]}")


if __name__ == "__main__":
    download_all_credits_msp(soup, BASE_URL, FOLDER)
    download_files_from_href(soup, BASE_URL, files_list)

    stats_soup = get_soup(url_for_stats)
    download_files_from_href(stats_soup, BASE_URL, files_list_stats)
