import argparse
import os
from datetime import datetime
from pathlib import Path

import requests
from dotenv import load_dotenv

from download_utils import download_image, get_response


def fetch_nasa_epic(api_key, images_count):
    api_url = 'https://api.nasa.gov/EPIC/api/natural'

    params = {
        'api_key': api_key,
    }

    try:
        response = get_response(api_url, params=params)
    except requests.RequestException:
        api_key = 'DEMO_KEY'

        params = {
            'api_key': api_key,
        }

        response = get_response(api_url, params=params)

    epic_images = response.json()

    images_dir = Path('images')
    images_dir.mkdir(exist_ok=True)

    downloaded_images = 0

    for epic_image in epic_images:
        if downloaded_images >= images_count:
            break

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
            / f'epic_{downloaded_images + 1}.png'
        )

        try:
            download_image(
                image_url,
                image_path,
                params={'api_key': api_key},
            )
        except requests.RequestException:
            continue

        downloaded_images += 1


def main():
    load_dotenv()

    nasa_api_key = os.environ['NASA_API_KEY']

    parser = argparse.ArgumentParser()

    parser.add_argument(
        '--count',
        type=int,
        default=5,
        help='Количество снимков',
    )

    args = parser.parse_args()

    fetch_nasa_epic(
        nasa_api_key,
        args.count,
    )


if __name__ == '__main__':
    main()