from json import JSONDecodeError, dumps
from requests import JSONDecodeError as RequestsJSONDecodeError

from RequestsLibrary.utils import is_file_descriptor
from robot.api import logger


def log_response(response):
    logger.info((f"Response: {response.request.method.upper()}\n"
        f"URL:      {response.url}\n"
        f"Status:   {response.status_code} - {response.reason}"
        )
    )
    logger.debug(f"Headers:  {response.headers}")
    if response.text:
        try:
            logger.debug(f"JSON:     {dumps(response.json(), indent=2)}")
        except (JSONDecodeError, RequestsJSONDecodeError) as err:
            logger.debug(f"Text:     {response.text}")


def log_request(response):
    request = response.request
    if response.history:
        original_request = response.history[0].request
        redirected = '(redirected)'
    else:
        original_request = request
        redirected = ''
    
    logger.info((f"Request:  {original_request.method.upper()}\n"
        f"URL:      {original_request.url} {redirected}\n"
        f"Path URL: {original_request.path_url}"
        )
    )
    logger.debug(f"Headers:  {original_request.headers}")
    logger.debug(f"Body:     {original_request.body}")
