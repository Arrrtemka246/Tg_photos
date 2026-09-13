import os
from urllib.parse import unquote, urlsplit

import requests


def get_response(url, params=None):
    headers = {
        'User-Agent': 'space-telegram/1.0',
    }

    response = requests.get(
        url,
        params=params,
        headers=headers,
        timeout=30,
    )
    response.raise_for_status()
    return response


def download_image(url, filepath, params=None):
    response = get_response(url, params=params)

    with open(filepath, 'wb') as file:
        file.write(response.content)


def get_file_extension(url):
    parsed_url = urlsplit(url)
    decoded_path = unquote(parsed_url.path)
    _, filename = os.path.split(decoded_path)
    _, extension = os.path.splitext(filename)

    return extension