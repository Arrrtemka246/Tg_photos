import os
from urllib.parse import unquote, urlsplit

import requests


REQUEST_TIMEOUT_SECONDS = 30


def get_proxies(proxy_url):
    if not proxy_url:
        return None

    return {
        'http': proxy_url,
        'https': proxy_url,
    }


def get_response(url, params=None, proxies=None):
    headers = {
        'User-Agent': 'space-telegram/1.0',
    }

    response = requests.get(
        url,
        params=params,
        headers=headers,
        proxies=proxies,
        timeout=REQUEST_TIMEOUT_SECONDS,
    )
    response.raise_for_status()

    return response


def download_image(url, filepath, params=None, proxies=None):
    response = get_response(
        url,
        params=params,
        proxies=proxies,
    )

    with open(filepath, 'wb') as file:
        file.write(response.content)


def get_file_extension(url):
    parsed_url = urlsplit(url)
    decoded_path = unquote(parsed_url.path)
    _, filename = os.path.split(decoded_path)
    _, extension = os.path.splitext(filename)

    return extension