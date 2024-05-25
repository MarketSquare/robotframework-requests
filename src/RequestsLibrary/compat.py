import copy
import http.client as httplib  # noqa
from urllib.parse import urlencode  # noqa
from urllib.parse import urljoin  # noqa

from requests.packages.urllib3.util import Retry


class RetryAdapter(Retry):

    @staticmethod
    def get_default_allowed_methods():
        try:
            return list(copy.copy(Retry.DEFAULT_ALLOWED_METHODS))
        except AttributeError:
            return list(copy.copy(Retry.DEFAULT_METHOD_WHITELIST))

    def __init__(self, **kwargs):
        try:
            super(RetryAdapter, self).__init__(**kwargs)
            # FIXME more specific except
        except TypeError:
            value = kwargs.pop("allowed_methods", None)
            kwargs["method_whitelist"] = value
            super(RetryAdapter, self).__init__(**kwargs)
