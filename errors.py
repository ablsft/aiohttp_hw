import json

from aiohttp.web import HTTPException


class HttpError(HTTPException):
    def __init__(self, description: dict | list | str):
        self.description = description

        super().__init__(
            text=json.dumps({'status': 'error', 'description': description}),
            content_type='application/json',
        )


class NotFound(HttpError):
    status_code = 404


class BadRequest(HttpError):
    status_code = 400


class Conflict(HttpError):
    status_code = 409


class Unauthorized(HttpError):
    status_code = 401


class Forbidden(HttpError):
    status_code = 403


class MethodNotAllowed(HttpError):
    status_code = 405


class UnexpectedError(HttpError):
    status_code = 500
