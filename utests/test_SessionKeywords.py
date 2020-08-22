from RequestsLibrary.RequestsKeywords import RequestsKeywords
from RequestsLibrary.SessionKeywords import SessionKeywords


def test_session_class_extends_keywords_class():
    keywords = SessionKeywords()
    assert isinstance(keywords, RequestsKeywords)

