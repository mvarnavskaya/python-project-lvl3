import pytest
from page_loader import naming


URL = 'https://artlyne.github.io/python-project-lvl3'
NAME_PREFIX = 'artlyne-github-io-python-project-lvl3'


@pytest.mark.parametrize('url, expected_name', [
    (URL, f'{NAME_PREFIX}.html'),
    (f'{URL}/python', f'{NAME_PREFIX}-python.html'),
    (f'{URL}/python.html', f'{NAME_PREFIX}-python.html'),
    (f'{URL}/python.png', f'{NAME_PREFIX}-python.png'),
    (f'{URL}/python.jpg', f'{NAME_PREFIX}-python.jpg'),
    (f'{URL}/python%1.jpg', f'{NAME_PREFIX}-python-1.jpg')])
def test_create_name(url: str, expected_name: str):
    assert naming.create_file_name(url) == expected_name


@pytest.mark.parametrize('url, expected_name_path', [
    (URL, f'{NAME_PREFIX}_files'),
    (f'{URL}/python', f'{NAME_PREFIX}-python_files'),
    (f'{URL}/python.html', f'{NAME_PREFIX}-python_files')])
def test_create_assets_path(url: str, expected_name_path: str):
    assert naming.create_assets_dir_name(url) == expected_name_path
