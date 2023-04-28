
import time

from ..file_utilities import get_path
from typing import List, Union
import requests
from bs4 import BeautifulSoup

import random


PATH = get_path()


def get_any_proxy() -> dict:
    """
    Pega um proxy aleatório da lista de proxies

    Arguments:
        None

    Returns:
        proxy: dict"""
    with open(f"{PATH}/../../data/proxies_list.txt", "r") as f:
        proxy_list = f.read().split("\n")
    proxy = random.choice(proxy_list)
    return proxy


def send_query(query: str) -> List[Union[str, int]]:
    """
    Envia uma query para o google e retorna a resposta contida no "Você quis dizer:"

    Arguments:
        query: str

    Returns:
        query: str
        status_code: int"""

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
            # logger.warning("Time to wait:")
            # print(html.headers)
            break
        else:
            # logger.warning("Error: ", html.status_code)
            # print(html)
            break

    return query, html.status_code


def fix_spelling_in_answer(answer: str) -> str:
    """
    Corrige a ortografia de uma resposta de forma recursiva se necessário

    Arguments:
        answer: str

    Returns:
        new_answer: str
        status_code: int"""
    new_answer, status_code = send_query(answer)
    if status_code == 429:
        time_to_sleep = random.randint(25, 35)
        time.sleep(time_to_sleep)
        new_answer, status_code = send_query(answer)

    return new_answer, status_code
