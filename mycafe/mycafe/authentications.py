# -*- coding: utf-8 -*-

from rest_framework import authentication
from rest_framework import exceptions

from mycafe.jwt import check_token

from account.models import InvalidatedToken


class TokenAuthentication(authentication.BaseAuthentication):
    """Token authentication class

    signature, exp만으로 요청 auth의 valid를 검사한다.

    Returns
    --------
    (User, auth) or None:
        User django object or None
        auth dict data or None
    """

    err_msg = "Unknown jwt exception"

    def authenticate(self, request):
        toekn_header = request.META.get('HTTP_AUTHORIZATION')
        if not toekn_header:
            return None

        try:
            token = toekn_header.split(' ')[1]
        except IndexError:
            raise exceptions.AuthenticationFailed('Invalid input')

        try:
            InvalidatedToken.objects.get(token=token)
            raise exceptions.AuthenticationFailed('Blacklisted token')
        except InvalidatedToken.DoesNotExist:
            pass
        
        payload, self.err_msg = check_token(token)

        if not payload:
            raise exceptions.AuthenticationFailed('Invalid token')

        return (None, payload)

    def authenticate_header(self, request):
        """
        Return a string to be used as the value of the `WWW-Authenticate`
        header in a `401 Unauthenticated` response, or `None` if the
        authentication scheme should return `403 Permission Denied` responses.
        """
        return self.err_msg