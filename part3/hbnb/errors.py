from flask import jsonify
from werkzeug.exceptions import HTTPException

class NotFound(HTTPException):
    code = 404
    description = "Resource not found"

class BadRequest(HTTPException):
    code = 400
    description = "Bad request"

class Conflict(HTTPException):
    code = 409
    description = "Conflict"

def register_error_handlers(app):
    def handle_http_exception(e):
        return jsonify({
            "error": e.description,
            "status": e.code
        }), e.code

    for exc in (NotFound, BadRequest, Conflict):
        app.register_error_handler(exc, handle_http_exception)
