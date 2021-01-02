import sys
import unittest

from RequestsLibrary import compat
from RequestsLibrary.RequestsKeywords import RequestsKeywords
from RequestsLibrary.SessionKeywords import SessionKeywords


def test_session_class_extends_keywords_class():
    keywords = SessionKeywords()
    assert isinstance(keywords, RequestsKeywords)


class TestUrlLibWarnings(unittest.TestCase):

    @unittest.skipIf(sys.version_info < (3, 2), "python version doesn't support assertWarns")
    def test_get_default_retry_method_list_not_raise_warning(self):
        with self.assertRaises(AssertionError):
            with self.assertWarns(DeprecationWarning):
                DEFAULT_RETRY_METHOD_LIST = compat.RetryAdapter.get_default_allowed_methods()
                assert "GET" in DEFAULT_RETRY_METHOD_LIST

    @unittest.skipIf(sys.version_info < (3, 2), "python version doesn't support assertWarns")
    def test_init_retry_adapter_not_raise_warning(self):
        with self.assertRaises(AssertionError):
            with self.assertWarns(DeprecationWarning):
                compat.RetryAdapter(total=1,
                                    backoff_factor=1,
                                    status_forcelist=[500],
                                    allowed_methods=['GET'])

    @unittest.skipIf(sys.version_info < (3, 2), "python version doesn't support assertWarns")
    def test_create_session_retry_not_raise_warning(self):
        keywords = SessionKeywords()
        with self.assertRaises(AssertionError):
            with self.assertWarns(DeprecationWarning):
                keywords.create_session('alias', 'http://mocking.rules')


