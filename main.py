import os
import requests
import argparse

from dotenv import load_dotenv
from urllib.parse import urlparse


def shorten_link(token, url):
    headers = {"Authorization": token}
    shorten_url = "https://api-ssl.bitly.com/v4/shorten"
    body = {"long_url": url}
    response = requests.post(shorten_url, headers=headers, json=body)
    response.raise_for_status()
    return response.json()["id"]


def count_clicks(token, link):
    headers = {"Authorization": token}
    url = f"https://api-ssl.bitly.com/v4/bitlinks/{link}/clicks/summary"
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()["total_clicks"]


def is_bitlink(bitlink, token):
    url = f"https://api-ssl.bitly.com/v4/bitlinks/{bitlink}"
    headers = {"Authorization": token}
    response = requests.get(url, headers=headers)
    return response.ok


if __name__ == "__main__":
    load_dotenv()
    token = os.environ["BITLY_TOKEN"]

    parser = argparse.ArgumentParser(description="Данная программа сокращает "
        "ссылки через интерфейс bit.ly и там же можно смотреть статистику кликов")
    parser.add_argument("link", help="Указанная пользователем ссылка")
    args = parser.parse_args()
    user_input = args.link

    parsed = urlparse(user_input)
    link = f"{parsed.netloc}{parsed.path}"

    try:
        if is_bitlink(link, token):
            clicks_count = count_clicks(token, link)
            print(f"По вашей ссылке прошли {clicks_count} раз(а)")
        else:
            bitlink = shorten_link(token, user_input)
            print(f"Битлинк {bitlink}")
    except requests.exceptions.HTTPError:
        print("Проверьте вводимый адрес")
    except requests.exceptions.ConnectionError:
        print("Нет соединения")
