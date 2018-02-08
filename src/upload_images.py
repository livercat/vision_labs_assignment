import logging
import os
import sys
import urllib.parse

import click
import requests

SERVER_URL = 'http://test.server.somewhere'
UPLOAD_URL = urllib.parse.urljoin(SERVER_URL, 'images')


@click.command()
@click.argument('directory')
def run(directory):
    if not os.path.isdir(directory):
        logging.info(f"Directory {directory} doesn't exist. Please provide valid path to the directory with images.")
        sys.exit(1)
    for fl in os.listdir(directory):
        with open(os.path.join(directory, fl), mode='rb') as f:
            image = f.read()

        # Assuming multi-part upload
        response = requests.post(url=UPLOAD_URL, files={'file': (fl, image)})
        logging.info(f'Uploaded image {fl} with status {response.status_code}')


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    run()
