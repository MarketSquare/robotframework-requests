# This code is part of httpbin project source code https://github.com/postmanlabs/httpbin
# See AUTHORS and LICENSE for more information

from flask import Flask, Response, jsonify as flask_jsonify
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
