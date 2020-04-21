import os

from RequestsLibrary.utils import is_file_descriptor


SCRIPT_DIR = os.path.dirname(__file__)


def test_none():
    assert is_file_descriptor(None) is False


def test_is_not_file_descriptor():
    nf = 'a string'
    assert is_file_descriptor(nf) is False


def test_is_file_descriptor():
    with open(os.path.join(SCRIPT_DIR, './test_utils.py')) as fd:
        assert is_file_descriptor(fd) is True
