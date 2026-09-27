import argparse
import os
from datetime import datetime
from pathlib import Path

import requests
from dotenv import load_dotenv

from download_utils import (
    download_image,
    get_proxies,
    get_response,
)


DEFAULT_IMAGES_COUNT = 5
NASA_DEMO_API_KEY = 'DEMO_KEY'


def fetch_nasa_epic(
    api_key,
    images_count,
    proxies=None,
):
    api_url = 'https://api.nasa.gov/EPIC/api/natural'

    params = {
        'api_key': api_key,
    }

    try:
        response = get_response(
            api_url,
            params=params,
            proxies=proxies,
        )
    except requests.RequestException:
        api_key = NASA_DEMO_API_KEY

        params = {
            'api_key': api_key,
        }

        response = get_response(
            api_url,
            params=params,
            proxies=proxies,
        )

    epic_images = response.json()

    images_dir = Path('images')
    images_dir.mkdir(exist_ok=True)

    for image_number, epic_image in enumerate(
        epic_images[:images_count],
        start=1,
    ):
        image_name = epic_image['image']

        image_date = datetime.strptime(
            epic_image['date'],
            '%Y-%m-%d %H:%M:%S',
        )

        image_url = (
            'https://api.nasa.gov/EPIC/archive/natural/'
            f'{image_date:%Y/%m/%d}/png/'
            f'{image_name}.png'
        )

        image_path = (
            images_dir
            / f'epic_{image_number}.png'
        )

        try:
            download_image(
                image_url,
                image_path,
                params={'api_key': api_key},
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
        description='Скачивает фотографии Земли из NASA EPIC.',
    )
    parser.add_argument(
        '--count',
        type=int,
        default=DEFAULT_IMAGES_COUNT,
        help='Количество фотографий для скачивания',
    )

    args = parser.parse_args()

    fetch_nasa_epic(
        nasa_api_key,
        args.count,
        proxies,
    )


if __name__ == '__main__':
    main()