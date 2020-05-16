from RequestsLibrary import RequestsLibrary


def test_initialize_keywords_like_robotframework():
    keywords = RequestsLibrary()
    assert hasattr(keywords, '_common_request')
    assert hasattr(keywords, '_create_session')
    assert hasattr(keywords, '_new_create_session')

