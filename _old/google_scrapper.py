
import time

import pandas as pd
import requests
from bs4 import BeautifulSoup

import random


PATH = "."


def get_any_proxy() -> dict:
    with open(f"{PATH}/proxies_list.txt", "r") as f:
        proxy_list = f.read().split("\n")
    proxy = random.choice(proxy_list)
    return proxy


def send_query(query: str):
    while True:
        url = "https://www.google.com.br/search?q={}".format(query)

        headers = {'User-agent': 'your bot 0.1',
                   'proxy': get_any_proxy()}

        html = requests.get(url, headers=headers)
        html = requests.get(url)

        if html.status_code == 200:  # Everything is OK
            soup = BeautifulSoup(html.text, 'lxml')

            a = soup.find("a", {"id": "scl"})

            if a == None:
                break

            query = a.text

        elif html.status_code == 429:  # Too many requests
            # print("Time to wait:")
            # print(html.headers)
            break
        else:
            # print("Error: ", html.status_code)
            # print(html)
            break

    return query, html.status_code


def fix_spelling_in_answer(answer):
    new_answer, status_code = send_query(answer)
    if status_code == 429:
        time_to_sleep = random.randint(25, 35)
        time.sleep(time_to_sleep)
        new_answer, status_code = send_query(answer)

    return new_answer, status_code
