import os
import requests
from progress.bar import ChargingBar
from page_loader import resources, naming
from page_loader.app_logger import logger


class AppInternalError(Exception):
    pass


def download(url: str, path='') -> str:
    logger.info(f'trying to download {url} to {path}')

    if not os.path.exists(path):
        logger.error(f"Directory {path} doesn't exists.")
        raise AppInternalError(f"Directory {path} doesn't exists.")

    try:
        response = requests.get(url)
        logger.info(f'received a response from {url}')
        response.raise_for_status()

    except requests.exceptions.RequestException as e:
        logger.error(e)
        raise AppInternalError(
            'Network error! See log for more details.') from e

    page_name = naming.create_file_name(url)
    logger.info(f'created name {page_name}')
    page_path = os.path.join(path, page_name)
    logger.info(f'created path {page_path} to the page')

    assets_dir_name = naming.create_assets_dir_name(url)
    logger.info(f'created assets dir name {assets_dir_name}')
    assets_path = os.path.join(path, assets_dir_name)
    logger.info(f'created path {assets_path} for assets')

    try:
        os.makedirs(assets_path, exist_ok=True)
        logger.info(f'created directory {assets_path} for assets')
    except OSError as e:
        logger.error(e)
        raise AppInternalError(
            'System error! See log for more details.') from e

    page, assets_links = resources.replace_links(url, response.text,
                                                 assets_dir_name)
    logger.info('all links replaced')

    try:
        with open(page_path, 'w', encoding='utf-8') as file:
            file.write(page)
            logger.info(f'page content written to {page_path}')
    except OSError as e:
        logger.error(e)
        raise AppInternalError(
            'System error! See log for more details.') from e

    if assets_links:
        with ChargingBar('Loading', max=len(assets_links)) as bar:
            for link in assets_links:
                resources.download_asset(link, assets_path)
                bar.next()

    logger.info(f'Function done! Returning {page_path}')
    return page_path
