# -*- coding: utf-8 -*-

from rest_framework.response import Response

from http import HTTPStatus


http_code_to_message = {v.value: v.description for v in HTTPStatus}


class CustomResponse(Response):
    def __init__(self, data=None, status=None, *args, **kwargs):

        message = http_code_to_message.get(status, 'Ok')
        kwargs.pop('pk', None)  # delete pk kwarg passed by view

        formatted_data = {
            'meta': {
                'code': status,
                'message': message
            },
            'data': data
        }
        super().__init__(data=formatted_data, status=status, *args, **kwargs)
