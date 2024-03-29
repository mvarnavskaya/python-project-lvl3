import os
import re

import requests
from bs4 import BeautifulSoup

from page_loader.app_logger import logger


class AppInternalError(Exception):
    pass


def download(url, dest_path=os.getcwd()):
    """
    Loads content from url
    """
    logger.info(f'download {url} to {dest_path}')

    if not os.path.exists(dest_path):
        logger.error(f"Directory {dest_path} doesn't exists.")
        raise AppInternalError(f"Directory {dest_path} doesn't exists.")

    try:
        html = requests.get(url)
        logger.info(f'received a response {url}')
        html.raise_for_status()

    except requests.exceptions.RequestException as e:
        logger.info(e)
        raise AppInternalError('Network error.') from e

    common_name = parse_url(url)

    try:
        html_local = save_images(url, html, dest_path, common_name)
        html_path = save_page(html_local, dest_path, common_name)
    except requests.exceptions.RequestException as e:
        logger.info(e)
        raise AppInternalError('Network error.') from e
    return html_path


def parse_url(url):
    """
    Replace
    """
    url = re.sub(r'^https?://', '', url)
    url = re.sub('[^a-zA-Z0-9]', '-', url)
    return url


def save_images(url: str, html: str, dest_path: str, common_name: str) -> str:
    """
    Extracts remote url from html and replaces them with links locale
    Saves images
    :returns - html with local links
    """
    try:
        soup = BeautifulSoup(html, 'html.parser')
        images = dict()
        img_in_html = soup.find_all('img')
        folder_for_locals = common_name + '_files'
        for tag in img_in_html:
            image_url = tag.attrs['src']
            image_data = requests.get(url + image_url).content
            local_file_name = parse_url_locals(image_url)
            images[local_file_name] = image_data
            tag.attrs['src'] = os.path.join(folder_for_locals, local_file_name)
        html_out = soup.prettify(formatter='html5')
        save_elements(os.path.join(dest_path, folder_for_locals), images)
        logger.info(f'Found {len(img_in_html)} local resource(s) to save.')
        return html_out
    except requests.exceptions.RequestException as e:
        logger.info(e)
        raise AppInternalError('Network error.') from e


def save_elements(dest_path, elements):
    """
    Saves data in elements to dest_path
    """
    if not os.path.isdir(dest_path):
        os.mkdir(dest_path)
    for name, data in elements.items():
        path_for_locals = os.path.join(dest_path, name)
        if not os.path.exists(path_for_locals):
            logger.error(f"Directory {path_for_locals} doesn't exists.")
            raise AppInternalError(f"Directory {path_for_locals} doesn't exists.")
        try:
            with open(path_for_locals, mode='wb') as opened_file:
                opened_file.write(data)
        except PermissionError:
            logger.info(
                'Permission denied',
                exc_info=logger.getEffectiveLevel() == logger.DEBUG,
            )
            raise


def save_page(html: str, dest_path: str, common_name: str) -> str:
    """
    ��������� html � ����
    """
    path_for_page = os.path.join(dest_path, common_name + '.html')
    try:
        with open(path_for_page, mode='w') as opened_file:
            opened_file.write(html)
            logger.info(f'page content written to {path_for_page}')
    except OSError as e:
        logger.error(e)
    return path_for_page


def parse_url_locals(url: str):
    """
    ������� �� ������ ���, ����� ���� � ����, � ����� .png � .jpg
    """
    url = re.sub(r'^/', '', url)
    url = re.sub(r'(?!.png|.jpg)[^a-zA-Z0-9]', '-', url)
    return url
