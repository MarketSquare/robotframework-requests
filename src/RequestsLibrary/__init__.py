from .RequestsOnSessionKeywords import RequestsOnSessionKeywords
from .version import VERSION

"""
** Inheritance structure **
Not exactly a best practice but forced by the fact that RF libraries
are instance of a class.

RequestsKeywords (common requests and sessionless keywords)
    |_ SessionKeywords (session creation and data)
        |_ RequestsOnSessionKeywords (new keywords that use sessions)

RequestsLibrary (extends RequestsOnSessionKeywords, DeprecatedKeywords)
"""


class RequestsLibrary(RequestsOnSessionKeywords):
    """ RequestsLibrary is a Robot Framework library aimed to provide HTTP api testing functionalities
     by wrapping the well known Python Requests Library.

        == Table of contents ==

        %TOC%

        = Usage =

        The quickest way to start is using the requests keywords and urls see below examples:

        |   *** Settings ***
        |   Library               RequestsLibrary
        |
        |   *** Test Cases ***
        |   Quick Get Request Test
        |       ${response}=    GET  https://www.google.com
        |
        |   Quick Get Request With Parameters Test
        |       ${response}=    GET  https://www.google.com/search  params=query=ciao  expected_status=200
        |
        |   Quick Get A JSON Body Test
        |       ${response}=    GET  https://jsonplaceholder.typicode.com/posts/1
        |       Should Be Equal As Strings    1  ${response.json()}[id]

        In order to share the HTTP Session (with the same url, headers, cookies, etc.) among multiple requests,
        a new connection needs to be prepared with ``Create Session`` and passed to the `* On Session` keywords.
        You can then execute any `* On Session` keywords on the shared session by passing the created session alias
        name, this will increase performances since the connection and ssl handshake is recycled and not repeated for
        each requests.
        Below some more advanced examples:

        |   *** Settings ***
        |   Library    Collections
        |   Library    RequestsLibrary
        |
        |   Suite Setup    Create Session  jsonplaceholder  https://jsonplaceholder.typicode.com
        |
        |   *** Test Cases ***
        |
        |   Get Request Test
        |       Create Session    google  http://www.google.com
        |
        |       ${resp_google}=   GET On Session  google  /  expected_status=200
        |       ${resp_json}=     GET On Session  jsonplaceholder  /posts/1
        |
        |       Should Be Equal As Strings          ${resp_google.reason}  OK
        |       Dictionary Should Contain Value     ${resp_json.json()}  sunt aut facere repellat provident
        |
        |   Post Request Test
        |       &{data}=    Create dictionary  title=Robotframework requests  body=This is a test!  userId=1
        |       ${resp}=    POST On Session    jsonplaceholder  /posts  json=${data}  expected_status=anything
        |
        |       Status Should Be                 201  ${resp}
        |       Dictionary Should Contain Key    ${resp.json()}  id

        = Response Object =

        All the HTTP requests keywords (GET, POST, PUT, etc.) return an extremely useful Response object.
        The Response object contains a server's response to an HTTP request.

        You can access the different attributes with the dot notation in this way: ``${response.json()}`` or
        ``${response.text}``. Below the list of the most useful attributes:

        | = Attributes = | = Explanation = |
        | content | Content of the response, in bytes. |
        | cookies | A CookieJar of Cookies the server sent back. |
        | elapsed | The amount of time elapsed between sending the request and the arrival of the response (as a timedelta). This property specifically measures the time taken between sending the first byte of the request and finishing parsing the headers. It is therefore unaffected by consuming the response content or the value of the stream keyword argument. |
        | encoding | Encoding to decode with when accessing ``response.text.`` |
        | headers | Case-insensitive Dictionary of Response Headers. For example, ``headers['content-encoding']`` will return the value of a `Content-Encoding' response header. |
        | history | A list of Response objects from the history of the Request. Any redirect responses will end up here. The list is sorted from the oldest to the most recent request. |
        | json    | Returns the json-encoded content of a response, if any. Parameters:	``**kwargs`` - Optional arguments that json.loads takes. Raises:	ValueError ? If the response body does not contain valid json. |
        | ok      | Returns True if status_code is less than 400, False if not. |
        | reason  | Textual reason of responded HTTP Status, e.g. ``Not Found`` or ``OK``. |
        | status_code | Integer Code of responded HTTP Status, e.g. 404 or 200. |
        | text    | Content of the response, in unicode. If ``response.encoding`` is ``None``, encoding will be guessed using chardet. The encoding of the response content is determined based solely on HTTP headers, following RFC 2616 to the letter. If you can take advantage of non-HTTP knowledge to make a better guess at the encoding, you should set ``response.encoding`` appropriately before accessing this property. |
        | url     | Final URL location of Response. |

        = POST a Multipart-Encoded File =

        RequestsLibrary makes it simple to upload Multipart-encoded files, but in order to make sure that the
        Python Library provides automatically the right ``Content-Length`` and ``multipart/form-data; boundary=...``
        headers you SHOULD NOT provide those headers manually, use the keyword
        `Get File For Streaming Upload` instead that opens the files in binary mode.

        Below an example of multiple file sent over a single POST:

        |   Test Post Multiple Files
        |       ${file_1}=  Get File For Streaming Upload  files/randombytes.bin
        |       ${file_2}=  Get File For Streaming Upload  files/randombytes.bin
        |       ${files}=   Create Dictionary  randombytes1  ${file_1}  randombytes2  ${file_2}
        |
        |       ${resp}=    POST  https://someurl  files=${files}

        You can find a working test example in `atests/test_post_multipart.robot`.

        For a complete reference verify the official Requests documentation:

          - https://2.python-requests.org/en/master/user/quickstart/#post-a-multipart-encoded-file
          - https://2.python-requests.org/en/master/user/advanced/#post-multiple-multipart-encoded-files

        """
    __version__ = VERSION
    ROBOT_LIBRARY_SCOPE = 'GLOBAL'
