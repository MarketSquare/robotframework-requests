from RequestsLibrary import RequestsLibrary, DeprecatedKeywords, RequestsOnSessionKeywords
from RequestsLibrary.RequestsKeywords import RequestsKeywords
from RequestsLibrary.SessionKeywords import SessionKeywords


class TestRequestsLibraryInheritance():

    @classmethod
    def setup_class(cls):
        cls.requests_library = RequestsLibrary()

    def test_make_sure_is_instance_of_requests_keywords(self):
        assert isinstance(self.requests_library, RequestsKeywords)

    def test_make_sure_is_instance_of_session_keywords(self):
        assert isinstance(self.requests_library, SessionKeywords)

    def test_make_sure_is_instance_of_deprecated_keywords(self):
        assert isinstance(self.requests_library, DeprecatedKeywords)

    def test_make_sure_is_instance_of_requests_on_session_keywords(self):
        assert isinstance(self.requests_library, RequestsOnSessionKeywords)

    def test_make_sure_it_has_methods_from_requests_keywords(self):
        assert hasattr(self.requests_library, '_common_request')

    def test_make_sure_it_has_methods_from_session_keywords(self):
        assert hasattr(self.requests_library, '_create_session')

    # FIXME with real methods
    def test_make_sure_it_has_methods_from_deprecated_keywords(self):
        assert hasattr(self.requests_library, 'get_request_deprecated')

    def test_make_sure_it_has_methods_from_requests_on_session_keywords(self):
        assert hasattr(self.requests_library, 'get_on_session')
