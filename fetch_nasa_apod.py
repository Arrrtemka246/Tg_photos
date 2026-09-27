import argparse
import os
from pathlib import Path

import requests
from dotenv import load_dotenv

from download_utils import (
    download_image,
    get_file_extension,
    get_proxies,
    get_response,
)


DEFAULT_IMAGES_COUNT = 30
FALLBACK_IMAGES_COUNT = 5
NASA_DEMO_API_KEY = 'DEMO_KEY'


def fetch_nasa_apod(
    api_key,
    images_count,
    proxies=None,
):
    api_url = 'https://api.nasa.gov/planetary/apod'

    params = {
        'api_key': api_key,
        'count': images_count,
    }

    try:
        response = get_response(
            api_url,
            params=params,
            proxies=proxies,
        )
    except requests.RequestException:
        params = {
            'api_key': NASA_DEMO_API_KEY,
            'count': FALLBACK_IMAGES_COUNT,
        }

        response = get_response(
            api_url,
            params=params,
            proxies=proxies,
        )

    apod_images = response.json()

    image_urls = [
        apod_image['url']
        for apod_image in apod_images
        if apod_image.get('media_type') == 'image'
    ]

    images_dir = Path('images')
    images_dir.mkdir(exist_ok=True)

    for image_number, image_url in enumerate(
        image_urls,
        start=1,
    ):
        extension = get_file_extension(image_url)

        image_path = (
            images_dir
            / f'nasa_apod_{image_number}{extension}'
        )

        try:
            download_image(
                image_url,
                image_path,
                proxies=proxies,
            )
        except requests.RequestException:
            continue


def main():
    load_dotenv()

    nasa_api_key = os.environ['NASA_API_KEY']
    proxy_url = os.getenv('PROXY_URL')
    proxies = get_proxies(proxy_url)

    parser = argparse.ArgumentParser(
        description='Скачивает фотографии NASA APOD.',
    )
    parser.add_argument(
        '--count',
        type=int,
        default=DEFAULT_IMAGES_COUNT,
        help='Количество фотографий для скачивания',
    )

    args = parser.parse_args()

    fetch_nasa_apod(
        nasa_api_key,
        args.count,
        proxies,
    )


if __name__ == '__main__':
    main()