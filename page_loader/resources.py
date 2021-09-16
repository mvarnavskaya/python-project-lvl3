import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
from page_loader import naming
from page_loader.app_logger import logger


ATTRIBUTES = {'img': 'src', 'script': 'src', 'link': 'href'}
ONE_MB = 2**20


def download_asset(link: str, assets_path: str):
    logger.info(f'trying to download {link} to {assets_path}')

    try:
        response = requests.get(link, stream=True)
        logger.info(f'received a response from {link}')
    except requests.exceptions.RequestException as e:
        logger.error(e)

    file_name = naming.create_file_name(link)
    logger.info(f'created name {file_name}')
    file_path = os.path.join(assets_path, file_name)
    logger.info(f'created path {file_path} to the page')

    try:
        with open(file_path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=ONE_MB):
                file.write(chunk)
            logger.info(f'file content written to {file_path}')
    except (OSError, requests.exceptions.RequestException) as e:
        logger.error(e)


def is_local(url: str, asset_link: str) -> bool:
    base_domain = urlparse(url).netloc
    asset_domain = urlparse(asset_link).netloc
    if not asset_domain:
        return True
    return base_domain == asset_domain


def replace_links(url: str, page: str, assets_dir_name: str):
    soup = BeautifulSoup(page, 'html.parser')
    assets_links = []

    logger.info('looking for links')
    for element in soup.findAll(ATTRIBUTES):
        attribute_name = ATTRIBUTES[element.name]
        asset_link = element.get(attribute_name)
        logger.info(f'received asset link {asset_link}')

        if is_local(url, asset_link):
            logger.info(f'asset link {asset_link} is local')
            link = urljoin(url, asset_link)
            asset_name = naming.create_file_name(link)
            asset_path = os.path.join(assets_dir_name, asset_name)
            element[attribute_name] = asset_path
            logger.info(f'asset link {asset_link} replaced with {asset_path}')
            assets_links.append(link)
            logger.info(f'link {link} added to assets_links')

    logger.info('Function done! Returning assets and page.')
    return soup.prettify(), assets_links
