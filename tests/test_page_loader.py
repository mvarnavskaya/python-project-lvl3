import os
import tempfile

import page_loader

URL = 'https://ru.hexlet.io/courses'
NAME_PREFIX = 'ru-hexlet-io-courses'
PATHS = [(f'/{NAME_PREFIX}_files/{NAME_PREFIX}-courses.html',
          './tests/fixtures/expected_courses.html')]
    # [(f'/{NAME_PREFIX}_files/{NAME_PREFIX}-assets-application.css',
    #      './tests/fixtures/expected_application.css'),

         # (f'/{NAME_PREFIX}_files/{NAME_PREFIX}-assets-nodejs.png',
         #  './tests/fixtures/expected_image.png'),
         # (f'/{NAME_PREFIX}_files/{NAME_PREFIX}-script.js',
         #  './tests/fixtures/expected_script.js')]


def test_download():
    with tempfile.TemporaryDirectory() as temp_dir:
        path_to_test_page = page_loader.download(URL, temp_dir)
        test_page = open(path_to_test_page, 'r')
        expected_page = open('./fixtures/expected_page.html', 'r')
        assert test_page.read() == expected_page.read()

        os.close(test_page)
        os.close(expected_page)
        for test_asset_path, expected_asset_path in PATHS:
            tmp_path_to_test_asset = temp_dir.join(test_asset_path)
            assert os.path.exists(tmp_path_to_test_asset)

            test_asset = open(tmp_path_to_test_asset, 'r')
            expected_asset = open(expected_asset_path, 'r')
            assert test_asset.read() == expected_asset.read()
