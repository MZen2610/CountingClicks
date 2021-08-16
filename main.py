import requests
from urllib.parse import urlparse
import os


def shorten_link(token, url):
    headers = {"Authorization": token}
    shorten_url = "https://api-ssl.bitly.com/v4/shorten"
    body = {"long_url": url}
    response_post = requests.post(shorten_url, headers=headers, json=body)
    response_post.raise_for_status()
    return response_post.json()["id"]

def count_clicks(token, link):
    headers = {"Authorization": token}
    url = f"https://api-ssl.bitly.com/v4/bitlinks/{link}/clicks/summary"
    response_get = requests.get(url, headers=headers)
    response_get.raise_for_status()
    return response_get.json()["total_clicks"]

def is_bitlink(bitlink):
  parsed = urlparse(str(bitlink))
  link = parsed.netloc + parsed.path

  token = os.environ['token'] 
  headers = {"Authorization": token}
  url = f"https://api-ssl.bitly.com/v4/bitlinks/{link}"          
  
  response_get = requests.get(url, headers=headers)
  if response_get.ok:
    try:
      clicks_count = count_clicks(token, response_get.json()["id"])
      print(f'По вашей ссылке прошли {clicks_count} раз(а)')
    except requests.exceptions.HTTPError:
      print("Проверьте вводимый адрес")
    except requests.exceptions.ConnectionError:
      print("Нет соединения")
  else:
    try:
      bitlink = shorten_link(token, bitlink)
      print(f'Битлинк {bitlink}')
    except requests.exceptions.HTTPError:
      print("Проверьте вводимый адрес")
    except requests.exceptions.ConnectionError:
      print("Нет соединения")


user_input = input("Введите ссылку ")

is_bitlink(user_input)