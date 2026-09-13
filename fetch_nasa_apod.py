import argparse
import os
from pathlib import Path

import requests
from dotenv import load_dotenv

from download_utils import (
    download_image,
    get_file_extension,
    get_response,
)


def fetch_nasa_apod(api_key, images_count):
    api_url = 'https://api.nasa.gov/planetary/apod'

    params = {
        'api_key': api_key,
        'count': images_count,
    }

    try:
        response = get_response(api_url, params=params)
    except requests.RequestException:
        api_key = 'DEMO_KEY'

        params = {
            'api_key': api_key,
            'count': 5,
        }

        response = get_response(api_url, params=params)

    apod_images = response.json()

    images_dir = Path('images')
    images_dir.mkdir(exist_ok=True)

    image_number = 1

    for apod_image in apod_images:
        if apod_image.get('media_type') != 'image':
            continue

        image_url = apod_image['url']
        extension = get_file_extension(image_url)

        image_path = (
            images_dir
            / f'nasa_apod_{image_number}{extension}'
        )

        try:
            download_image(image_url, image_path)
        except requests.RequestException:
            continue

        image_number += 1


def main():
    load_dotenv()

    nasa_api_key = os.environ['NASA_API_KEY']

    parser = argparse.ArgumentParser()

    parser.add_argument(
        '--count',
        type=int,
        default=30,
        help='Количество снимков',
    )

    args = parser.parse_args()

    fetch_nasa_apod(
        nasa_api_key,
        args.count,
    )


if __name__ == '__main__':
    main()