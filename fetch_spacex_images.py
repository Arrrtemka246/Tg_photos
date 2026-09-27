import argparse
import os
from pathlib import Path

from dotenv import load_dotenv

from download_utils import (
    download_image,
    get_file_extension,
    get_proxies,
    get_response,
)


DEFAULT_SEARCH_QUERY = 'Starlink 17-38'
WIKIMEDIA_FILE_NAMESPACE = 6
SEARCH_RESULTS_LIMIT = 10


def fetch_spacex_last_launch(search_query, proxies=None):
    api_url = 'https://commons.wikimedia.org/w/api.php'

    params = {
        'action': 'query',
        'format': 'json',
        'generator': 'search',
        'gsrsearch': search_query,
        'gsrnamespace': WIKIMEDIA_FILE_NAMESPACE,
        'gsrlimit': SEARCH_RESULTS_LIMIT,
        'prop': 'imageinfo',
        'iiprop': 'url|mime',
    }

    response = get_response(
        api_url,
        params=params,
        proxies=proxies,
    )
    response_payload = response.json()

    pages = response_payload.get('query', {}).get('pages', {})

    image_urls = []

    for page in pages.values():
        image_info = page.get('imageinfo')

        if not image_info:
            continue

        image = image_info[0]

        if not image['mime'].startswith('image/'):
            continue

        image_urls.append(image['url'])

    images_dir = Path('images')
    images_dir.mkdir(exist_ok=True)

    for image_number, image_url in enumerate(
        image_urls,
        start=1,
    ):
        extension = get_file_extension(image_url)
        image_path = (
            images_dir
            / f'spacex_{image_number}{extension}'
        )

        download_image(
            image_url,
            image_path,
            proxies=proxies,
        )


def main():
    load_dotenv()

    proxy_url = os.getenv('PROXY_URL')
    proxies = get_proxies(proxy_url)

    parser = argparse.ArgumentParser(
        description=(
            'Скачивает фотографии запуска SpaceX '
            'из Wikimedia Commons.'
        ),
    )
    parser.add_argument(
        '--query',
        default=DEFAULT_SEARCH_QUERY,
        help='Поисковый запрос для Wikimedia Commons',
    )

    args = parser.parse_args()

    fetch_spacex_last_launch(
        args.query,
        proxies,
    )


if __name__ == '__main__':
    main()