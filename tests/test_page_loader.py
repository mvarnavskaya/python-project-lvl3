import os
import tempfile
import pytest
from page_loader import page_loader


URL = 'https://artlyne.github.io/python-project-lvl3'
NAME_PREFIX = 'artlyne-github-io-python-project-lvl3'
PATHS = [(f'/{NAME_PREFIX}_files/{NAME_PREFIX}-assets-application.css',
         './tests/fixtures/expected_application.css'),
         (f'/{NAME_PREFIX}_files/{NAME_PREFIX}-courses.html',
          './tests/fixtures/expected_courses.html'),
         (f'/{NAME_PREFIX}_files/{NAME_PREFIX}-assets-nodejs.png',
          './tests/fixtures/expected_image.png'),
         (f'/{NAME_PREFIX}_files/{NAME_PREFIX}-script.js',
          './tests/fixtures/expected_script.js')]


def test_download():
    with tempfile.TemporaryDirectory() as tmpdir:
        path_to_test_page = page_loader.download(URL, tmpdir)
        test_page = open(path_to_test_page, 'r')
        expected_page = open('./tests/fixtures/expected_page.html', 'r')
        assert test_page.read() == expected_page.read()

        for test_asset_path, expected_asset_path in PATHS:
            tmp_path_to_test_asset = tmpdir.join(test_asset_path)
            assert os.path.exists(tmp_path_to_test_asset)

            test_asset = open(tmp_path_to_test_asset, 'rb')
            expected_asset = open(expected_asset_path, 'rb')
            assert test_asset.read() == expected_asset.read()


def test_network_errors(requests_mock):
    for code in (400, 404, 500, 502):
        requests_mock.get('https://test.com', text='data', status_code=code)
        with tempfile.TemporaryDirectory() as tmpdirname:
            with pytest.raises(page_loader.AppInternalError):
                page_loader.download('https://test.com', tmpdirname)


def test_os_errors():
    with pytest.raises(page_loader.AppInternalError):
        page_loader.download('https://test.com', 'not_exists')
