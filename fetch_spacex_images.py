import argparse
from pathlib import Path

from download_utils import download_image, get_response


def fetch_spacex_last_launch(search_query):
    api_url = 'https://commons.wikimedia.org/w/api.php'

    params = {
        'action': 'query',
        'format': 'json',
        'generator': 'search',
        'gsrsearch': search_query,
        'gsrnamespace': 6,
        'gsrlimit': 10,
        'prop': 'imageinfo',
        'iiprop': 'url|mime',
    }

    response = get_response(api_url, params=params)
    response_payload = response.json()

    pages = response_payload.get('query', {}).get('pages', {})

    images_dir = Path('images')
    images_dir.mkdir(exist_ok=True)

    image_number = 1

    for page in pages.values():
        image_info = page.get('imageinfo')

        if not image_info:
            continue

        image = image_info[0]

        if not image['mime'].startswith('image/'):
            continue

        image_url = image['url']
        image_path = images_dir / f'spacex_{image_number}.jpg'

        download_image(image_url, image_path)

        image_number += 1


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        '--query',
        default='Starlink 17-38',
        help='Поисковый запрос для Wikimedia Commons',
    )

    args = parser.parse_args()

    fetch_spacex_last_launch(args.query)


if __name__ == '__main__':
    main()