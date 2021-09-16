import pytest
from page_loader import resources

URL = 'https://artlyne.github.io/python-project-lvl3'
IMG = 'https://artlyne.github.io/python-project-lvl3/assets/nodejs.png'


@pytest.mark.parametrize('url, link, expected_result', [
    (URL, f'{URL}/courses', True),
    (URL, 'https://hexlet.github.io/courses', False),
    (URL, '/assets/image.png', True),
    (URL, 'https://github.io/python-project-lvl3/image.png', False)])
def test_is_local(url: str, link: str, expected_result: bool):
    assert resources.is_local(url, link) == expected_result


def test_download_asset(tmpdir):
    resources.download_asset(IMG, tmpdir)
    path_to_test_img = tmpdir.join(
        '/artlyne-github-io-python-project-lvl3-assets-nodejs.png')
    test_img = open(path_to_test_img, 'rb')
    expected_img = open('./tests/fixtures/expected_image.png', 'rb')
    assert bytearray(expected_img.read()) == bytearray(test_img.read())
