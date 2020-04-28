# This code is part of httpbin project source code https://github.com/postmanlabs/httpbin
# See AUTHORS and LICENSE for more information

from flask import Flask, Response, jsonify as flask_jsonify, request

from .structures import CaseInsensitiveDict
from .helpers import get_dict, status_code
from .utils import weighted_choice


app = Flask(__name__)


def jsonify(*args, **kwargs):
    response = flask_jsonify(*args, **kwargs)
    if not response.data.endswith(b"\n"):
        response.data += b"\n"
    return response


@app.route("/")
def index():
    return "Flask Http Test Server"


@app.route("/headers")
def view_headers():
    """Return the incoming request's HTTP headers.
    ---
    tags:
      - Request inspection
    produces:
      - application/json
    responses:
      200:
        description: The request's headers.
    """

    return jsonify(get_dict('headers'))


@app.route("/anything", methods=["GET", "POST", "PUT", "DELETE", "PATCH", "TRACE"])
def view_anything(anything=None):
    """Returns anything passed in request data.
    ---
    tags:
      - Anything
    produces:
      - application/json
    responses:
      200:
        description: Anything passed in request
    """

    return jsonify(
        get_dict(
            "url",
            "args",
            "headers",
            "origin",
            "method",
            "form",
            "data",
            "files",
            "json",
        )
    )


@app.route(
    "/status/<codes>", methods=["GET", "POST", "PUT", "DELETE", "PATCH", "TRACE"]
)
def view_status_code(codes):
    """Return status code or random status code if more than one are given
    ---
    tags:
      - Status codes
    parameters:
      - in: path
        name: codes
    produces:
      - text/plain
    responses:
      100:
        description: Informational responses
      200:
        description: Success
      300:
        description: Redirection
      400:
        description: Client Errors
      500:
        description: Server Errors
    """

    if "," not in codes:
        try:
            code = int(codes)
        except ValueError:
            return Response("Invalid status code", status=400)
        return status_code(code)

    choices = []
    for choice in codes.split(","):
        if ":" not in choice:
            code = choice
            weight = 1
        else:
            code, weight = choice.split(":")

        try:
            choices.append((int(code), float(weight)))
        except ValueError:
            return Response("Invalid status code", status=400)

    code = weighted_choice(choices)

    return status_code(code)


@app.route("/redirect-to", methods=["GET", "POST", "PUT", "DELETE", "PATCH", "TRACE"])
def redirect_to():
    """302/3XX Redirects to the given URL.
    ---
    tags:
      - Redirects
    produces:
      - text/html
    get:
      parameters:
        - in: query
          name: url
          type: string
          required: true
        - in: query
          name: status_code
          type: int
    post:
      consumes:
        - application/x-www-form-urlencoded
      parameters:
        - in: formData
          name: url
          type: string
          required: true
        - in: formData
          name: status_code
          type: int
          required: false
    patch:
      consumes:
        - application/x-www-form-urlencoded
      parameters:
        - in: formData
          name: url
          type: string
          required: true
        - in: formData
          name: status_code
          type: int
          required: false
    put:
      consumes:
        - application/x-www-form-urlencoded
      parameters:
        - in: formData
          name: url
          type: string
          required: true
        - in: formData
          name: status_code
          type: int
          required: false
    responses:
      302:
        description: A redirection.
    """

    args_dict = request.args.items()
    args = CaseInsensitiveDict(args_dict)

    # We need to build the response manually and convert to UTF-8 to prevent
    # werkzeug from "fixing" the URL. This endpoint should set the Location
    # header to the exact string supplied.
    response = app.make_response("")
    response.status_code = 302
    if "status_code" in args:
        status_code = int(args["status_code"])
        if status_code >= 300 and status_code < 400:
            response.status_code = status_code
    response.headers["Location"] = args["url"].encode("utf-8")

    return response
