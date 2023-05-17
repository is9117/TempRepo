# -*- coding: utf-8 -*-
"""전체 에러코드 규격화

Ref: https://rednafi.github.io/reflections/uniform-error-response-in-django-rest-framework.html
"""

from rest_framework.views import exception_handler
from http import HTTPStatus
from typing import Any

from rest_framework.views import Response


http_code_to_message = {v.value: v.description for v in HTTPStatus}

def api_exception_handler(exc: Exception, context: dict[str, Any]) -> Response:
    """Custom API exception handler."""

    global http_code_to_message

    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)

    if response is not None:
        # Using the description's of the HTTPStatus class as error message.
        
        error_payload = {
            "meta": {
                "code": 0,
                "message": ""
            },
            "data": None
        }
        meta = error_payload["meta"]
        status_code = response.status_code

        if status_code == 204:  # 204 예외
            return response

        meta["code"] = status_code
        meta["message"] = http_code_to_message[status_code]
        error_payload["data"] = response.data
        response.data = error_payload
    return response

