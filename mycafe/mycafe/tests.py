# -*- coding: utf-8 -*-

import re
import functools

from django.http import HttpResponse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from faker import Faker

from account.models import Account


class CommonAPIClient(APIClient):

    def __init__(self, enforce_csrf_checks=False, **defaults):
        super().__init__(enforce_csrf_checks, **defaults)
        self.__token = None

    @property
    def token(self):
        return self.__token

    @token.setter
    def token(self, val):
        self.__token = val

    def __process_token(self, extra):
        if token := extra.pop('token', None):
            extra['HTTP_AUTHORIZATION'] = f'Bearer {token}'
        elif self.__token:
            extra['HTTP_AUTHORIZATION'] = f'Bearer {self.__token}'
        if extra.pop('no_token', False):
            extra.pop('HTTP_AUTHORIZATION', None)

    def login(self, phone_num: str, password: str):
        res = self.post(
            path='/api/v1/token',
            data={'phone_num': phone_num, 'password': password})
        self.__token = res.json()['data']

    def get(self, path, data=None, follow=False, **extra):
        self.__process_token(extra)
        return super().get(path, data=data, follow=follow, **extra)

    def post(self, path, data=None, format=None, 
             content_type=None, follow=False, **extra):
        self.__process_token(extra)
        _format = format
        if not _format:
            _format = 'json'
        return super().post(path, data=data, format=_format, 
                    content_type=content_type, follow=follow, **extra)

    def put(self, path, data=None, format=None, 
            content_type=None, follow=False, **extra):
        self.__process_token(extra)
        _format = format
        if not _format:
            _format = 'json'
        return super().put(path, data=data, format=_format, 
                    content_type=content_type, follow=follow, **extra)

    def patch(self, path, data=None, format=None, 
              content_type=None, follow=False, **extra):
        self.__process_token(extra)
        _format = format
        if not _format:
            _format = 'json'
        return super().patch(path, data=data, format=_format, 
                    content_type=content_type, follow=follow, **extra)

    def delete(self, path, data=None, format=None, 
               content_type=None, follow=False, **extra):
        self.__process_token(extra)
        return super().delete(path, data=data, format=format, 
                    content_type=content_type, follow=follow, **extra)

class CommonAPITest(APITestCase):
    faker = Faker('ko-KR')
    client_class = CommonAPIClient

    def gen_token(self, user: Account, password: str) -> dict:
        res = self.client.post(
            path='/api/v1/token',
            data={'phone_num': user.phone_num, 'password': password})
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        return res.json()['data']

    def assertStatusCode(self, status_code: int, res: HttpResponse):
        errors = None
        if hasattr(res, 'data'):
            errors = res.data
        self.assertEqual(res.status_code, status_code, errors)

    def __getattr__(self, attr: str) -> any:
        if r := re.match(r'assert(?P<status>\d{3})$', attr):
            status_code = int(r.groups()[0])
            return functools.partial(self.assertStatusCode, status_code)
        raise AttributeError
